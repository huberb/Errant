from hashlib import sha1
import sys
import time
import bencode

def write_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)

def read_file(path):
    data = ''
    with open(path) as f:
        data = f.read()
    return data

def getChunks(data, chunksize):
    cl = list()
    for h in [data[i:i+chunksize] for i in range(0, len(data), chunksize)]:
        yield h

def generateTorrent(data, name):
    tracker = 'http://tracker.opentrackr.org:1337/announce'
    chunksize = 16384

    torrent = {}
    torrent["announce"] = tracker
    torrent["announce-list"] = [tracker]
    torrent["creation date"] = 1000
    torrent["created by"] = 'Ben'
    torrent["comment"] = 'BitErrant Proof of Concept'

    info = {}
    info["piece length"] = chunksize
    info["length"] = len(data)
    info["name"] = name
    pieces = [sha1(p).digest() for p in getChunks(data, chunksize)]
    info["pieces"] = ''.join(pieces)
    torrent["info"] = info

    bencoded_torrent = bencode.bencode(torrent)
    return bencoded_torrent

torrent = generateTorrent(read_file(sys.argv[1]), "main")
write_file(torrent, sys.argv[1] + '.torrent')

