# Module 3 Homework: Data Warehouse with AWS Athena

This homework adapts the original BigQuery assignment to use **AWS Athena + S3 + Glue**.


### Load data into S3

```bash
pip install boto3
python load_yellow_taxi_data.py
```

This downloads parquet files and uploads them to `s3://de-zoomcamp-datalake/yellow_taxi/`.

## Answers

### Question 1. Counting records

- **20,332,093**

```sql
SELECT COUNT(*) FROM zoomcamp.yellow_taxi_external;
```

### Question 2. Data read estimation

BigQuery shows an estimate before you run the query. For external tables, BigQuery has no metadata about the data sitting in GCS, so it can't estimate — it shows 0 MB. For native tables, it has column statistics in its catalog, so it can predict ~155 MB.

Athena shows actual data scanned after the query finishes. It doesn't estimate anything upfront. Both the external table and the CTAS table contain the same data stored as parquet in S3, so reading scans roughly the same amount from both:
- "Data scanned: 16.56 MB" - materialized view
- "Data scanned: 13.91 MB"

So, for the BigQuery the answer is:

- **0 MB for the External Table and 155.12 MB for the Materialized Table**

```sql
SELECT COUNT(DISTINCT PULocationID) FROM zoomcamp.yellow_taxi_external; 
SELECT COUNT(DISTINCT PULocationID) FROM zoomcamp.yellow_taxi_materialized;
```

### Question 3. Understanding columnar storage

- **BigQuery is a columnar database**, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.

### Question 4. Counting zero fare trips

- **8,333**

```sql
SELECT COUNT(*) FROM zoomcamp.yellow_taxi_materialized WHERE fare_amount = 0;
```

### Question 5. Partitioning and clustering

- **Partition by tpep_dropoff_datetime and Cluster on VendorID**

In Athena, this is achieved with `partitioned_by` + `bucketed_by` in CTAS:

```sql
CREATE TABLE zoomcamp.yellow_taxi_partitioned
WITH (
    format = 'PARQUET',
    external_location = 's3://de-zoomcamp-datalake/yellow_taxi_partitioned/',
    partitioned_by = ARRAY['dropoff_month'],
    bucketed_by = ARRAY['VendorID'],
    bucket_count = 4
) AS
SELECT *, DATE_FORMAT(tpep_dropoff_datetime, '%Y-%m') AS dropoff_month
FROM zoomcamp.yellow_taxi_external;
```

Monthly partitions are used to stay within Athena's 100-partition CTAS limit.

### Question 6: Partition benefits — data scanned comparison

- **310.24 MB for non-partitioned table and 26.84 MB for the partitioned table**

```sql
-- Non-partitioned:
SELECT DISTINCT VendorID FROM zoomcamp.yellow_taxi_materialized
WHERE tpep_dropoff_datetime >= TIMESTAMP '2024-03-01' AND tpep_dropoff_datetime < TIMESTAMP '2024-03-16';

-- Partitioned:
SELECT DISTINCT VendorID FROM zoomcamp.yellow_taxi_partitioned
WHERE dropoff_month = '2024-03';
```

For the Anthena:
- Data scanned: 93.43 MB - without partitioning
- Data scanned: 16.49 MB - with partitioning

### Question 7: Where is the data stored in the External Table?

- **GCP Bucket** 

Or S3 in AWS

### Question 8: Is it best practice to always cluster your data?

- **False**

Clustering adds overhead for small tables and high-cardinality columns.

### Question 9: SELECT COUNT(\*) — bytes scanned

- **0 bytes**

Both BigQuery and Athena resolve `COUNT(*)` from metadata (table stats / parquet footer row counts) without scanning data.
