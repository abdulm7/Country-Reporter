module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "18.29.0"

  cluster_name    = "cr-cluster"
  cluster_version = "1.25"

  cluster_endpoint_private_access = true
  # remove public access
  cluster_endpoint_public_access  = true

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  enable_irsa = true

  eks_managed_node_groups = {
    general = {
      desired_size = 1
      min_size     = 1
      max_size     = 6

      labels = {
        role = "on-demand"
      }

      instance_types = ["t3.micro"]
      capacity_type  = "ON_DEMAND"

    }

    spot = {
      desired_size = 1
      min_size     = 1
      max_size     = 6

      labels = {
        role = "spot"
      }

      instance_types = ["t3.micro"]
      capacity_type  = "SPOT"
    }
  }

}
