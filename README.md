# Nordata

Nordata is a small collection of utility functions for accessing AWS S3 and AWS Redshift. The goal of this project is to create a simple, robust package to ease data work-flow and allow the same tool to be used for development and production. Nordata is not intended to handle every possible need (for example credential management is largely left to the user) but it is designed to streamline common tasks.

### Installing Nordata
Nordata can be install via pip. As always, use of a project-level virtual environment is recommended.

```bash
$ pip install nordata
```

### Credentials
- S3
- Redshift

### How to use Nordata
# TODO
```python
import nordata as nd
```

```python
sql = nd.redshift_read_sql(sql_filename='../sql/my_script.sql')
```

```python
nd.redshift_execute_sql(
    sql=sql,
    env_var='REDSHIFT_CREDS',
    return_data=False,
    return_dict=False,
)
```

```python
data, columns = nd.redshift_execute_sql(
    sql=sql,
    env_var='REDSHIFT_CREDS',
    return_data=True,
    return_dict=False,
)
```

```python
import pandas as pd
```

```python
df = pd.DataFrame(**nd.redshift_execute_sql(
    sql=sql,
    env_var='REDSHIFT_CREDS',
    return_data=True,
    return_dict=True,
))
```

```python
conn = nd.redshift_get_conn(env_var='REDSHIFT_CREDS')
```

### Troubleshooting
# TODO