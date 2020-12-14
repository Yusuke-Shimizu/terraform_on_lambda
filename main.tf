provider "aws" {
  region  = "ap-northeast-1"
}

resource "aws_s3_bucket" "default" {
  bucket = "created-by-lambda"
  acl    = "private"
}
