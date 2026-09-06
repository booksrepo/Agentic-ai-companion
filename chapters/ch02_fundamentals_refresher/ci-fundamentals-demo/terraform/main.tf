terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

resource "local_file" "greeting" {
  filename = "${path.module}/greeting.txt"
  content  = "Hello from Terraform, provisioned declaratively.\n"
}
