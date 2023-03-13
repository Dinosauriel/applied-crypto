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

tn = telnetlib.Telnet(host, 50342)

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

def gen_mask(mask_int):
    return bytes(0).join([m.to_bytes(1) for m in mask_int])

def main():
    for i in range(10):
        json_send({"command": "challenge"})
        res = json_recv()
        challenge = bytes.fromhex(res["res"])
        iv = challenge[:16]
        print(f"challenge: {challenge.hex()}")
        mask_int = [0] * 16

        for l in range(16):
            mask_int_p = [0] * (16 - l) + [m ^ (l + 1) for m in mask_int[16 - l:]]
            # print(f"l = {l}, {mask_int_p}")
            for b in range(256):
                mask_int_p[16 - l - 1] = b
                mask = gen_mask(mask_int_p)
                json_send({"command": "decrypt", "ciphertext": (xor(mask, iv) + challenge[16:]).hex()})
                res = json_recv()

                if len(res["res"]) != 128:
                    # print(f"{mask_int_p} generates valid padding")
                    # plaintext[16 - l - 1] XOR b = l + 1
                    mask_int[16 - l - 1] = b ^ (l + 1)
                    break

        last_chars = gen_mask(mask_int).decode()
        print(f"last chars: {last_chars}")

        json_send({"command": "guess", "guess": last_chars})
        print(json_recv())

    json_send({"command": "flag"})
    print(json_recv())

if __name__ == "__main__":
    main()
