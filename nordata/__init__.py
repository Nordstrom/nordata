'''Convenience wrappers for connecting to AWS S3 and Redshift'''

__version__ = '0.1'


# Redshift functions
from ._redshift import redshift_get_conn
from ._redshift import read_sql
from ._redshift import redshift_execute_sql
# S3 functions
from ._s3 import create_session
from ._s3 import s3_get_bucket
from ._s3 import s3_download
from ._s3 import s3_upload
from ._s3 import s3_delete


__all__ = ['_redshift', '_s3']