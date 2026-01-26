FROM python:3.13.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code
ENV PATH="/code/.venv/bin:$PATH"
ENV TAXI_DATA_URL="https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
ENV ZONES_DATA_URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"

COPY pyproject.toml .python-version uv.lock ./
RUN uv sync --locked

COPY pipeline/ingest_data.py .

ENTRYPOINT ["uv", "run", "python", "ingest_data.py"]