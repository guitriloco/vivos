#[cxx::bridge]
mod ffi {
    unsafe extern "C++" {
        include!("zenith_core/cpp/fragment_engine.hpp");

        type FragmentedProcessor;

        fn new_processor() -> UniquePtr<FragmentedProcessor>;
        fn process_fragment(&self, data: &[u8]) -> bool;
        fn connect_mesh(&self, peer_addr: &str) -> bool;
    }
}

pub struct ZenithEngine {
    processor: cxx::UniquePtr<ffi::FragmentedProcessor>,
}

impl ZenithEngine {
    pub fn new() -> Self {
        Self {
            processor: ffi::new_processor(),
        }
    }

    pub fn ingest(&self, data: &[u8]) -> bool {
        self.processor.process_fragment(data)
    }

    pub fn link_mesh(&self, addr: &str) -> bool {
        self.processor.connect_mesh(addr)
    }
}
