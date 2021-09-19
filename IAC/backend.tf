terraform {
  backend "s3" {
    bucket = "terraform-monitor-provide-states-files"
    key    = "adapa-v2.tfstate"
    region = "us-east-1"
  }
}