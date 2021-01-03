resource "aws_ecs_task_definition" "main" {
  family = var.family-name
  container_definitions = <<EOF
  [
    {
      "name": "repo-inferencer",
      "image": "602326443068.dkr.ecr.us-east-1.amazonaws.com/repo-inferencer:${var.ecr_image_tag}",
      "cpu": 0,
      "portMappings": [],
      "essential": true,
      "environment": [
          {
              "name": "MODEL_NAME",
              "value": "model_system1"
          },
          {
              "name": "DEVICE_NAME",
              "value": "cpu"
          },
          {
              "name": "DATA_PATH",
              "value": "data/"
          },
          {
              "name": "MODEL_URL",
              "value": "https://github.com/sainathadapa/dcase2019-task5-urban-sound-tagging/releases/download/1.0/model_system1"
          },
          {
              "name": "GROUP_ID",
              "value": "inferencer-group"
          },
          {
              "name": "AUDIO_UPLOAD_EVENT",
              "value": "audio-upload-event"
          },
          {
              "name": "KAFKA_SERVER",
              "value": "200.69.103.29:26240"
          },
          {
              "name": "AWS_KEY",
              "value": "${var.aws_inferencer_key}"
          },
          {
              "name": "AWS_SECRET",
              "value": "${var.aws_inferencer_secret}"
          },
          {
              "name": "ENCODE_FORMAT",
              "value": "utf-8"
          },
          {
              "name": "CHANNEL_MEANS_FILE",
              "value": "channel_means.npy"
          },
          {
              "name": "INFERENCE_EVENT",
              "value": "inference-event"
          },
          {
              "name": "BUCKET_NAME",
              "value": "sistemamonitoreoacustico"
          },
          {
              "name": "CHANNEL_STDS_FILE",
              "value": "channel_stds.npy"
          }
      ],
      "mountPoints": [],
      "volumesFrom": [],
      "logConfiguration": {
          "logDriver": "awslogs",
          "options": {
              "awslogs-group": "/ecs/monitor-adapa",
              "awslogs-region": "us-east-1",
              "awslogs-stream-prefix": "ecs"
          }
      }
    }
  ]
  EOF

  cpu = 256
  memory = 512
  requires_compatibilities = ["FARGATE"]
  network_mode = "awsvpc"
  execution_role_arn = aws_iam_role.monitor-adapa-task-execution-role.arn
}