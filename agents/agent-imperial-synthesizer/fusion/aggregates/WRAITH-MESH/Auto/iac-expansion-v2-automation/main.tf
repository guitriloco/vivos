terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    spacelift = {
      source = "spacelift-io/spacelift"
    }
  }
}

provider "aws" {
  region = "us-east-1"
  # Optimization for high-scale provisioning
  max_retries = 10
  retry_mode  = "adaptive"
}

provider "digitalocean" {
  # Credentials handled via environment variables
}

provider "google" {
  project = var.gcp_project
  region  = "us-central1"
  # Optimization for latency and reliability
  request_timeout = "60s"
}

# Deploy 5 niche environments with 99.99% availability logic (Multi-Cloud + Multi-Region)
module "niche_environments" {
  for_each             = toset(var.niches)
  source               = "./modules/niche"
  niche                = each.key
  instances_per_region = var.instance_count
  app_name             = var.app_name
  use_spot             = var.use_spot
  regions_aws          = var.regions_aws
  regions_do           = var.regions_do
  regions_gcp          = var.regions_gcp
}

# Regional Spacelift Private Worker Pools for Sovereignty
module "spacelift_workers" {
  for_each               = toset(var.regions_gcp)
  source                 = "./modules/spacelift_worker"
  region                 = each.value
  worker_pool_id         = "gcp-${each.value}-pool"
  worker_pool_config_b64 = var.spacelift_worker_pool_config_b64
}
