#!/usr/bin/env python3
# vim: set fileencoding=utf-8 sw=4 et tw=79
import pytest
import requests
import responses
import r_u_done_yet_syncthing as rudys
from urllib.parse import urlencode

url_db_completion = 'http://localhost:8384/rest/db/completion'
db_completion_params = {
        'device': 'JGWHCJ5-TBCPDOH-VYSIO3N-GPAQS6Y-YTS5Q5N-NJCDC2U-4SIMPFQ-TFJFQAS',
        'folder': 'Documents',
        }
db_completion_response = {
        "completion": 100,
        "globalBytes": 1337,
        "needBytes": 0,
        "needDeletes": 0,
        "needItems": 0
        }

@responses.activate
def test_check_db_completion():
    responses.add(responses.GET, '{}?{}'.format(url_db_completion, urlencode(db_completion_params)),
            json=db_completion_response)
    assert rudys.check_db_completion(deviceID=db_completion_params['device'], folder=db_completion_params['folder']) == True

@responses.activate
def test_check_db_completion_negative():
    db_completion_response_negative = db_completion_response.copy()
    db_completion_response_negative['completion'] = 99
    responses.add(responses.GET, '{}?{}'.format(url_db_completion, urlencode(db_completion_params)),
            json=db_completion_response_negative)
    assert rudys.check_db_completion(deviceID=db_completion_params['device'], folder=db_completion_params['folder']) == False

@responses.activate
def test_check_db_completion_api_down():
    responses.add(responses.GET, '{}?{}'.format(url_db_completion, urlencode(db_completion_params)),
                  body=ConnectionError('...'))
    # https://github.com/getsentry/responses/issues/72
    # Sadly all exceptions are swallowed so we can't see that it returns False
    with pytest.raises(ConnectionError):
        rudys.check_db_completion(deviceID=db_completion_params['device'], folder=db_completion_params['folder'])

@responses.activate
def test_check_db_completion_uses_auth(mocker):
    mocker.patch('r_u_done_yet_syncthing.API_KEY', '1337')
    responses.add(responses.GET, '{}?{}'.format(url_db_completion, urlencode(db_completion_params)),
            json=db_completion_response)
    assert rudys.check_db_completion(deviceID=db_completion_params['device'], folder=db_completion_params['folder']) == True
    assert responses.calls[0].request.headers['X-API-Key'] == '1337'

@responses.activate
def test_get_folders_and_devices(mocker):
    mocker.patch('r_u_done_yet_syncthing.API_KEY', '1337')
    mock_our_syncthing_id = "TOTALLY-US"
    mock_system_config_folders = [
            {
                "id": "Documents",
                "path": "/path/to/Documents",
                "devices": [
                    {
                        "deviceID": "SOMONE-ELSE",
                        "introducedBy": ""
                        },
                    {
                        "deviceID": mock_our_syncthing_id,
                        "introducedBy": ""
                        }
                    ],
                },
            {
                "id": "Pictures",
                "path": "/path/to/Pictures",
                "devices": [
                    {
                        "deviceID": "SOMONE-ELSE",
                        "introducedBy": ""
                        },
                    {
                        "deviceID": mock_our_syncthing_id,
                        "introducedBy": ""
                        }
                    ],
                },
            ]
    mock_folders = [
            {
                "id": "Documents",
                "path": "/path/to/Documents",
                "devices": [
                    {
                        "deviceID": "SOMONE-ELSE",
                        "introducedBy": ""
                        },
                    ],
                },
            {
                "id": "Pictures",
                "path": "/path/to/Pictures",
                "devices": [
                    {
                        "deviceID": "SOMONE-ELSE",
                        "introducedBy": ""
                        },
                    ],
                },
            ]
    mock_system_config = {
            "version": 28,
            "folders": mock_folders,
            }

    responses.add(
            responses.GET,
            'http://localhost:8384/rest/system/config',
            json=mock_system_config,
            headers={
                'X-Syncthing-Id': mock_our_syncthing_id,
                }
            )
    assert rudys.get_folders_and_devices() == mock_folders

@responses.activate
def test_device_lastseen():
    import datetime
    mocked_device_stats = {
            '42VHOQQ-7U7TMW2-ZSCBSZN-G53FPXS-NHXRWVX-AQBPVXQ-VX5BLKO-YB6JJQW': {
                'lastSeen': '1970-01-01T00:00:00Z',
                'returns': False,
                },
            'I2FVSQQ-5I3FBXY-OBBUNP6-QKJOVVS-WSYNS3G-MNSQENV-SK2IINT-7IWJ3AH': {
                'lastSeen': datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat(),
                'returns': True,
                },
            }
    for device in mocked_device_stats:
        responses.add(responses.GET, 'http://localhost:8384/rest/stats/device',
                json={device: {k: v for k, v in mocked_device_stats[device].items() if
                    k != 'returns' }})
    # This needs to be in two loops otherwise we will just get the first
    # response o_O
    for device in mocked_device_stats:
        assert rudys.check_device_lastseen(deviceID=device) == mocked_device_stats[device]['returns']
    assert len(responses.calls) == 2
