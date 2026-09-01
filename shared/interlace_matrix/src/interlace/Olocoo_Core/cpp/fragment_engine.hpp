#pragma once
#include <memory>
#include <vector>
#include <cstdint>
#include "rust/cxx.h"

class FragmentedProcessor {
public:
    FragmentedProcessor();
    bool process_fragment(const uint8_t* data, size_t len) const;
    bool connect_mesh(rust::Str peer_addr) const;
};

std::unique_ptr<FragmentedProcessor> new_processor();
