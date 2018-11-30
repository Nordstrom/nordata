# Nordata

Nordata is a small collection of utility functions for accessing AWS S3 and AWS Redshift. The goal of this project is to create a simple, robust package to ease data work-flow and allow the same tool to be used for development and production. Nordata is not intended to handle every possible need (for example credential management is largely left to the user) but it is designed to streamline common tasks.

## Installing Nordata
Nordata can be install via pip. As always, use of a project-level virtual environment is recommended.

```bash
$ pip install nordata
```

## Setting up credentials for Nordata
### Redshift
Nordata is designed to ingest your Redshift credentials as an environment variable in the below format. This method allows the user freedom to handle credentials a number of ways. As always, best practices are advised. Your credentials should never be placed in the code of your project such as in a `Dockerfile` or `.env` file. Instead, you may wish to place them in your `.bash_profile` locally or take advantage of a key management service such as the one offered by AWS.
```bash
'host=my_hostname dbname=my_dbname user=my_user password=my_password port=1234'
```
### S3:
If the user is running locally, their `Home` directory should contain a `.aws/` directory with a `credentials` file. The `credentials` file should look similar to the example below where the profile name is in brackets. Note that the specific values and region may vary. If the user is running on an EC2 instance permission to access S3 is handled by the IAM role for the instance.
```bash
[default]
aws_access_key_id=MYAWSACCESSKEY
aws_secret_access_key=MYAWSSECRETACCESS
aws_session_token="long_string_of_random_characters=="
aws_security_token="another_string_of_random_characters=="
region=us-west-2
```
## How to use Nordata
### Redshift functions:
- Importing nordata functions:
```python
from nordata import read_sql, redshift_execute_sql, redshift_get_conn
```
- Reading a SQL script into Python as a string:
```python
sql = read_sql(sql_filename='../sql/my_script.sql')
```
- Executing a SQL query that does not return data:
```python
redshift_execute_sql(
    sql=sql,
    env_var='REDSHIFT_CREDS',
    return_data=False,
    return_dict=False)
```
- Executing a SQL script that returns data as a list of tuples and column names as a list of strings:
```python
data, columns = redshift_execute_sql(
    sql=sql,
    env_var='REDSHIFT_CREDS',
    return_data=True,
    return_dict=False)
```
- Executing a SQL script that returns data as a dict for easy ingestion into a pandas DataFrame:
```python
import pandas as pd

df = pd.DataFrame(**redshift_execute_sql(
    sql=sql,
    env_var='REDSHIFT_CREDS',
    return_data=True,
    return_dict=True))
```
- Create a connection object that can be manipulated directly by experienced users:
```python
conn = redshift_get_conn(env_var='REDSHIFT_CREDS')
```
### S3 functions:
- Importing S3 functions:
```python
from nordata import s3_download, s3_upload, s3_delete, create_session, s3_get_bucket
```
- Downloading a single file from S3:
```python
s3_download(
    bucket='my_bucket',
    s3_filepath='tmp/my_file.csv',
    filepath='../data/my_file.csv')
```
- Downloading a list of files from S3 (will not upload contents of subdirectories):
```python
s3_download(
    bucket='my_bucket',
    s3_filepath=['tmp/my_file1.csv', 'tmp/my_file2.csv', 'img.png'],
    filepath=['../data/my_file1.csv', '../data/my_file2.csv', '../img.png'])
```
- Downloading files matching a pattern (will not upload contents of subdirectories):
```python
s3_upload(
    bucket='my_bucket',
    s3_filepath='tmp/',
    filepath='../data/*.csv')
```
- Uploading a single file to S3:
```python
s3_upload(
    bucket='my_bucket',
    filepath='../data/my_file.csv',
    s3_filepath='tmp/my_file.csv')
```
- Uploading a list of files to S3 (will not upload contents of subdirectories):
```python
s3_upload(
    bucket='my_bucket',
    filepath=['../data/my_file1.csv', '../data/my_file2.csv', '../img.png'],
    s3_filepath=['tmp/my_file1.csv', 'tmp/my_file2.csv', 'img.png'])
```
- Uploading files matching a pattern (will not upload contents of subdirectories):
```python
s3_upload(
    bucket='my_bucket',
    s3_filepath='tmp/',
    filepath='../data/*.csv')
```
- Deleting a single file in S3:
```python
resp = s3_delete(bucket='my_bucket', s3_filepath='tmp/my_file.csv')
```
- Deleting a list of files in S3:
```python
resp = s3_delete(
    bucket='my_bucket',
    s3_filepath=['tmp/my_file1.csv', 'tmp/my_file2.csv', 'img.png'])
```
- Deleting files matching a pattern in S3:
```python
resp = s3_delete(bucket='my_bucket', s3_filepath='tmp/*.csv')
```
- Delete all files in a directory in S3:
```python
resp = s3_delete(bucket='my_bucket', s3_filepath='tmp/*')
```
- Creating a boto3 session object that can be manipulated directly by experienced users:
```python
session = create_session(profile_name='default', region_name='us-west-2')
```
- Creating a bucket object that can be manipulated directly by experienced users:
```python
bucket = s3_get_bucket(
    bucket='my_bucket',
    profile_name='default',
    region_name='us-west-2')
```

## Troubleshooting
# TODO

## FAQ
# TODO