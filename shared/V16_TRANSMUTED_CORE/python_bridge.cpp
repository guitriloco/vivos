#include <chrono>
#include <cstdint>
#include <cstring>
#include <cmath>
#include <algorithm>

extern "C" {

    struct EngineState {
        double threshold;
        double solana_price;
        double base_price;
        uint64_t trade_count;
        int64_t last_latency_ns;
    };

    EngineState* engine_create(double threshold) {
        EngineState* e = new EngineState();
        e->threshold = threshold;
        e->solana_price = 0.0;
        e->base_price = 0.0;
        e->trade_count = 0;
        e->last_latency_ns = 0;
        return e;
    }

    void engine_destroy(EngineState* e) {
        delete e;
    }

    int64_t engine_update_solana(EngineState* e, double price) {
        auto start = std::chrono::high_resolution_clock::now();
        e->solana_price = price;
        if (e->solana_price > 0.0 && e->base_price > 0.0) {
            double s = e->solana_price, b = e->base_price;
            double spread = std::abs(s - b) / std::max(s, b);
            if (spread > e->threshold) e->trade_count++;
        }
        auto end = std::chrono::high_resolution_clock::now();
        e->last_latency_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count();
        return e->last_latency_ns;
    }

    int64_t engine_update_base(EngineState* e, double price) {
        auto start = std::chrono::high_resolution_clock::now();
        e->base_price = price;
        if (e->solana_price > 0.0 && e->base_price > 0.0) {
            double s = e->solana_price, b = e->base_price;
            double spread = std::abs(s - b) / std::max(s, b);
            if (spread > e->threshold) e->trade_count++;
        }
        auto end = std::chrono::high_resolution_clock::now();
        e->last_latency_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count();
        return e->last_latency_ns;
    }

    double engine_get_spread(EngineState* e) {
        if (e->solana_price <= 0.0 || e->base_price <= 0.0) return 0.0;
        double s = e->solana_price, b = e->base_price;
        return std::abs(s - b) / std::max(s, b);
    }

    uint64_t engine_get_trades(EngineState* e) {
        return e->trade_count;
    }

    int64_t engine_get_latency(EngineState* e) {
        return e->last_latency_ns;
    }

    double run_benchmark(int iterations) {
        EngineState* e = engine_create(0.005);
        int64_t total_ns = 0;
        for (int i = 0; i < iterations; i++) {
            double sol = 145.0 + (i % 100) / 10.0;
            double base = 146.0 + (i % 100) / 10.0;
            total_ns += engine_update_solana(e, sol);
            total_ns += engine_update_base(e, base);
        }
        double avg = static_cast<double>(total_ns) / (iterations * 2);
        engine_destroy(e);
        return avg;
    }
}
