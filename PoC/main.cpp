#include <iostream>
#include <fstream>
#include <iterator>
#include <vector>
#include <stdio.h>

void good() {
    std::cout << "This is harmless code\n";
}
void evil() {
    std::cout << "This is the evil code\n";
}

int main(int argc, char *argv[]) {
    std::cout << "Starting..\n";
    std::cout << "Program Name: " << argv[0] << "\n";
    std::cout << "Reading File..\n";

    // the program reads itself as binary
    std::ifstream input(argv[0], std::ios::binary );
    // and saves it to the buffer
    std::vector<char> buffer((
            std::istreambuf_iterator<char>(input)), 
            (std::istreambuf_iterator<char>()));

    std::cout << "Filesize: " << buffer.size() << "\n";

    if(buffer.size() % 16384 != 0) {
        std::cout << "PDF has not been injected yet! Exiting..\n";
        return 1;
    } else {
        std::cout << "Size is correct..\n";

        int shatter_start_point = buffer.size() - 425984;
        std::vector<char>::const_iterator begin = buffer.begin() + shatter_start_point;
        std::vector<char>::const_iterator end = buffer.begin() + buffer.size();
        std::vector<char> pdf_buffer(begin, end);

        std::cout << "PDF Size: " << pdf_buffer.size() << "\n";

        if((int)pdf_buffer[192] == 127) {
            good();
            return 0;
        }
        if((int)pdf_buffer[192] == 115) {
            evil();
            return 0;
        }
    }
}
