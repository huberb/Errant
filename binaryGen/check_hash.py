import bencode
import sys

with open(sys.argv[1], 'rb') as fh:
    torrent_data = fh.read()

def byte2carray(data, n=16):
    t = ""
    for chunk in [data[i:i + n] for i in xrange(0, len(data), n)]:
        t += '"'
        for c in chunk:
            t += '\\x'+c.encode('hex')
        t += '"\r\n'
    return t[:-2]

torrent = bencode.bdecode(torrent_data)
print(byte2carray(torrent['info']['pieces']))
