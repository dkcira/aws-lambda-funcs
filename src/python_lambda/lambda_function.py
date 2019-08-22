# first create a handler method
def handler(event, context):
    # event => event executor of the lambda function
    #          triggered from S3, CloudWatch, etc
    # context => environment in which the lambda is executed
    return {
        'statusCode': 200,
        'message': 'Hello from Python Lambda Function'
    }
