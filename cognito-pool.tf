resource "aws_cognito_user_pool" "is-my-burguer" {

  name              = local.name
  mfa_configuration = "OFF"

  alias_attributes = [ "email", "preferred_username" ]
  auto_verified_attributes = ["email"]

  account_recovery_setting {
    recovery_mechanism {
      name     = "verified_email"
      priority = 1
    }
  }

  email_configuration {
    email_sending_account = "COGNITO_DEFAULT"
  }

  username_configuration {
    case_sensitive = false
  }

  schema {
    attribute_data_type      = "String"
    developer_only_attribute = false
    mutable                  = true
    name                     = "CPF"
    required                 = false

    string_attribute_constraints {
      min_length = 11
      max_length = 11
    }
  }

}

resource "random_string" "random" {
  length  = 16
  special = false
  upper   = false
}

resource "aws_cognito_user_pool_domain" "cognito-domain" {
  domain       = random_string.random.result
  user_pool_id = aws_cognito_user_pool.is-my-burguer.id
}

resource "aws_cognito_resource_server" "is-my-burguer-resource-server" {
  identifier = "is-my-burguer-resource-server"
  name       = "is-my-burguer-resource-server"

  scope {
    scope_name        = "read"
    scope_description = "read"
  }

  scope {
    scope_name        = "write"
    scope_description = "write"
  }

  user_pool_id = aws_cognito_user_pool.is-my-burguer.id
}

resource "aws_cognito_user_pool_client" "is-my-burguer-api-client" {
  name = "is-my-burguer-api-client"

  user_pool_id = aws_cognito_user_pool.is-my-burguer.id

  generate_secret                      = true
  allowed_oauth_flows_user_pool_client = true
  explicit_auth_flows                  = ["ADMIN_NO_SRP_AUTH"]
  callback_urls                        = ["http://localhost/swagger-ui/index.hmtl"]
  allowed_oauth_flows                  = ["client_credentials"]
  allowed_oauth_scopes = [
    "${aws_cognito_resource_server.is-my-burguer-resource-server.name}/read",
    "${aws_cognito_resource_server.is-my-burguer-resource-server.name}/write"
  ]
  supported_identity_providers         = ["COGNITO"]
}

resource "aws_cognito_user_pool_client" "is-my-burguer-lambda-client" {
  name = "is-my-burguer-lambda-client"

  user_pool_id = aws_cognito_user_pool.is-my-burguer.id

  generate_secret                      = true
  allowed_oauth_flows_user_pool_client = true
  explicit_auth_flows                  = ["ADMIN_NO_SRP_AUTH"]
  callback_urls                        = ["http://localhost/swagger-ui/index.hmtl"]
  allowed_oauth_flows                  = ["code", "implicit"]
  allowed_oauth_scopes                 = ["phone", "email", "openid", "profile", "aws.cognito.signin.user.admin"]
  supported_identity_providers         = ["COGNITO"]
}

resource "aws_cognito_user_pool_client" "is-my-burguer-totem-client" {
  name = "is-my-burguer-totem-client"

  user_pool_id = aws_cognito_user_pool.is-my-burguer.id

  generate_secret                      = true
  allowed_oauth_flows_user_pool_client = true
  explicit_auth_flows                  = ["ADMIN_NO_SRP_AUTH"]
  callback_urls                        = ["http://localhost/swagger-ui/index.hmtl"]
  allowed_oauth_flows                  = ["client_credentials"]
  allowed_oauth_scopes = [
    "${aws_cognito_resource_server.is-my-burguer-resource-server.name}/read",
    "${aws_cognito_resource_server.is-my-burguer-resource-server.name}/write"
  ]
  supported_identity_providers         = ["COGNITO"]
}

