# precisa começar com TF_VAR_
variable "TF_VAR_postgres_user" {
  description = "The master username for the database."
  type        = string
  sensitive   = true
}

# precisa começar com TF_VAR_
variable "TF_VAR_postgres_password" {
  description = "The master password for the database."
  type        = string
  sensitive   = true
}