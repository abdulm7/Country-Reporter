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

