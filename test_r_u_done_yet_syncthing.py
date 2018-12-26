#!/usr/bin/env python3
# vim: set fileencoding=utf-8 sw=4 et tw=79
import pytest
import requests
import responses
from r_u_done_yet_syncthing import check_db_completion

url_db_completion = 'http://localhost:8384/rest/db/completion'

@responses.activate
def test_check_db_completion():
    responses.add(responses.GET, url_db_completion)
    assert check_db_completion() == True

@responses.activate
def test_check_db_completion_api_down():
    responses.add(responses.GET, url_db_completion,
                  body=ConnectionError('...'))
    # https://github.com/getsentry/responses/issues/72
    # Sadly all exceptions are swallowed so we can't see that it returns False
    with pytest.raises(ConnectionError):
        check_db_completion()
