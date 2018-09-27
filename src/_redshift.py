import json
import psycopg2


def redshift_get_conn(json_path, database_key):
    """ Creates a Redshift connection object

    Parameters
    ----------
    json_path : str
        path to and name of the credentials json file
    database_key : str
        key for the database and account in the credentials json file

    Returns
    -------
    psycopg2 connection object
    """
    with open(json_path, 'r') as f:
        cfg = json.load(f)
    conn = psycopg2.connect(
        host=cfg[database_key]['host'],
        dbname=cfg[database_key]['dbname'],
        password=cfg[database_key]['password'],
        port=int(cfg[database_key]['port']),
        user=cfg[database_key]['user'],
    )
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


def redshift_execute_sql(sql, json_path, database_key, return_data=False):
    """ Ingests a SQL query as a string and executes it (potentially returning data)

    Parameters
    ----------
    sql : str
        SQL query to be executed
    json_path : str
        path to and name of the credentials json file
    database_key : str
        key for the database and account in the credentials json file
    return_data : bool
        whether or not the query should return data

    Returns
    -------
    list of tuples or None
        TODO dig into data types
    """
    try:
        with redshift_get_conn(json_path=json_path, database_key=database_key) as conn:
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

