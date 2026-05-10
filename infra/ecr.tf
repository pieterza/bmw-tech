resource "aws_ecr_repository" "bmw-helm" {
  name                 = "bmw-helm"
  image_tag_mutability = "MUTABLE"

  tags = {
    Application = "bmw-helm"
    ManagedBy   = "terraform"
  }
}

resource "aws_ecr_repository" "bmw-app" {
  name                 = "bmw-app"
  image_tag_mutability = "MUTABLE"

  tags = {
    Application = "bmw-app"
    ManagedBy   = "terraform"
  }
}
