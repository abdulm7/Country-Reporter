# Networking Services:

# Virtual Private Cloud (VPC)
# Subnets
# Route Tables
# Security Groups
# Network ACLs
# Identity and Access Management (IAM):

# IAM Roles
# IAM Policies
# Instance Profiles
# Amazon EKS:

# Amazon EKS Cluster
# Compute Resources:

# Managed Node Groups (if applicable)
# EC2 Instances (if manually managing worker nodes)
# Load Balancers and Ingress Controllers:

# Application Load Balancers (ALB)
# Network Load Balancers (NLB)
# Ingress Controllers (e.g., Nginx Ingress Controller)

# Container Registries:

# Amazon Elastic Container Registry (ECR)
# Docker Registries (if using a different registry)
# Route 53 (DNS):

# Hosted Zones
# DNS Records
# Database Services:

# Amazon RDS (Relational Database Service)
# Amazon DynamoDB (NoSQL Database)
# Storage Services:

# Amazon S3 (Simple Storage Service)
# Amazon EBS (Elastic Block Store) Volumes (if applicable)
# Other Application Services:

# AWS Lambda (if used for serverless functions)
# Amazon API Gateway (if used for API management)
# Amazon Elasticsearch Service (if used for search)
# Frontend-Related Resources:

# Load Balancer Target Groups
# Amazon CloudFront (Content Delivery Network)
# Amazon S3 Buckets (for static assets)
# Application-specific resources, such as AWS Lambda functions or API Gateway endpoints used by the frontend.

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "ca-central-1"
}

resource "aws_iam_role" "cr_cluster_service_role" {
  name = "eksctl-cr-cluster-cluster-ServiceRole-1Q6VQWZA14CWN"

  assume_role_policy = <<EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": "sts:AssumeRole",
          "Effect": "Allow",
          "Principal": {
            "Service": "eks.amazonaws.com"
          }
        }
      ]
    }
  EOF

  tags = {
    "Name"                                        = "eksctl-cr-cluster-cluster/ServiceRole"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
  }
  tags_all = {
    "Name"                                        = "eksctl-cr-cluster-cluster/ServiceRole"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
  }
}

### EKS CLUSTER ###

resource "aws_eks_cluster" "cr-cluster" {
  name     = "cr-cluster"
  role_arn = aws_iam_role.cr_cluster_service_role.arn

  vpc_config {
    public_access_cidrs = [
      "0.0.0.0/0",
    ]
    security_group_ids = [
      aws_security_group.ctrl-pln-sg.id
    ]
    subnet_ids = [
      aws_subnet.cr_subnet_public1.id, aws_subnet.cr_subnet_public2.id,
      aws_subnet.cr_subnet_public3.id, aws_subnet.cr_subnet_priv1.id,
      aws_subnet.cr_subnet_priv2.id, aws_subnet.cr_subnet_priv3.id
    ]
  }

  tags = {
    "Name"                                        = "eksctl-cr-cluster-cluster/ControlPlane"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
  }
  tags_all = {
    "Name"                                        = "eksctl-cr-cluster-cluster/ControlPlane"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
  }
}
