variable "region" {}
variable "worker_pool_id" {}
variable "worker_pool_config_b64" {}

resource "google_compute_instance" "spacelift_worker" {
  name         = "spacelift-worker-${var.region}"
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

  metadata_startup_script = <<-EOT
    #!/bin/bash
    apt-get update
    apt-get install -y docker.io
    docker run -d \
      --name spacelift-worker \
      --restart always \
      -v /var/run/docker.sock:/var/run/docker.sock \
      -e SPACELIFT_TOKEN=${var.worker_pool_config_b64} \
      -e SPACELIFT_POOL_ID=${var.worker_pool_id} \
      spacelift/worker-launcher
  EOT

  labels = {
    type = "spacelift-worker"
    region = var.region
  }
}

output "instance_ip" {
  value = google_compute_instance.spacelift_worker.network_interface.0.access_config.0.nat_ip
}
