terraform {
  backend "s3" {
    bucket  = "terraform-monitor-provide-states-files"
    key     = "inferencer-adapa.tfstate"
    region  = "us-east-1"
  }
}