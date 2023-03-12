#!/usr/bin/env python3
# from https://cryptohack.org/challenges/introduction/

from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import telnetlib
import json
from itertools import cycle

# Change this to REMOTE = False if you are running against a local instance of the server
REMOTE = True
if REMOTE:
    host = "aclabs.ethz.ch"
else:
    host = "localhost"

tn = telnetlib.Telnet(host, 50340)

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
    for i in range(300):
        json_send({"command": "decrypt", "ciphertext": i.to_bytes(16).hex()})
        res = json_recv()

        if len(res["res"]) == 128:
            print("hi!")

        g = {"command": "guess", "guess": len(res["res"]) != 128}
        json_send(g)
        res = json_recv()
        print(res)

    json_send({"command": "flag"})
    print(json_recv())

if __name__ == "__main__":
    main()
