
def main():
    encoding = "596f752063616e206465636f646521"
    m = bytes.fromhex(encoding)
    print(m.decode())

if __name__ == "__main__":
    main()