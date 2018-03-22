# does a c++ binary stay the same after we added zero bytes at the end?
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
write_file('./binary_test_filled_up', file_data + '\x00' * NUMBER_OF_ZERO_BYTES)
