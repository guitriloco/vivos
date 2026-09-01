# olocoo Usage Guide

This guide describes how to interact with the Zenith Engine provided by olocoo.

## 🛠 Prerequisites

- Rust (latest stable)
- C++ Compiler (supporting C++17 or later)
- `cargo-cxx` for bridge generation

## 💻 Programmatic Usage (Rust)

```rust
use zenith_core::ZenithEngine;

fn main() {
    let engine = ZenithEngine::new();
    
    // Ingest data fragments
    let data = vec![0x01, 0x02, 0x03];
    engine.ingest(&data);
    
    // Connect to the distributed mesh
    engine.link_mesh("127.0.0.1:9000");
}
```

## 🌐 API Interaction

While olocoo is primarily a library, it is often wrapped in a service that exposes a high-performance endpoint for fragment ingestion.

### `POST /ingest`
Ingests a raw data fragment into the processor.

### `POST /connect`
Establishes a link with another Zenith node in the mesh.
