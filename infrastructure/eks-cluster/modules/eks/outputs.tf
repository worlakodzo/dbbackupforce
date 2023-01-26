output "endpoint" {
  value = aws_eks_cluster.self.endpoint
}
output "kubeconfig-certificate-authority-data" {
  value = aws_eks_cluster.self.certificate_authority[0].data
}
output "cluster_id" {
  value = aws_eks_cluster.self.id
}
output "cluster_endpoint" {
  value = aws_eks_cluster.self.endpoint
}
output "cluster_name" {
  value = aws_eks_cluster.self.name
}
output "node_group_name" {
  value = aws_eks_node_group.self.node_group_name
}

output "ssh_private_key_pem" {
  value = tls_private_key.self.private_key_pem
}

output "ssh_public_key_pem" {
  value = tls_private_key.self.public_key_pem
}