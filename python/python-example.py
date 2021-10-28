# We Suggest using the PyCryptoDome library
import json
import requests
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from base64 import b64decode,b64encode

 # GET Request Example

xKey = "YOUR_X-KEY"
privateKeyBase64 = b64decode("YOUR_PRIVATE_KEY")

# If no Data being sent - This is the format required
emptyBody = f"Signature{{body='', queryParam=''}}".encode()

privateKey = RSA.import_key(privateKeyBase64)
hashedMessage = SHA256.new(emptyBody)

signature = pkcs1_15.new(privateKey).sign(hashedMessage)
base64Sig = b64encode(signature)

r = requests.get(url="https://api.finxflo.com/me", headers={"x-key": xKey, "x-signature": base64Sig.decode()})
data = r.json()

# POST Request Example

payload = {"type": "MARKET", "market": "ETH_BTC", "side": "ASK", "quantity": 0.1, "stopPrice": 1}
bodyWithData = f"Signature{{body='{json.dumps(payload)}', queryParam=''}}".encode()

hashedMessageData = SHA256.new(bodyWithData)
signatureWithData = pkcs1_15.new(privateKey).sign(hashedMessage)

base64SigWithData = b64encode(signatureWithData)

url = "https://api.finxflo.com/orders"
headers = {"x-key": xKey, "x-signature": base64SigWithData.decode()}

r = requests.post(url=url, json=payload, headers=headers)
data = r.json()