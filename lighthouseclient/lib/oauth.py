from base64 import b64encode
from json.decoder import JSONDecodeError

import requests

from lighthouseclient.lib.exceptions import AuthenticationException


class OAuthClient:
    def __init__(self, root_url, client_id, client_secret):
        self.root_url = root_url
        self.encoded_creds = b64encode(
            f"{client_id}:{client_secret}".encode()
        ).decode('utf-8')

    def get_new_access_token(self):
        response = requests.post(
            f"{self.root_url}/oauth/token",
            headers={
                'Authorization': f"Basic {self.encoded_creds}"
            },
            json={
                'grant_type': 'client_credentials'
            }
        )
        try:
            return response.json()['access_token']
        except (JSONDecodeError, KeyError):
            raise AuthenticationException()
