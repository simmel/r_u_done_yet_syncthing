#!/usr/bin/env python3
# vim: set fileencoding=utf-8 sw=4 et tw=79
import pytest
import requests
import responses
import r_u_done_yet_syncthing as rudys

url_db_completion = 'http://localhost:8384/rest/db/completion'

@responses.activate
def test_check_db_completion():
    responses.add(responses.GET, url_db_completion)
    assert rudys.check_db_completion() == True

@responses.activate
def test_check_db_completion_api_down():
    responses.add(responses.GET, url_db_completion,
                  body=ConnectionError('...'))
    # https://github.com/getsentry/responses/issues/72
    # Sadly all exceptions are swallowed so we can't see that it returns False
    with pytest.raises(ConnectionError):
        rudys.check_db_completion()

@responses.activate
def test_check_db_completion_uses_auth(mocker):
    mocker.patch('r_u_done_yet_syncthing.API_KEY', '1337')
    responses.add(responses.GET, url_db_completion)
    assert rudys.check_db_completion() == True
    assert responses.calls[0].request.headers['X-API-Key'] == '1337'

@responses.activate
def test_get_folders_and_devices(mocker):
    mocker.patch('r_u_done_yet_syncthing.API_KEY', '1337')
    responses.add(
            responses.GET,
            'http://localhost:8384/rest/system/config',
            )
    assert rudys.get_folders_and_devices() == []
