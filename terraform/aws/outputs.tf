output "server_public_ip" {
  value       = aws_instance.server.public_ip
  description = "Public IP of the CloudOpsHub server"
}

output "vpc_id" {
  value = aws_vpc.main.id
}

output "security_group_id" {
  value = aws_security_group.server.id
}
