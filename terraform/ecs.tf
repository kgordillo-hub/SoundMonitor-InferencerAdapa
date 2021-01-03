resource "aws_ecs_cluster" "main" {
  name = "monitor-inferencers-cluster"
}


resource "aws_ecs_service" "main" {
  name            = "monitor-adapa-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.main.arn
  launch_type     = "FARGATE"
  desired_count   = 1

  network_configuration {
    subnets          = [aws_default_subnet.default_subnet_a.id, aws_default_subnet.default_subnet_b.id]
    assign_public_ip = true
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