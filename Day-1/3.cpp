#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main() {
    string ciphertext = "ahainesntkhg";
    int k = 3; // Key lebar kolom
    int n = ciphertext.length();
    int rows = n / k;
    
    char grid[rows][k];
    int current = 0;

    // Memasukkan ciphertext ke grid secara vertikal (kebalikan dari cara baca enkripsi)
    for (int col = 0; col < k; col++) {
        for (int row = 0; row < rows; row++) {
            grid[row][col] = ciphertext[current++];
        }
    }

    // Membaca plaintext secara horizontal
    string plaintext = "";
    for (int row = 0; row < rows; row++) {
        for (int col = 0; col < k; col++) {
            plaintext += grid[row][col];
        }
    }

    cout << "Ciphertext: " << ciphertext << endl;
    cout << "Hasil Dekripsi: " << plaintext << endl;

    return 0;
}
