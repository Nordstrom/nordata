import os
import pytest
from ..nordata import _redshift as rs


os.environ['TEST_CREDS'] = 'host=my_hostname dbname=my_dbname user=my_user password=my_password port=1234'


def test_read_sql_type_error():
    # test whether read_sql() raises the proper error
    with pytest.raises(TypeError):
        rs.read_sql(1)


def test_read_sql_return_type():
    # test type returned by read_sql()
    assert isinstance(rs.read_sql('test/test.sql'), str)


def test_read_sql_contents():
    # test whether contents of str returned by read_sql() are correct
    test_str = "select\n     col1\n     col2\n from\n     pretend.first_table\n limit\n     1000;"
    assert rs.read_sql('test/test.sql') == test_str


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
