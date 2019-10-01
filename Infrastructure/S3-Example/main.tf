
#########################################################
# SETUP
#########################################################
provider "aws" {

  region = "eu-central-1"

}

#########################################################
# S3 
#########################################################

resource "aws_s3_bucket" "mybucket" {
  bucket = "oliver-goetz-capstone-bucket" # must be UNIQUE
  acl    = "private"                      # restrict public access

  tags = {
    Name   = "OliverGoetz"
    Team   = "AXA"
    Entity = "AXAGO"
  }
}
