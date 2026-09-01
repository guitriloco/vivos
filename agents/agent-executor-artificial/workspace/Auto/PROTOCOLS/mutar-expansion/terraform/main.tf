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
  }
}

provider "aws" {
  region = "us-east-1"
}

provider "digitalocean" {}

# Deploy 5 niche environments
module "niche_environments" {
  for_each       = toset(var.niches)
  source         = "./modules/niche"
  niche          = each.key
  instance_count = var.instance_count
  app_name       = var.app_name
  use_spot       = var.use_spot
}
