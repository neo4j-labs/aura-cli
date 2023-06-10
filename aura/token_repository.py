import os
from datetime import datetime, timedelta
import json

AURA_TOKEN_PATH = '~/.aura/token.json'

def check_existing_token():
    token_path = os.path.expanduser(AURA_TOKEN_PATH)
    token_file_exists = os.path.isfile(token_path)

    if not token_file_exists:
        return
    
    with open(token_path, "r") as f:
        token_file = json.load(f)
        token = token_file["token"]
        expiry_time_str = token_file["expires_in"]
        expiry_time = datetime.strptime(expiry_time_str, "%Y-%m-%d %H:%M:%S")

        # token expired
        if expiry_time < datetime.now():
            return
        
        # TODO what if token was for different credentials?
        
        return token


def save_token(token, expires_in):
    token_path = os.path.expanduser(AURA_TOKEN_PATH)
    expiry_time = datetime.now() + timedelta(minutes=expires_in)
    expiry_time_str = expiry_time.strftime("%Y-%m-%d %H:%M:%S")
    token_json = {'token': token, 'expires_in': expiry_time_str}
    with open(token_path, 'w') as tokenfile:
        json.dump(token_json, tokenfile)

def delete_token_file():
    token_path = os.path.expanduser(AURA_TOKEN_PATH)
    if os.path.isfile(token_path):
        os.remove(token_path)