#include <fstream>
#include <span>
#include <vector>

using namespace std;

constexpr size_t MiB = 1024 * 1024;

int main() {
    vector<int> sizes = {1, 2, 4, 8, 16, 32, 64, 128};
    ofstream csv("results/exp3.csv", ios::app);
    for (int size_mib : sizes) {
        size_t size = size_mib * MiB;
        vector<uint8_t> base(size, 1);
        vector<vector<uint8_t>> copies;
        for (int i = 0; i < 6; ++i) {
            copies.push_back(base);
        }
        vector<span<uint8_t>> views;
        for (int i = 0; i < 6; ++i) {
            views.push_back(span<uint8_t>(base));
        }
        csv << "cpp,memory_pressure,"
            << size_mib << ","
            << (size_mib * 6) << ","
            << 0
            << "\n";
    }
}