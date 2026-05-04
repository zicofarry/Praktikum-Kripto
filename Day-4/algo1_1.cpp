#include <iostream>
#include <vector>
#include <string>
#include <cstdint>
#include <cstdio>

using namespace std;

// --- Helper untuk Operasi Bitwise ---
#define ROTL(bits, word) (((word) << (bits)) | ((word) >> (32 - (bits))))

struct SHA1_State {
    uint32_t H[5];
};

// LANGKAH 4: Pengolahan pesan dalam blok 512 bit (The Transform Engine)
void prosesBlok(SHA1_State &state, const uint8_t blok[64]) {
    uint32_t w[80];
    for (int i = 0; i < 16; i++) {
        w[i] = (blok[i*4] << 24) | (blok[i*4+1] << 16) | (blok[i*4+2] << 8) | (blok[i*4+3]);
    }
    for (int i = 16; i < 80; i++) {
        w[i] = ROTL(1, w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16]);
    }

    uint32_t a = state.H[0], b = state.H[1], c = state.H[2], d = state.H[3], e = state.H[4];

    for (int i = 0; i < 80; i++) {
        uint32_t f, k;
        if (i < 20) { f = (b & c) | ((~b) & d); k = 0x5A827999; }
        else if (i < 40) { f = b ^ c ^ d; k = 0x6ED9EBA1; }
        else if (i < 60) { f = (b & c) | (b & d) | (c & d); k = 0x8F1BBCDC; }
        else { f = b ^ c ^ d; k = 0xCA62C1D6; }

        uint32_t temp = ROTL(5, a) + f + e + k + w[i];
        e = d; d = c; c = ROTL(30, b); b = a; a = temp;
    }

    state.H[0] += a; state.H[1] += b; state.H[2] += c; state.H[3] += d; state.H[4] += e;
}

string hitungSHA1(string pesan) {
    // LANGKAH 3: Inisialisasi MD Buffer
    SHA1_State state;
    state.H[0] = 0x67452301;
    state.H[1] = 0xEFCDAB89;
    state.H[2] = 0x98BADCFE;
    state.H[3] = 0x10325476;
    state.H[4] = 0xC3D2E1F0;

    // Persiapan data (mengubah string ke byte array)
    vector<uint8_t> data(pesan.begin(), pesan.end());
    uint64_t bitLength = data.size() * 8;

    // LANGKAH 1: Penambahan Padding Bits
    // Tambahkan bit '1' (0x80 dalam byte)
    data.push_back(0x80);
    // Tambahkan bit '0' sampai panjangnya bersisa 64 bit dari kelipatan 512
    while ((data.size() % 64) != 56) {
        data.push_back(0x00);
    }

    // LANGKAH 2: Penambahan Nilai Panjang Pesan Semula (64-bit Big Endian)
    for (int i = 7; i >= 0; i--) {
        data.push_back((uint8_t)(bitLength >> (i * 8)));
    }

    // LANGKAH 4 (Lanjutan): Pengolahan pesan dalam blok berukuran 512 bit
    for (size_t i = 0; i < data.size(); i += 64) {
        prosesBlok(state, &data[i]);
    }

    // Konversi hasil ke format Hex
    char hexOutput[41];
    for (int i = 0; i < 5; i++) {
        sprintf(hexOutput + (i * 8), "%08x", state.H[i]);
    }
    return string(hexOutput);
}

int main() {
    string input = "abc";
    cout << "Input  : " << input << endl;
    cout << "SHA-1  : " << hitungSHA1(input) << endl;
    return 0;
}
