#!/usr/bin/python3
import requests
import re
import base64
import sys

target = sys.argv[1]
#pattern = 'name=\"__VIEWSTATE\" value=\"(?P<viewstate_b64>[a-zA-Z0-9+\=\_\/])\"'
viewstate_pattern = r'id="__VIEWSTATE"\svalue="(?P<viewstate_b64>[a-zA-Z0-9+=_/]{3,128})"'
generator_pattern = r'id="__VIEWSTATEGENERATOR"\svalue="(?P<generator_hex>[a-fA-F0-9]{8})"'

resp = requests.get(f'http://{target}:80/test.aspx')
#Regex match to search for base64 encoded VIEWSTATE string
viewstate_match = re.search(viewstate_pattern, resp.text)
generator_match = re.search(generator_pattern, resp.text)
if viewstate_match and generator_match:
    viewstate_dict = viewstate_match.groupdict()
    generator_dict = generator_match.groupdict()
    if viewstate_dict['viewstate_b64']:
        viewstate_data = viewstate_dict['viewstate_b64']
    if generator_dict['generator_hex']:
        generator_data = generator_dict['generator_hex']
    
    print(f"ViewState: {viewstate_data} , Generator: {generator_data}")

