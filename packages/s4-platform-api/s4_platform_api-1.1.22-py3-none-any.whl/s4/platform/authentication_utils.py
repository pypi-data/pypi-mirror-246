import logging

import requests
from requests.exceptions import HTTPError


log = logging.getLogger(__name__)


def get_auth_token(
    auth0_domain: str, auth0_audience: str, client_id: str, client_secret: str
) -> str:
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": auth0_audience,
    }
    auth_url = f"https://{auth0_domain}/oauth/token"
    response = requests.post(auth_url, data, headers)

    try:
        response.raise_for_status()
    except HTTPError as ex:
        log.error(f"Could not retrieve auth token from {auth_url}")
        raise ex

    auth = response.json()
    return auth["access_token"]
