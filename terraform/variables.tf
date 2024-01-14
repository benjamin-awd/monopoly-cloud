variable "ocbc_passwords" {
  description = "Passwords for encrypted OCBC PDFs"
  type        = list(string)
  sensitive   = true
}

variable "hsbc_passwords" {
  description = "Passwords for encrypted HSBC PDFs"
  type        = list(string)
  sensitive   = true
}

variable "gmail_address" {
  description = "Gmail address to which bank statements/transactions are sent"
  type        = string
  sensitive   = true
}

variable "trusted_emails" {
  description = "Trusted user emails"
  type        = list(string)
  sensitive   = true
}

variable "google_cloud_project" {
  description = "Google project ID"
  type        = string
}

variable "region" {
  description = "Google region"
  type        = string
}

variable "gmail_credential_secret" {
  description = "Name of secret containing client secret and token for Gmail account"
  type        = string
}

variable "dbs_user_id" {
  description = "DBS user id"
  type = string
  sensitive = true
}

variable "dbs_pin" {
  description = "DBS PIN"
  type = string
  sensitive = true
}

variable "dbs_gmail_credential_secret" {
  description = "Name of secret containing client secret and token for DBS Gmail account"
  type        = string
}

variable "dbs_from_email" {
  type      = string
  sensitive = true
}

variable "dbs_to_email" {
  type      = string
  sensitive = true
}
