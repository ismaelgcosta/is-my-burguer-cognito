data "aws_iam_policy_document" "lambda_policy" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = [
      "sts:AssumeRole",
      "cognito-idp:DescribeUserPool",
      "cognito-idp:CreateUserPoolClient",
      "cognito-idp:DeleteUserPoolClient",
      "cognito-idp:DescribeUserPoolClient",
      "cognito-idp:AdminInitiateAuth",
      "cognito-idp:AdminUserGlobalSignOut",
      "cognito-idp:ListUserPoolClients",
      "cognito-identity:DescribeIdentityPool",
      "cognito-identity:UpdateIdentityPool",
      "cognito-identity:SetIdentityPoolRoles",
      "cognito-identity:GetIdentityPoolRoles"
    ]
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.lambda_policy.json
}

data "archive_file" "lambda-client-credentials" {
  type        = "zip"
  source_file = "lambda-client-credentials/lambda_function.py"
  output_path = "lambda-client-credentials.zip"
}

data "archive_file" "lambda-sign-up" {
  type        = "zip"
  source_file = "lambda-sign-up/lambda_function.py"
  output_path = "lambda-sign-up.zip"
}

data "archive_file" "lambda-confirm-sign-up" {
  type        = "zip"
  source_file = "lambda-confirm-sign-up/lambda_function.py"
  output_path = "lambda-confirm-sign-up.zip"
}

data "archive_file" "lambda-signin" {
  type        = "zip"
  source_file = "lambda-signin/lambda_function.py"
  output_path = "lambda-signin.zip"
}

resource "aws_lambda_function" "cognito-client-credentials" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "lambda-client-credentials.zip"
  function_name = "cognito-client-credentials"
  handler       = "lambda_function.lambda_handler"
  role          = aws_iam_role.iam_for_lambda.arn

  source_code_hash = data.archive_file.lambda-client-credentials.output_base64sha256

  runtime = "python3.12"

  environment {
    variables = {
      CLIENT_DOMAIN = "${aws_cognito_user_pool_domain.cognito-domain.domain}",
      CLIENT_RESOURCE_SERVER = "${aws_cognito_resource_server.is-my-burguer-resource-server.identifier}"
    }
  }
}

resource "aws_lambda_function" "cognito-sign-up" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "lambda-sign-up.zip"
  function_name = "cognito-sign-up"
  handler       = "lambda_function.lambda_handler"
  role          = aws_iam_role.iam_for_lambda.arn

  source_code_hash = data.archive_file.lambda-sign-up.output_base64sha256

  runtime = "python3.12"

  environment {
    variables = {
      CLIENT_ID     = "${aws_cognito_user_pool_client.is-my-burguer-lambda-client.id}"
      CLIENT_SECRET = "${aws_cognito_user_pool_client.is-my-burguer-lambda-client.client_secret}"
      USER_POOL_ID  = "${aws_cognito_user_pool.is-my-burguer.id}"
    }
  }
}

resource "aws_lambda_function" "cognito-confirm-sign-up" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "lambda-confirm-sign-up.zip"
  function_name = "cognito-confirm-sign-up"
  handler       = "lambda_function.lambda_handler"
  role          = aws_iam_role.iam_for_lambda.arn

  source_code_hash = data.archive_file.lambda-confirm-sign-up.output_base64sha256

  runtime = "python3.12"

  environment {
    variables = {
      CLIENT_ID     = "${aws_cognito_user_pool_client.is-my-burguer-lambda-client.id}"
      CLIENT_SECRET = "${aws_cognito_user_pool_client.is-my-burguer-lambda-client.client_secret}"
      USER_POOL_ID  = "${aws_cognito_user_pool.is-my-burguer.id}"
    }
  }
}

resource "aws_lambda_function" "cognito-sign-in" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "lambda-signin.zip"
  function_name = "cognito-sign-in"
  handler       = "lambda_function.lambda_handler"
  role          = aws_iam_role.iam_for_lambda.arn

  source_code_hash = data.archive_file.lambda-signin.output_base64sha256

  runtime = "python3.12"

  environment {
    variables = {
      CLIENT_ID = "${aws_cognito_user_pool_client.is-my-burguer-lambda-client.id}"
      CLIENT_SECRET = "${aws_cognito_user_pool_client.is-my-burguer-lambda-client.client_secret}"
      USER_POOL_ID = "${aws_cognito_user_pool.is-my-burguer.id}"
    }
  }
}
