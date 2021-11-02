import base64
import json
import ssl
import stomper
import time
import websocket as ws
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


def sign(api_key: str, api_secret: str):
    base64_private_key = base64.b64decode(api_secret)
    private_key = RSA.import_key(base64_private_key)
    msg = bytearray(api_key.encode("utf-8"))
    hashed_message = SHA256.new(msg)
    raw_sig = pkcs1_15.new(private_key).sign(hashed_message)
    base64_sig = base64.b64encode(raw_sig)
    return base64_sig.decode()


def create_auth_header(api_key: str, api_secret: str):
    sig = sign(api_key, api_secret)
    header = {
        "x-key": api_key,
        "x-signature": sig
    }
    return header


def create_connect_frame(headers):
    NULL = '\x00'
    LF = '\x0A'
    lines = ['CONNECT']
    for entry in headers:
        value = headers[entry]
        lines.append("" + entry + ":" + value)

    lines.append(LF)
    joined = LF.join(lines)
    return joined + NULL


uri = "wss://ws.finxflo.com/stomp"
apikey = '' # your API key ID
secret = '' # your API secret
auth_headers = create_auth_header(apikey, secret)


def on_msg(ws, msg):
    frame = stomper.unpack_frame(msg)
    print("cmd: {}".format(frame['cmd']))
    body = frame['body']
    if not body:
        return
    json_body = json.loads(body)
    print("json body: {}".format(json_body))


def on_error(ws, err):
    print(err)


def on_closed(ws, close_status_code, close_msg):
    print("closed")


def on_open(ws):
    out = create_connect_frame(auth_headers)
    ws.send(out)
    time.sleep(2)
    sub = stomper.subscribe("/topic/ETH_BTC.depth", "sub-0", ack="auto")
    ws.send(sub)


ws = ws.WebSocketApp(uri, header=auth_headers, on_message=on_msg, on_error=on_error, on_close=on_closed)
ws.on_open = on_open
ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}, ping_interval=2)
