resource "google_secret_manager_secret_iam_binding" "dbs" {
  secret_id = data.google_secret_manager_secret_version.dbs.secret
  project   = data.google_secret_manager_secret_version.dbs.project
  role      = "roles/secretmanager.secretAccessor"

  members = [
    "serviceAccount:${google_service_account.default.email}"
  ]
}

resource "google_storage_bucket_iam_member" "statements" {
  bucket = google_storage_bucket.statements.name
  role   = "roles/storage.admin"
  member = "serviceAccount:${google_service_account.default.email}"
}

resource "google_cloud_run_v2_job" "dbs" {
  name     = "dbs"
  location = var.region

  template {
    template {
      service_account = google_service_account.default.email
      max_retries     = 1

      containers {
        resources {
          limits = {
            cpu    = "1"
            memory = "1024Mi"
          }
        }

        image = "${local.container_uri_prefix}/dbs/dbs:main"

        args = ["--email", "--upload", "--page-size=1"]

        env {
          name  = "OTP_EMAIL_SUBJECT"
          value = "DBS OTP"
        }
        env {
          name  = "PROJECT_ID"
          value = var.google_cloud_project
        }
        env {
          name  = "SECRET_ID"
          value = var.dbs_gmail_credential_secret
        }
        env {
          name  = "DBS_USER_ID"
          value = var.dbs_user_id
        }
        env {
          name  = "DBS_PIN"
          value = var.dbs_pin
        }
        env {
          name  = "BUCKET_NAME"
          value = google_storage_bucket.statements.name
        }
        env {
          name  = "FROM_EMAIL"
          value = var.dbs_from_email
        }
        env {
          name  = "TO_EMAIL"
          value = var.dbs_to_email
        }
      }
    }
  }
}

resource "google_cloud_scheduler_job" "dbs" {
  name        = "monthly-dbs-bank-statement-extraction"
  description = "Extracts bank statements from dbs"
  schedule    = "0 0 15 * *"  # 00:00 UTC (8AM SGT) on 15th day of each month
  time_zone   = "UTC"

  http_target {
    http_method = "POST"
    uri         = "${local.cloud_run_scheduler_prefix}/jobs/${google_cloud_run_v2_job.dbs.name}:run"
    oauth_token {
      service_account_email = google_service_account.default.email
    }
  }
}
