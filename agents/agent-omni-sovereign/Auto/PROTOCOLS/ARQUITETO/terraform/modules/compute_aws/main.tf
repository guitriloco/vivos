terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "instance_count" {}
variable "region" {}
variable "app_name" {}

resource "aws_instance" "app_node" {
  count         = var.instance_count
  ami           = "ami-0c55b159cbfafe1f0" # Placeholder Ubuntu AMI
  instance_type = "t3.medium"

  user_data = file("${path.module}/../../scripts/bootstrap.sh")

  tags = {
    Name   = "${var.app_name}-node-${count.index}"
    Region = var.region
  }
}

output "instance_ips" {
  value = aws_instance.app_node[*].public_ip
}
