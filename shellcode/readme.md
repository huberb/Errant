execute shellcode on Linux 4.4

    #include <stdio.h>

    char shellcode[] = /* insert shellcode here */


    int main(int argc, char **argv) {
            (*(void(*)())shellcode)();
            return 0;
    }

generate shellcode with this msfvenom command:

    [*] exec: msfvenom -p linux/x64/exec CMD=/bin/bash -b "\x00" -f c
