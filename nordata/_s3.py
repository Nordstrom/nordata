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
        session=None):
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
        profile name for credentials (typically 'default' or organization-specific)
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
        filepath='..data/my_file.csv')

    # Download all files in a directory (will not upload contents of subdirectories):
    s3_download(
        bucket='my_bucket',
        s3_filepath='tmp/*',
        filepath='..data/')

    # Download all files in a directory matching a wildcard (will not download contents of subdirectories):
    s3_download(
        bucket='my_bucket',
        s3_filepath='tmp/*.csv',
        filepath='..data/')
    """
    # TODO give the below some tidying
    # TODO think about most efficient flow and parsimonious code
    if isinstance(s3_filepath, list):
        if len(s3_filepath) != len(local_filepath):
            raise ValueError('Length of s3_filepath arguments must equal length of local_filepath arguments')
    elif isinstance(s3_filepath, str):
        pass
    else:
        # raise TypeError('The parameter s3_filepath must be of str or list type')
        # if s3 and local paths are a single string
        s3_filepath = [s3_filepath]
        local_filepath = [local_filepath]
    my_bucket = s3_get_bucket(
        bucket=bucket,
        profile_name=profile_name,
        region_name=region_name)
    # multipart_threshold and multipart_chunksize defaults = Amazon defaults
    config = TransferConfig(multipart_threshold=multipart_threshold, multipart_chunksize=multipart_chunksize)
    if '*' in s3_filepath:
        # use left and right for pattern matching
        left = s3_filepath.split('*')[0]
        right = s3_filepath.split('*')[-1]
        # construct s3_path without wildcard
        s3_path = '/'.join(s3_filepath.split('/')[:-1]) + '/'
        # get keys, filter out directories, match wildcard, get filenames
        keys = [item.key for item in my_bucket.objects.filter(Prefix=s3_path)
                if item.key[-1] != '/' and left in item.key and right in item.key]
        filenames = [key.split('/')[-1] for key in keys]
    else:
        keys = s3_filepath
        filenames = local_filepath

    for key, local in zip(keys, filenames):
        try:
            my_bucket.download_file(
                key,
                local,
                Config=config)
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 400:
                raise NameError('If running locally, you must run awscreds in the background. ' + str(e))
            else:
                raise e
        print('{} download complete'.format(key))


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
        path and filename within the bucket for the file to be uploaded
    region_name : str
        name of AWS region (default value 'us-west-2')
    profile_name : str
        profile name for credentials (typically 'default' or organization-specific)
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
    s3_upload(bucket='persis-datalab-team',
              s3_filepath='tmp/myfile.csv',
              filepath='..data/myfile.csv',
              environment='local')

    # to upload all files in a directory (will not upload contents of subdirectories)
    s3_upload(bucket='persis-datalab-team',
              s3_filepath='tmp/',
              filepath='..data/*',
              environment='local')

    # to upload all files in a directory matching a wildcard (will not upload contents of subdirectories)
    s3_upload(bucket='persis-datalab-team',
              s3_filepath='tmp/',
              filepath='../data/*.csv')
    """
    # TODO check that permission is a proper type
    if type(s3_filepath) == list:
        if len(s3_filepath) != len(local_filepath):
            raise ValueError('Length of s3_filepath arguments must equal length of local_filepath arguments')

    my_bucket = s3_get_bucket(
        bucket=bucket,
        profile_name=profile_name,
        region_name=region_name)
    # multipart_threshold and multipart_chunksize defaults = Amazon defaults
    config = TransferConfig(multipart_threshold=multipart_threshold,
                            multipart_chunksize=multipart_chunksize)
    if '*' in local_filepath:
        items = glob.glob(local_filepath)
        # filter out directories
        filepaths = [item for item in items if os.path.isfile(item)]
        filenames = [f.split('/')[-1] for f in filepaths]
    else:
        filepaths = [local_filepath]
        filenames = ['']
    for i, filepath in enumerate(filepaths):
        try:
            my_bucket.upload_file(
                filepath,
                s3_filepath + filenames[i],
                Config=config)
        except boto3.exceptions.S3UploadFailedError as e:
            raise S3UploadFailedError(str(e))
        print('{} upload complete'.format(filepath))


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
        profile name for credentials (typically 'default' or organization-specific)
    region_name : str
        name of AWS region (default value 'us-west-2')

    Returns
    -------
    List
        Deleted keys

    Example use
    -----------
    # Delete a single item:
    resp = nordypy.s3_delete(bucket='my_bucket', s3_filepath='file1.txt')

    # Delete multiple items:
    to_delete = ['file1.txt', 'image.png', 'model.pkl']
    resp = nordypy.s3_delete(bucket='my_bucket', s3_filepath=to_delete)

    # Delete all files matching a pattern:
    TODO

    # Delete all files in an S3 directory:
    TODO
    """
    if type(s3_filepath) is str:
        s3_filepath = [s3_filepath]
    del_dict = {}
    objects = []
    for key in s3_filepath:
        objects.append({'Key': key})
    del_dict['Objects'] = objects
    my_bucket = s3_get_bucket(
        bucket=bucket,
        profile_name=profile_name,
        region_name=region_name)
    response = my_bucket.delete_objects(Delete=del_dict)
    return response['Deleted']
