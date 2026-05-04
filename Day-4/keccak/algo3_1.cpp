#include <iostream>
#include <iomanip>
#include <string>

extern "C" {
    #include "Keccak-readable-and-compact.c"
}

int main() {
    std::string pesan = "FufuFafa";
    unsigned char hash[32]; // Buffer untuk 256-bit

    // Memanggil fungsi Keccak dari file yang di-include
    // Parameter: rate=1088, capacity=512, input, len, suffix=0x06 (SHA-3), output, outLen=32
    Keccak(1088, 512, (const unsigned char*)pesan.c_str(), pesan.length(), 0x06, hash, 32);

    std::cout << "Input  : " << pesan << std::endl;
    std::cout << "SHA3-256: ";
    for(int i = 0; i < 32; i++) {
        std::cout << std::hex << std::setw(2) << std::setfill('0') << (int)hash[i];
    }
    std::cout << std::dec << std::endl;

    return 0;
}
