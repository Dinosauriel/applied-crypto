
def pad(m, k):
    p = k - (len(m) % k)
    pad = p * p.to_bytes(1)
    return m + pad

def unpad(m):
    p = m[-1]
    return m[:-p]

def main():
    flag_b = "flag".encode("utf-8")
    res = pad(flag_b, 16)
    print(res.hex())
    print(unpad(res).hex())

if __name__ == "__main__":
    main()
