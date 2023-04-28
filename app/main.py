import base64
import secrets
from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException
from fastapi.params import Query
from fastapi.responses import RedirectResponse, PlainTextResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

from settings import USERS, ADMIN, REDIRECT, CONFIGS
from utils import hash_str

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
    return '\n'.join(f"{name} - {hash_str(uuid)}" for name, uuid in USERS)


@app.get("/{sub_hash}", response_class=PlainTextResponse)
async def get_sub(sub_hash: str, raw: bool = Query(False)):
    possible_users = [(name, uuid) for name, uuid in USERS if hash_str(uuid) == sub_hash]
    if len(possible_users) == 0:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    name, uuid = possible_users[0]
    links = []
    for config in CONFIGS:
        links.append(config.get(uuid))

    text = '\n'.join(links)
    if raw:
        return text
    else:
        return base64.b64encode(text.encode('ascii'))
