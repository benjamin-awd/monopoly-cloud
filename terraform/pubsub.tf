resource "google_pubsub_topic" "default" {
  name    = "monopoly-topic"
  project = var.google_cloud_project

  message_retention_duration = "86600s"
}

module "pubsub_topic-iam-bindings" {
  source        = "terraform-google-modules/iam/google//modules/pubsub_topics_iam"
  project       = var.google_cloud_project
  pubsub_topics = [google_pubsub_topic.default.id]
  mode          = "authoritative"

  bindings = {
    "roles/pubsub.publisher" = [
      "serviceAccount:gmail-api-push@system.gserviceaccount.com",
    ]
  }
}
