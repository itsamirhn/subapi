import base64
import secrets
from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse, PlainTextResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

from settings import USERS, ADMIN, REDIRECT
from utils import generate_all_links, hash_uuid

app = FastAPI(docs_url=None)
security = HTTPBasic()


def admin_auth(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    current_username_bytes = credentials.username.encode('utf8')
    is_correct_username = secrets.compare_digest(current_username_bytes, ADMIN[0])
    current_password_bytes = credentials.password.encode('utf8')
    is_correct_password = secrets.compare_digest(current_password_bytes, ADMIN[1])
    if not (is_correct_username and is_correct_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return credentials


@app.get("/", response_class=RedirectResponse)
async def root():
    return REDIRECT


@app.get("/users", response_class=PlainTextResponse)
async def list_users(_: Annotated[HTTPBasicCredentials, Depends(admin_auth)]):
    return '\n'.join(f"{name} - {hash_uuid(uuid)}" for name, uuid in USERS)


@app.get("/{sub_hash}", response_class=PlainTextResponse)
async def get_sub(sub_hash: str):
    possible_users = [user for user in USERS if hash_uuid(user[1]) == sub_hash]
    if len(possible_users) == 0:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    user = possible_users[0]
    return base64.b64encode('\n'.join(generate_all_links(user[1])).encode('ascii'))
