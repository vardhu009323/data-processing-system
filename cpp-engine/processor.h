#ifndef PROCESSOR_H
#define PROCESSOR_H

#include <vector>

struct ProcessingResult {
    int maximum;
    int minimum;
    long long sum;
};

ProcessingResult processData(const std::vector<int>& data);

#endif