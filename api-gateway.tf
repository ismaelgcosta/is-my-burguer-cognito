resource "aws_apigatewayv2_api" "cognito-api-gateway" {
  name          = "cognito-api-gateway"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "cognito-api-gateway-stage" {
  api_id      = aws_apigatewayv2_api.cognito-api-gateway.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_apigatewayv2_deployment" "cognito-api-gateway" {
  depends_on = [ 
    aws_apigatewayv2_route.cognito-api-gateway-auth,
    aws_apigatewayv2_route.cognito-api-gateway-user-sign-up,
    aws_apigatewayv2_route.cognito-api-gateway-user-token
   ]

  api_id      = aws_apigatewayv2_api.cognito-api-gateway.id
  description = "Cognito API Gateway"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_apigatewayv2_authorizer" "cognito-api-gateway" {
  api_id           = aws_apigatewayv2_api.cognito-api-gateway.id
  authorizer_type  = "JWT"
  identity_sources = ["$request.header.Authorization"]
  name             = "cognito-authorizer"
  jwt_configuration {
    audience = [
      aws_cognito_user_pool_client.is-my-burguer-api-client.id,
      aws_cognito_user_pool_client.is-my-burguer-lambda-client.id
    ]
    issuer   = "https://cognito-idp.us-east-1.amazonaws.com/${aws_cognito_user_pool.is-my-burguer.id}"
  }
}

resource "aws_apigatewayv2_route" "cognito-api-gateway-auth" {
  api_id    = aws_apigatewayv2_api.cognito-api-gateway.id
  route_key = "ANY /auth/token"
  
  target = "integrations/${aws_apigatewayv2_integration.cognito-api-gateway-auth.id}"
}

resource "aws_apigatewayv2_route" "cognito-api-gateway-user-token" {
  api_id             = aws_apigatewayv2_api.cognito-api-gateway.id
  route_key          = "ANY /user/token"
  authorization_type = "JWT"
  authorizer_id      = aws_apigatewayv2_authorizer.cognito-api-gateway.id

  target = "integrations/${aws_apigatewayv2_integration.cognito-api-gateway-user-token.id}"
}

resource "aws_apigatewayv2_route" "cognito-api-gateway-user-info" {
  api_id             = aws_apigatewayv2_api.cognito-api-gateway.id
  route_key          = "ANY /user/info"
  authorization_type = "JWT"
  authorizer_id      = aws_apigatewayv2_authorizer.cognito-api-gateway.id

  target = "integrations/${aws_apigatewayv2_integration.cognito-api-gateway-user-info.id}"
}

resource "aws_apigatewayv2_route" "cognito-api-gateway-user-sign-up" {
  api_id             = aws_apigatewayv2_api.cognito-api-gateway.id
  route_key          = "ANY /user/sign-up"
  authorization_type = "JWT"
  authorizer_id      = aws_apigatewayv2_authorizer.cognito-api-gateway.id

  target = "integrations/${aws_apigatewayv2_integration.cognito-api-gateway-user-sign-up.id}"
}

resource "aws_apigatewayv2_route" "cognito-api-gateway-user-confirm-sign-up" {
  api_id             = aws_apigatewayv2_api.cognito-api-gateway.id
  route_key          = "ANY /user/sign-up/confirm"
  authorization_type = "JWT"
  authorizer_id      = aws_apigatewayv2_authorizer.cognito-api-gateway.id

  target = "integrations/${aws_apigatewayv2_integration.cognito-api-gateway-user-confirm-sign-up.id}"
}

resource "aws_apigatewayv2_integration" "cognito-api-gateway-auth" {
  api_id           = aws_apigatewayv2_api.cognito-api-gateway.id
  integration_type = "AWS_PROXY"

  integration_uri  = aws_lambda_function.cognito-client-credentials.invoke_arn
  payload_format_version = "2.0"
}


resource "aws_apigatewayv2_integration" "cognito-api-gateway-user-token" {
  api_id           = aws_apigatewayv2_api.cognito-api-gateway.id
  integration_type = "AWS_PROXY"
 
  integration_uri  = aws_lambda_function.cognito-sign-in.invoke_arn
  payload_format_version = "2.0"
}


resource "aws_apigatewayv2_integration" "cognito-api-gateway-user-info" {
  api_id           = aws_apigatewayv2_api.cognito-api-gateway.id
  integration_type = "AWS_PROXY"
 
  integration_uri  = aws_lambda_function.cognito-user-info.invoke_arn
  payload_format_version = "2.0"
}


resource "aws_apigatewayv2_integration" "cognito-api-gateway-user-sign-up" {
  api_id           = aws_apigatewayv2_api.cognito-api-gateway.id
  integration_type = "AWS_PROXY"

  integration_uri  = aws_lambda_function.cognito-sign-up.invoke_arn
  payload_format_version = "2.0"
} 

resource "aws_apigatewayv2_integration" "cognito-api-gateway-user-confirm-sign-up" {
  api_id           = aws_apigatewayv2_api.cognito-api-gateway.id
  integration_type = "AWS_PROXY"

  integration_uri  = aws_lambda_function.cognito-confirm-sign-up.invoke_arn
  payload_format_version = "2.0"
} 

 
resource "aws_lambda_permission" "lambda-permission-cognito-sign-in" {
  statement_id  = "cognitoSignInAPIInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.cognito-sign-in.arn}"
  principal     = "apigateway.amazonaws.com"

  # The /* part allows invocation from any stage, method and resource path
  # within API Gateway.
  source_arn = "${aws_apigatewayv2_api.cognito-api-gateway.execution_arn}/*/*/user/token"
} 

resource "aws_lambda_permission" "lambda-permission-cognito-sign-up" {
  statement_id  = "cognitoSignUpAPIInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.cognito-sign-up.arn}"
  principal     = "apigateway.amazonaws.com"

  # The /* part allows invocation from any stage, method and resource path
  # within API Gateway.
  source_arn = "${aws_apigatewayv2_api.cognito-api-gateway.execution_arn}/*/*/user/sign-up"
}

resource "aws_lambda_permission" "lambda-permission-cognito-confirm-sign-up" {
  statement_id  = "cognitoConfirmSignUpAPIInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.cognito-confirm-sign-up.arn}"
  principal     = "apigateway.amazonaws.com"

  # The /* part allows invocation from any stage, method and resource path
  # within API Gateway.
  source_arn = "${aws_apigatewayv2_api.cognito-api-gateway.execution_arn}/*/*/user/sign-up/confirm"
}


resource "aws_lambda_permission" "lambda-permission-cognito-user-info" {
  statement_id  = "cognitoUserInfoAPIInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.cognito-user-info.arn}"
  principal     = "apigateway.amazonaws.com"

  # The /* part allows invocation from any stage, method and resource path
  # within API Gateway.
  source_arn = "${aws_apigatewayv2_api.cognito-api-gateway.execution_arn}/*/*/user/info"
} 


resource "aws_lambda_permission" "lambda-permission-cognito-client-credentials" {
  statement_id  = "cognitoClientCredentialsAPIInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.cognito-client-credentials.arn}"
  principal     = "apigateway.amazonaws.com"

  # The /* part allows invocation from any stage, method and resource path
  # within API Gateway.
  source_arn = "${aws_apigatewayv2_api.cognito-api-gateway.execution_arn}/*/*/auth/token"
}