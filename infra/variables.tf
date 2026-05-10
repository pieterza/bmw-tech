variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
}

variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "bmw-eks"
}

variable "cluster_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.35"
}
