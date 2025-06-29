import typing

from slinkieforumsserver import models

from .database import User, Role, Content, Thread, Reply, UserRole
from . import database
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import base64
import json
import traceback
from hashlib import sha3_256
import secrets
from cryptography.fernet import Fernet
from typing import *
import logging

key = b'FHs4C3teBlPxMqak3bgPXcdTD6hIlb2whBnHz73QH2k='

"""
    Oauth tokens consist of a data packed header followed by a signature.
    We're calculating that signature by taking a sha3_256 hash of the header then encrypting it with our private key.
    If the hash of the header and the decrypted signature do not match, it means this token has been tampered with or is a forgery. 
"""

class TokenHeader(TypedDict):
    userID: str
    emittedOn: str
    expiry: int

class Token(TypedDict):
    header: TokenHeader
    signature: str

def create_token(user: User, valid_for = timedelta(days=14)):
    header = {
        "userID": user.id, # just for a test so i don't have to fetch a user from the db.
        "emittedOn": datetime.now().timestamp(),
        "expiry": (datetime.now() + valid_for).timestamp(),
    }
    
    hash = sha3_256(json.dumps(header).encode()).digest()
    signature = Fernet(key).encrypt(hash)
    token: Token = {
        "header": header,
        "signature": base64.b64encode(signature).decode()
    }
    
    return json.dumps(token)


def validate_token(token: Token):
    """
        Returns: is_valid: bool, valid_token_header: TokenHeader
    """
    try:
        header = token["header"]
        
        hash = sha3_256(json.dumps(header).encode()).digest()
        encrypted_signature = base64.b64decode(token["signature"])
        retrieved_hash = Fernet(key).decrypt(encrypted_signature)
        
        return retrieved_hash == hash and header["expiry"] > datetime.now().timestamp(), header
    except:
        logging.error(traceback.format_exc())
        return False, None
        
        
def login(password: str, user_id: int = None, username: str = None):
    session = database.Session()
    try:
        if user_id != None: 
            user: User = session.query(User).where(User.id == user_id).first()
        elif username != None:
            user: User = session.query(User).where(User.username == username).first()
            
        if user == None:
            session.close()
            return False, None, "No matching credentials were found."
        
        salt, account_hash = user.passwordHash.split(":")
        password_hash: str = sha3_256((salt+password).encode()).hexdigest()
        
        if password_hash == account_hash:
            user.lastLogin = datetime.now().timestamp()
            token = create_token(user)
            session.commit()
            session.close()
            return True, token, "Successfull log-in."
        
        else:
            session.close()
            return False, None, "No matching credentials were found."

    except Exception as e:
        session.rollback()
        session.close()
        return False, None, str(e)


def delete_user(user_id: int) -> bool:
    try:
        session = database.Session()
        del_num = session.query(User).where(User.id == user_id).delete()
        session.commit()
        session.close()
        print(f"[delete_user()]: deleted {del_num} columns")
        return True
    
    except:
        print(traceback.format_exc())
        return False
    
def add_role(user_id: int, role_id: int):
    with database.Session() as session:
        print(user_id)
        assert session.query(database.User).where(database.User.id == user_id).first() is not None
        assert session.query(database.Role).where(database.Role.id == role_id).first() is not None

        session.add(
            database.UserRole(
                user_id = user_id,
                role_id = role_id
            )
        )

        session.commit()



def create_user(password: str, username: str, role_id: int = database.ROLES_ENUM.user) -> tuple[bool, int, str]:
    """
        Returns: success:bool, user_id:int, error_msg: str
    """
    try:
        session = database.Session()
        if len(session.query(User).where(User.username == username).all()) > 0: 
            return False, 0, "Username already in use."
        
        if session.query(Role).where(Role.id == role_id).first() == None:
            return False, 0, "User Role does not exist."
        
        salt = secrets.token_hex(16)
        password_hash = sha3_256((salt+password).encode()).hexdigest()
                
        new_user = User(
            username = username,
            passwordHash = f"{salt}:{password_hash}",
            date = datetime.now().timestamp()
        )

        session.add(new_user)
        session.commit()
        session.add(UserRole(user_id = new_user.id, role_id = role_id))
        session.commit()

        result = True, new_user.id, "User successfully created."
        session.close()
        return result
    
    except Exception as e:
        print(traceback.format_exc())
        return False, 0, str(e)
    
try:
    create_user("123", "kheprep", database.ROLES_ENUM.admin)
    add_role(2, database.ROLES_ENUM.user)
except: pass
    
def make_thread(
        user_id: int,
        payload: models.CreateThreadRequest
    ):
    try: 
        with database.Session() as session:
            body_decoded = base64.b64decode(payload.body_content)

            for attachment in payload.attachments:
                attachment_content = Content(
                    attachment.mime_type,
                    attachment.data,
                    user_id,
                    False
                )

                session.add(attachment_content)
                session.commit()

                body_decoded.replace(attachment.temporary_id, attachment_content.id)

            content = Content(
                payload.body_mime_type,
                body_decoded,
                user_id,
                False
            )
            session.add(content)
            session.commit()
            
            thread = Thread(
                created_by = user_id,
                title = payload.title,
                category_id = payload.category,
                body = content.id,
                allowReplies=payload.allow_replies,
                allowEdits=True,
                date = datetime.now().timestamp(),
            )

            session.add(thread)
            session.commit()

            return thread.id

    except Exception as e:
        session.rollback()
        session.close()

        raise e
    
    
def model_thread(thread: database.Thread, session: Session) -> models.ThreadModel:
    last_edit = session.query(database.Edit.date).\
        where(database.Edit.reptacle_id == thread.id).\
        order_by(database.Edit.date.desc()).\
        first()
                    
    author_ids = set()

    author_ids.update(
        session.query(database.ThreadAuthorship.user_id).\
        where(database.ThreadAuthorship.thread_id == thread.id).\
        all()
    )
    author_ids.add(thread.created_by)
                    
    return models.ThreadModel(
        id = thread.id,
        title = thread.title,
        date = thread.date,
        body = thread.body,
        last_edited = last_edit,
        authors = (
            session.query(database.User.username).where(database.User.id == id).first()[0]
            for id in author_ids
        )
    )


def has_perm(user_id: int, perm: str):
    with database.Session() as session:
        try:
            roles:list[Role] = session.\
                query(database.Role).\
                join(database.UserRole).\
                where(database.UserRole.user_id == user_id and database.Role.id == database.UserRole.role_id).\
                all()
            
            if len(roles) < 1: return False
            
            result = False
            for index in range(len(roles)):
                role:Role = roles[index]
                perm_result = getattr(role, perm)
                if perm_result == None: pass
                elif type(perm_result) == bool: result = perm_result
                
            return result
        except:
            print(traceback.format_exc())
            session.rollback()
            return False
    