output "aws_subnet_list" {
  # value = flatten([aws_subnet.public[*].id, aws_subnet.private[*].id])
  value = flatten([aws_subnet.public[*].id])
}

output "vpc_id" {
  value = aws_vpc.self.id
}