terraform {

  required_providers {

    aws = {
      source  = "hashicorp/aws"
      # version = "~> 4.15.0"
    }

    random = {
      source  = "hashicorp/random"
      # version = "3.1.0"
    }

    kubernetes = {
      source  = "hashicorp/kubernetes"
      # version = ">= 2.0.1"
    }

    helm = {
      source = "hashicorp/helm"
      version = "2.8.0"
    }

  }

  backend "s3" {
    bucket         = "worlakoterraformstate"
    key            = "store/terraform.tfstate"
    region         = "us-west-2"
    dynamodb_table = "worlakoterraformstatelock"
    encrypt = true

  }


}


data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_id
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_id
}


provider "kubernetes" {
  cluster_ca_certificate = base64decode(module.eks.kubeconfig-certificate-authority-data)
  host                   = data.aws_eks_cluster.cluster.endpoint
  token                  = data.aws_eks_cluster_auth.cluster.token
}

provider "helm" {
  kubernetes {
    cluster_ca_certificate = base64decode(module.eks.kubeconfig-certificate-authority-data)
    host                   = data.aws_eks_cluster.cluster.endpoint
    token                  = data.aws_eks_cluster_auth.cluster.token
    exec {
      api_version = "client.authentication.k8s.io/v1"
      args        = ["eks", "get-token", "--cluster-name", data.aws_eks_cluster.cluster.name]
      command     = "aws"
    }
  }
}


provider "aws" {
  region                   = "us-west-2"
  # shared_config_files      = ["~/.aws/config"]
  # shared_credentials_files = ["~/.aws/credentials"]
  # profile                  = "worlako-aws-iam-connection"

  default_tags {
    tags = {
      Project         = "WorlakoPorfolio"
      Environment     = "Production"
      Manager         = "TFProviders"
      owner           = "Worlako"
      bootcamp        = "ghana1"
      expiration_date = "05-02-23"
    }
  }

}


# random string for availability zone 
# selection
resource "random_string" "suffix" {
  length  = 5
  special = false
}





