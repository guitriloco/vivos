variable "instance_count" {
  description = "Number of instances to deploy per region"
  type        = number
  default     = 10
}

variable "regions_aws" {
  description = "AWS regions to deploy to"
  type        = list(string)
  default     = ["us-east-1", "eu-west-1", "ap-southeast-1"]
}

variable "regions_do" {
  description = "DigitalOcean regions to deploy to"
  type        = list(string)
  default     = ["nyc1", "ams3", "sgp1"]
}

variable "app_name" {
  description = "Name of the application"
  type        = string
  default     = "devops-squad-app"
}

variable "niches" {
  description = "List of high-margin niches to deploy"
  type        = list(string)
  default     = ["bio-wealth", "financas", "e-commerce", "health-tech", "real-estate"]
}
