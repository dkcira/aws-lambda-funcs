import boto3


def lambda_client():
    aws_lambda = boto3.client('lambda', region='us-east-2')
    """ :type: pyboto3.lambda """
    return aws_lambda


def iam_