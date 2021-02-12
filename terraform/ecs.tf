resource "aws_ecs_service" "main" {
  name = var.service-name
  cluster = var.cluster-arn
  task_definition = aws_ecs_task_definition.main.arn
  launch_type = "FARGATE"
  desired_count = 1

  lifecycle {
    ignore_changes = [
      desired_count]
  }

  network_configuration {
    subnets          = [aws_default_subnet.default_subnet_a.id, aws_default_subnet.default_subnet_b.id]
  }

}

resource "aws_default_vpc" "default_vpc" {
}

resource "aws_default_subnet" "default_subnet_a" {
  availability_zone = "${var.aws_region}a"
}

resource "aws_default_subnet" "default_subnet_b" {
  availability_zone = "${var.aws_region}b"
}