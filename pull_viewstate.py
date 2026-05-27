#!/usr/bin/python3
import requests
import re
import base64
import sys

target = sys.argv[1]
#pattern = 'name=\"__VIEWSTATE\" value=\"(?P<viewstate_b64>[a-zA-Z0-9+\=\_\/])\"'
pattern = r'id="__VIEWSTATE"\svalue="(?P<viewstate_b64>[a-zA-Z0-9+=_/]{3,128})"'


resp = requests.get(f'http://{target}:80/test.aspx')
#Regex match to search for base64 encoded VIEWSTATE string
match = re.search(pattern, resp.text)

if match:
    viewstate_dict = match.groupdict()
    if viewstate_dict['viewstate_b64']:
        viewstate_data = viewstate_dict['viewstate_b64']
    print(f"ViewState: {viewstate_data}")

