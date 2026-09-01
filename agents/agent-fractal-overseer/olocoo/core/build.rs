fn main() {
    cxx_build::bridge("src/lib.rs")
        .file("cpp/fragment_engine.cpp")
        .file("../../Auto/src/soup_log.c")
        .include("cpp")
        .include("../../Auto/include")
        .flag_if_supported("-std=c++14")
        .compile("zenith-core");

    println!("cargo:rerun-if-changed=src/lib.rs");
    println!("cargo:rerun-if-changed=cpp/fragment_engine.cpp");
    println!("cargo:rerun-if-changed=cpp/fragment_engine.hpp");
    println!("cargo:rerun-if-changed=../../Auto/src/soup_log.c");
    println!("cargo:rerun-if-changed=../../Auto/include/soup_log.h");
}
