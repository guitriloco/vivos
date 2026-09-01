#include "arbitrage_engine.h"
#include "siphon_network.h"
#include <thread>
#include <atomic>
#include <vector>

std::atomic<bool> global_running(true);

void run_capture_loop(int port, ArbitrageEngine& engine, bool is_solana) {
    HighPerformanceSocket sock(port);
    double price;
    
    std::cout << "Starting Capture Loop on port " << port << (is_solana ? " [SOLANA]" : " [BASE]") << std::endl;
    
    while (global_running) {
        if (sock.poll_price(price)) {
            if (is_solana) {
                engine.update_solana_price(price);
            } else {
                engine.update_base_price(price);
            }
        }
        // No sleep here for bare-metal performance, but in a real system we'd use select/poll/epoll
        // To minimize CPU usage while keeping latency low
    }
}

int main(int argc, char** argv) {
    ArbitrageEngine engine(0.002); // 0.2% threshold for high sensitivity
    
    std::cout << "🔱 YIELD-SIPHON TRANSMUTED CORE V16.0 🔱" << std::endl;
    std::cout << "Target Latency: <10us | Arch: x86/ARM" << std::endl;
    
    std::thread sol_thread(run_capture_loop, 9001, std::ref(engine), true);
    std::thread base_thread(run_capture_loop, 9002, std::ref(engine), false);
    
    // Management loop
    size_t last_trades = 0;
    while (global_running) {
        std::this_thread::sleep_for(std::chrono::seconds(1));
        size_t current_trades = engine.get_trade_count();
        if (current_trades > last_trades) {
            std::cout << "[STATUS] Trades Executed: " << current_trades 
                      << " | Last Latency: " << engine.get_last_latency_ns() << "ns" << std::endl;
            last_trades = current_trades;
        }
    }
    
    sol_thread.join();
    base_thread.join();
    
    return 0;
}
