def main():
    c = bytes.fromhex("210e09060b0b1e4b4714080a02080902470b0213470a0247081213470801470a1e4704060002")

    for key in range(256):
        m = [key ^ b for b in c]
        print(bytes(m))

if __name__ == "__main__":
    main()