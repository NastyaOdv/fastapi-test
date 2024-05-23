import os

import typing

from fastapi_keycloak_middleware import KeycloakConfiguration, setup_keycloak_middleware, get_user
from starlette.middleware.cors import CORSMiddleware

from src.models.authConfiguration import User
from src.models.logger import logger
from src.routes import audio_2_text
from fastapi import FastAPI, Depends

from src.routes.authentication import get_user_info

app = FastAPI(
    title=os.getenv("APP_NAME", "My API"),
    version=os.getenv("VERSION", "1.0.0")
)
# keycloak_config = KeycloakConfiguration(
#     url="http://localhost:8080",
#     realm="myrealm",
#     client_id="my-client",
#     client_secret="QGptUew9wbyus5I3aw323Q2I9yfr4zVm",
#     admin_client_secret="FS8fNlxTipXYRjhpJax2lVPEx928H18i",
#     # callback_uri="http://localhost:5000/callback",
#     claims=["sub", "name", "email"],
#     reject_on_missing_claim=False,
# )


# async def map_user(userinfo: typing.Dict[str, typing.Any]) -> User:
#     id = userinfo.get('sub')
#     username = userinfo.get('preferred_username')
#     email = userinfo.get('email')
#
#     # Creating a User instance
#     user = User(
#         id=id,
#         username=username,
#         email=email
#     )
#     return user


# setup_keycloak_middleware(
#     app,
#     keycloak_configuration=keycloak_config,
#     user_mapper=map_user
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

logger.info('API is starting up')

app.include_router(audio_2_text.router)


# @app.get("/")
# async def root(user: User = Depends(get_user)):
#     return {"message": "Hello World"}
# error:
# {
#     "detail": "An error occurred: AuthClaimMissing"
# }


# @app.get("/user")  # Requires logged in
# def current_users(authorization_result: AuthorizationResult = Depends(get_authorization_result), ):
#     return authorization_result


# @app.get("/callback")
# def callback(session_state: str, code: str):
#     return keycloak_config.exchange_authorization_code(session_state=session_state,
#                                                        code=code)  # This will return an access token


@app.get("/secure")
async def root(user: User = Depends(get_user_info)):
    return {"message": f"Hello {user.username}  with email: {user.email}"}
