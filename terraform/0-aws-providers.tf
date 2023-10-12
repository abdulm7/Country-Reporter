provider "aws" {
  region = "ca-central-1"
}


terraform {
  required_version = "~> 1.0"

  backend "remote" {
    organization = "AM-ORG"
    workspaces {
      name = "Country-Reporter"
    }

  }

  required_providers {
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = ">= 1.7.0"
    }

    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.6.0"
    }
  }
}
