from urllib.request import Request, urlopen  
from urllib.error import HTTPError
import urllib
import json
import traceback
import datetime
import time

from Crypto.Cipher import DES3, AES
from Crypto import Random
from Crypto.Util.Padding import pad
from base64 import b64encode, b64decode
import secrets
import string


class AuthProvider():
    authObject = {}
    AuthType = ""
    Token = ""
    def EncryptForJobpac(self, username, password, key):
        date = "%s+00:00" % (datetime.datetime.utcnow().replace(microsecond=0).isoformat())
        # Pad to length 10 with spaces
        username = username.ljust(10)
        password = password.ljust(10)
        
        if len(key) == 32:
            # Use AES encryption with new format UsernamePassword
            plaintext = "%s%s" % (username, password)
            
            # Encrypted text = plaintext encrypted with the key/Iv, with the IV at the start of the string.
            encrypted_text, iv = encrypt_with_aes(plaintext, key)
            return encrypted_text
        elif len(key) == 24:
            plaintext = "%s%s%s" % (date, username, password)
            # Use Triple DES (DES3) encryption
            return encrypt_with_des3(plaintext, key)
        else:
            raise ValueError("Invalid key length. Key must be either 24 bytes (Triple DES) or 32 bytes (AES).")


    def encrypt_with_des3(self, plaintext, key):
        print(plaintext)
        plaintext = pad(plaintext.encode("utf-8"), 8, style="pkcs7")
        cipher_encrypt = DES3.new(key, DES3.MODE_ECB)
        encrypted_text = cipher_encrypt.encrypt(plaintext)
        ct = b64encode(encrypted_text).decode("utf-8")
        return ct


    def encrypt_with_aes(self, plaintext, key):
        iv = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
        print(iv)
        iv_padded = iv.ljust(16, '0')  # Pad with zeros to make the length 16
        iv_bytes = iv_padded.encode('utf-8')

        # print(len(iv_bytes))
        cipher_encrypt = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv_bytes)
        encrypted_text = cipher_encrypt.encrypt(pad(plaintext.encode("utf-8"), AES.block_size))
        # print(encrypted_text)
        ct = iv+ b64encode(encrypted_text).decode("utf-8")
        return ct, iv


    def __init__(self, AuthType, AuthDetails):
        self.AuthType = AuthType
        self.authDetails = AuthDetails
        if (AuthType == "jobpac"):
            # Value was generated in previous step of step function 
            if ("value" in AuthDetails["authObject"]):
                AuthDetails["authObject"] = {
                    "Environment": AuthDetails["authObject"]["Environment"],
                    "application": AuthDetails["authObject"]["application"],
                    "value": AuthDetails["authObject"]["value"]
                }
            # Provided username and pw and we generate the value
            else:
                AuthDetails["authObject"] = {
                    "Environment": AuthDetails["authObject"]["Environment"],
                    "application": AuthDetails["authObject"]["application"],
                    "value": self.EncryptForJobpac(username=AuthDetails["authObject"]["username"], password=AuthDetails["authObject"]["password"], key=AuthDetails["authObject"]["EncryptionKey"]),
                }

    def getToken(self):
        if (self.AuthType == "jobpac"):
            Token = getFromJobpac(
                self.authDetails["authServer"], "/GiveMeAToken", genVariablesFromDict(self.authDetails["authObject"]))
            if (Token == None):
                return "ERROR: Jobpac didnt respond"
            elif (Token[0]["ErrorMessage"] != ""):
                return Token[0]["ErrorMessage"]
            else:
                self.Token = Token[0]["Token"]
                return "Success"
        else:
            return {"error": "no valid Auth Type set for object"}

    def doAuthorizedGetRequest(self, function, variables):
        if (self.AuthType == "jobpac"):
            if (variables == ""):
                return getFromJobpac(self.authDetails["requestServer"], function,  variables + "?Token=" + str(self.Token))
            else:
                return getFromJobpac(self.authDetails["requestServer"], function,  variables + "&Token=" + str(self.Token))
        else:
            return {"error": "no valid Auth Type set for object"}

    def doAuthorizedPatchRequest(self, function, variables, data):
        if (self.AuthType == "jobpac"):
            raise "UNIMPLEMENTED"
        else:
            return {"error": "no valid Auth Type set for object"}

    def doAuthorizedRequest(self, function, variables, data, requestType):
        if (self.AuthType == "jobpac"):
            if (variables == ""):
                return Request_Jobpac(self.authDetails["requestServer"] + str(function) + str(variables) + "?Token=" + str(self.Token), data,  self.Token, requestType)
            else:
                return Request_Jobpac(self.authDetails["requestServer"] + str(function) + str(variables) + "&Token=" + str(self.Token), data,  self.Token, requestType)


    def doAuthorizedGetRequest_pageN(self, function, variables):
        if (self.AuthType == "jobpac"):
            raise "UNIMPLEMENTED"


def Request_Jobpac(url, data, auth, requestType):
    print(url)
    print(data)
    print(auth)
    print(requestType)
    values = data

    if (requestType == "GET"):
        return self.getfromJobpac(url, "", "")
    else:
        headers = {
            "Content-Type": "application/json"
        }

    data = json.dumps(values).encode("utf-8")

    try:
        req = urllib.request.Request(url, data, headers, method=requestType)
        with urllib.request.urlopen(req) as f:
            res = json.loads(f.read())
            # res = f.getcode()

        print(res)

# Use loads to decode from text
        json_obj = res.get("data")
        return json_obj
    except HTTPError as e:

        print(e)
        print(e.code)
        # print(e.read().decode("utf8", 'ignore'))
        errorMessage = e.read().decode("utf8", 'ignore')
        print(errorMessage)
        error = {
            "message": errorMessage,
            "code": str(e)
        }
        return {"error": error}

def getFromJobpac(url, function, variables):
    print(url+function+variables)
    try:
        response = urlopen(url+function+variables)
        data = json.load(response).get("data")
        return data
    except Exception as e:
        print(e)
        # raise Exception("Jobpac request ERROR")
        print("BROKE FOR: " + url+function+variables)
        return None

def genVariablesFromDict(dict):
    ret = "?"
    for key in dict.keys():
        # quote plus library removes control characters from the key, eg. Spaces and & etc.
        ret += key+"="+urllib.parse.quote_plus(str(dict[key])) + "&"

    return ret[:-1]

