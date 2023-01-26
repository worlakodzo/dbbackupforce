module "eks" {
  source                  = "./modules/eks"
  aws_subnet_list         = module.vpc.aws_subnet_list
  vpc_id                  = module.vpc.vpc_id
  cluster_name            = var.cluster_name
  endpoint_public_access  = var.endpoint_public_access
  endpoint_private_access = var.endpoint_private_access
  public_access_cidrs     = var.public_access_cidrs
  node_group_name         = var.node_group_name
  scaling_desired_size    = var.scaling_desired_size
  scaling_max_size        = var.scaling_max_size
  scaling_min_size        = var.scaling_min_size
  instance_types          = var.instance_types
  key_pair                = var.key_pair
}

module "vpc" {
  source                  = "./modules/vpc"
  tags                    = var.vpc_tags
  instance_tenancy        = var.instance_tenancy
  vpc_cidr                = var.vpc_cidr
  access_ip               = var.access_ip
  public_sn_count         = var.public_sn_count
  public_cidrs            = var.public_cidrs
  private_sn_count        = var.private_sn_count
  private_cidrs           = var.private_cidrs
  map_public_ip_on_launch = var.map_public_ip_on_launch
  rt_route_cidr_block     = var.rt_route_cidr_block

}