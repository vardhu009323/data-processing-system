
#include <iostream>
#include <vector>
#include <exception>
#include "processor.h"

int main() {
    int n;

    if (!(std::cin >> n) || n <= 0) {
        std::cerr << "Error: Expected a positive element count.\n";
        return 1;
    }

    std::vector<int> data;
    data.reserve(n);

    for (int i = 0; i < n; i++) {
        int value;

        if (!(std::cin >> value)) {
            std::cerr << "Error: Expected integer values.\n";
            return 1;
        }

        data.push_back(value);
    }

    try {
        ProcessingResult result = processData(data);

        std::cout << "{\n";
        std::cout << "  \"maximum\": " << result.maximum << ",\n";
        std::cout << "  \"minimum\": " << result.minimum << ",\n";
        std::cout << "  \"sum\": " << result.sum << "\n";
        std::cout << "}\n";
    }
    catch (const std::exception& error) {
        std::cerr << "Error: " << error.what() << '\n';
        return 1;
    }

    return 0;
}
