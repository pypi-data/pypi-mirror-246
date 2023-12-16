"""
*******************************************************************************
File: deUtils.py

Purpose: Creates some nice helper functions

Dependencies/Helpful Notes : 

*******************************************************************************
"""

from eimutils.aws_secrets import get_secrets
from eimutils.decrypt import getDERKey
from eimutils.delogging import log_to_console
from eimutils.snowflake_connection import connect_database
#import snowflake.connector as snc
import json

"""
*******************************************************************************
Function: get_db_connection_from_secret

Purpose: Generate a database connection from AWS secret.

Parameters:
     secret_name - AWS secret name from the account the process is running in
                   that contains the db connection information.  

Calls:
    get_secret
    connect_database
    
Called by:

Returns: database connection

*******************************************************************************
"""

def get_snowflake_connection_from_secret(secret_arn, env, aws_region):

    try:
        # get the secret
        # ToDo: Add Role to the secret. Then we can remove env.
        secrets = get_secrets(secret_arn, aws_region)
        dictSecrets = json.loads(secrets)

        # Identifying the user
        if "DW30SFSVCUSER" in dictSecrets:
            my_user = dictSecrets["DW30SFSVCUSER"]
        elif "SFSVCUSER" in dictSecrets: 
            my_user = dictSecrets["SFSVCUSER"]
        else:
            print('Valid user not returned from secret.')

        # Identifying the key
        #Decrypt the pkbDER key
        if "DW30SFSVCPKEY" in dictSecrets and "DW30SFSVCPPRS" in dictSecrets:
            my_pkbDER = getDERKey(dictSecrets["DW30SFSVCPKEY"], dictSecrets["DW30SFSVCPPRS"])
            #pkbPEM = getPEMKey(dictSecrets["DW30SFSVCPKEY"], dictSecrets["DW30SFSVCPPRS"])
        elif "SFSVCPKEY" in dictSecrets and "SFSVCPPRS" in dictSecrets:
            my_pkbDER = getDERKey(dictSecrets["SFSVCPKEY"], dictSecrets["SFSVCPPRS"])
        else:
            print('Valid private key not returned from secret.')

        # Identifying the role.
        if "SFROLE" in dictSecrets:
            my_role = dictSecrets["SFROLE"]
        else:
            my_role = f'EIM_{env}_DW3_ADMIN'

        # Identify the Account
        if "SFACCOUNT" in dictSecrets:
            my_account = dictSecrets["SFACCOUNT"]
        else:
            print('Valid account not returned from secret')

        # ToDo: Create the connection to snowflake using connect_database in snowflake_connection.py
                
        db_connection = connect_database(my_user, my_account, my_pkbDER, my_role)

    except Exception as e:
        log_to_console(__name__, 'Err', str(e))
        db_connection = {"Status":"Failed"}

    return db_connection

"""
*******************************************************************************
Change History:

Author		Date		Description
----------	----------	-------------------------------------------------------
Frank		2023-09-19  Initial Iteration

*******************************************************************************
"""