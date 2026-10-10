
#include <chrono>
#include <iomanip>
#include <iostream>
#include <vector>
#include "processor.h"

int main() {
    const std::vector<int> sizes = {
        100,
        10000,
        100000,
        1000000
    };

    std::cout
        << "Dataset Size,Average Time (ns),Throughput (integers/sec)\n";

    volatile long long checksum = 0;

    for (int size : sizes) {
        std::vector<int> data(size);

        for (int i = 0; i < size; ++i) {
            data[i] = (i % 2001) - 1000;
        }

        // Warm-up
        ProcessingResult warmup = processData(data);
        checksum += warmup.sum + warmup.maximum + warmup.minimum;

        int repetitions;

        if (size <= 100) {
    repetitions = 1000000;
} else if (size <= 10000) {
    repetitions = 2000;
} else if (size <= 100000) {
    repetitions = 200;
} else {
    repetitions = 30;
}

        const auto start = std::chrono::steady_clock::now();

        for (int i = 0; i < repetitions; ++i) {
            ProcessingResult result = processData(data);
            checksum += result.sum + result.maximum + result.minimum;
        }

        const auto end = std::chrono::steady_clock::now();

        const auto elapsedNs =
            std::chrono::duration_cast<std::chrono::nanoseconds>(
                end - start
            ).count();

        const double averageNs =
            static_cast<double>(elapsedNs) / repetitions;

        const double throughput =
            static_cast<double>(size) * repetitions * 1e9
            / elapsedNs;

        std::cout << size << ","
                  << std::fixed << std::setprecision(2)
                  << averageNs << ","
                  << std::setprecision(0)
                  << throughput << '\n';
    }

    // Make the accumulated results observable.
    std::cerr << "Checksum: " << checksum << '\n';

    return 0;
}
