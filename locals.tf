locals {
  name   = "is-my-burguer"
  region = "us-east-1"

  tags = {
    Example = local.name
  }
}
