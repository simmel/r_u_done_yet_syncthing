#!/usr/bin/env python3
# vim: set fileencoding=utf-8 sw=4 et tw=79
#https://forum.syncthing.net/t/how-can-i-check-a-progress-of-a-synchronization-on-a-given-host-from-a-server-side-syncthing-cli/8705
#https://docs.syncthing.net/rest/stats-device-get.html
#https://docs.syncthing.net/rest/db-completion-get.html
import requests
from requests.exceptions import ConnectionError

def check_db_completion():
    headers = {'X-API-Key': '1337'}
    try:
        requests.get(
                'http://localhost:8384/rest/db/completion',
                headers=headers,
                )
    except ConnectionError:
        return False
    return True

def main():
    print("Are you done yet Syncthing?")

if __name__ == "__main__":
    main()
