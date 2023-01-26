# EKS
cluster_name            = "worlako-portfolio-eks"
endpoint_public_access  = true
endpoint_private_access = true
public_access_cidrs     = ["0.0.0.0/0"]
node_group_name         = "worlako-portfolio-cluster-node-group"
scaling_desired_size    = 4
scaling_max_size        = 4
scaling_min_size        = 2
instance_types          = ["t3.medium"]
key_pair                = "worlako-portfolio-eks-key"

# VPC
vpc_tags                = "worlako-portfolio-vpc"
instance_tenancy        = "default"
vpc_cidr                = "10.0.0.0/16"
access_ip               = "0.0.0.0/0"
public_sn_count         = 2
private_sn_count        = 2
public_cidrs            = ["10.0.1.0/24", "10.0.2.0/24"]
private_cidrs           = ["10.0.3.0/24", "10.0.4.0/24"]
map_public_ip_on_launch = true
rt_route_cidr_block     = "0.0.0.0/0"