variable "instances_per_region" {}
variable "app_name" {}
variable "niche" {}
variable "use_spot" {
  default = false
}

variable "regions_aws" {
  type = list(string)
}
variable "regions_do" {
  type = list(string)
}
variable "regions_gcp" {
  type = list(string)
}

# AWS Nodes for this niche across multiple regions
module "aws_nodes" {
  for_each       = toset(var.regions_aws)
  source         = "../compute_aws"
  region         = each.key
  instance_count = var.instances_per_region
  app_name       = var.app_name
  niche          = var.niche
  use_spot       = var.use_spot
}

# DO Nodes for this niche across multiple regions
module "do_nodes" {
  for_each       = toset(var.regions_do)
  source         = "../compute_do"
  region         = each.key
  instance_count = var.instances_per_region
  app_name       = var.app_name
  niche          = var.niche
  use_spot       = var.use_spot
}

# GCP Nodes for this niche across multiple regions
module "gcp_nodes" {
  for_each       = toset(var.regions_gcp)
  source         = "../compute_gcp"
  region         = each.key
  instance_count = var.instances_per_region
  app_name       = var.app_name
  niche          = var.niche
  use_spot       = var.use_spot
}

# Monitoring for this niche
module "monitoring" {
  source   = "../monitoring"
  app_name = "${var.app_name}-${var.niche}"
  niches   = [var.niche]
  target_ips_by_niche = {
    (var.niche) = flatten([
      for provider_map in [module.aws_nodes, module.do_nodes, module.gcp_nodes] : [
        for region_module in provider_map : region_module.instance_ips
      ]
    ])
  }
}
