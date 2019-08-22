import boto3
import json
from os import path

from src.utils import Utils

LAMBDA_ROLE = 'Lambda_Execution_Role'
LAMBDA_ACCESS_POLICY_ARN = 'arn:aws:iam::094380402750:policy/LambdaS3AccessPolicy'
LAMBDA_ROLE_ARN = 'arn:aws:iam::094380402750:role/Lambda_Execution_Role'
LAMBDA_TIMEOUT = 10 # seconds
LAMBDA_MEMORY = 128 # MBs
LAMBDA_HANDLER = 'lambda_function.handler'
PYTHON_36_RUNTIME = 'python3.6'
PYTHON_LAMBDA_NAME = 'PythonLambdaFunction'

NODEJS_810_RUNTIME = 'nodejs8.10'
NODEJS_LAMBDA_NAME ='NodeJSLambdaFunction'

JAVA_8_RUNTIME = 'java8'
JAVA_LAMBDA_NAME = 'JavaLambdaFunction'


def lambda_client():
    aws_lambda = boto3.client('lambda', region_name='us-east-2')
    """ :type : pyboto3.lambda """
    return aws_lambda


def iam_client():
    iam = boto3.client('iam')  # no region, iam is a global service
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
        PolicyName='LambdaS3AccessPolicy',
        PolicyDocument=json.dumps(s3_access_policy_document),
        Description='Allows lambda function to access S3 resources.'
    )


def create_execution_role_for_lambda():
    lambda_execution_assumption_role = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

    return iam_client().create_role(
        RoleName=LAMBDA_ROLE,
        AssumeRolePolicyDocument=json.dumps(lambda_execution_assumption_role),
        Description="Gives necessary permissions for lambda to be executed."
    )


def attach_access_policy_to_execution_role():
    return iam_client().attach_role_policy(
        RoleName=LAMBDA_ROLE,
        PolicyArn=LAMBDA_ACCESS_POLICY_ARN
    )


def deploy_lambda_function(function_name, runtime, handler, role_arn, source_folder):
    # read everything from source_folder under the present path
    folder_path = path.join(path.dirname(path.abspath(__file__)), source_folder)

    if runtime is not JAVA_8_RUNTIME:
        zip_file = Utils.make_zip_file_bytes(path=folder_path)
    else:
        zip_file = Utils.read_jar_file(folder_path)

    return lambda_client().create_function(
        FunctionName=function_name,
        Runtime=runtime,
        Role=role_arn,
        Handler=handler,
        Code={
            'ZipFile': zip_file
        },
        Timeout=LAMBDA_TIMEOUT,
        MemorySize=LAMBDA_MEMORY,
        Publish=False
    )


if __name__ == '__main__':
    # print(create_access_policy_for_lambda())
    # print(create_execution_role_for_lambda())
    # print(attach_access_policy_to_execution_role())
    #
    #  # deploy python lambda
    # print(
    #   deploy_lambda_function(
    #       PYTHON_LAMBDA_NAME,
    #       PYTHON_36_RUNTIME,
    #       LAMBDA_HANDLER,
    #       LAMBDA_ROLE_ARN,
    #       'python_lambda' # source folder
    #     )
    # )
    #
    # # deploy javascript lambda
    # print(
    #     deploy_lambda_function(
    #         NODEJS_LAMBDA_NAME,
    #         NODEJS_810_RUNTIME,
    #         LAMBDA_HANDLER,
    #         LAMBDA_ROLE_ARN,
    #         'nodejs_lambda' # source folder
    #     )
    # )
    # deploy java lambda
    print(
        deploy_lambda_function(
            JAVA_LAMBDA_NAME,
            JAVA_8_RUNTIME,
            'com.amazonaws.lambda.demo.LambdaFunctionHandler::handleRequest',
            LAMBDA_ROLE_ARN,
            'java_lambda/demo-1.0.0.jar' # source folder (file for java)
        )
    )
