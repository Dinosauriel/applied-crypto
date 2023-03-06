#!/usr/bin/env python3

"""
This is a simple client implementation based on telnetlib that can help you connect to the remote server.

Taken from https://cryptohack.org/challenges/introduction/
"""

import telnetlib
import json

# Change this to REMOTE = False if you are running against a local instance of the server
REMOTE = True

# Remember to change the port if you are re-using this client for other challenges
PORT = 50220

if REMOTE:
    host = "aclabs.ethz.ch"
else:
    host = "localhost"

tn = telnetlib.Telnet(host, PORT)

def readline():
    return tn.read_until(b"\n")

def json_recv():
    line = readline()
    return json.loads(line.decode())

def json_send(req):
    request = json.dumps(req).encode()
    tn.write(request + b"\n")


def main():
    question = "flag, please!".encode()
    p = 16 - len(question)
    padding = p * p.to_bytes(1)

    request = {
        "command": "encrypt",
        "prepend_pad": (question + padding).hex()
    }
    json_send(request)
    response = json_recv()
    print(response)

    encrypted_question = bytes.fromhex(response["res"])[:16]

    req2 = {
        "command": "solve",
        "ciphertext": encrypted_question.hex()
    }

    json_send(req2)
    response = json_recv()
    print(response)


if __name__ == "__main__":
    main()
