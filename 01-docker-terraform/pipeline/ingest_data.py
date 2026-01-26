#!/usr/bin/env python
# coding: utf-8

import os

import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

TAXI_DATA_URL = os.getenv(
    "TAXI_DATA_URL",
    "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet",
)
ZONES_DATA_URL = os.getenv(
    "ZONES_DATA_URL",
    "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv",
)

DATASETS = {
    "taxi": {
        "url": TAXI_DATA_URL,
        "table": "yellow_taxi_data",
        "format": "parquet",
    },
    "zones": {
        "url": ZONES_DATA_URL,
        "table": "zones",
        "format": "csv",
        "dtype": {
            "LocationID": "Int64",
            "Borough": "string",
            "Zone": "string",
            "service_zone": "string",
        },
    },
}


def ingest_csv(engine, table_name: str, url: str, dtype: dict | None = None, chunksize: int = 100000):
    """Ingest CSV data into PostgreSQL in chunks."""
    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        iterator=True,
        chunksize=chunksize,
    )

    first_chunk = next(df_iter)

    first_chunk.head(0).to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
    )
    print("Table created")

    first_chunk.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
    )
    print(f"Inserted first chunk: {len(first_chunk)}")

    for df_chunk in tqdm(df_iter):
        df_chunk.to_sql(
            name=table_name,
            con=engine,
            if_exists="append",
        )
        print(f"Inserted chunk: {len(df_chunk)}")


def ingest_parquet(engine, table_name: str, url: str, chunksize: int = 100000):
    """Ingest parquet data into PostgreSQL in chunks."""
    df = pd.read_parquet(url)

    df.head(0).to_sql(name=table_name, con=engine, if_exists="replace")
    print("Table created")

    for i in tqdm(range(0, len(df), chunksize)):
        chunk = df.iloc[i:i + chunksize]
        chunk.to_sql(name=table_name, con=engine, if_exists="append")
        print(f"Inserted chunk: {len(chunk)}")


@click.command()
@click.option("--pg-user", default="root", help="PostgreSQL user")
@click.option("--pg-pass", default="root", help="PostgreSQL password")
@click.option("--pg-host", default="localhost", help="PostgreSQL host")
@click.option("--pg-port", default=5432, type=int, help="PostgreSQL port")
@click.option("--pg-db", default="ny_taxi", help="PostgreSQL database name")
@click.option(
    "--dataset",
    type=click.Choice(["taxi", "zones"]),
    required=True,
    help="Dataset to ingest",
)
def main(pg_user, pg_pass, pg_host, pg_port, pg_db, dataset):
    """Ingest NYC taxi data into PostgreSQL."""
    connection_string = f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
    engine = create_engine(connection_string)

    config = DATASETS[dataset]
    if config["format"] == "parquet":
        ingest_parquet(engine, table_name=config["table"], url=config["url"])
    else:
        ingest_csv(engine, table_name=config["table"], url=config["url"], dtype=config.get("dtype"))


if __name__ == "__main__":
    main()
