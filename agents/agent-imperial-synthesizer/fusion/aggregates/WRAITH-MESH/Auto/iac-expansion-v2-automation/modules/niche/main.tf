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

# AWS Nodes for this niche
module "aws_nodes" {
  for_each       = toset(var.regions_aws)
  source         = "../compute_aws"
  region         = each.value
  instance_count = var.instances_per_region
  app_name       = var.app_name
  niche          = var.niche
  use_spot       = var.use_spot
}

# DO Nodes for this niche
module "do_nodes" {
  for_each       = toset(var.regions_do)
  source         = "../compute_do"
  region         = each.value
  instance_count = var.instances_per_region
  app_name       = var.app_name
  niche          = var.niche
  use_spot       = var.use_spot
}

# GCP Nodes for this niche
module "gcp_nodes" {
  for_each       = toset(var.regions_gcp)
  source         = "../compute_gcp"
  region         = each.value
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
    (var.niche) = concat(
      flatten([for m in module.aws_nodes : m.instance_ips]),
      flatten([for m in module.do_nodes : m.instance_ips]),
      flatten([for m in module.gcp_nodes : m.instance_ips])
    )
  }
}
