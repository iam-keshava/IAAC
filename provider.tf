
# Configure the AWS Provider
provider "aws" {
  region = "ap-south-1"
}
terraform {
  backend "s3" {
    bucket  = "statefile-bucket-terraraja"
    key     = "terraform.tfstate"
    region  = "ap-south-1" # Specify the AWS region for your S3 bucket
    encrypt = true
    # dynamodb_table = "terraform-lock-table"  # Optional: Use DynamoDB for state locking
  }
}
