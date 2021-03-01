module "inferencer" {
  source = "git::https://github.com/AlienX456/SoundMonitor-IAC-Infrastructure-Common.git//inferencer"

  cluster-name= var.cluster-name
  service-name= var.service-name
  family-name = var.family-name
  soundmonitor-main-subnet= var.soundmonitor-main-subnet
  cpu= var.cpu
  memory= var.memory

  aws_region= "us-east-1"
  aws_provider_key= var.aws_provider_key
  aws_provider_secret= var.aws_provider_secret

  aws_inferencer_key= var.aws_inferencer_key
  aws_inferencer_secret= var.aws_inferencer_secret

  kafka_group_id= var.kafka_group_id
  kafka_audio_upload_event= var.kafka_audio_upload_event
  kafka_inference_event= var.kafka_inference_event
  kafka_encode_format= var.kafka_encode_format
  kafka_server= var.kafka_server

  ecr_image_tag= var.ecr_image_tag
  ecr_image_repo= var.ecr_image_repo
  records_bucket_name= var.records_bucket_name

  device_selector= var.device_selector
}