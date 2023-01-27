resource "aws_eks_cluster" "self" {
  name     = var.cluster_name
  role_arn = aws_iam_role.cluster_role.arn

  vpc_config {
    subnet_ids              = var.aws_subnet_list
    endpoint_public_access  = var.endpoint_public_access
    endpoint_private_access = var.endpoint_private_access
    public_access_cidrs     = var.public_access_cidrs
    security_group_ids      = [aws_security_group.cluster.id]
  }

  depends_on = [
    aws_security_group.cluster,
    aws_iam_role_policy_attachment.self_AmazonEKSClusterPolicy,
    aws_iam_role_policy_attachment.self_AmazonEKSVPCResourceController,
  ]
}



# Create Key Pair
resource "tls_private_key" "self" {
  algorithm = "RSA"
  rsa_bits  = 4096
}


resource "aws_key_pair" "self" {
  key_name = var.key_pair
  public_key = tls_private_key.self.public_key_openssh

  depends_on = [aws_eks_cluster.self, tls_private_key.self]
}



resource "aws_eks_node_group" "self" {
  cluster_name    = aws_eks_cluster.self.name
  node_group_name = var.node_group_name
  node_role_arn   = aws_iam_role.node_role.arn
  subnet_ids      = var.aws_subnet_list
  instance_types  = var.instance_types

  remote_access {
    source_security_group_ids = [aws_security_group.node_group.id]
    ec2_ssh_key               = var.key_pair
  }

  scaling_config {
    desired_size = var.scaling_desired_size
    max_size     = var.scaling_max_size
    min_size     = var.scaling_min_size
  }

  depends_on = [
    aws_eks_cluster.self,
    aws_security_group.node_group,
    aws_key_pair.self,
    aws_iam_role_policy_attachment.self_AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.self_AmazonEKS_CNI_Policy,
    aws_iam_role_policy_attachment.self_AmazonEC2ContainerRegistryReadOnly,
  ]
}


resource "aws_security_group" "cluster" {
  name_prefix = var.cluster_name
  vpc_id      = var.vpc_id

  ingress {
    from_port = 80
    to_port   = 80
    protocol  = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_security_group" "node_group" {
  name_prefix = var.node_group_name
  vpc_id      = var.vpc_id



  ingress {
    description = "Ping"
    from_port   = 0
    to_port     = 0
    protocol    = "ICMP"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }


  ingress {
    from_port = 80
    to_port   = 80
    protocol  = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}




resource "aws_iam_role" "cluster_role" {
  name = "worlako_eks_cluster_role"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}


resource "aws_iam_role_policy_attachment" "self_AmazonEKSClusterPolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.cluster_role.name
}


# Optionally, enable Security Groups for Pods
# Reference: https://docs.aws.amazon.com/eks/latest/userguide/security-groups-for-pods.html
resource "aws_iam_role_policy_attachment" "self_AmazonEKSVPCResourceController" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSVPCResourceController"
  role       = aws_iam_role.cluster_role.name
}


resource "aws_iam_role" "node_role" {
  name = "worlako_eks_node_group_role"

  assume_role_policy = jsonencode({
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
    Version = "2012-10-17"
  })
}

resource "aws_iam_role_policy_attachment" "self_AmazonEKSWorkerNodePolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.node_role.name
}

resource "aws_iam_role_policy_attachment" "self_AmazonEKS_CNI_Policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.node_role.name
}

resource "aws_iam_role_policy_attachment" "self_AmazonEC2ContainerRegistryReadOnly" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.node_role.name
}




# Enabling IAM Role for Service Account
data "tls_certificate" "tls" {
  url = aws_eks_cluster.self.identity[0].oidc[0].issuer
}

resource "aws_iam_openid_connect_provider" "opidc" {
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.tls.certificates[0].sha1_fingerprint]
  url             = aws_eks_cluster.self.identity[0].oidc[0].issuer
}

data "aws_iam_policy_document" "self" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    condition {
      test     = "StringEquals"
      variable = "${replace(aws_iam_openid_connect_provider.opidc.url, "https://", "")}:sub"
      values   = ["system:serviceaccount:kube-system:aws-node"]
    }

    principals {
      identifiers = [aws_iam_openid_connect_provider.opidc.arn]
      type        = "Federated"
    }
  }
}




resource "null_resource" "kubectl" {

  depends_on = [aws_eks_cluster.self, aws_eks_node_group.self]



  // Update kubeconfig file
  provisioner "local-exec" {
    command = "aws eks update-kubeconfig --name worlako-portfolio-eks --region us-west-2"
  }


  // Create namespaces
  provisioner "local-exec" {
    command = "kubectl apply -f ${path.module}/manifest/namespaces.yaml"
  }

  // Create Storage Class 
  provisioner "local-exec" {
    command = "helm install local-path-storage ${path.module}/manifest/storage-class/"
  }


  # Add local-path storage class default
  provisioner "local-exec" {
    working_dir = "${path.module}/script/"
    command = "bash add-storage-class-to-default.sh"
  }

  # Remove gp2 storage class default
  provisioner "local-exec" {
    working_dir = "${path.module}/script/"
    command = "bash remove-storage-class-from-default.sh"
  }

}



# argocd deployment
resource "helm_release" "argocd" {

  name       = "argocd"
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  version    = "5.17.0" #"5.19.x"

  values = [
    file("${path.module}/manifest/argocd-values.yaml")
  ]

  namespace = "argocd"

  depends_on = [null_resource.kubectl]
}


resource "helm_release" "nginx_ingress" {
  name       = "nginx-ingress-controller"

  repository = "https://charts.bitnami.com/bitnami"
  chart      = "nginx-ingress-controller"
  version    = "9.3.26"

  values = [
    file("${path.module}/manifest/ingress-nginx-values.yaml")
  ]

  depends_on = [helm_release.argocd]

}