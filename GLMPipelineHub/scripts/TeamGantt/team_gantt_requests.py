import requests
from requests.auth import HTTPBasicAuth

# TeamGantt Token
client_id = '23c6d10e-fd7c-4e6b-bd0f-0d78410cb263'
client_secret = 'DG0LAmIC7U/mqkL8iPiOPmtJltU6dRGex8xIiVg1ewGM716Q7jTuhJFswWdoU/YG'
token = 'eyJraWQiOiJtRVNwOVFJUzNBMVluQWJVUXFaUHZWZjM1Rk5PZGlLeTNWSFFRbTRNR0prPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI0YzUxMTc3ZS00NDNkLTQ4NGUtYTdkZi0yMDNkMWEzNTJjOTgiLCJldmVudF9pZCI6ImFjOWM4NDBhLWIxOGItNGI0OC05NDQ5LTdlZDdlMDY5OGM0ZCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3NDUyODQ5OTksImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTIuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0yX1FIejQzMzhJbSIsImV4cCI6MTc0NTI4ODU5OSwiaWF0IjoxNzQ1Mjg0OTk5LCJqdGkiOiIxMTA5OTAzZC1hN2JiLTQ5ZWEtOTgwZC04YjlkOWU3ZTA5NjYiLCJjbGllbnRfaWQiOiI1ZXBkZzVrb2hsOHR0b21qNmtjZThydWNqZCIsInVzZXJuYW1lIjoiNGM1MTE3N2UtNDQzZC00ODRlLWE3ZGYtMjAzZDFhMzUyYzk4In0.I4er46IlbaLx0gUeu-FaN27y2W8DrNxmFzpLtq4ZwncX_asdaM7vwuDandy3yUaR0BJX_a3Ejj70qlTPoLiqvbLSoNaED_V2Iq6_WRWGZ0AN5o9NysEB7i3VzY9srVJSPYOUmErCMwDOdCVlwoQudynYtNo-bk9TaovqJTTPSig-0wrIAMIXErDOxVdBUIVf6J1XZCON8f36bg2tVfX1leKEoXT1TYOSqK-KusMLgq67ATw6IjvDQ-Q2bPAPPWABMI0DNrxTEF1Ki-j0xPsLKn-zDaINJ517COkrqdJCw9yyM72b9Vswhp9uidN3hO9qOjIH1ghpmmduNUmGYV8W6Q'

# token_header

def request_token(username, password):
    """Prints the requested token or an error if the request fails. Returns the response."""
    auth_url = 'https://auth.teamgantt.com/oauth2/token'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'password',
        'username': username,
        'password': password
    }

    response = requests.post(auth_url, data=data, auth=HTTPBasicAuth(client_id, client_secret), headers=headers)

    if response.ok:
        print('Access Token', response.json()['access_token'])
    else:
        print(f'Error: {response.status_code}')
        print(response.text)

    return response

def request_users():
    url = 'https://api.teamgantt.com/v1/companies/VFX EDU/users'

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)

    if response.ok:
        users = response.json()
        for user in users:
            print(f'{user["first_name"]} {user["last_name"]}')
    else:
        print(f'Error: {response.status_code}')
        print(response.text)

    return response

def request_get_task(id):
    url = f'https://api.teamgantt.com/v1/tasks/{id}'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.ok:
        print(response.json())
    else:
        print(f'Error: {response.status_code}')
        print(response.text)

request_get_task(4210843)