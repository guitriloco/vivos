# Contributing to olocoo

We welcome contributions to the Zenith Engine. As a core component of the Aetheris ecosystem, high standards for performance and safety are required.

## 🤝 Development Workflow

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/optimization`
3. **Write Rust/C++ code**
4. **Run tests:** `cargo test`
5. **Submit a PR**

## 📜 Coding Standards

- **Safety First:** All `unsafe` blocks in Rust must be documented.
- **C++ Interop:** Use `cxx` for all bridges; avoid manual FFI where possible.
- **Performance:** Include benchmarks for any changes to the fragment processor.

---
*Part of the Aetheris Resonance Project.*
