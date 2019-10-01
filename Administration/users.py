import boto3
import json
import argparse
import random
import string
import logging
import pandas as pd

#####################################################
# ---> GET A SESSION TO CALL THE AWS API
#####################################################


session = boto3.Session(profile_name="sandbox")
client = session.client('iam')


#####################################################
# ---> CONFIGURATION OF LOGGING
#####################################################


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )


#####################################################
# ---> CONFIGURATION OF THE ARGUMENT PARSER
#####################################################


parser = argparse.ArgumentParser(description="Manage IAM users")

group = parser.add_mutually_exclusive_group()

group.add_argument("-cp", '--createIamPolicy', action="store_true",
                   help="Calls the creatIamPolicy function")
group.add_argument("-cus", '--createUsers', action="store", type=str,
                   help="Calls the createUser function. You MUST provide an IAM policy ARN")
group.add_argument("-dus", '--deleteUsers', nargs='+',
                   help="Calls the deleteUser function. You MUST provide the username and IAM policy ARN attached to the user")


#####################################################
# ---> HELPERS
#####################################################


# Generate a random string
def randomString(stringLength):

    letters = string.ascii_letters
    prefix = 'A'
    suffix = '$9'
    middle = ''.join(random.choice(letters) for i in range(stringLength))

    # Build a random password satisfying the requirements of AWS
    password = prefix+middle+suffix
    return password


#####################################################
# ---> CONFIGURATION OF THE IAM POLICY
#####################################################


def createIamPolicy():

        # Define the policy
    my_managed_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "elasticbeanstalk:*",
                    "s3:*",
                    "ec2:*",
                    "iam:ListUsers",
                    "iam:GetUser",
                    "iam:ChangePassword",
                    "iam:DeleteAccessKey",
                    "iam:CreateAccessKey",
                    "iam:ListAccessKeys",
                    "cloudwatch:*"
                ],
                "Resource": "*",

                "Condition": {
                    "StringEquals": {"account:TargetRegion": "eu-central-1"}
                }
            }
        ]
    }

    # Create the policy
    logging.info('Creating IAM Policy')
    iam_policy_response = client.create_policy(
        PolicyName="University_of_Cologne",
        PolicyDocument=json.dumps(my_managed_policy),
        Description="Policy for students of th UoC to play around with S3, EC2 and Beanstalk"
    )

    return iam_policy_response


#####################################################
# ---> USER MANAGEMENT
#####################################################


def createUsers(iam_policy_arn):

    logging.info('Creating users')

    students = []
    # df = pd.read_excel(
    #     '/Users/olivergoetz/Development/Capstone-Uni/Administration/Capstone_WS1920_Teilnehmer.xlsx')

    df = pd.read_excel("cpt.xlsx")
    for index, row in df.iterrows():
        userName = row["Benutzername"]
        password = randomString(15)
        row["Passwort"] = password
        students.append(row)

        client.create_user(
            UserName=userName
        )

        client.create_login_profile(
            UserName=userName,
            Password=password,
            PasswordResetRequired=True
        )

        logging.info('Users created')

        waiter = client.get_waiter('user_exists')

        waiter.wait(UserName=userName)

        logging.info('Attaching IAM policy')

        client.attach_user_policy(
            UserName=userName,
            PolicyArn=iam_policy_arn
        )

        logging.info('IAM policy attached')

    new_df = pd.DataFrame(students)
    new_df.to_excel('cptp.xlsx')


def deleteUsers(data):

    # userName = data[0]
    Arn = data[0]

    df = pd.read_excel("Capstone_WS1920_Teilnehmer.xlsx")
    for index, row in df.iterrows():
        userName = row["Benutzername"]

        logging.info(f"Deleting user {userName}")

        client.detach_user_policy(
            UserName=userName,
            PolicyArn=Arn
        )

        client.delete_login_profile(
            UserName=userName
        )

        client.delete_user(
            UserName=userName
        )

        logging.info(f'{userName} deleted')


#####################################################
# ---> MAIN
#####################################################


if __name__ == '__main__':

    args = parser.parse_args()

    iam_policy_arn = ''

    # Call functions according to the passed arguments
    if args.createIamPolicy:
        iam_policy_arn = createIamPolicy()
        logging.info(f"The policy ARN is: {iam_policy_arn['Policy']['Arn']}")

    if args.createUsers:

        createUsers(args.createUsers)

    if args.deleteUsers:
        deleteUsers(args.deleteUsers)
