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


"""
    logs the user in.
"""
@app.get("/token/acquire")
async def aquire_token(request: Request):
    data = await Request.json()
    

"""
    creates a new account
"""
@app.get("/users/make")
async def aquire_token(request: Request):
    data = await Request.json()
    

## <token required>

"""
    follows/blocks a user
"""
@app.get("/users/relationships")
async def aquire_token(request: Request):
    data = await Request.json()


"""
    Returns base64 binary data to whatever content object matches the ID
"""
@app.get("/content/get/{id}")
def fetch_content(): pass


"""
    Returns all categories in the database
"""
@app.get("/content/categories")
def fetch_content(): pass


"""
    Returns data about a thread by ID.
"""
@app.get("/content/thread/get/{id}")
def fetch_content(): pass


"""
    Returns all replies of a thread
"""
@app.get("/content/thread/getReplies/{id}")
def fetch_content(): pass


"""
    makes a thread
"""
@app.get("/content/thread/make")
def fetch_content(): pass


"""
    makes a reply to a thread/reply by ID.
    If a reply is specified, the ThreadID will match the parent reply's ThreadID. 
"""
@app.get("/content/reply/make")
def fetch_content(): pass

"""
    soft-deletes a thread/reply/quote, by ID.
"""
@app.get("/content/delete")
def fetch_content(): pass

"""
    takes in b64 encoded data and uploads a content entry to the database
"""
@app.get("/content/upload")
def fetch_content(): pass

## </token required>

## <admin required>

"""
    delete content entry in DB
"""
@app.get("/admin/content/delete")
def fetch_content(): pass


"""
    edit content entry in DB
"""
@app.get("/admin/content/edit")
def fetch_content(): pass


"""
    sets suspencion date.
"""
@app.get("/admin/users/ban")
def fetch_content(): pass

## </admin required>
