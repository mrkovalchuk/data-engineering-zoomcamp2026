output "s3_bucket_name" {
  description = "S3 bucket name"
  value       = aws_s3_bucket.data_lake.bucket
}

output "glue_database_name" {
  description = "Glue database name for Athena queries"
  value       = aws_glue_catalog_database.dataset.name
}

output "athena_output_location" {
  description = "S3 location for Athena query results"
  value       = "s3://${aws_s3_bucket.data_lake.bucket}/athena-results/"
}
