from Crypto.Hash import SHA256
from Crypto.Cipher import AES

iv = bytes.fromhex("e764ea639dc187d058554645ed1714d8")

def generate_aes_key(integer: int, key_length: int):
    seed = integer.to_bytes(2, byteorder='big')
    hash_object = SHA256.new(seed)
    aes_key = hash_object.digest()
    trunc_key = aes_key[:key_length]
    return trunc_key

def aes_cbc_decryption(ciphertext: bytes, key: bytes):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

def main():
    f = open("lab02/flag.enc", "r")
    c = bytes.fromhex(f.readline())

    keys = set()
    for seed in range(256 * 256):
        key = generate_aes_key(seed, 16)
        keys.add(key)

    print(f"keyset generated, {len(keys)}")

    out = open("lab02/m3.out", "w")

    for key in keys:
        msg = aes_cbc_decryption(c, key)
        for i in range(0, len(msg), 16):
            try:
                t = msg[i : i + 16].decode()
                out.write(f"{t}\t\t{key.hex()}\n")
            except:
                pass

    out.close()
    f.close()

    correct_key = bytes.fromhex("d32b5677700fc98af4ba5b139c080d7e")
    print(aes_cbc_decryption(c, correct_key).decode(errors="replace"))

if __name__ == "__main__":
    main()