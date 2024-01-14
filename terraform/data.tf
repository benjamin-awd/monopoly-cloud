data "google_secret_manager_secret_version" "default" {
  secret  = "monopoly-gmail-token"
  project = var.google_cloud_project
}

data "google_secret_manager_secret_version" "dbs" {
  secret  = "dbs-otp-email-token"
  project = var.google_cloud_project
}

data "google_secret_manager_secret_version" "monopoly_passwords" {
  secret  = "monopoly-passwords"
  project = var.google_cloud_project
}

data "google_project" "project" {
}
