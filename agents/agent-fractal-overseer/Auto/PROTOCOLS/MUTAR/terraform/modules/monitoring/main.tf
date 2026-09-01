variable "app_name" {}
variable "niches" {
  type = list(string)
}
variable "target_ips_by_niche" {
  type = map(list(string))
}

resource "aws_instance" "global_monitoring" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.large"

  user_data = templatefile("${path.module}/monitoring_bootstrap.sh.tpl", {
    target_ips_by_niche = var.target_ips_by_niche
  })

  tags = {
    Name = "${var.app_name}-global-monitoring"
  }
}

output "monitoring_ip" {
  value = aws_instance.global_monitoring.public_ip
}
