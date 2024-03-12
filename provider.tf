provider "aws" {
  region = local.region
}


terraform {
  cloud {
    organization = "is-my-burguer"

    workspaces {
      name = "is-my-burguer-cognito"
    }
  }

  required_providers {
    aws = {
      version = "~> 5.38.0"
    }
  }
}
