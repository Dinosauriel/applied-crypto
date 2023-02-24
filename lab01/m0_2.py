from Crypto.Hash import SHA256

def main():
    m = b'LoremipsumdolorsitametconsecteturadipiscingelitseddoeiusmodtemporincididuntutlaboreetdoloremagnaaliquaUtenimadminimveniamquisnostrudexercitationullamcolaborisnisiutaliquipexeacommodoconsequatDuisauteiruredolorinreprehenderitinvoluptatevelitessecillumdoloreeufugiatnullapariaturExcepteurs.'
    s = [m[i : i + 16] for i in range(0, len(m), 16)]
    last = [block[-1:] for block in s]
    concat = b"".join(last)
    res = SHA256.new(data=concat).hexdigest()
    print(res)

if __name__ == "__main__":
    main()