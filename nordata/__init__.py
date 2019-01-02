'''Convenience wrappers for connecting to AWS S3 and Redshift'''

__version__ = '0.2.1'


# Boto3 function
from ._boto import boto_get_creds
from ._boto import boto_create_session
# Redshift functions
from ._redshift import redshift_get_conn
from ._redshift import read_sql
from ._redshift import redshift_execute_sql
# S3 functions
from ._s3 import s3_get_bucket
from ._s3 import s3_download
from ._s3 import s3_upload
from ._s3 import s3_delete


__all__ = ['_boto', '_redshift', '_s3']