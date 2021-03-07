variable "cluster-name" {
  default = "monitor-inferencers-cluster"
}

variable "soundmonitor-main-subnet" {
    description = "subnet of SoundMonitorVPC"
}

variable "service-name" {
  default = "monitor-inferencer-service"
}

variable "aws_region" {
  description = "AWS Region to deploy"
  default = "us-east-1"
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

variable "records_bucket_name" {
  description =  "audio files bucket NAME"
}

variable "cpu" {
  description =  "Cpu"
}

variable "memory" {
  description =  "Memory"
}

variable "kafka_group_id" {
  description = "Kafka inferencers group id"
}

variable "kafka_audio_upload_event" {
  description = "Kafka event of audio uploading"
}
variable "kafka_inference_event" {
  description = "Kafka event of inference"
}

variable "kafka_encode_format" {
  description = "encode format"
}

variable "ecr_image_repo" {
  description = "Inferencer repo"
}

variable "kafka_server" {
  description =  "Endpoint of kafkaserver"
}

variable "device_selector" {
  description =  "Device to use"
}

variable "family-name" {
  default = "monitor-inferencer"
}
