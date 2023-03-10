#!/usr/bin/env python3
# from https://cryptohack.org/challenges/introduction/

import telnetlib
import json

tn = telnetlib.Telnet("aclabs.ethz.ch", 50390)

def readline():
    return tn.read_until(b"\n")

def json_recv():
    line = readline()
    return json.loads(line.decode())

def json_send(req):
    request = json.dumps(req).encode()
    tn.write(request + b"\n")

def main():
    invalid_char = 0x80
    request = {
        "command": "hex_command",
        "hex_command": invalid_char.to_bytes(1).hex()
    }
    json_send(request)

    response = json_recv()

    print(response)

if __name__ == "__main__":
    main()
