#include <iostream>
#include <fstream>
#include <iterator>
#include <vector>

// the shattered pdfs differ only in small chunks
// this program finds the first byte thats different
// answer: the first byte is number 192

int main() {
    // first pdf..
    std::ifstream input1("../shatterPDFs/shattered-1.pdf", std::ios::binary );
    std::vector<char> shattered1((
            std::istreambuf_iterator<char>(input1)), 
            (std::istreambuf_iterator<char>()));
    // second pdf..
    std::ifstream input2("../shatterPDFs/shattered-2.pdf", std::ios::binary );
    std::vector<char> shattered2((
            std::istreambuf_iterator<char>(input2)), 
            (std::istreambuf_iterator<char>()));

    // we assume they are the same size
    for(int i = 0; i < shattered1.size(); i++) {
        if((int)shattered1[i] != (int)shattered2[i]) {
            std::cout << "Byte Number: " << i << "\n";
        }
    }
    std::cout << shattered1.size() << "\n";
}
