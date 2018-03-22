import hashlib

def read_file(path):
    data = ''
    with open(path) as f:
        data = f.read()
    return data

def sha1(data):
    return hashlib.sha1(data).digest()

if __name__ == '__main__':
    shattered1 = read_file('../shatterPDFs/shattered-1.pdf')
    shattered2 = read_file('../shatterPDFs/shattered-2.pdf')

    sha_1 = sha1(shattered1)
    sha_2 = sha1(shattered2)

    # this is the obvious one:
    print("SHA of PDF files are equal: " + str(sha_1 == sha_2))

    # this is interesting..
    sha_1 = sha1(shattered1[100 * 1024])
    sha_2 = sha1(shattered2[100 * 1024])
    print("SHA of first 100 kb of PDF files are equal: " + str(sha_1 == sha_2))

    # this will be useful
    i = 100
    sha_1 = sha1(shattered1[i])
    sha_2 = sha1(shattered2[i])
    print("SHA of first " + str(i) + " bytes of PDF files are equal: " + str(sha_1 == sha_2))

    # lets try to concat them
    sha_1 = sha1(shattered1 * 2)
    sha_2 = sha1(shattered2 * 2)
    print("SHA of concatenated PDFs: " + str(sha_1 == sha_2))
    # does not work..

    # however, adding zero bytes at the end
    sha_1 = sha1(shattered1 + '\x00' * i)
    sha_2 = sha1(shattered2 + '\x00' * i)
    print("SHA of PDFs with zero bytes: " + str(sha_1 == sha_2))
    # actually works
