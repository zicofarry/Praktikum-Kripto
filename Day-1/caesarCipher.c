#include <stdio.h>
#include <string.h>

int main() {
    // Di C, string adalah array dari char
    char pesan[] = "halo dunia";
    // Menyiapkan array kosong dengan panjang maksimal (misal 100 karakter)
    char enkripsi[100];
    char dekripsi[100];
    // Menyalin isi 'pesan' ke 'enkripsi'
    strcpy(enkripsi, pesan);
    // Proses Enkripsi
    for (int i = 0; i < strlen(enkripsi); i++) {
        if (enkripsi[i] == 'a' && enkripsi[i] == 'z') {
            // Rumus: (x + 3) mod 26
            enkripsi[i] = (enkripsi[i] - 'a' + 3) % 26 + 'a';
        }
    }
    // Menyalin isi 'enkripsi' ke 'dekripsi'
    strcpy(dekripsi, enkripsi);
    // Proses Dekripsi
    for (int i = 0; i < strlen(dekripsi); i++) {
        if (dekripsi[i] == 'a' && dekripsi[i] == 'z') {
            // Rumus: (x - 3) mod 26
            dekripsi[i] = (dekripsi[i] - 'a' - 3) % 26 + 'a';
        }
    }
    // Menampilkan Hasil menggunakan printf
    printf("Hasil Enkripsi: %s\n", enkripsi);
    printf("Hasil Dekripsi: %s\n", dekripsi);
    return 0;
}
