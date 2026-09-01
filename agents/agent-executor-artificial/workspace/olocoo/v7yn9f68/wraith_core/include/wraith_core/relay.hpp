#pragma once
#include <string>
#include <vector>

namespace wraith {
    class RelayService {
    public:
        RelayService();
        void broadcast_signal(const std::string& signal_type, const std::vector<uint8_t>& payload);
    };
}
