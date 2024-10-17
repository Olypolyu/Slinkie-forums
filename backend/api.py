from database import User
import datetime
import base64
import json
from cryptography.fernet import Fernet

key = b'FHs4C3teBlPxMqak3bgPXcdTD6hIlb2whBnHz73QH2k='

def createToken(user: User, valid_for = 14):
    header = {
        "userID": user.id,
        "emittedOn": datetime.datetime.now().timestamp(),
        "expiry": (datetime.datetime.now() + datetime.timedelta(days=valid_for)).timestamp(),
    }
    
    encoded_header = base64.b64encode(json.dumps(header).encode())
    signature = Fernet(key).encrypt(encoded_header)
    JWT = {
        "header": encoded_header.decode(),
        "signature": base64.b64encode(signature).decode()
    }
    
    return json.dumps(JWT)
    
def validateToken(JWT):
    try:
        JWT = json.loads(JWT)
        header = base64.b64decode(JWT["header"]).decode()
        encoded_header = Fernet(key).decrypt(base64.b64decode(JWT["signature"]))
        decoded_signature = base64.b64decode(encoded_header).decode()
        return decoded_signature == header, json.loads(header)
    except:
        return False, None
        

print(validateToken(createToken(1))) 

