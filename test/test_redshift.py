import os
import pytest
import psycopg2
from ..nordata import _redshift as rs


os.environ['TEST_CREDS'] = 'host=my_hostname dbname=my_dbname user=my_user password=my_password port=1234'


def test_create_creds_dict_type():
    # test type returned by _create_creds_dict()
    assert isinstance(rs._create_creds_dict(os.environ['TEST_CREDS']), dict)


def test_create_creds_dict_len():
    # test length of dict returned by _create_creds_dict()
    assert len(rs._create_creds_dict(os.environ['TEST_CREDS'])) == 5


def test_create_creds_dict_keys():
    # test whether proper keys are present in dict returned by _create_creds_dict()
    keys = ['host', 'dbname', 'user', 'password', 'port']
    creds_dict = rs._create_creds_dict(os.environ['TEST_CREDS'])
    assert all(key in creds_dict for key in keys)
