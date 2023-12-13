import os
import ocs
import pytest

from unittest.mock import MagicMock
from ocs.ocs_agent import OpSession
from ocs.ocs_client import OCSReply

from sorunlib._internal import check_response, check_running

os.environ["OCS_CONFIG_DIR"] = "./test_util/"


def create_session(op_name, status=None, success=None):
    """Create an OpSession with a mocked app for testing."""
    mock_app = MagicMock()
    session = OpSession(1, op_name, app=mock_app)
    session.op_name = 'test_op'
    if status is not None:
        session.set_status(status)
    session.success = success

    return session.encoded()


# Very partial mock as we only need the instance_id to exist.
class MockClient:
    def __init__(self):
        self.instance_id = 'test-id'


invalid_responses = [(MockClient(), OCSReply(ocs.TIMEOUT,
                                             'msg',
                                             create_session('test', success=True))),
                     (MockClient(), OCSReply(ocs.ERROR,
                                             'msg',
                                             create_session('test', success=False)))]

valid_responses = [
    (MockClient(), OCSReply(ocs.OK, 'msg', create_session('test', success=True)))]

invalid_running_responses = [
    (MockClient(), OCSReply(ocs.OK, 'msg', create_session('test')))]

running_responses = [
    (MockClient(), OCSReply(ocs.OK, 'msg', create_session('test', status='running')))]


@pytest.mark.parametrize("client,response", invalid_responses)
def test_check_response_raises(client, response):
    with pytest.raises(RuntimeError):
        check_response(client, response)


@pytest.mark.parametrize("client,response", valid_responses)
def test_check_response(client, response):
    check_response(client, response)


@pytest.mark.parametrize("client,response", invalid_running_responses)
def test_check_running_raises(client, response):
    with pytest.raises(RuntimeError):
        check_running(client, response)


@pytest.mark.parametrize("client,response", running_responses)
def test_check_running(client, response):
    check_running(client, response)
