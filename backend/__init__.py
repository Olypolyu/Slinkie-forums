from typing import *
from fastapi import FastAPI, Request, Response, Header, Body, HTTPException, Depends
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
async def aquire_token(password: str = Body(), userID: int|None = Body(None), username: str|None = Body(None)):
    """
        logs the user in.
        
        **Query:**
        ```
        {
            userID:   int|None,
            username: str|None,
            password: str
        }
        ```
        
        **Response:** ```
        {
            Token: str|None,
            error: str
        }```
    """
    
    try:
        result = login(password, userID, username)
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
    try: result, header = validate_token(json.loads(token))
    except: raise HTTPException(status_code=400, detail="Token Failed to parse.")
    if result: return header
    raise HTTPException(status_code=401, detail="Attempted to access resource with invalid Token.")


async def soft_require_token(token: str = Header(None)):
    """
        Will pass the result of the query+header forward. The endpoint can decide what to do from there.
    """
    if token == None: return False, None
    try: return validate_token(json.loads(token))
    except: return False, None
    
    
Token = Annotated[tuple[bool, TokenHeader], Depends(soft_require_token)]
RequireToken = Annotated[TokenHeader, Depends(strict_require_token)]
    

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
                    "date": thread.date,
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

@app.get("/thread/{id}")
async def get_thread(id: int, token: Token):    
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
            print(traceback.format_exc())
            return HTTPException(status_code=500, detail=str(e))
        
        
@app.get("/content/{id}")
async def get_content(id:int, token: Token): 
    with database.Session() as session:
        try:
            content = session.query(database.Content).where(database.Content.id == int(id)).first()
            if content == None:
                print("aaa")
                return HTTPException(status_code=404, detail="Couldn't find content in database")
            
            return Response(
                status_code=200,
                media_type=content.contentType,
                content=content.data
            )
            
        except Exception as e:
                print(traceback.format_exc())
                return HTTPException(status_code=500, detail=str(e))


@app.post("/content/")
async def post_content(token: RequireToken, contentType: str = Body("text/plain"), data: str = Body(), zipped: bool = Body(False)):
    """
        Uploads a content-shard to the database.
    """
    if not has_perm(token["userID"], "makeContent"):
        return HTTPException(status_code=401, detail="User lacks required Credentials.")
    
    with database.Session() as session:
        try:
            content = Content(contentType, base64.b64decode(data), token["userID"], zipped)
            session.add(content)
            session.commit()
            return JSONResponse(
                status_code=200,
                content={
                    "contentID": content.id
                }
            )

        except Exception as e:
            print(traceback.format_exc())
            session.rollback()
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

