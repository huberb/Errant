# does a c++ binary stay the same after we added zero bytes at the end? yes
# actually it does not even have to be a zero byte
# any byte works!

BYTE = '\x42'

def read_file(path):
    data = ''
    with open(path) as f:
        data = f.read()
    return data

def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)

file_data = read_file('./binary_test')
# this works!
NUMBER_OF_ZERO_BYTES = 100000
write_file('./binary_test_filled_up', file_data + BYTE * NUMBER_OF_ZERO_BYTES)
