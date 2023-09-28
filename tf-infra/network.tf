# Networking Services:

# Virtual Private Cloud (VPC)
# Subnets
# Route Tables
# Security Groups
# Network ACLs
# Identity and Access Management (IAM):

### VPC ###

resource "aws_vpc" "cr-vpc" {
  cidr_block = "192.168.0.0/16"

  tags = {
    "Name"                                        = "cr-vpc"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
  }
  tags_all = {
    "Name"                                        = "cr-vpc"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
  }
}

### Subnets ###

resource "aws_subnet" "cr_subnet_public1" {
  vpc_id     = aws_vpc.cr-vpc.id
  cidr_block = "192.168.32.0/19"

  map_public_ip_on_launch = true
  tags = {
    "Name"                                        = "cr-subnet-public1"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
    "kubernetes.io/role/elb"                      = "1"
  }
  tags_all = {
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
    "kubernetes.io/role/elb"                      = "1"
  }
}

resource "aws_subnet" "cr_subnet_public2" {
  vpc_id     = aws_vpc.cr-vpc.id
  cidr_block = "192.168.0.0/19"

  map_public_ip_on_launch = true
  tags = {
    "Name"                                        = "cr_subnet_public2"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
    "kubernetes.io/role/elb"                      = "1"
  }
  tags_all = {
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
    "kubernetes.io/role/elb"                      = "1"
  }
}

resource "aws_subnet" "cr_subnet_public3" {
  vpc_id     = aws_vpc.cr-vpc.id
  cidr_block = "192.168.64.0/19"

  map_public_ip_on_launch = true
  tags = {
    "Name"                                        = "cr_subnet_public3"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
    "kubernetes.io/role/elb"                      = "1"
  }
  tags_all = {
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
    "kubernetes.io/role/elb"                      = "1"

  }
}

resource "aws_subnet" "cr_subnet_priv1" {
  vpc_id     = aws_vpc.cr-vpc.id
  cidr_block = "192.168.128.0/19"

  tags = {
    "Name"                                        = "cr_subnet_priv1"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
    "kubernetes.io/role/internal-elb"             = "1"
  }
  tags_all = {
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
    "kubernetes.io/role/internal-elb"             = "1"
  }
}

resource "aws_subnet" "cr_subnet_priv2" {
  vpc_id     = aws_vpc.cr-vpc.id
  cidr_block = "192.168.96.0/19"

  tags = {
    "Name"                                        = "cr_subnet_priv2"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
    "kubernetes.io/role/internal-elb"             = "1"
  }
  tags_all = {
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
    "kubernetes.io/role/internal-elb"             = "1"
  }
}


resource "aws_subnet" "cr_subnet_priv3" {
  vpc_id     = aws_vpc.cr-vpc.id
  cidr_block = "192.168.160.0/19"

  tags = {
    "Name"                                        = "cr_subnet_priv3"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
    "kubernetes.io/role/internal-elb"             = "1"
  }
  tags_all = {
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
    "kubernetes.io/role/internal-elb"             = "1"
  }
}

### Route Tables ###

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.cr-vpc.id

  tags = {
    "Name"                                        = "eksctl-cr-cluster-cluster/PublicRouteTable"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
  }
  tags_all = {
    "Name"                                        = "eksctl-cr-cluster-cluster/PublicRouteTable"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
  }
}

resource "aws_route_table" "priv_ca1a_rt" {
  vpc_id = aws_vpc.cr-vpc.id
  tags = {
    "Name"                                        = "eksctl-cr-cluster-cluster/PrivateRouteTableCACENTRAL1A"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
  }
  tags_all = {
    "Name"                                        = "eksctl-cr-cluster-cluster/PrivateRouteTableCACENTRAL1A"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
  }
}

resource "aws_route_table" "priv_ca1b_rt" {
  vpc_id = aws_vpc.cr-vpc.id
  tags = {
    "Name"                                        = "eksctl-cr-cluster-cluster/PrivateRouteTableCACENTRAL1B"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
  }
  tags_all = {
    "Name"                                        = "eksctl-cr-cluster-cluster/PrivateRouteTableCACENTRAL1B"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
  }
}

resource "aws_route_table" "priv_ca1d_rt" {
  vpc_id = aws_vpc.cr-vpc.id
  tags = {
    "Name"                                        = "eksctl-cr-cluster-cluster/PrivateRouteTableCACENTRAL1D"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
  }
  tags_all = {
    "Name"                                        = "eksctl-cr-cluster-cluster/PrivateRouteTableCACENTRAL1D"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
  }
}
