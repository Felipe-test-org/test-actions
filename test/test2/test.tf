terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
    }
  }
}
provider "aws" {
  region = "us-east-1"
}
resource "aws_s3_bucket" "mybucket" {
   acl = "private"
   versioning {
      enabled = false
   }
   server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
   tags = {
     Name = "mybucket"
     Environment = "Staging"
     Role = "Dev"
     Owner = "Felipe"
   }
}
resource "aws_s3_bucket_public_access_block" "mybucket-public-access" {
  bucket = aws_s3_bucket.mybucket.id

  block_public_acls   = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}
