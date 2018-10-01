import os
import psycopg2


def redshift_get_conn(env_var):
    """ Creates a Redshift connection object

    Parameters
    ----------
    env_var : str
        name of the environment variable containing the credentials str
        creds_str should have the below format where the user has inserted their values:
        'host=my_hostname dbname=my_dbname user=my_user password=my_password port=1234'

    Returns
    -------
    psycopg2 connection object
    """
    cred_str = os.environ[env_var]
    creds_dict = _create_creds_dict(cred_str)
    conn = psycopg2.connect(**creds_dict)
    return conn


def redshift_read_sql(sql_filename):
    """ Ingests a SQL file and returns a str containing the contents of the file

    Parameters
    ----------
    sql_filename : str
        path to and name of SQL file to be ingested

    Returns
    -------
    str
        contents of the SQL file ingested
    """
    with open(sql_filename, 'r') as f:
        sql_str = ' '.join(f.readlines())
    return sql_str


def redshift_execute_sql(sql, env_var, return_data=False):
    """ Ingests a SQL query as a string and executes it (potentially returning data)

    Parameters
    ----------
    sql : str
        SQL query to be executed
    env_var : str
        name of the environment variable containing the credentials str
        creds_str should have the below format where the user has inserted their values:
        'host=my_hostname dbname=my_dbname user=my_user password=my_password port=1234'
    return_data : bool
        whether or not the query should return data

    Returns
    -------
    list of tuples or None
        TODO dig into data types
    """
    try:
        with redshift_get_conn(env_var=env_var) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                if return_data:
                    header = [desc[0] for desc in cursor.description]
                    data = [row for row in cursor]
                    conn.commit()
                    return data, header
                else:
                    conn.commit()
                    return
    except psycopg2.ProgrammingError as p:
        raise RuntimeError('SQL ProgrammingError! = {0}'.format(p))
    except Exception as e:
        raise RuntimeError('SQL error = {0}'.format(e))


def _create_creds_dict(creds_str):
    """ Takes the credentials str and converts it to a dict

    Parameters
    ----------
    creds_str : str
        credentials string with the below format where the user has inserted their values:
        'host=my_hostname dbname=my_dbname user=my_user password=my_password port=1234'

    Returns
    -------
    dict
        credentials in dict form
    """
    creds_dict = {}
    for param in creds_str.split(' '):
        split_param = param.split('=')
        creds_dict[split_param[0]] = split_param[1]
    return creds_dict