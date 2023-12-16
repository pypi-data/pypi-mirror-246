"""
*******************************************************************************
File: data_hub_connection.py

Purpose: Core functions invoked by the Data Hub class that interact with the db.

Dependencies/Helpful Notes :

*******************************************************************************
"""
from eimutils.delogging import log_to_console
import snowflake.connector as sfc


def connect_database(sf_user, sf_account, pkbDER, sf_role):
    """
    Creates a pymssql connection for use by the class
    :return: pymssql connection
    """
    try:

        db_connection =  sfc.connect(
        user=sf_user,
        account=sf_account,
        private_key=pkbDER,
        role=sf_role,
        )

    except sfc.Error as err:
        e_msg = "snowflake_connection.connect_database :: Connection error. " + err
        log_to_console(__name__,'Error',e_msg)
        return {'Status': 'Failure'}

    return db_connection

"""
*******************************************************************************
Change History:

Author		Date		Description
----------	----------	-------------------------------------------------------
ffortunato  11/03/2023  Initial Iteration

*******************************************************************************
"""