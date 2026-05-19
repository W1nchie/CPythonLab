#include <chrono>
#include <fstream>
#include <numeric>
#include <span>
#include <string>
#include <vector>

using namespace std;
constexpr size_t MiB = 1024 * 1024;

static double benchmark_copy(const vector<uint8_t>& data) {
    auto start = chrono::high_resolution_clock::now();
    vector<uint8_t> copy = data;
    auto end = chrono::high_resolution_clock::now();
    return chrono::duration<double, milli>(end - start).count();
}

static double benchmark_span(const vector<uint8_t>& data) {
    auto start = chrono::high_resolution_clock::now();
    span<const uint8_t> view(data);
    volatile auto x = view[0];
    auto end = chrono::high_resolution_clock::now();
    return chrono::duration<double, milli>(end - start).count();
}

int main() {
    vector<int> sizes = {1, 2, 4, 8, 16, 32, 64, 128};
    ofstream csv("results/exp1.csv", ios::app);
    for (int size_mib : sizes) {
        size_t size = size_mib * MiB;
        vector<uint8_t> data(size, 1);
        double copy_ms = benchmark_copy(data);
        double span_ms = benchmark_span(data);
        csv << "cpp,copy_vs_view,vector_copy,"
            << size_mib << ","
            << copy_ms << ","
            << (size_mib / (copy_ms / 1000.0))
            << "\n";
        csv << "cpp,copy_vs_view,span_view,"
            << size_mib << ","
            << span_ms << ","
            << (size_mib / (span_ms / 1000.0))
            << "\n";
    }
}