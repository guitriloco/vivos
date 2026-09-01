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
  alias  = "us_east_1"
}

provider "aws" {
  region = "eu-west-1"
  alias  = "eu_west_1"
}

provider "digitalocean" {}

# AWS - US East 1
module "aws_nodes_us_east_1" {
  source = "./modules/compute_aws"
  providers = {
    aws = aws.us_east_1
  }
  region         = "us-east-1"
  instance_count = var.instance_count
  app_name       = var.app_name
}

# AWS - EU West 1
module "aws_nodes_eu_west_1" {
  source = "./modules/compute_aws"
  providers = {
    aws = aws.eu_west_1
  }
  region         = "eu-west-1"
  instance_count = var.instance_count
  app_name       = var.app_name
}

# DigitalOcean - NYC1
module "do_nodes_nyc1" {
  source         = "./modules/compute_do"
  region         = "nyc1"
  instance_count = var.instance_count
  app_name       = var.app_name
}

# Global Monitoring
module "monitoring" {
  source   = "./modules/monitoring"
  app_name = var.app_name
  # Pass all node IPs to monitoring for scraping
  target_ips = concat(
    module.aws_nodes_us_east_1.instance_ips,
    module.aws_nodes_eu_west_1.instance_ips,
    module.do_nodes_nyc1.instance_ips
  )
}
