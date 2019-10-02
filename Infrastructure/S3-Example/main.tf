
#########################################################
# SETUP
#########################################################
provider "aws" {

  region                  = "eu-central-1"
  shared_credentials_file = "/Users/olivergoetz/.aws/credentials"
  profile                 = "sandbox"

}

#########################################################
# S3 
#########################################################

resource "aws_s3_bucket" "mybucket" {
  bucket = "oliver-goetz-capstone-bucket" # must be UNIQUE
  acl    = "public-read"

  force_destroy = true

  website {
    index_document = "index.html"
    error_document = "404.html"

  }

  tags = {
    Name   = "OliverGoetz"
    Team   = "AXA"
    Entity = "AXAGO"
  }
}
