use std::thread::sleep;
use std::time::Duration;

use sysinfo::System;

use zero_copy_lab::common::*;

fn rss_mib(
    sys: &mut System
) -> f64 {
    sys.refresh_memory();
    let pid = sysinfo::get_current_pid().unwrap();
    let process = sys.process(pid) .unwrap();
    process.memory() as f64 / 1024.0
}

fn main() {
    let sizes = vec![1, 2, 4, 8, 16, 32, 64, 128];

    let retained_count = 4;

    let mut sys =
        System::new_all();

    for size_mib in sizes {
        println!("Running Rust exp3: {} MiB", size_mib);
        let size = size_mib * MIB;
        let base = vec![1u8; size];
        sleep(Duration::from_millis(200));
        let rss_before = rss_mib(&mut sys);

        let copies:
            Vec<Vec<u8>> =
            (0..retained_count)
                .map(|_| {
                    base.clone()
                })
                .collect();

        std::hint::black_box(&copies);
        sleep(Duration::from_millis(300));
        let rss_after_copy = rss_mib(&mut sys);
        let copy_delta = rss_after_copy - rss_before;

        drop(copies);
        sleep(Duration::from_millis(500));

        let rss_before_view = rss_mib(&mut sys);
        let views:
            Vec<&[u8]> =
            (0..retained_count)
                .map(|_| &base[..])
                .collect();

        std::hint::black_box(&views);
        sleep(Duration::from_millis(300));
        let rss_after_view = rss_mib(&mut sys);
        let view_delta = rss_after_view - rss_before_view;

        append_csv2(
            "../results/exp3.csv",
            &MemoryRow {
                language:
                    "rust".into(),
                experiment:
                    "memory_pressure"
                        .into(),
                size_mib,
                copy_rss_delta:
                    copy_delta,
                view_rss_delta:
                    view_delta,
            },
        );
    }
}