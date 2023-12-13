import argparse
import itertools
import pathlib

import arcticdb
import pandas as pd
import yaml
from trading_ig import IGService
from trading_ig.config import config

S3_BUCKET_NAME = "tradingo-price-store"
ARCTIC_CONNECTION = (
    f"s3://s3.eu-west-2.amazonaws.com:{S3_BUCKET_NAME}?aws_auth=true"
)
ARCTIC_CONNECTION = "lmdb:///home/rory/.trading/.tradingo-db.test"


def extract(
    arctic,
    epics,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
    resolution: str = "1D",
):
    ig_service = IGService(
        config.username, config.password, config.api_key, config.acc_type
    )
    ig_service.create_session()

    lib = arctic.get_library(
        f"INSTRUMENTS_{resolution.upper()}",
        create_if_missing=True,
        library_options=arcticdb.LibraryOptions(dedup=True),
    )

    for epic in epics:
        meta = ig_service.fetch_market_by_epic(epic)

        data = ig_service.fetch_historical_prices_by_epic_and_date_range(
            epic=epic,
            resolution=resolution,
            end_date=end_date,
            start_date=start_date,
        )

        prices = data["prices"]

        prices.columns = [
            "_".join(i).lower() for i in prices.columns.to_series()
        ]

        lib.update(
            epic,
            prices,
            upsert=True,
            date_range=(start_date, end_date),
            metadata=dict(meta),
        )


def transform(
    arctic: arcticdb.Arctic,
    epics,
    universe_name: str,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
    resolution: str = "1D",
):
    in_lib = arctic.get_library(f"INSTRUMENTS_{resolution}")
    out_lib = arctic.get_library(
        f"{universe_name.upper()}_PRICE_{resolution}",
        create_if_missing=True,
        library_options=arcticdb.LibraryOptions(dedup=True),
    )

    for field, obvs in itertools.product(
        ("bid", "ask"), ("open", "close", "high", "low")
    ):
        symbol = f"{field}.{obvs}".upper()

        out_df = pd.concat(
            (
                in_lib.read(
                    symbol,
                    columns=[f"{field}_{obvs}"],
                    date_range=(start_date, end_date),
                )
                .data.squeeze(axis="columns")
                .rename(symbol)
                for symbol in epics
            ),
            axis=1,
        )

        metadata = {"universe": epics, "universe_name": universe_name}

        out_lib.update(
            symbol,
            out_df,
            upsert=True,
            date_range=(start_date, end_date),
            metadata=metadata,
        )


def load(
    arctic: arcticdb.Arctic,
    epics,
    universe_name: str,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
    resolution: str = "1D",
):
    lib = arctic.get_library(f"{universe_name.upper()}_PRICE_{resolution}")

    data = {
        fld: lib.read(
            "_".join(fld).upper(),
            date_range=(start_date, end_date),
            columns=epics,
        ).data
        for fld in itertools.product(
            ("bid", "ask"), ("open", "close", "high", "low")
        )
    }
    return pd.concat(data.values(), keys=data.keys(), axis=1)


def cli_app():
    app = argparse.ArgumentParser("tradingo-price-etl")
    app.add_argument("actions", nargs="+")
    app.add_argument("--epics", required=False, nargs="+")
    app.add_argument("--universe-file", required=False, type=pathlib.Path)
    app.add_argument("--resolution", default="1D")
    app.add_argument(
        "--end-date", type=pd.Timestamp, default=pd.Timestamp.now()
    )
    app.add_argument("--start-date", type=pd.Timestamp)
    app.add_argument("--universe-name", required=True)

    return app


def main():
    args = cli_app().parse_args()
    universe_config = yaml.load(args.universe_file.open("r"), yaml.Loader)

    if "epics" in universe_config:
        args.epics = universe_config["epics"]

    if "resolution" in universe_config:
        args.resolution = universe_config["resolution"]

    if "universe_name" in universe_config:
        args.universe_name = universe_config["universe_name"]

    arctic = arcticdb.Arctic(ARCTIC_CONNECTION)

    for action in args.actions:
        if action == "extract":
            extract(
                arctic,
                epics=args.epics,
                start_date=args.start_date,
                end_date=args.end_date,
                resolution=args.resolution,
            )

        elif action == "transform":
            transform(
                arctic,
                epics=args.epics,
                start_date=args.start_date,
                universe_name=args.universe_name,
                end_date=args.end_date,
                resolution=args.resolution,
            )

        elif action == "load":
            load(
                arctic,
                universe_name=args.universe_name,
                epics=args.epics,
                start_date=args.start_date,
                end_date=args.end_date,
                resolution=args.resolution,
            )

        elif action == 'run':
            raise NotImplementedError

        else:
            raise ValueError(f"Invalid action {action}")


if __name__ == "__main__":
    main()
