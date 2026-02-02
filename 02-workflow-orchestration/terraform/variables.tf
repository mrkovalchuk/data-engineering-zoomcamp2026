variable "aws_region" {
  description = "AWS region to deploy resources in"
  type        = string
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "S3 bucket for staging data, Iceberg warehouse, and Athena results"
  type        = string
  default     = "kestra-sandbox-zoomcamp"
}

variable "dataset_name" {
  description = "Glue Catalog database name used by Athena"
  type        = string
  default     = "zoomcamp"
}

variable "iam_user_name" {
  description = "IAM user name for Kestra service account"
  type        = string
  default     = "kestra-service"
}
