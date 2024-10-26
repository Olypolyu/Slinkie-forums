from typing import *
from fastapi import FastAPI, Request, Response, Header, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from .api import *
from . import database
import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/token/isvalid")
async def isvalid_token(token: Annotated[str, Header()] ):
    """returns whether a token is valid."""
    
    try:
        logging.debug("Validating token.")
        token = json.loads(token)
        validity, _ = validate_token(token)
        
        return Response(status_code=200 if validity else 401)
    except:
        logging.error(traceback.format_exc())
        return Response(status_code=400)


@app.get("/token/refresh")
def refresh_token(token: str):
    """
        When used, invalidates the current token and then returns a brand new one.\n
        The new token will be associated with a "use" count (how long the current renew chain is), when it
        reaches it's limit, the backend will deny creating any refresh attemps.
    """
    return "no."


@app.post("/token/acquire")
async def aquire_token(request: Request):
    """
        logs the user in.
        
        Payload:
        {
            "userID: int|None
            "username":str|None,
            "password":str
        }
        
        Response:
        {
            Token: str|None
            error: str
        }
    """
    try:
        data = await request.json()
        result = login(data.get("password"), data.get("userID"), data.get("username"))
        return JSONResponse(
            status_code=200 if result[0] else 401,
            content={
                "token":result[1],
                "error": "" if result[2] == None else result[2]
            }
        )
    except:
        logging.error(traceback.format_exc())
        return Response(status_code=400)
    
        
        
async def strict_require_token(token: str = Header()):
    """
        Will not let you in unless you have a valid token.
    """
    try:
        result, header = validate_token(json.loads(token))
        if result: return header
        raise HTTPException(status_code=401, detail="Attempted to access resource with invalid Token.")
    except: 
        raise HTTPException(status_code=400, detail="Something went wrong.")


async def require_token(token: str = Header()):
    """
        Will pass the result of the query+header forward. The endpoint can decide what to do from there.
    """
    try: return validate_token(json.loads(token))
    except: return False, None
    
RequireToken = Annotated[tuple[bool, TokenHeader], Depends(require_token)]
    
    
    
"""
creates a new account
"""
@app.get("/users/make")
async def aquire_token(request: Request):
    data = await Request.json()
    

@app.get("/category/")
async def fetch_categories():
    with database.Session() as session:
        try:
            categories = [   
                {
                "id": category.id,
                "title":category.title,
                "icon": category.icon,
                "description": category.description
                }
                for category in session.query(database.Category).limit(50).all()
            ]
            
            return JSONResponse(
                status_code=200,
                content=categories,
            )
        except:
            return HTTPException(status_code=500, detail="Something went wrong.")
        
        
@app.get("/category/{id}")
async def fetch_threads_in_category(id: int, offset: int = Header(0), pageSize: int = Header(20)):
    with database.Session() as session:
        try: 
            threads_json = [
                {
                    "id":thread.id,
                    "body": thread.body,
                    "metrics": {
                        "replies": session.query(Reply).where(Reply.threadID == thread.id).count(),
                        "lastReply": session.query(Reply).where(Reply.threadID == thread.id).order_by(desc(Reply.date)).first(),
                    }
                }
                
                for thread in session.query(Thread).where(Thread.categoryID == id).offset(offset).limit(pageSize).all()
            ]
            print(threads_json)
            session.close()
            return JSONResponse(
                status_code=200,
                content=threads_json,
            )
            
        except:
            print(traceback.format_exc())
            return HTTPException(status_code=500, detail="Something went wrong.")


## <token required>

app.get("/thread/{id}")
async def get_content(id:int, token: RequireToken):    
    with database.Session() as session:
        try:
            thread = session.query(database.Thread).where(database.Thread.id == int(id)).first()
            
            if (thread.display == database.DISPLAY_ENUM.only_authors):
                if not token[0]:
                    return Response(status_code=401)
                
                elif json.loads(token[1])["userID"] not in thread.listAuthorID:
                    return Response(status_code=401)
                
            return JSONResponse(
                status_code=200,
                content = {
                    "id":thread.id,
                    "body": thread.body,
                    "date": thread.date,
                    "metrics": {
                        "replies": session.query(Reply).where(Reply.threadID == thread.id).count(),
                        "lastReply": session.query(Reply).where(Reply.threadID == thread.id).order_by(desc(Reply.date)).first(),
                    }
                }
            )
        except Exception as e:
            return HTTPException(status_code=500, detail=str(e))
        

#app.delete("/content/{id}")
#app.post("/content/{id}")
#app.get("/content/{id}")
#
#app.delete("/thread/{id}")
#app.post("/thread/{id}")
#app.get("/thread/{id}")
#
#app.delete("/reply/{id}")
#app.post("/reply/{id}")
#app.get("/reply/{id}")

## </token required>

## <admin required>

"""
    delete content entry in DB
"""
@app.delete("/admin/content")
def fetch_content(): pass


"""
    edit content entry in DB
"""
@app.patch("/admin/content")
def fetch_content(): pass


"""
    sets suspencion date.
"""
@app.patch("/admin/manage")
def fetch_content(): pass

## </admin required>

