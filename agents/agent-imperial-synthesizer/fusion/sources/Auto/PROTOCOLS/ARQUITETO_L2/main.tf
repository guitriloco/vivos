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
  }
}

provider "aws" {
  region = "us-east-1"
}

provider "digitalocean" {}

provider "google" {
  project = var.gcp_project
  region  = "us-central1"
}

# Deploy 5 niche environments with 99.99% availability logic (Multi-Cloud + Multi-Region)
module "niche_environments" {
  for_each             = toset(var.niches)
  source               = "./modules/niche"
  niche                = each.key
  instances_per_region = var.instances_per_region
  app_name             = var.app_name
  use_spot             = var.use_spot
  regions_aws          = var.regions_aws
  regions_do           = var.regions_do
  regions_gcp          = var.regions_gcp
}
