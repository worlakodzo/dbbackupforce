
# EKS
variable "cluster_name" {}
variable "endpoint_private_access" {}
variable "endpoint_public_access" {}
variable "public_access_cidrs" {}
variable "node_group_name" {}
variable "scaling_desired_size" {}
variable "scaling_max_size" {}
variable "scaling_min_size" {}
variable "instance_types" {}
variable "key_pair" {}

# VPC
variable "vpc_cidr" {}
variable "access_ip" {}
variable "public_sn_count" {}
variable "public_cidrs" {type = list(any)}
variable "private_sn_count" {}
variable "private_cidrs" {type = list(any)}
variable "instance_tenancy" {}
variable "vpc_tags" {}
variable "map_public_ip_on_launch" {}
variable "rt_route_cidr_block" {}

