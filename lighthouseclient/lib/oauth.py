import asyncio
from base64 import b64encode
from json.decoder import JSONDecodeError

import requests

from lighthouseclient import sio
from lighthouseclient.lib.exceptions import AuthenticationException


class OAuthClient:
    def __init__(self, root_url, client_id, client_secret):
        self.root_url = root_url
        self.encoded_creds = b64encode(
            f"{client_id}:{client_secret}".encode()
        ).decode('utf-8')

    async def get_new_access_token(self, expiration_callback=None):
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
            response = response.json()
        except (JSONDecodeError, KeyError):
            raise AuthenticationException()

        if expiration_callback:
            sio.start_background_task(
                self.schedule_refresh, response['expires_in'],
                expiration_callback
            )

        return response['access_token']

    async def schedule_refresh(self, expires_in, callback):
        await asyncio.sleep(max(expires_in - 60, 0))
        await callback(await self.get_new_access_token(callback))
