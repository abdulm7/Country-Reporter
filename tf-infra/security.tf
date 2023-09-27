resource "aws_security_group" "ctrl-pln-sg" {
  name        = "eksctl-cr-cluster-cluster-ControlPlaneSecurityGroup-WKM432F3J3K4"
  description = "Communication between the control plane and worker nodegroups"
  vpc_id      = aws_vpc.cr-vpc.id


  tags = {
    "Name"                                        = "eksctl-cr-cluster-cluster/ControlPlaneSecurityGroup"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
  }
  tags_all = {
    "Name"                                        = "eksctl-cr-cluster-cluster/ControlPlaneSecurityGroup"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
  }
}


resource "aws_security_group" "cluster-shared-node-sg" {
  name        = "eksctl-cr-cluster-cluster-ClusterSharedNodeSecurityGroup-CNN7I9QHCRRU"
  description = "Communication between all nodes in the cluster"
  vpc_id      = aws_vpc.cr-vpc.id
  tags = {
    "Name"                                        = "eksctl-cr-cluster-cluster/ClusterSharedNodeSecurityGroup"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
  }
  tags_all = {
    "Name"                                        = "eksctl-cr-cluster-cluster/ClusterSharedNodeSecurityGroup"
    "alpha.eksctl.io/cluster-name"                = "cr-cluster"
    "alpha.eksctl.io/cluster-oidc-enabled"        = "false"
    "alpha.eksctl.io/eksctl-version"              = "0.157.0"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "cr-cluster"
  }
}


resource "aws_security_group" "cr-cluster-eni-sg" {
  name        = "eks-cluster-sg-cr-cluster-177200484"
  description = "EKS created security group applied to ENI that is attached to EKS Control Plane master nodes, as well as any managed workloads."
  vpc_id      = aws_vpc.cr-vpc.id

  tags = {
    "Name"                             = "eks-cluster-sg-cr-cluster-177200484"
    "kubernetes.io/cluster/cr-cluster" = "owned"
  }
  tags_all = {
    "Name"                             = "eks-cluster-sg-cr-cluster-177200484"
    "kubernetes.io/cluster/cr-cluster" = "owned"
  }

}
