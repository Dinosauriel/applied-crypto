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

tn = telnetlib.Telnet(host, 50341)

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
    for i in range(100):
        json_send({"command": "challenge"})
        res = json_recv()
        challenge = bytes.fromhex(res["res"])
        iv = challenge[:16]
        print(f"challenge: {challenge.hex()}")
        mask_int = [0] * 16

        for b in range(256):
            mask = b.to_bytes(16)
            json_send({"command": "decrypt", "ciphertext": (xor(mask, iv) + challenge[16:]).hex()})
            res = json_recv()

            if len(res["res"]) != 128:
                # print(f"{mask.hex()} generates valid padding")
                mask_int[-1] = b ^ 1
                break

        last_chars = mask_int[-1].to_bytes(1).decode()
        # print(f"last chars: {mask_int[-1]}, {last_chars}")

        json_send({"command": "guess", "guess": last_chars})
        print(json_recv())

    json_send({"command": "flag"})
    print(json_recv())

if __name__ == "__main__":
    main()
