terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

variable "instance_count" {}
variable "region" {}
variable "app_name" {}

resource "digitalocean_droplet" "app_node" {
  count  = var.instance_count
  name   = "${var.app_name}-node-${count.index}"
  region = var.region
  size   = "s-2vcpu-4gb"
  image  = "ubuntu-22-04-x64"

  user_data = file("${path.module}/../../scripts/bootstrap.sh")
}

output "instance_ips" {
  value = digitalocean_droplet.app_node[*].ipv4_address
}
