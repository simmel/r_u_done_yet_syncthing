#!/usr/bin/env python3
#https://forum.syncthing.net/t/how-can-i-check-a-progress-of-a-synchronization-on-a-given-host-from-a-server-side-syncthing-cli/8705
#https://docs.syncthing.net/rest/stats-device-get.html
#https://docs.syncthing.net/rest/db-completion-get.html
import requests
from requests.exceptions import ConnectionError

def check_db_completion():
    try:
        requests.get('http://localhost:8384/rest/db/completion')
    except ConnectionError:
        return False
    return True

def main():
    print("Are you done yet Syncthing?")

if __name__ == "__main__":
    main()
