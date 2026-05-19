use zero_copy_lab::common::*;

fn copy_pipeline(
    data: &[u8]
) -> u64 {
    let payload = data.to_vec();

    let middle =
        payload[
            payload.len() / 8..
            payload.len() * 7 / 8
        ].to_vec();

    middle.iter().map(|v| *v as u64).sum()
}

fn view_pipeline(
    data: &[u8]
) -> u64 {
    let middle =&data[data.len() / 8.. data.len() * 7 / 8];
    middle.iter().map(|v| *v as u64).sum()
}

fn main() {
    let sizes = vec![1, 2, 4, 8, 16, 32, 64];

    for size_mib in sizes {
        let size = size_mib * MIB;

        println!("Running Rust exp2: {} MiB", size_mib);

        let data = vec![1u8; size];

        let copy_ms =
            benchmark(
                || {
                    std::hint::black_box(
                        copy_pipeline(&data)
                    );
                },
                10,
            );

        let view_ms =
            benchmark(
                || {
                    std::hint::black_box(
                        view_pipeline(&data)
                    );
                },
                10,
            );

        append_csv(
            "../results/exp2.csv",
            &BenchmarkRow {
                language:
                    "rust".into(),
                experiment:
                    "pipeline".into(),
                operation:
                    "copy_pipeline"
                        .into(),
                size_mib,
                median_ms:
                    copy_ms,
                throughput_mib_s:
                    size_mib as f64
                        / ((copy_ms + 1e-9)
                            / 1000.0),
            },
        );

        append_csv(
            "../results/exp2.csv",
            &BenchmarkRow {
                language:
                    "rust".into(),
                experiment:
                    "pipeline".into(),
                operation:
                    "view_pipeline"
                        .into(),
                size_mib,
                median_ms:
                    view_ms,
                throughput_mib_s:
                    size_mib as f64
                        / ((view_ms + 1e-9)
                            / 1000.0),
            },
        );
    }
}