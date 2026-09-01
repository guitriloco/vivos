terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
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

resource "google_compute_instance" "app_node" {
  count        = var.instance_count
  name         = "${var.app_name}-${var.niche}-node-${count.index}"
  machine_type = "e2-medium"
  zone         = "${var.region}-a"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }
  }

  network_interface {
    network = "default"
    access_config {
      // Ephemeral public IP
    }
  }

  metadata_startup_script = templatefile("${path.module}/../../scripts/bootstrap.sh.tpl", {
    niche_name = var.niche
  })

  scheduling {
    preemptible        = var.use_spot
    automatic_restart  = var.use_spot ? false : true
    provisioning_model = var.use_spot ? "SPOT" : "STANDARD"
  }

  labels = {
    niche = var.niche
    type  = var.use_spot ? "spot" : "on_demand"
  }
}

output "instance_ips" {
  value = google_compute_instance.app_node[*].network_interface.0.access_config.0.nat_ip
}
