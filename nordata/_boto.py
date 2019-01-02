import boto3


def boto_create_session(profile_name='default', region_name='us-west-2'):
    """ Instantiates and returns a boto3 session object

    Parameters
    ----------
    profile_name : str
        profile name under which credentials are stored (default 'default' unless organization specific)
    region_name : str
        name of AWS regions (default 'us-west-2')

    Returns
    -------
    boto3 session object

    Example use
    -----------
    session = create_session(profile_name='default', region_name='us-west-2')
    """
    return boto3.session.Session(profile_name=profile_name, region_name=region_name)


def boto_get_creds(
        profile_name='default',
        region_name='us-west-2',
        session=None):
    """ Generates and returns an S3 credential string

    Parameters
    ----------
    profile_name : str
        profile name under which credentials are stores (default 'default' unless organization specific)
    region_name : str
        name of AWS regions (default 'us-west-2')
    session : boto3 session object or None
        you can optionally provide a boto3 session object or the function can instantiate a new one if None

    Returns
    -------
    str
        credentials for accessing S3

    Example use
    -----------
    creds = boto_get_creds(
        profile_name='default',
        region_name='us-west-2',
        session=None)
    """
    if session is None:
        session = boto_create_session(profile_name=profile_name, region_name=region_name)
    access_key = session.get_credentials().access_key
    secret_key = session.get_credentials().secret_key
    token = session.get_credentials().token
    return f'''aws_access_key_id={access_key};aws_secret_access_key={secret_key};token={token}'''
