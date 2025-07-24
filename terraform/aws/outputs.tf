output "cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = aws_eks_cluster.metricflow_cluster.endpoint
}

output "cluster_security_group_id" {
  description = "Security group ids attached to the cluster control plane"
  value       = aws_eks_cluster.metricflow_cluster.vpc_config[0].cluster_security_group_id
}

output "cluster_name" {
  description = "Kubernetes Cluster Name"
  value       = aws_eks_cluster.metricflow_cluster.name
}

output "rds_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.metricflow_db.endpoint
  sensitive   = true
}