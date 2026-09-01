fn main() {
    cxx_build::bridge("src/lib.rs")
        .file("cpp/fragment_engine.cpp")
        .include("cpp")
        .flag_if_supported("-std=c++14")
        .compile("zenith-core");

    println!("cargo:rerun-if-changed=src/lib.rs");
    println!("cargo:rerun-if-changed=cpp/fragment_engine.cpp");
    println!("cargo:rerun-if-changed=cpp/fragment_engine.hpp");
}
