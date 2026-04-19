#include <stdio.h>
#include <string.h>

int main() {
    char plain[] = "saya sudah TAHU";
    char cipher[100];
    int k = 7; // Diperoleh dari analisis pesan sebelumnya

    strcpy(cipher, plain);

    for (int i = 0; i < strlen(cipher); i++) {
        // Enkripsi huruf kecil
        if (cipher[i] >= 'a' && cipher[i] <= 'z') {
            cipher[i] = (cipher[i] - 'a' + k) % 26 + 'a';
        }
        // Enkripsi huruf kapital
        else if (cipher[i] >= 'A' && cipher[i] <= 'Z') {
            cipher[i] = (cipher[i] - 'A' + k) % 26 + 'A';
        }
        // Spasi dan karakter lain dibiarkan tetap
    }

    printf("Plaintext: %s\n", plain);
    printf("Hasil Enkripsi: %s\n", cipher);

    return 0;
}
