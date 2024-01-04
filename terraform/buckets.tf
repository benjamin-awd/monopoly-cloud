resource "random_id" "bucket_prefix" {
  byte_length = 8
}

resource "google_storage_bucket" "transactions" {
  name          = "monopoly-${random_id.bucket_prefix.hex}"
  location      = "US"
  storage_class = "STANDARD"

  encryption {
    default_kms_key_name = google_kms_crypto_key.terraform_state_bucket.id
  }

  depends_on = [google_project_iam_member.kms]
}

resource "google_storage_bucket" "statements" {
  name          = "statements-${random_id.bucket_prefix.hex}"
  location      = "US"
  storage_class = "STANDARD"

  encryption {
    default_kms_key_name = google_kms_crypto_key.terraform_state_bucket.id
  }

  depends_on = [google_project_iam_member.kms]
}

resource "google_storage_bucket" "terraform" {
  name          = "tfstate-${random_id.bucket_prefix.hex}"
  force_destroy = false
  location      = "US"
  storage_class = "STANDARD"

  encryption {
    default_kms_key_name = google_kms_crypto_key.terraform_state_bucket.id
  }

  depends_on = [google_project_iam_member.kms]
}
