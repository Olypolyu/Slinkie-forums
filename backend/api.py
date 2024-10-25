from database import User, Role
from datetime import datetime, timedelta
import base64
import json
import database
import traceback
from hashlib import sha3_256
import secrets
from cryptography.fernet import Fernet
from typing import *

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
    try:
        token = json.loads(token)
        header = token["header"]
        
        hash = sha3_256(json.dumps(header).encode()).digest()
        encrypted_signature = base64.b64decode(token["signature"])
        retrieved_hash = Fernet(key).decrypt(encrypted_signature)
        
        return retrieved_hash == hash and header["expiry"] > datetime.now().timestamp(), header
    except:
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
                
        new_user = User(username, f"{salt}:{password_hash}", role=role_id, date=datetime.now().timestamp())
        session.add(new_user)
        session.commit()
        result = True, new_user.id, "User successfully created."
        session.close()
        return result
    
    except Exception as e:
        print(traceback.format_exc())
        return False, 0, str(e)