data "aws_caller_identity" "current" {}

data "aws_availability_zones" "available" {}

data "terraform_remote_state" "is-my-burguer-postgres" {
  backend = "remote"

  config = {
    organization = "is-my-burguer"
    workspaces = {
      name = "is-my-burguer-postgres"
    }
  }
}
