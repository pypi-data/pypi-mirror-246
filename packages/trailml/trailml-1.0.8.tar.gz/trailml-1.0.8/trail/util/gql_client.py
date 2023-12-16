from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport

from trail.libconfig import libconfig
from trail.util import auth


def build_gql_client(auth_token: str = None):
    if auth_token is None:
        auth_token = auth.retrieve_id_token()
    transport = AIOHTTPTransport(
        libconfig.gql_endpoint_url,
        headers={"authorization": f"Bearer {auth_token}"}
    )
    return Client(transport=transport)
