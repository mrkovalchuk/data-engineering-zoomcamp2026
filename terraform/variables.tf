variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "S3 bucket for data lake (parquet files, Athena results, warehouse)"
  type        = string
  default     = "de-zoomcamp-datalake"
}

variable "dataset_name" {
  description = "Glue Catalog database name used by Athena"
  type        = string
  default     = "zoomcamp"
}
