variable "instance_count" {}
variable "app_name" {}
variable "niche" {}

# AWS Nodes for this niche
module "aws_nodes" {
  source         = "../compute_aws"
  region         = "us-east-1"
  instance_count = var.instance_count
  app_name       = var.app_name
  niche          = var.niche
}

# DO Nodes for this niche
module "do_nodes" {
  source         = "../compute_do"
  region         = "nyc1"
  instance_count = var.instance_count
  app_name       = var.app_name
  niche          = var.niche
}

# Monitoring for this niche
module "monitoring" {
  source   = "../monitoring"
  app_name = "${var.app_name}-${var.niche}"
  niches   = [var.niche]
  target_ips_by_niche = {
    (var.niche) = concat(
      module.aws_nodes.instance_ips,
      module.do_nodes.instance_ips
    )
  }
}
