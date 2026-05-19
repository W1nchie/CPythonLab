use zero_copy_lab::common::*;

fn main() {
    let sizes = vec![1, 2, 4, 8, 16, 32, 64, 128];

    for size_mib in sizes {
        let size = size_mib * MIB;

        let data = vec![1u8; size];

        let copy_ms = benchmark(
            || {
                let copy = data.clone();
                std::hint::black_box(copy);
            },
            10,
        );

        let slice_ms = benchmark(
            || {
                let slice = &data[..];
                std::hint::black_box(slice);
            },
            10,
        );

        append_csv(
            "../results/exp1.csv",
            &BenchmarkRow {
                language: "rust".into(),
                experiment: "copy_vs_view".into(),
                operation: "vec_clone".into(),
                size_mib,
                median_ms: copy_ms,
                throughput_mib_s:
                    size_mib as f64 / ((copy_ms + 0.00000001) / 1000.0),
            },
        );

        append_csv(
            "../results/exp1.csv",
            &BenchmarkRow {
                language: "rust".into(),
                experiment: "copy_vs_view".into(),
                operation: "slice_view".into(),
                size_mib,
                median_ms: slice_ms,
                throughput_mib_s:
                    size_mib as f64 / ((slice_ms + 0.0000001) / 1000.0),
            },
        );
    }
}