from string import ascii_letters, digits
from Crypto.Util.Padding import pad, unpad
import telnetlib
import json

ALPHABET = ascii_letters + digits + "{} "
TARGET = 5

# Change this to REMOTE = False if you are running against a local instance of the server
REMOTE = True

# Remember to change the port if you are re-using this client for other challenges
PORT = 50222

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

def create_repo(postfix):
    repo = {}
    for bt in range(256):
        padded_msg = pad(bt.to_bytes(1) + postfix, 16)

        request = {
            "command": "encrypt",
            "prepend_pad": padded_msg.hex()
        }
        json_send(request)
        response = json_recv()

        encrypted_char = bytes.fromhex(response["res"])[:len(padded_msg)].hex()

        repo[encrypted_char] = bt.to_bytes(1) + postfix
        # print(f"{encrypted_char}: {bt.to_bytes(1) + postfix}")

    return repo, len(pad(bytes(1) + postfix, 16))

def find_last(repo, len):
    for offset in range(len):
        request = {
            "command": "encrypt",
            "prepend_pad": bytes(offset).hex()
        }
        json_send(request)
        response = json_recv()
        last_block = bytes.fromhex(response["res"])[-len:].hex()

        if last_block in repo:
            print(f"found last block {repo[last_block]} for offset {offset}")
            return repo[last_block]

    print("char not found!")
    exit()

def main():
    flag = bytes()
    for _ in range(64):
        repo, len = create_repo(flag)
        flag = find_last(repo, len)
        print(f"flag: {flag}")
    print(flag)



if __name__ == "__main__":
    main()
