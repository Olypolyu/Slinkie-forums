from typing import *
from fastapi import FastAPI, Request
from datetime import datetime, timedelta

app = FastAPI()

@app.get("/token/isvalid")
def isvalid_token(token: str):
    """returns whether a token is valid and then it expires/expired."""
    print(token)
    return {
        "validity": True,
        "expirationDate": (datetime.now() + timedelta(days=7)).timestamp()
    }
    
@app.get("/token/refresh")
def refresh_token(token: str):
    """
        When used, invalidates the current token and then returns a brand new one.\n
        The new token will be associated with a "use" count (how long the current renew chain is), when it
        reaches it's limit, the backend will deny creating any refresh attemps.
    """
    return "no."

@app.get("/token/acquire")
async def aquire_token(request: Request):
    data = await Request.json()
    