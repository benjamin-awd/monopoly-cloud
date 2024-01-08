data "google_secret_manager_secret_version" "default" {
  secret  = "monopoly-gmail-token"
  project = var.project_id
}

data "google_secret_manager_secret_version" "dbs" {
  secret  = "dbs-otp-email-token"
  project = var.project_id
}

data "google_secret_manager_secret_version" "monopoly_passwords" {
  secret  = "monopoly-passwords"
  project = var.project_id
}

data "google_project" "project" {
}
