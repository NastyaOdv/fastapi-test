import typing
from fastapi_keycloak_middleware import KeycloakConfiguration

from src.models.authConfiguration import User

keycloak_config = KeycloakConfiguration(
    url="http://localhost:8080/auth/",
    realm="myrealm",
    client_id="my-client",
    client_secret="QGptUew9wbyus5I3aw323Q2I9yfr4zVm",
    admin_client_secret="FS8fNlxTipXYRjhpJax2lVPEx928H18i",
    # callback_uri="http://localhost:5000/callback",
    claims=["sub", "name", "email"],
    reject_on_missing_claim=False,
    # authorization_url="http://localhost:8080/realms/myrealm/protocol/openid-connect/auth",
    # token_url="http://localhost:8080/realms/myrealm/protocol/openid-connect/token",
)


async def map_user(userinfo: typing.Dict[str, typing.Any]) -> User:
    id = userinfo.get('sub')
    username = userinfo.get('preferred_username')
    email = userinfo.get('email')

    # Creating a User instance
    user = User(
        id=id,
        username=username,
        email=email
    )
    return user
