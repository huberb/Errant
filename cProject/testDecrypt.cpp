#include <iostream>
#include <sys/mman.h>
#include <unistd.h>
#include "collisionData.h"

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

int main() {
    char enc[] = "\x66\xe9\x4b\xd4\xef\x8a\x2c\x3b\x88\x4c\xfa\x59\xca\x34\x2b\x2e"
                 "\x01\x43\xdb\x63\xee\x66\xb0\xcd\xff\x9f\x69\x91\x76\x80\x15\x1e";
    char* shellcode;
    shellcode = (char*)malloc(16);
    CRijndael oRijndael;
    oRijndael.MakeKey("\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", "\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0", 16, 16);
    oRijndael.Decrypt(shellcode, enc, 32, CRijndael::ECB);
    print_bytes(shellcode, 16);
}
