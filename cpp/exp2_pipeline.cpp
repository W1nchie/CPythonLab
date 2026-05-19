#include <chrono>
#include <fstream>
#include <numeric>
#include <span>
#include <vector>

using namespace std;

constexpr size_t MiB = 1024 * 1024;
constexpr size_t HEADER = 64;

uint64_t copy_pipeline(const vector<uint8_t>& packet, size_t body_size) {
    vector<uint8_t> payload(packet.begin() + HEADER, packet.begin() + HEADER + body_size);
    vector<uint8_t> middle(payload.begin() + body_size / 4, payload.end());
    return accumulate(middle.begin(), middle.end(), uint64_t(0));
}

uint64_t view_pipeline(const vector<uint8_t>& packet, size_t body_size) {
    span<const uint8_t> payload(packet.data() + HEADER, body_size);
    span<const uint8_t> middle(payload.data() + body_size / 4, payload.size() - body_size / 4);
    return accumulate(middle.begin(), middle.end(), uint64_t(0));
}

static double benchmark(auto fn) {
    auto start = chrono::high_resolution_clock::now();
    fn();
    auto end = chrono::high_resolution_clock::now();
    return chrono::duration<double, milli>(end - start).count();
}

int main() {
    vector<int> sizes = {1, 2, 4, 8, 16, 32, 64};
    ofstream csv("results/exp2.csv", ios::app);
    for (int size_mib : sizes) {
        size_t body_size = size_mib * MiB;
        vector<uint8_t> packet(body_size + HEADER, 1);
        double copy_ms = benchmark([&]() {
            copy_pipeline(packet, body_size);
        });
        double view_ms = benchmark([&]() {
            view_pipeline(packet, body_size);
        });
        csv << "cpp,pipeline,copy_pipeline,"
            << size_mib << ","
            << copy_ms << ","
            << (size_mib / (copy_ms / 1000.0))
            << "\n";
        csv << "cpp,pipeline,view_pipeline,"
            << size_mib << ","
            << view_ms << ","
            << (size_mib / (view_ms / 1000.0))
            << "\n";
    }
}