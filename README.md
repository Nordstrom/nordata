# Nordata

## Author:
Nick Buker

## Introduction:
Nordata is a small collection of utility functions for accessing AWS S3 and AWS Redshift. It was written by a data scientist on the Nordstrom Analytics Team. The goal Nordata is to be a simple, robust package to ease data work-flow. It is not intended to handle every possible need (for example credential management is largely left to the user) but it is designed to streamline common tasks.

## Table of contents:

### Installing Nordata:
- [Installation instructions](#pip-installing-nordata)

### Setting up credentials for Nordata:
- [Credentials instructions](#nordata-credentials)

### How to use Nordata:
- [Nordata instructions](#using-nordata)

    Redshift:

    - [Importing nordata Redshift functions](#redshift-import)
    - [Reading a SQL script into Python as a string](#read-sql)
    - [Executing a SQL query that does not return data](#redshift-execute-sql-no-return)
    - [Executing a SQL query that returns data](#redshift-execute-sql-return)
    - [Executing a SQL query that returns data for pandas](#redshift-execute-sql-return-dict)
    - [Creating a connection object (experienced users)](#redshift-get-conn)

    S3:

    - [Importing S3 functions](#s3-import)
    - [Downloading a single file from S3](#s3-download-single)
    - [Downloading a list of files from S3](#s3-download-list)
    - [Downloading files matching a pattern from S3](#s3-download-pattern)
    - [Downloading all files in a directory from S3](#s3-download-all)
    - [Uploading a single file to S3](#s3-upload-single)
    - [Uploading a list of files to S3](#s3-upload-list)
    - [Uploading files matching a pattern to S3](#s3-upload-pattern)
    - [Uploading all files in a directory to S3](#s3-upload-all)
    - [Deleting a single file in S3](#s3-delete-single)
    - [Deleting a list of files in S3](#s3-delete-list)
    - [Deleting files matching a pattern in S3](#s3-delete-pattern)
    - [Deleting all files in a directory in S3](#s3-delete-all)
    - [Creating a boto3 session object (experienced users)](#boto-session)
    - [Creating a bucket object (experienced users)](#get-bucket)


<a name="pip-installing-nordata"></a>
## Installing Nordata:
Nordata can be install via pip. As always, use of a project-level virtual environment is recommended.

 **Nordata requires Python >= 3.6.**

```bash
$ pip install nordata
```

<a name="nordata-credentials"></a>
## Setting up credentials for Nordata:

### Redshift:
Nordata is designed to ingest your Redshift credentials as an environment variable in the below format. This method allows the user freedom to handle credentials a number of ways. As always, best practices are advised. Your credentials should never be placed in the code of your project such as in a `Dockerfile` or `.env` file. Instead, you may wish to place them in your `.bash_profile` locally or take advantage of a key management service such as the one offered by AWS.

```bash
'host=my_hostname dbname=my_dbname user=my_user password=my_password port=1234'
```

### S3:
If the user is running locally, their `Home` directory should contain a `.aws/` directory with a `credentials` file. The `credentials` file should look similar to the example below where the profile name is in brackets. Note that the specific values and region may vary. If the user is running on an EC2, instance permission to access S3 is handled by the IAM role for the instance.

```bash
[default]
aws_access_key_id=MYAWSACCESSKEY
aws_secret_access_key=MYAWSSECRETACCESS
aws_session_token="long_string_of_random_characters=="
aws_security_token="another_string_of_random_characters=="
region=us-west-2
```

<a name="using-nordata"></a>
## How to use Nordata:

### Redshift:

<a name="redshift-import"></a>
Importing nordata Redshift functions:


```python
from nordata import read_sql, redshift_execute_sql, redshift_get_conn
```

<a name="read-sql"></a>
Reading a SQL script into Python as a string:


```python
sql = read_sql(sql_filename='../sql/my_script.sql')
```

<a name="redshift-execute-sql-no-return"></a>
Executing a SQL query that does not return data:


```python
redshift_execute_sql(
    sql=sql,
    env_var='REDSHIFT_CREDS',
    return_data=False,
    return_dict=False)
```

<a name="redshift-execute-sql-return"></a>
Executing a SQL query that returns data as a list of tuples and column names as a list of strings:


```python
data, columns = redshift_execute_sql(
    sql=sql,
    env_var='REDSHIFT_CREDS',
    return_data=True,
    return_dict=False)
```

<a name="redshift-execute-sql-return-dict"></a>Executing a SQL query that returns data as a dict for easy ingestion into a pandas DataFrame:


```python
import pandas as pd

df = pd.DataFrame(**redshift_execute_sql(
    sql=sql,
    env_var='REDSHIFT_CREDS',
    return_data=True,
    return_dict=True))
```

<a name="redshift-get-conn"></a>
Creating a connection object that can be manipulated directly by experienced users:

```python
conn = redshift_get_conn(env_var='REDSHIFT_CREDS')
```

### S3:
<a name="s3-import"></a>
Importing S3 functions:

```python
from nordata import s3_download, s3_upload, s3_delete, create_session, s3_get_bucket
```

<a name="s3-download-single"></a>
Downloading a single file from S3:

```python
s3_download(
    bucket='my_bucket',
    s3_filepath='tmp/my_file.csv',
    filepath='../data/my_file.csv')
```

<a name="s3-download-list"></a>
Downloading a list of files from S3 (will not upload contents of subdirectories):

```python
s3_download(
    bucket='my_bucket',
    s3_filepath=['tmp/my_file1.csv', 'tmp/my_file2.csv', 'img.png'],
    filepath=['../data/my_file1.csv', '../data/my_file2.csv', '../img.png'])
```

<a name="s3-download-pattern"></a>
Downloading files matching a pattern from S3 (will not upload contents of subdirectories):

```python
s3_upload(
    bucket='my_bucket',
    s3_filepath='tmp/',
    filepath='../data/*.csv')
```

<a name="s3-download-all"></a>
Downloading all files in a directory from S3 (will not upload contents of subdirectories):

```python
s3_upload(
    bucket='my_bucket',
    s3_filepath='tmp/',
    filepath='../data/*')
```

<a name="s3-upload-single"></a>
Uploading a single file to S3:

```python
s3_upload(
    bucket='my_bucket',
    filepath='../data/my_file.csv',
    s3_filepath='tmp/my_file.csv')
```

<a name="s3-upload-list"></a>
Uploading a list of files to S3 (will not upload contents of subdirectories):

```python
s3_upload(
    bucket='my_bucket',
    filepath=['../data/my_file1.csv', '../data/my_file2.csv', '../img.png'],
    s3_filepath=['tmp/my_file1.csv', 'tmp/my_file2.csv', 'img.png'])
```

<a name="s3-upload-pattern"></a>
Uploading files matching a pattern to S3 (will not upload contents of subdirectories):

```python
s3_upload(
    bucket='my_bucket',
    filepath='../data/*.csv',
    s3_filepath='tmp/')
```

<a name="s3-upload-all"></a>
Uploading all files in a directory to S3 (will not upload contents of subdirectories):

```python
s3_upload(
    bucket='my_bucket',
    filepath='../data/*'
    s3_filepath='tmp/')
```

<a name="s3-delete-single"></a>
Deleting a single file in S3:

```python
resp = s3_delete(bucket='my_bucket', s3_filepath='tmp/my_file.csv')
```

<a name="s3-delete-list"></a>
Deleting a list of files in S3:

```python
resp = s3_delete(
    bucket='my_bucket',
    s3_filepath=['tmp/my_file1.csv', 'tmp/my_file2.csv', 'img.png'])
```

<a name="s3-delete-pattern"></a>
Deleting files matching a pattern in S3:

```python
resp = s3_delete(bucket='my_bucket', s3_filepath='tmp/*.csv')
```

<a name="s3-delete-all"></a>
Deleting all files in a directory in S3:

```python
resp = s3_delete(bucket='my_bucket', s3_filepath='tmp/*')
```

<a name="boto-session"></a>
Creating a boto3 session object that can be manipulated directly by experienced users:

```python
session = create_session(profile_name='default', region_name='us-west-2')
```

<a name="get-bucket"></a>
Creating a bucket object that can be manipulated directly by experienced users:

```python
bucket = s3_get_bucket(
    bucket='my_bucket',
    profile_name='default',
    region_name='us-west-2')
```
