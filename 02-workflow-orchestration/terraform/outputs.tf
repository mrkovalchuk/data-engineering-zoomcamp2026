output "s3_bucket_name" {
  description = "S3 bucket name (Kestra KV: S3_BUCKET_NAME)"
  value       = aws_s3_bucket.data_lake.bucket
}

output "glue_database_name" {
  description = "Glue database name (Kestra KV: AWS_DATASET)"
  value       = aws_glue_catalog_database.dataset.name
}

output "athena_output_location" {
  description = "Athena query results location (Kestra KV: ATHENA_OUTPUT_LOCATION)"
  value       = "s3://${aws_s3_bucket.data_lake.bucket}/athena-results/"
}

output "kestra_access_key_id" {
  description = "Access key ID for Kestra (Kestra KV: AWS_ACCESS_KEY_ID)"
  value       = aws_iam_access_key.kestra.id
}

output "kestra_secret_access_key" {
  description = "Secret access key for Kestra (Kestra KV: AWS_SECRET_ACCESS_KEY)"
  value       = aws_iam_access_key.kestra.secret
  sensitive   = true
}
