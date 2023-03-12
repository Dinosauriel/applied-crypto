#!/usr/bin/env python3
# from https://cryptohack.org/challenges/introduction/

from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import telnetlib
import json
from itertools import cycle

tn = telnetlib.Telnet("aclabs.ethz.ch", 50303)

def xor(a, b):
    if len(a) < len(b):
        a, b = b, a
    return bytes([i ^ j for i, j in zip(a, cycle(b))])

def readline():
    return tn.read_until(b"\n")

def json_recv():
    line = readline()
    return json.loads(line.decode())

def json_send(req):
    request = json.dumps(req).encode()
    tn.write(request + b"\n")

def main():
    json_send({"command": "howto"})
    res = json_recv()

    enc = bytes.fromhex(res["res"][-64:])
    print(enc.hex())

    iv = enc[:16]
    enc_intro = enc[16:]
    flag = pad(b"flag", 16)
    intro = pad(b"intro", 16)

    # B xor IV = "intro"
    # B xor IV xor "intro" = 0
    # B xor IV xor "intro" xor "flag" = "flag"
    # -> new_IV = IV xor "intro" xor "flag"
    new_iv = xor(iv, xor(intro, flag))

    json_send({"command": "encrypted_command", "encrypted_command": (new_iv + enc_intro).hex()})
    print(json_recv())
    exit()

if __name__ == "__main__":
    main()
