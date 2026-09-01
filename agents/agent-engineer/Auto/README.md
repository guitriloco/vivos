# Auto - Soup Tasting Log

A robust, high-performance C-based foundation for logging soup tastings.

## Features
- **High Performance**: Binary storage with fixed-size records for $O(1)$ access.
- **Modular Design**: Separated CLI, business logic, and storage abstraction.
- **Minimalist**: Clean C11 code with minimal dependencies.

## Structure
- `include/`: Header files defining the data structures and interfaces.
- `src/`: Implementation of the core logic and storage.
- `data/`: Binary storage for tasting logs (ignored by Git).
- `legacy/`: Previous Python-based scripts and documentation.

## Getting Started

### Prerequisites
- CMake 3.10+
- C Compiler (GCC, Clang, or MSVC)

### Building
```bash
mkdir build
cd build
cmake ..
make
```

### Usage
Run the generated `souplog` executable:

**Add a tasting entry:**
```bash
./souplog add "Tomato Soup" 5 "Delicious and creamy."
```

**List all entries:**
```bash
./souplog list
```

## Philosophy
This project follows a "Soberania Digital" and "Custo Zero" philosophy, focusing on efficiency, open-source standards, and high performance.
