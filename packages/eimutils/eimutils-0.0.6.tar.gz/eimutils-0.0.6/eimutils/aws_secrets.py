"""
*******************************************************************************
File: aws_secrets.py

Purpose: Gets secret values from AWS Secrets.

Dependencies/Helpful Notes :

*******************************************************************************
"""
# Use this code snippet in your app.
# If you need more information about configurations or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developers/getting-started/python/

import boto3
from botocore.exceptions import ClientError
import base64

"""
*******************************************************************************
Function: get_secret

Purpose: Gets AWS secret data.

Parameters:
     secret_name - AWS secret name from the account the process is running in
                   that contains the db connection information.  

Calls:

Called by:

Returns: dictionary of secret values

*******************************************************************************
"""

def get_secrets(srcArn,aws_region):
    print(
        "============================================\nParameters and Secrets\n============================================\n")

    secret_name = srcArn  

    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=aws_region)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        print("Got an Error :: get_secrets")
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            print("Secrets Manager can't decrypt the protected secret text using the provided KMS key.")
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            print("An error occurred on the server side.")
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("You provided an invalid value for a parameter")
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("You provided a parameter value that is not valid for the current state of the resource.")
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("We can't find the resource that you asked for.")
            raise e
    except Exception as err:
        print (err)

    if 'SecretString' in get_secret_value_response:
        print("Retrieving Secret String")
        secret = get_secret_value_response['SecretString']
        return secret
    elif 'SecretBinary' in get_secret_value_response:
        print("Retrieving Secret Binary")
        decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        return decoded_binary_secret
    else:
        print('Unexpected secret format.')

"""
*******************************************************************************
Change History:

Author		Date		Description
----------	----------	-------------------------------------------------------
ffortunato  11/1/2023   + new flavor of get secrets: getSecrets(srcPS, srcArn):
ffortunato  12/15/2023  + additional exception handling.
*******************************************************************************
"""