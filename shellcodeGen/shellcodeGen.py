from shellcodeEncryptor import AESCipher, byte2carray

# SHELLCODE = (
#     "\x55\x48\x89\xe5\x41\xb0\x02\x49\xc1\xe0\x18\x49\x83\xc8\x04\x4c"
#     "\x89\xc0\x48\x31\xff\x66\xbf\x01\x00\xeb\x1e\x5e\x48\x31\xd2\xb2"
#     "\x0e\x0f\x05\x41\xb0\x02\x49\xc1\xe0\x18\x49\x83\xc8\x01\x4c\x89"
#     "\xc0\x31\xff\x0f\x05\x48\x89\xec\x5d\xe8\xdd\xff\xff\xff\x48\x65"
#     "\x6c\x6c\x6f\x2c\x20\x57\x6f\x72\x6c\x64\x21\x0a"
# )

SHELLCODE = ( "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" )

if __name__ == '__main__':
    VERIFIER = 'BADCODE'
    print("reading key from SHAtter2 file..")
    # read the first 320 bytes
    # TODO: why 320?
    # key = open('../shatterPDFs/shattered-2.pdf', 'rb').read(0x140)
    key = open('../shatterPDFs/shattered-2.pdf', 'rb').read(0x140)[0xc0:0xd0]

    print("key: ")
    print(byte2carray(key))
    print('')
    print("encrypting shellcode with key..")

    key = "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    enc = AESCipher(key)
    # encdata = enc.encrypt(VERIFIER + SHELLCODE)
    encdata = enc.encrypt(SHELLCODE)
    encdata = byte2carray(encdata)

    print("shellcode encrypted: ")
    print(encdata)
