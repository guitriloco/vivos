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
variable "niche" {}
variable "use_spot" {
  default = false
}

resource "digitalocean_droplet" "app_node" {
  count  = var.instance_count
  name   = "${var.app_name}-${var.niche}-node-${count.index}"
  region = var.region
  size   = "s-2vcpu-4gb"
  image  = "ubuntu-22-04-x64"

  # Necromancy Logic: DigitalOcean currently managed via tags for cost audit
  # (Native Preemptible support pending provider update)
  # preemptible = var.use_spot

  user_data = templatefile("${path.module}/../../scripts/bootstrap.sh.tpl", {
    niche_name = var.niche
  })

  tags = [
    var.niche,
    var.use_spot ? "SPOT" : "ON_DEMAND"
  ]
}

output "instance_ips" {
  value = digitalocean_droplet.app_node[*].ipv4_address
}
