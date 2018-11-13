# Nordata

Nordata is a small collection of utility functions for accessing AWS S3 and AWS Redshift. The goal of this project is to create a simple, robust package to ease data work-flow and allow the same tool to be used for development and production. Nordata is not intended to handle every possible need (for example credential management is largely left to the user) but it is designed to streamline common tasks.

## Installing Nordata
Nordata can be install via pip. As always, use of a project-level virtual environment is recommended.

```bash
$ pip install nordata
```

## Credentials
- Redshift: TODO
- S3: TODO

## How to use Nordata
### Redshift functions:
Importing nordata functions:
```python
from nordata import read_sql, redshift_execute_sql, redshift_get_conn
```
Reading a SQL script into Python as a string:
```python
sql = read_sql(sql_filename='../sql/my_script.sql')
```
Executing a SQL query that does not return data:
```python
redshift_execute_sql(
    sql=sql,
    env_var='REDSHIFT_CREDS',
    return_data=False,
    return_dict=False)
```
Executing a SQL script that returns data as a list of tuples and column names as a list of strings:
```python
data, columns = redshift_execute_sql(
    sql=sql,
    env_var='REDSHIFT_CREDS',
    return_data=True,
    return_dict=False)
```
Executing a SQL script that returns data as a dict for easy ingestion into a pandas DataFrame:
```python
import pandas as pd

df = pd.DataFrame(**redshift_execute_sql(
    sql=sql,
    env_var='REDSHIFT_CREDS',
    return_data=True,
    return_dict=True))
```
Create a connection object that can be manipulated directly by experienced users:
```python
conn = redshift_get_conn(env_var='REDSHIFT_CREDS')
```
### S3 functions:
Importing S3 functions:
```python
from nordata import s3_download, s3_upload, s3_delete, create_session, s3_get_bucket
```
Downloading a single file from S3:
```python
s3_download(
    bucket='my_bucket',
    s3_filepath='tmp/my_file.csv',
    filepath='../data/my_file.csv')
```
Downloading a list of files from S3 (will not upload contents of subdirectories):
```python
s3_download(
    bucket='my_bucket',
    s3_filepath=['tmp/my_file1.csv', 'tmp/my_file2.csv', 'img.png'],
    filepath=['../data/my_file1.csv', '../data/my_file2.csv', '../img.png'])
```
Downloading files matching a pattern (will not upload contents of subdirectories):
```python
s3_upload(
    bucket='my_bucket',
    s3_filepath='tmp/',
    filepath='../data/*.csv')
```
Uploading a single file to S3:
```python
s3_upload(
    bucket='my_bucket',
    filepath='../data/my_file.csv',
    s3_filepath='tmp/my_file.csv')
```
Uploading a list of files to S3 (will not upload contents of subdirectories):
```python
s3_upload(
    bucket='my_bucket',
    filepath=['../data/my_file1.csv', '../data/my_file2.csv', '../img.png'],
    s3_filepath=['tmp/my_file1.csv', 'tmp/my_file2.csv', 'img.png'])
```
Uploading files matching a pattern (will not upload contents of subdirectories):
```python
s3_upload(
    bucket='my_bucket',
    s3_filepath='tmp/',
    filepath='../data/*.csv')
```
Deleting a single file in S3:
```python
resp = s3_delete(bucket='my_bucket', s3_filepath='tmp/my_file.csv')
```
Deleting a list of files in S3:
```python
resp = s3_delete(
    bucket='my_bucket',
    s3_filepath=['tmp/my_file1.csv', 'tmp/my_file2.csv', 'img.png'])
```
Deleting files matching a pattern in S3:
```python
resp = s3_delete(bucket='my_bucket', s3_filepath='tmp/*.csv')
```
Delete all files in a directory in S3:
```python
resp = s3_delete(bucket='my_bucket', s3_filepath='tmp/*')
```
Creating a boto3 session object that can be manipulated directly by experienced users:
```python
session = create_session(profile_name='default', region_name='us-west-2')
```
Creating a bucket object that can be manipulated directly by experienced users:
```python
bucket = s3_get_bucket(
    bucket='my_bucket',
    profile_name='default',
    region_name='us-west-2')
```

## Troubleshooting
# TODO