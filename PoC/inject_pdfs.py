import sys

def read_file(path):
    data = ''
    with open(path) as f:
        data = f.read()
    return data

def write_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)

def fill_to_chunk_size(data):
    while not len(data) % 2**14 == 0:
        data += '\x00'
    return data

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("need a filepath as first argument.. Exit!")
        sys.exit(1)

    print("Reading File as Binary..")
    file_data = read_file(sys.argv[1])
    print("Original File Length: " + str(len(file_data)))
    print("Filling up with zero bytes until filesize is correct..")
    file_data = fill_to_chunk_size(file_data)

    print("Preparing SHAtter PDFs..")
    shatter1 = read_file('../shatterPDFs/shattered-1.pdf')
    shatter2 = read_file('../shatterPDFs/shattered-2.pdf')
    shatter1 = fill_to_chunk_size(shatter1)
    shatter2 = fill_to_chunk_size(shatter2)
    print("added zero bytes to both PDF. Size is now: " + str(len(shatter1)))

    print("Writing File as: " + sys.argv[1] + "_injected_1")
    write_file(file_data + shatter1, sys.argv[1] + "_injected_1")
    print("Writing File as: " + sys.argv[1] + "_injected_2")
    write_file(file_data + shatter2, sys.argv[1] + "_injected_2")
