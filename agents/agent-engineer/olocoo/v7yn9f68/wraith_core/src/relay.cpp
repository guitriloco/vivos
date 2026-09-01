#include "wraith_core/relay.hpp"
#include <iostream>

namespace wraith {
    RelayService::RelayService() {}
    void RelayService::broadcast_signal(const std::string& signal_type, const std::vector<uint8_t>& payload) {
        std::cout << "[WRAITH-LINK] Broadcasting signal: " << signal_type << " (" << payload.size() << " bytes)" << std::endl;
    }
}
