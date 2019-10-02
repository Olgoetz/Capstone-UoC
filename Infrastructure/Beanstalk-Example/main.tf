provider "aws" {

  region                  = var.region
  shared_credentials_file = "/Users/olivergoetz/.aws/credentials"
  profile                 = "sandbox"
}




resource "aws_elastic_beanstalk_application" "bsapp" {
  name        = "oliver-goetz-app"
  description = "Dockerized App"

  tags = {
    Name   = "OliverGoetz"
    Team   = "AXA"
    Entity = "AXAGO"
  }
}



resource "aws_elastic_beanstalk_environment" "bsappenvtest" {
  name                = "oliver-goetz-app-env"
  application         = aws_elastic_beanstalk_application.bsapp.name
  solution_stack_name = "64bit Amazon Linux 2018.03 v2.12.17 running Docker 18.06.1-ce"

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "IamInstanceProfile"
    value     = "aws-elasticbeanstalk-ec2-role"
  }

  tags = {
    Name   = "OliverGoetz"
    Team   = "AXA"
    Entity = "AXAGO"
  }
}


output "eb_all_settings" {
  value = aws_elastic_beanstalk_environment.bsappenvtest.all_settings
}
output "eb_cname" {
  value = aws_elastic_beanstalk_environment.bsappenvtest.cname
}
