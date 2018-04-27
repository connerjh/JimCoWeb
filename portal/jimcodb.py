import logging
import pymysql
import rds_config
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ------------------------------------------------------------------------------


def get_connection():

    rds_host = rds_config.db_endpoint
    name = rds_config.db_username
    password = rds_config.db_password
    db_name = rds_config.db_name
    port = rds_config.db_port

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    try:

        return pymysql.connect(rds_host, port=port, user=name, passwd=password, db=db_name, connect_timeout=5)

    except Exception as e:

        logger.error("ERROR: Unexpected error: Could not connect to MySql instance. {}".format(e))

    logger.info("SUCCESS: Connection to RDS mysql instance succeeded")


# -----------------------------------------------------------------------------


def get_account(account_number):

    try:

        connection = get_connection()

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM jimcodb.IndividualAccountView where AccountNumber = %s;", (account_number,))
            account = cursor.fetchone()
            logger.info('returned account: {}'.format(json.dumps(account)))
            return account

    except Exception as e:

        logger.error('JimCoAccountQuery Error: ' + str(e))
        return None


# -----------------------------------------------------------------------------


def get_individual_by_user(username):

    try:

        connection = get_connection()

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * from jimcodb.Individuals where UserName = %s;", (username,))
            user = cursor.fetchone()

            cursor.execute("SELECT * from jimcodb.IndividualCommunication where UserId = %s;", (user['IndividualId'],))
            user['Communication'] = cursor.fetchall()

            cursor.execute("SELECT * from jimcodb.Accounts where IndividualId = %s;", (user['IndividualId'],))
            accounts_temp = cursor.fetchall()
            accounts = []

            for account in accounts_temp:
                cursor.execute("SELECT AccountMessageId, AccountId, AccountMessage, Priority FROM jimcodb.AccountMessages where AccountId = %s and EffectiveFrom <= Now() and EffectiveTo >= Now() order by Priority asc;", (account['AccountId'],))
                account['Messages'] = cursor.fetchall()
                accounts.append(account)

            user['Accounts'] = accounts

            logger.info('returned user: {}'.format(json.dumps(user)))

            return user

    except Exception as e:

        logger.error('JimCoAccountQuery Error: ' + str(e))
        return None

# -----------------------------------------------------------------------------


def get_account_messages(account_number):

    try:

        connection = get_connection()

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(
                "SELECT AccountNumber, SocialCode, AccountMessage, MessageType, Priority " +
                "FROM jimcodb.AccountMessagesView " +
                "where AccountNumber = %s and EffectiveFrom <= Now() and EffectiveTo >= Now() " +
                "order by Priority asc;",
                (
                    account_number,
                )
            )
            messages = cursor.fetchall()
            logger.info('returned messages: {}'.format(json.dumps(messages)))
            return messages

    except Exception as e:

        logger.error('JimCoAccountQuery Error: ' + str(e))
        return None


