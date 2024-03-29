terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.75.1"
    }
  }
}

provider "google" {
  project = var.google_cloud_project
  region  = var.region
}
