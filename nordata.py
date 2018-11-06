""" TODO awesome package """
__version__ = '0.1'


import os
import psycopg2
import boto3
import botocore


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


def redshift_execute_sql(
        sql,
        env_var,
        return_data=False,
    ):
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
    # TODO is there a way to clean this up?
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



def create_session(profile_name='default', region_name='us-west-2'):
    """ Instantiates and returns a boto3 session object

    Parameters
    ----------
    profile_name : str
        profile name under which credentials are stores (typically 'default' unless organization specific)
    region_name : str
        name of AWS regions (typically 'us-west-2')

    Returns
    -------
    boto3 session object
    """
    return boto3.session.Session(profile_name=profile_name, region_name=region_name)


def _s3_get_creds(
        profile_name='default',
        region_name='us-west-2',
        session=None,
    ):
    """ Generates and returns an S3 credential string

    Parameters
    ----------
    profile_name : str
        profile name under which credentials are stores (typically 'default' unless organization specific)
    region_name : str
        name of AWS regions (typically 'us-west-2')
    session : boto3 session object or None
        you can optionally provide a boto3 session object or the function can instantiate a new one if None
    Returns
    -------
    str
        credentials for accessing S3
    """
    if session is None:
        session = create_session(profile_name=profile_name, region_name=region_name)
    access_key = session.get_credentials().access_key,
    secret_key = session.get_credentials().secret_key,
    token = session.get_credentials().token,
    return f'aws_access_key_id={access_key};aws_secret_access_key={secret_key};token={token}'


def s3_get_bucket(
        bucket,
        profile_name='default',
        region_name='us-west-2',
    ):
    """ Creates and returns a boto3 bucket object

    Parameters
    ----------
    bucket : str
        name of S3 bucket
    profile_name: str
        profile name for credentials (typically default or organization-specific)
    region_name : str
        name of AWS regions (typically 'us-west-2')

    Returns
    -------
    boto3 bucket object
    """
    session = create_session(profile_name=profile_name, region_name=region_name)
    s3 = session.resource('s3')
    my_bucket = s3.Bucket(bucket)
    try:
        s3.meta.client.head_bucket(Bucket=bucket)
    except botocore.exceptions.ClientError as e:
        # Check if bucket exists, if not raise error
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            raise NameError('404 Bucket does not exist')
        if error_code == 400:
            raise NameError('400 The credentials were expired or incorrect.')
    return my_bucket



def s3_download_file(
        bucket,
        s3_filepath,
        s3_filename,
        local_filepath,
        local_filename=None,
        profile_name='default',
        verbose=False,
    ):
    """ Downloads a file or collection of files from S3

    Parameters
    ----------
    bucket : str
        name of S3 bucket
    s3_filepath : str
        path to the fil(e) to be downloaded in S3 bucket
    s3_filename : str or list of str or None
        name of the file(s) to be downloaded
    local_filepath : str
        path to where the downloaded file(s) will be saved locally
    local_filename : str or list of str or None
         name of file(s) once downloaded (if None, the same file name(s) will be used)
    profile_name: str
        profile name for credentials (typically default or organization-specific)
    verbose : bool
        whether or not to indicate progress

    Returns
    -------
    None
    """
    # TODO
    return


def s3_upload_file(
        bucket,
        local_filepath,
        local_filename,
        s3_filepath,
        s3_filename=None,
        profile_name='default',
        verbose=False,
    ):
    """ Uploads a file or collection of files to S3

    Parameters
    ----------
    bucket : str
        name of S3 bucket
    local_filepath : str
        path to the file(s) to be uploaded locally
    local_filename : str or list of str
        name of the file(s) to be uploaded
    s3_filepath : str
        path to where the uploaded file(s) will be saved in the S3 bucket
    s3_filename : str or list of str or None
        name of file(s) once uploaded (if None, the same file name(s) will be used)
    profile_name: str
        profile name for credentials (typically default or organization-specific)
    verbose :  bool
        whether or not to indicate progress

    Returns
    -------
    None
    """
    # TODO
    return


def s3_delete_file(
        bucket,
        s3_filepath,
        s3_filename,
        profile_name='default',
        verbose=False,
    ):
    """ Deletes a file or collection of files from S3

    Parameters
    ----------
    bucket : str
        name of S3 bucket
    s3_filepath : str
        path to file in S3 bucket
    s3_filename : str or list of str
        name of file(s) to be deleted
    profile_name : str
        profile name for credentials (typically default or organization-specific)
    verbose : bool
        whether or not to indicate progress

    Returns
    -------
    None
    """
    # TODO
    return