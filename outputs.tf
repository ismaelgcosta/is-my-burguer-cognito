output "cognito_domain" {
  description = "The endpoint for the Cognito domain"
  value       = aws_cognito_user_pool_domain.cognito-domain.domain
}

output "cognito_id" {
  description = "The Cognito id"
  value       = aws_cognito_user_pool.is-my-burguer.id
}

output "is-my-burguer-api-client-id" {
  description = "The Cognito id"
  value       = aws_cognito_user_pool_client.is-my-burguer-api-client.id
}

output "api_gateway_domain" {
  description = "The endpoint for the API Gateway domain"
  value       = aws_apigatewayv2_api.cognito-api-gateway.id
}


