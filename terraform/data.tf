variable "family-name" {
  default = "monitor-inferencer-adapa"
}

variable "cluster-name" {
  default = "monitor-inferencers-cluster"
}

variable "service-name" {
  default = "monitor-adapa-service"
}

variable "aws_region" {
  description = "AWS Region to deploy"
}

variable "aws_provider_key" {
  description = "AWS key for deploy and infrastructure providing"
}

variable "aws_provider_secret" {
  description = "AWS secret for deploy and infrastructure providing"
}

variable "aws_inferencer_key" {
  description = "AWS key for inferencer"
}

variable "aws_inferencer_secret" {
  description = "AWS secret for inferencer"
}

variable "ecr_image_tag" {
  description = "Inferencer latest image tag"
}