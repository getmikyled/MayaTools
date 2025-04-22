import requests
from requests.auth import HTTPBasicAuth

# TeamGantt Token
client_id = '23c6d10e-fd7c-4e6b-bd0f-0d78410cb263'
client_secret = 'DG0LAmIC7U/mqkL8iPiOPmtJltU6dRGex8xIiVg1ewGM716Q7jTuhJFswWdoU/YG'

# Token Authentication URL
auth_url = 'https://auth.teamgantt.com/oauth2/token'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

data = {
    'grant_type': 'password',
    'username': 'mikyle.mosquera@sjsu.edu',
    'password': '27972kNX'
}

response = requests.post(auth_url, data=data, auth=HTTPBasicAuth(client_id, client_secret), headers=headers)

if response.ok:
    print('Access Token', response.json()['access_token'])
else:
    print(f'Error: {response.status_code}')
    print(response.text)


