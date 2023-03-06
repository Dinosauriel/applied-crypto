
B_SIZE = 16

def main():
    f = open("lab02/aes.data", "r")

    for i, l in enumerate(f.readlines()):
        c = bytes.fromhex(l)
        blocks = set()

        for b in range(0, len(c), B_SIZE):
            if c[b : b + B_SIZE] in blocks:
                print(f"repeat! {i + 1}: {c[b : b + B_SIZE].hex()}")
            blocks.add(c[b : b + B_SIZE])

    f.close()

if __name__ == "__main__":
    main()