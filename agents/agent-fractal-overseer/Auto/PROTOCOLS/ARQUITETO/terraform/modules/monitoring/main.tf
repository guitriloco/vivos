terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "app_name" {}
variable "target_ips" {
  type = list(string)
}

resource "aws_instance" "monitoring" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.large"

  user_data = templatefile("${path.module}/monitoring_bootstrap.sh.tpl", {
    target_ips = var.target_ips
  })

  tags = {
    Name = "${var.app_name}-monitoring"
  }
}

output "monitoring_ip" {
  value = aws_instance.monitoring.public_ip
}
