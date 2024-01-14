locals {
  container_uri_prefix       = "${var.region}-docker.pkg.dev/${var.google_cloud_project}"
  cloud_run_scheduler_prefix = "https://${var.region}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${var.google_cloud_project}"
}
