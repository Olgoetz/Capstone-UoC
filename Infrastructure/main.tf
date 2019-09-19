provider "aws" {

  region                  = var.region
  shared_credentials_file = "/Users/olivergoetz/.aws/credentials"
  profile                 = "cloud_garage"
}


resource "aws_s3_bucket" "bs" {
  bucket = "oliver-goetz-docker-eb"
  acl    = "private"

  tags = var.tags
}


resource "aws_elastic_beanstalk_application" "bsapp" {
  name        = "docker-app"
  description = "Dockerized React App"

  tags = var.tags
}



resource "aws_elastic_beanstalk_environment" "bsappenvtest" {
  name                = "docker-app"
  application         = aws_elastic_beanstalk_application.bsapp.name
  solution_stack_name = "64bit Amazon Linux 2018.03 v2.12.17 running Docker 18.06.1-ce"

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "IamInstanceProfile"
    value     = "aws-elasticbeanstalk-ec2-role"
  }

  tags = var.tags
}


output "eb_all_settings" {
  value = aws_elastic_beanstalk_environment.bsappenvtest.all_settings
}
output "eb_cname" {
  value = aws_elastic_beanstalk_environment.bsappenvtest.cname
}
