from string import ascii_letters, digits
from Crypto.Util.Padding import pad, unpad
import telnetlib
import json

ALPHABET = ascii_letters + digits
TARGET = 5

# Change this to REMOTE = False if you are running against a local instance of the server
REMOTE = True

# Remember to change the port if you are re-using this client for other challenges
PORT = 50221

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

def find_last(repo):
    for offset in range(16):
        request = {
            "command": "encrypt",
            "prepend_pad": bytes(offset).hex()
        }
        json_send(request)
        response = json_recv()
        last_block = bytes.fromhex(response["res"])[-16:].hex()

        if last_block in repo:
            print(f"found last char {repo[last_block]} for offset {offset}")
            return repo[last_block]
        
    print("char not found!")
    return "a"

def main():
    repo = {}
    for char in ALPHABET:
        request = {
            "command": "encrypt",
            "prepend_pad": pad(char.encode(), 16).hex()
        }
        json_send(request)
        response = json_recv()

        encrypted_char = bytes.fromhex(response["res"])[:16].hex()

        repo[encrypted_char] = char
        print(f"{encrypted_char}: {char}")

    for i in range(TARGET):
        last_char = find_last(repo)
        request = {
            "command": "solve",
            "solve": last_char
        }
        json_send(request)
        response = json_recv()
        print(response)
        if i == TARGET - 1:
            print(json_recv())



if __name__ == "__main__":
    main()
