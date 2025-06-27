from fastapi import APIRouter

import logging
from typing import *

from slinkieforumsserver import database
from slinkieforumsserver.api import *

from fastapi import Response, Header, Body, HTTPException, Depends
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/token/isvalid")
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


@router.post("/token/refresh")
def refresh_token(token: str = Body()):
    """
        When used, invalidates the current token and then returns a brand new one.\n
        The new token will be associated with a "use" count (how long the current renew chain is), when it
        reaches it's limit, the backend will deny creating any refresh attemps.
    """
    return "no."


@router.post("/token/acquire")
async def aquire_token(password: str = Body(), username: str|None = Body(None), userID: int|None = Body(None)):
    """
        logs the user in.
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
    
#@app.post("/account")
#async def aquire_token(password: str = Body(), username: str = Body(), email: str = Body()):
#    re.match(r".{16,}",password)
#    re.match(r"[a-z]",password)
#    re.match(r"[A-Z]",password)
#    re.match(r"[0-9]",password)
#    re.match(r"[a-zA-Z0-9!@#%^&*()_+=[]{};:\|,.<>?]", password)
#    re.match(r"[\"']",password)

        
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
    
    
type Token = Annotated[tuple[bool, TokenHeader], Depends(soft_require_token)]
type RequireToken = Annotated[TokenHeader, Depends(strict_require_token)]

@router.get("/category/")
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
        
        
@router.get("/category/{id}")
async def fetch_threads_in_category(id: int, offset: int = Header(0), pageSize: int = Header(20)):
    with database.Session() as session:
        try: 
            threads_json = [
                {
                    "id":thread.id,
                    "title": thread.title,
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

@router.post("/thread")
async def make_thread(token: RequireToken, category: int = Body(), title: str = Body(), data: str = Body(), contentType: str = Body(), zipped: bool = Body(False), allowReplies: bool = Body(True), allowEdits: bool = Body(True)):
    if not has_perm(token["userID"], "makeThreads"):
        return HTTPException(status_code=401, detail="User lacks required Credentials.")
    
    try:
        with database.Session() as session:
            content = Content(contentType, base64.b64decode(data), token["userID"], zipped)
            session.add(content)
            session.commit()
            
            thread = Thread(token["userID"], title, content.id, category, allowReplies=allowReplies, allowEdits=allowEdits)
            session.add(thread)
            session.commit()
                
    except Exception as e:
        print(traceback.format_exc())
        session.rollback()
        return HTTPException(status_code=500, detail=str(e))
    
            
@router.get("/thread/{id}")
async def get_thread(id: int, token: Token):    
    with database.Session() as session:
        try:
            thread = session.query(database.Thread).where(database.Thread.id == int(id)).first()
            if thread is None:
                return HTTPException(status_code=404, detail="Thread Not found.")
            
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
                    "title": thread.title,
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


@router.get("/thread/{id}/replies")
async def fetch_replies_from_thread(id: int, token: Token):
    with database.Session() as session:
        try:
            return JSONResponse(
                content = [
                    {
                        "id": reply.id,
                        "body": reply.body,
                        "data": reply.date,
                        "author": reply.authorID,
                        "history": reply.history,
                        "allowEdits": reply.allowEdits,
                        "allowReplies": reply.allowReplies,
                        "deletionDate": reply.deletionDate,
                        "children": [child.id for child in session.query(database.Reply).where(database.Reply.parentID == reply.id).all()]
                    }
                    for reply in session.query(database.Reply).where(database.Reply.threadID == id).all()
                ]
            )
            
        except Exception as e:
            print(traceback.format_exc())
            return HTTPException(status_code=500, detail=str(e))


@router.get("/reply/{id}")
async def fetch_reply(id: int, token: Token):
    with database.Session() as session:
        try:
            reply = session.query(database.Reply).where(database.Reply.id == id).first()
            if reply is None:
                return HTTPException(status_code=404, detail="Reply Not found.")
            
            return JSONResponse(
                content = {
                    "id": reply.id,
                    "body": reply.body,
                    "data": reply.date,
                    "author": reply.authorID,
                    "history": reply.history,
                    "allowEdits": reply.allowEdits,
                    "allowReplies": reply.allowReplies,
                    "deletionDate": reply.deletionDate,
                    "children": [child.id for child in session.query(database.Reply).where(database.Reply.parentID == reply.id).all()]
                }
            )
            
        except Exception as e:
            print(traceback.format_exc())
            return HTTPException(status_code=500, detail=str(e))


@router.post("/reply")
async def make_reply(token: RequireToken, threadID:int = Body(), parentID: int|None = Body(None), data: str = Body(), contentType: str = Body(), zipped: bool = Body(False), allowReplies: bool = Body(True), allowEdits: bool = Body(True)):
    with database.Session() as session:
        try:
            body = Content(contentType, base64.b64decode(data), token["userID"], zipped)
            session.add(body)
            session.commit()
            reply = Reply(token["userID"], parentID, threadID, body.id, allowEdits = allowEdits, allowReplies = allowReplies)
            session.add(reply)
            session.commit()
        except Exception as e:
            print(traceback.format_exc())
            return HTTPException(status_code=500, detail=str(e))


@router.get("/content/{id}")
async def get_content(id:int, token: Token): 
    with database.Session() as session:
        try:
            content = session.query(database.Content).where(database.Content.id == int(id)).first()
            if content == None:
                return HTTPException(status_code=404, detail="Couldn't find content in database")
            
            return Response(
                status_code=200,
                media_type=content.contentType,
                content=content.data
            )
            
        except Exception as e:
                print(traceback.format_exc())
                return HTTPException(status_code=500, detail=str(e))


@router.post("/content/")
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
#app.delete("/thread/{id}")
#app.delete("/reply/{id}")

## </token required>

## <admin required>

"""
    delete content entry in DB
"""
@router.delete("/admin/content")
def fetch_content(): pass


"""
    edit content entry in DB
"""
@router.patch("/admin/content")
def fetch_content(): pass


"""
    sets suspencion date.
"""
@router.patch("/admin/manage")
def fetch_content(): pass

## </admin required>