import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import boto3

BUCKET_NAME = "de-zoomcamp-datalake"
S3_PREFIX = "yellow_taxi"
BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-"
MONTHS = [f"{i:02d}" for i in range(1, 7)]
DOWNLOAD_DIR = "/tmp/yellow_taxi"

s3 = boto3.client("s3")


def download_file(month):
    url = f"{BASE_URL}{month}.parquet"
    file_path = os.path.join(DOWNLOAD_DIR, f"yellow_tripdata_2024-{month}.parquet")

    try:
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, file_path)
        print(f"Downloaded: {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None


def upload_to_s3(file_path):
    key = f"{S3_PREFIX}/{os.path.basename(file_path)}"

    print(f"Uploading {file_path} to s3://{BUCKET_NAME}/{key}...")
    s3.upload_file(file_path, BUCKET_NAME, key)

    resp = s3.head_object(Bucket=BUCKET_NAME, Key=key)
    size_mb = resp["ContentLength"] / (1024 * 1024)
    print(f"Verified: s3://{BUCKET_NAME}/{key} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    with ThreadPoolExecutor(max_workers=4) as executor:
        file_paths = list(executor.map(download_file, MONTHS))

    for fp in filter(None, file_paths):
        upload_to_s3(fp)

    print("All files processed and verified.")
