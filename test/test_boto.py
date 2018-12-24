# TODO: write boto creds tests
import boto3
from ..nordata import _boto as bt


def test_boto_create_session_type():
    # test whether _create_session() returns the proper type
    assert isinstance(bt.boto_create_session(), boto3.session.Session)