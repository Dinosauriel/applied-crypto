#!/usr/bin/env python3
# from https://cryptohack.org/challenges/introduction/

from Crypto.Util.Padding import pad, unpad
import telnetlib
import json
from itertools import cycle

tn = telnetlib.Telnet("aclabs.ethz.ch", 50301)

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
    response = json_recv()
    print(response)


    intro_encrypted = bytes.fromhex("01f0ceb3dad5f9cd23293937c893e0ec")
    magic = (1337).to_bytes(16)
    p = pad(b"intro", 16)

    R = xor(xor(p, magic), intro_encrypted)

    flag = pad(b"flag", 16)
    flag_encrypted = xor(xor(flag, magic), R)

    request = {
        "command": "encrypted_command",
        "encrypted_command": flag_encrypted.hex()
    }
    json_send(request)

    response = json_recv()

    print(response)

if __name__ == "__main__":
    main()
