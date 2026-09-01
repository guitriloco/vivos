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
variable "use_spot" {
  default = false
}

data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_instance" "app_node" {
  count             = var.instance_count
  ami               = "ami-0c55b159cbfafe1f0" # Placeholder Ubuntu AMI
  instance_type     = "t3.medium"
  availability_zone = data.aws_availability_zones.available.names[count.index % length(data.aws_availability_zones.available.names)]

  user_data = templatefile("${path.module}/../../scripts/bootstrap.sh.tpl", {
    niche_name = var.niche
  })

  # Necromancy Logic: Enable Spot Instances if use_spot is true
  dynamic "instance_market_options" {
    for_each = var.use_spot ? [1] : []
    content {
      market_type = "spot"
      spot_options {
        max_price = "0.05" # ROI Optimization Limit
      }
    }
  }

  tags = {
    Name   = "${var.app_name}-${var.niche}-node-${count.index}"
    Region = var.region
    Niche  = var.niche
    Type   = var.use_spot ? "SPOT" : "ON_DEMAND"
  }
}

output "instance_ips" {
  value = aws_instance.app_node[*].public_ip
}
