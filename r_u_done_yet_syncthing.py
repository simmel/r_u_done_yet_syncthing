#!/usr/bin/env python3
# vim: set fileencoding=utf-8 sw=4 et tw=79
#https://forum.syncthing.net/t/how-can-i-check-a-progress-of-a-synchronization-on-a-given-host-from-a-server-side-syncthing-cli/8705
#https://docs.syncthing.net/rest/stats-device-get.html
#https://docs.syncthing.net/rest/db-completion-get.html
import os.path
import requests
import xml.etree.ElementTree as ET
from requests.exceptions import ConnectionError

API_KEY = None

def get_api_key():
    tree = ET.parse(os.path.expanduser('~/.config/syncthing/config.xml'))
    api_key = tree.getroot().find('./gui/apikey').text
    return api_key

def get_folders_and_devices():
    headers = {'X-API-Key': API_KEY}
    r = requests.get(
            'http://localhost:8384/rest/system/config',
            headers=headers,
            )
    our_device_id = r.headers['X-Syncthing-Id']
    f = r.json()
    f = f['folders']
    folders = []
    for folder in f:
        a = {}
        if folder["devices"]:
            a["devices"] = list(
                    filter(
                        lambda d: d["deviceID"] != our_device_id,
                        folder["devices"],
                        )
                    )
        for k in ("id", "path"):
            a[k] = folder[k]
        folders.append(a)
    return folders

def check_db_completion():
    headers = {'X-API-Key': API_KEY}
    try:
        requests.get(
                'http://localhost:8384/rest/db/completion',
                headers=headers,
                )
    except ConnectionError:
        return False
    return True

def main():
    # Set API_KEY once
    global API_KEY
    API_KEY = get_api_key()
    print(get_folders_and_devices())
    print(check_db_completion())
    print("Are you done yet Syncthing?")

if __name__ == "__main__":
    main()
