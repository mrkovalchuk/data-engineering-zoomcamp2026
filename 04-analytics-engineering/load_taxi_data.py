import argparse
import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import boto3

BUCKET_NAME = "de-zoomcamp-datalake"
BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"
DOWNLOAD_DIR = "/tmp/taxi_data"

s3 = boto3.client("s3")


def download_file(args):
    dataset, year, month = args
    filename = f"{dataset}_tripdata_{year}-{month:02d}.parquet"
    url = f"{BASE_URL}/{filename}"
    file_path = os.path.join(DOWNLOAD_DIR, filename)

    try:
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, file_path)
        print(f"Downloaded: {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None


def upload_to_s3(file_path, dataset):
    key = f"{dataset}_taxi/{os.path.basename(file_path)}"

    print(f"Uploading to s3://{BUCKET_NAME}/{key}...")
    s3.upload_file(file_path, BUCKET_NAME, key)

    resp = s3.head_object(Bucket=BUCKET_NAME, Key=key)
    size_mb = resp["ContentLength"] / (1024 * 1024)
    print(f"Verified: s3://{BUCKET_NAME}/{key} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load taxi data to S3")
    parser.add_argument("--dataset", required=True, choices=["yellow", "green"],
                        help="Dataset name: yellow or green")
    parser.add_argument("--years", required=True, nargs="+", type=int,
                        help="Years to download (e.g. 2019 2020)")
    args = parser.parse_args()

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    tasks = [
        (args.dataset, year, month)
        for year in args.years
        for month in range(1, 13)
    ]

    with ThreadPoolExecutor(max_workers=4) as executor:
        file_paths = list(executor.map(download_file, tasks))

    for fp in filter(None, file_paths):
        upload_to_s3(fp, args.dataset)

    print("All files processed and verified.")
