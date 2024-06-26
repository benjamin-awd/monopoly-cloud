resource "google_service_account" "default" {
  account_id   = "monopoly"
  display_name = "Monopoly"
}

resource "google_artifact_registry_repository" "default" {
  location      = var.region
  repository_id = "monopoly"
  format        = "DOCKER"
}

resource "google_artifact_registry_repository" "dbs" {
  location      = var.region
  repository_id = "dbs"
  format        = "DOCKER"
}

resource "google_secret_manager_secret_iam_binding" "default" {
  secret_id = data.google_secret_manager_secret_version.default.secret
  project   = data.google_secret_manager_secret_version.default.project
  role      = "roles/secretmanager.secretAccessor"

  members = [
    "serviceAccount:${google_service_account.default.email}"
  ]
}

resource "google_secret_manager_secret_iam_binding" "pdf_passwords" {
  secret_id = data.google_secret_manager_secret_version.monopoly_passwords.secret
  project   = data.google_secret_manager_secret_version.monopoly_passwords.project
  role      = "roles/secretmanager.secretAccessor"

  members = [
    "serviceAccount:${google_service_account.default.email}"
  ]
}

resource "google_storage_bucket_iam_member" "storage" {
  bucket = google_storage_bucket.transactions.name
  role   = "roles/storage.admin"
  member = "serviceAccount:${google_service_account.default.email}"
}

resource "google_cloud_run_v2_job" "default" {
  name     = "monopoly-tf"
  location = var.region

  template {
    template {
      service_account = google_service_account.default.email
      max_retries     = 1

      containers {
        image = "${local.container_uri_prefix}/monopoly/monopoly:main"

        env {
          name  = "PUBSUB_TOPIC"
          value = google_pubsub_topic.default.id
        }
        env {
          name  = "GMAIL_ADDRESS"
          value = var.gmail_address
        }
        env {
          name  = "GOOGLE_CLOUD_PROJECT"
          value = var.google_cloud_project
        }
        env {
          name  = "GCS_BUCKET"
          value = google_storage_bucket.transactions.name
        }
        env {
          name  = "SECRET_ID"
          value = var.gmail_credential_secret
        }
        env {
          name  = "TRUSTED_USER_EMAILS"
          value = jsonencode(var.trusted_emails)
        }
        env {
          name  = "PASSWORDS"
          value_source {
            secret_key_ref {
              secret = data.google_secret_manager_secret_version.monopoly_passwords.secret
              version = "latest"
            }
          }
        }
      }
    }
  }
}

resource "google_cloud_scheduler_job" "default" {
  name        = "daily-bank-statement-extraction"
  description = "Extracts bank statements"
  schedule    = "0 * * * *"
  time_zone   = "UTC"

  http_target {
    http_method = "POST"
    uri         = "${local.cloud_run_scheduler_prefix}/jobs/${google_cloud_run_v2_job.default.name}:run"
    oauth_token {
      service_account_email = google_service_account.default.email
    }
  }
}

resource "google_project_iam_binding" "cloud_run_invoker" {
  project = var.google_cloud_project
  role    = "roles/run.invoker"

  members = [
    "serviceAccount:${google_service_account.default.email}"
  ]
}
