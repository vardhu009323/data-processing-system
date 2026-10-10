#include <iostream>
#include <cassert>
#include <stdexcept>
#include <vector>
#include "processor.h"

int main() {
    // Test 1: Normal input
    std::vector<int> data = {12, 45, 7, 23};
    ProcessingResult result = processData(data);

    assert(result.maximum == 45);
    assert(result.minimum == 7);
    assert(result.sum == 87);

    // Test 2: Negative numbers
    std::vector<int> negative = {-8, -3, -12};
    result = processData(negative);

    assert(result.maximum == -3);
    assert(result.minimum == -12);
    assert(result.sum == -23);

    // Test 3: Empty input
    std::vector<int> empty;

    bool errorCaught = false;

    try {
        processData(empty);
    }
    catch (const std::invalid_argument&) {
        errorCaught = true;
    }

    assert(errorCaught);

    // Test 4: Single element
std::vector<int> single = {5};
result = processData(single);

assert(result.maximum == 5);
assert(result.minimum == 5);
assert(result.sum == 5);

// Test 5: Repeated values
std::vector<int> repeated = {4, 4, 4};
result = processData(repeated);

assert(result.maximum == 4);
assert(result.minimum == 4);
assert(result.sum == 12);

    std::cout << "All tests passed!\n";

    return 0;
}