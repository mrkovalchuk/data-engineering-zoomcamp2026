## Homework 1: Docker, SQL and Terraform for Data Engineering Zoomcamp 2026

### Question 1. What's the version of pip in the python:3.13 image?
```bash
~/projects/data-engineering-zoomcamp2026 (main) » docker run -it python:3.13 bash                                                   andreikovalcuk@Andreis-MacBook-Pro
root@65416e79ca42:/# pip --version
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
```
- 25.3

### Question 2. Given the docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?
- db:5432
- postgres:5432

both will do

### Question 3. For the trips in November 2025, how many trips had a trip_distance of less than or equal to 1 mile?
- 8007

```sql
SELECT
    COUNT(1)
FROM
    yellow_taxi_data as t
WHERE
    t.lpep_pickup_datetime >= '2025-11-01' AND t.lpep_pickup_datetime < '2025-12-01' 
	and t.trip_distance <= 1
;
```

### Question 4. Longest trip for each day
Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors).

- 2025-11-14

```sql
SELECT
    date_trunc('day', t.lpep_pickup_datetime) as day,
	MAX(t.trip_distance) as longesttrip
FROM
    yellow_taxi_data as t
WHERE
    t.trip_distance < 100
GROUP BY
	day
ORDER BY 
    longesttrip DESC
LIMIT 1
;
```

### Question 5. Biggest pickup zone
Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?

- East Harlem North

```sql
SSELECT
	t."PULocationID" as pickup,
	z."Zone" as location,
	SUM(t.total_amount) as total
FROM
    yellow_taxi_data as t
JOIN 
	zones as z ON t."PULocationID" = z."LocationID"
WHERE
    t.lpep_pickup_datetime >= '2025-11-18 00:00:00'
    AND t.lpep_pickup_datetime <  '2025-11-19 00:00:00'
GROUP BY
    pickup, location
ORDER BY 
	total DESC
LIMIT 1;
```

### Question 6. Largest tip
For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

- Yorkville West

```sql
SELECT
	t."DOLocationID" as dropoff,
	z."Zone" as zone_name,
	t.tip_amount
FROM
    yellow_taxi_data as t
JOIN 
	zones as z ON t."DOLocationID" = z."LocationID"
WHERE
    t.lpep_pickup_datetime >= '2025-11-01 00:00:00'
    AND t.lpep_pickup_datetime <  '2025-12-01 00:00:00'
	AND t."PULocationID" = 74
ORDER BY 
	tip_amount DESC
;
```