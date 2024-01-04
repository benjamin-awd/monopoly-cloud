locals {
  container_uri_prefix       = "${var.region}-docker.pkg.dev/${var.project_id}"
  cloud_run_scheduler_prefix = "https://${var.region}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${var.project_id}"
}
