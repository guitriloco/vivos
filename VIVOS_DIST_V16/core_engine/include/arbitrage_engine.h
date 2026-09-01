#ifndef ARBITRAGE_ENGINE_H
#define ARBITRAGE_ENGINE_H

#include <iostream>
#include <chrono>
#include <atomic>
#include <vector>
#include <string>
#include <cmath>
#include <iomanip>

class ArbitrageEngine {
public:
    ArbitrageEngine(double threshold = 0.005) 
        : threshold(threshold), solana_price(0.0), base_price(0.0), trade_count(0) {}

    void update_solana_price(double price) {
        solana_price.store(price, std::memory_order_relaxed);
        check_arbitrage();
    }

    void update_base_price(double price) {
        base_price.store(price, std::memory_order_relaxed);
        check_arbitrage();
    }

    void check_arbitrage() {
        auto start = std::chrono::high_resolution_clock::now();
        
        double s_price = solana_price.load(std::memory_order_relaxed);
        double b_price = base_price.load(std::memory_order_relaxed);

        if (s_price <= 0.0 || b_price <= 0.0) return;

        double spread = (s_price > b_price) ? (s_price - b_price) / b_price : (b_price - s_price) / s_price;

        if (spread > threshold) {
            execute_trade();
        }

        auto end = std::chrono::high_resolution_clock::now();
        last_latency_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count();
    }

    void execute_trade() {
        trade_count.fetch_add(1, std::memory_order_relaxed);
    }

    long long get_last_latency_ns() const { return last_latency_ns; }
    size_t get_trade_count() const { return trade_count.load(std::memory_order_relaxed); }

private:
    double threshold;
    std::atomic<double> solana_price;
    std::atomic<double> base_price;
    std::atomic<size_t> trade_count;
    long long last_latency_ns = 0;
};

#endif // ARBITRAGE_ENGINE_H
