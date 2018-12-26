#!/usr/bin/env python3
import responses
import requests
from r_u_done_yet_syncthing import check_db_completion

def test_check_db_completion():
    assert check_db_completion() == True

def test_check_db_completion_fail():
    assert check_db_completion() == False
