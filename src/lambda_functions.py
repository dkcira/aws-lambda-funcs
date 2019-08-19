import boto3
import json


def lambda_client():
    aws_lambda = boto3.client('lambda', region='us-east-2')
    """ :type : pyboto3.lambda """
    return aws_lambda


def iam_client():
    iam = boto3.client('iam') # no region, iam is a global service
    """ :type : pyboto3.iam """
    return iam


def create_access_policy_for_lambda():
    s3_access_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "s3:*",
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Effect": "Allow",
                "Resource": "*"
            }
        ]
    }

    return iam_client().create_policy(
        PolicyName = 'LambdaS3AccessPolicy',
        PolicyDocument = json.dumps(s3_access_policy_document),
        Description = 'Allows lambda function to access S3 resources.'
    )


def create_execution_role_for_lambda():
    lambda_execution_assumption_role = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                }
                "Action": "sts:AssumeRole"
            }
        ]
    }

if __name__ == '__main__':
    print(create_access_policy_for_lambda())