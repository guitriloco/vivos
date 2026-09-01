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
variable "niche" {}

resource "aws_instance" "app_node" {
  count         = var.instance_count
  ami           = "ami-0c55b159cbfafe1f0" # Placeholder Ubuntu AMI
  instance_type = "t3.medium"

  user_data = templatefile("${path.module}/../../scripts/bootstrap.sh.tpl", {
    niche_name = var.niche
  })

  tags = {
    Name   = "${var.app_name}-${var.niche}-node-${count.index}"
    Region = var.region
    Niche  = var.niche
  }
}

output "instance_ips" {
  value = aws_instance.app_node[*].public_ip
}
