#include "processor.h"
#include <stdexcept>

ProcessingResult processData(const std::vector<int>& data) {
    if (data.empty()) {
        throw std::invalid_argument("Dataset cannot be empty");
    }

    ProcessingResult result = {data[0], data[0], 0};

    for (int value : data) {
        if (value > result.maximum) {
            result.maximum = value;
        }

        if (value < result.minimum) {
            result.minimum = value;
        }

        result.sum += value;
    }

    return result;
}