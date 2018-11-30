import os
import glob
import boto3
from botocore.exceptions import ClientError
from boto3.exceptions import S3UploadFailedError
from boto3.s3.transfer import TransferConfig


def create_session(profile_name='default', region_name='us-west-2'):
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


def _s3_get_creds(
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
    """
    if session is None:
        session = create_session(profile_name=profile_name, region_name=region_name)
    access_key = session.get_credentials().access_key,
    secret_key = session.get_credentials().secret_key,
    token = session.get_credentials().token,
    return f'''aws_access_key_id={access_key};aws_secret_access_key={secret_key};token={token}'''


def s3_get_bucket(
        bucket,
        profile_name='default',
        region_name='us-west-2'):
    """ Creates and returns a boto3 bucket object

    Parameters
    ----------
    bucket : str
        name of S3 bucket
    profile_name: str
        profile name for credentials (default 'default' or organization-specific)
    region_name : str
        name of AWS regions (default 'us-west-2')

    Returns
    -------
    boto3 bucket object

    Example use
    -----------
    bucket = s3_get_bucket(
        bucket='my_bucket',
        profile_name='default',
        region_name='us-west-2')
    """
    session = create_session(profile_name=profile_name, region_name=region_name)
    s3 = session.resource('s3')
    my_bucket = s3.Bucket(bucket)
    try:
        s3.meta.client.head_bucket(Bucket=bucket)
    except ClientError as e:
        # Check if bucket exists, if not raise error
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            raise NameError('404 Bucket does not exist')
        if error_code == 400:
            raise NameError('400 The credentials were expired or incorrect.')
    return my_bucket


def s3_download(
        bucket,
        s3_filepath,
        local_filepath,
        profile_name='default',
        region_name='us-west-2',
        multipart_threshold=8388608,
        multipart_chunksize=8388608):
    """ Downloads a file or collection of files from S3

    Parameters
    ----------
    bucket : str
        name of S3 bucket
    s3_filepath : str or list
        path and filename within bucket to file(s) you would like to download
    local_filepath : str or list
        path and filename for file(s) to be saved locally
    profile_name : str
        profile name for credentials (default 'default' or organization-specific)
    region_name : str
        name of AWS region (default value 'us-west-2')
    multipart_threshold : int
        minimum file size to initiate multipart download
    multipart_chunksize : int
        chunksize for multipart download

    Returns
    -------
    None

    Example use
    -----------
    # Download a single file:
    s3_download(
        bucket='my_bucket',
        s3_filepath='tmp/my_file.csv',
        filepath='../data/my_file.csv')

    # Download all files in a directory (will not upload contents of subdirectories):
    s3_download(
        bucket='my_bucket',
        s3_filepath='tmp/*',
        filepath='../data/')

    # Download all files in a directory matching a wildcard (will not download contents of subdirectories):
    s3_download(
        bucket='my_bucket',
        s3_filepath='tmp/*.csv',
        filepath='../data/')
    """
    # validate s3_filepath and local_filepath arguments
    _download_upload_filepath_validator(s3_filepath=s3_filepath, local_filepath=local_filepath)
    # create bucket object
    my_bucket = s3_get_bucket(
        bucket=bucket,
        profile_name=profile_name,
        region_name=region_name)
    # multipart_threshold and multipart_chunksize, defaults = Amazon defaults
    config = TransferConfig(multipart_threshold=multipart_threshold,
                            multipart_chunksize=multipart_chunksize)
    if isinstance(s3_filepath, str):
        # find keys matching wildcard
        if '*' in s3_filepath:
            s3_filepath = _s3_glob(s3_filepath=s3_filepath, my_bucket=my_bucket)
            local_filepath = [os.path.join(local_filepath, key.split('/')[-1]) for key in s3_filepath]
        # insert into list so same looping structure can be used
        else:
            s3_filepath = [s3_filepath]
            local_filepath = [local_filepath]
    # download all files from S3
    for s3_key, local_file in zip(s3_filepath, local_filepath):
        try:
            my_bucket.download_file(
                s3_key,
                local_file,
                Config=config)
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 400:
                raise NameError('The credentials are expired or not valid. ' + str(e))
            else:
                raise e
    return


def s3_upload(
        bucket,
        local_filepath,
        s3_filepath,
        profile_name='default',
        region_name='us-west-2',
        multipart_threshold=8388608,
        multipart_chunksize=8388608):
    """ Uploads a file or collection of files to S3

    Parameters
    ----------
    bucket : str
        name of S3 bucket
    local_filepath : str or list
        path and filename(s) to be uploaded
    s3_filepath : str or list
        path and filename(s) within the bucket for the file to be uploaded
    region_name : str
        name of AWS region (default value 'us-west-2')
    profile_name : str
        profile name for credentials (default 'default' or organization-specific)
    multipart_threshold : int
        minimum file size to initiate multipart upload
    multipart_chunksize : int
        chunksize for multipart upload

    Returns
    -------
    None

    Example use
    -----------
    # to upload a single file
    s3_upload(
        bucket='my_bucket',
        s3_filepath='tmp/my_file.csv',
        filepath='../data/my_file.csv')

    # to upload all files in a directory (will not upload contents of subdirectories)
    s3_upload(
        bucket='my_bucket',
        s3_filepath='tmp/',
        filepath='../data/*')

    # to upload all files in a directory matching a wildcard (will not upload contents of subdirectories)
    s3_upload(
        bucket='my_bucket',
        s3_filepath='tmp/',
        filepath='../data/*.csv')
    """
    _download_upload_filepath_validator(s3_filepath=s3_filepath, local_filepath=local_filepath)
    my_bucket = s3_get_bucket(
        bucket=bucket,
        profile_name=profile_name,
        region_name=region_name)
    # multipart_threshold and multipart_chunksize, defaults = Amazon defaults
    config = TransferConfig(multipart_threshold=multipart_threshold,
                            multipart_chunksize=multipart_chunksize)
    if isinstance(local_filepath, str):
        if '*' in local_filepath:
            items = glob.glob(local_filepath)
            # filter out directories
            local_filepath = [item for item in items if os.path.isfile(item)]
            tmp_s3_filepath = [s3_filepath + f.split('/')[-1] for f in local_filepath]
            s3_filepath = tmp_s3_filepath
        else:
            local_filepath = [local_filepath]
            s3_filepath = [s3_filepath]
    # upload all files to S3
    for local_file, s3_key in zip(local_filepath, s3_filepath):
        try:
            my_bucket.upload_file(
                local_file,
                s3_key,
                Config=config)
        except boto3.exceptions.S3UploadFailedError as e:
            raise S3UploadFailedError(str(e))
    return


def s3_delete(
        bucket,
        s3_filepath,
        profile_name='default',
        region_name='us-west-2'):
    """ Deletes a file or collection of files from S3

    Parameters
    ----------
    bucket : str
        name of S3 bucket
    s3_filepath : str or list
        path and filename of item(s) within the bucket to be deleted
    profile_name : str
        profile name for credentials (default 'default' or organization-specific)
    region_name : str
        name of AWS region (default value 'us-west-2')

    Returns
    -------
    List
        Deleted keys

    Example use
    -----------
    # Delete a single item:
    resp = s3_delete(bucket='my_bucket', s3_filepath='file1.txt')

    # Delete multiple items:
    resp = s3_delete(
        bucket='my_bucket',
        s3_filepath=['tmp/my_file1.csv', 'tmp/my_file2.csv', 'img.png'])

    # Delete all files matching a pattern:
    resp = s3_delete(bucket='my_bucket', s3_filepath='tmp/*.csv')

    # Delete all files in an S3 directory:
    resp = s3_delete(bucket='my_bucket', s3_filepath='tmp/*')
    """
    _delete_filepath_validator(s3_filepath=s3_filepath)
    my_bucket = s3_get_bucket(
        bucket=bucket,
        profile_name=profile_name,
        region_name=region_name)
    if isinstance(s3_filepath, str):
        if '*' in s3_filepath:
            s3_filepath = _s3_glob(s3_filepath=s3_filepath, my_bucket=my_bucket)
            if not s3_filepath:  # check if this list of S3 filepaths is empty
                return []
        else:
            s3_filepath = [s3_filepath]
    del_dict = {}
    objects = []
    for key in s3_filepath:
        objects.append({'Key': key})
    del_dict['Objects'] = objects
    response = my_bucket.delete_objects(Delete=del_dict)
    return response['Deleted']


def _download_upload_filepath_validator(s3_filepath, local_filepath):
    """ Validates the s3_filepath and local_filepath arguments and raises clear errors

    Parameters
    ----------
    s3_filepath : str or list of str
        path and filename of item(s) within the S3 bucket
    local_filepath : str or list of str
        path and filename for local file(s)

    Returns
    -------
    None
    """
    for arg in (s3_filepath, local_filepath):
        if not isinstance(arg, (list, str)):
            raise TypeError('Both s3_filepath and local_filepath must be of type list or str')
    if type(s3_filepath) != type(local_filepath):
        raise TypeError('Both s3_filepath and local_filepath must be of same type')
    if isinstance(s3_filepath, list):
        for f in s3_filepath + local_filepath:
            if not isinstance(f, str):
                raise TypeError('If s3_filepath and local_filepath are lists, they must contain strings')
            if '*' in f:
                raise ValueError('Wildcards (*) are not permitted within a list of filepaths')
        if len(s3_filepath) != len(local_filepath):
            raise ValueError('The s3_filepath list must the same number of elements as the local_filepath list')
    return


def _delete_filepath_validator(s3_filepath):
    """ Validates the s3_filepath argument and raises clear errors

    Parameters
    ----------
    s3_filepath : str or list of str
        path and filename of item(s) within the S3 bucket

    Returns
    -------
    None
    """
    if not isinstance(s3_filepath, (list, str)):
        raise TypeError('s3_filepath must be of type list or str')
    if isinstance(s3_filepath, list):
        for f in s3_filepath:
            if not isinstance(f, str):
                raise TypeError('If s3_filepath is a list, it must contain strings')
            if '*' in f:
                raise ValueError('Wildcards (*) are not permitted within a list of filepaths')
    return


def _s3_glob(s3_filepath, my_bucket):
    """ Searches a directory in an S3 bucket and returns keys matching the wildcard

    Parameters
    ----------
    s3_filepath : str
        the S3 filepath (with wildcard) to be searched for matches
    my_bucket : boto3 bucket object
        the S3 bucket object containing the directories to be searched

    Returns
    -------
    list of str
        S3 filepaths matching the wildcard
    """
    # use left and right for pattern matching
    left, _, right = s3_filepath.partition('*')
    # construct s3_path without wildcard
    s3_path = '/'.join(s3_filepath.split('/')[:-1]) + '/'
    filtered_s3_filepath = []
    for item in my_bucket.objects.filter(Prefix=s3_path):
        # filter out directories
        if item.key[-1] != '/':
            p1, p2, p3 = item.key.partition(left)
            # pattern matching
            if p1 == '' and p2 == left and right in p3:
                filtered_s3_filepath.append(item.key)
    return filtered_s3_filepath
