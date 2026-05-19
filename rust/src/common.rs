use csv::WriterBuilder;
use serde::Serialize;
use std::fs::OpenOptions;
use std::time::Instant;

pub const MIB: usize = 1024 * 1024;

#[derive(Serialize)]
pub struct BenchmarkRow {
    pub language: String,
    pub experiment: String,
    pub operation: String,
    pub size_mib: usize,
    pub median_ms: f64,
    pub throughput_mib_s: f64,
}

pub fn benchmark<F>(mut f: F, repeats: usize) -> f64
where
    F: FnMut(),
{
    let mut samples = Vec::new();

    for _ in 0..repeats {
        let start = Instant::now();

        f();

        let elapsed =
            start.elapsed().as_secs_f64() * 1000.0;

        samples.push(elapsed);
    }

    samples.sort_by(|a, b| a.partial_cmp(b).unwrap());

    samples[samples.len() / 2]
}

pub fn append_csv(
    filename: &str,
    row: &BenchmarkRow,
) {
    let file = OpenOptions::new()
        .append(true)
        .create(true)
        .open(filename)
        .unwrap();

    let mut writer = WriterBuilder::new()
        .has_headers(false)
        .from_writer(file);

    writer.serialize(row).unwrap();

    writer.flush().unwrap();
}

#[derive(Serialize)]
pub struct MemoryRow {
    pub language: String,
    pub experiment: String,
    pub size_mib: usize,
    pub copy_rss_delta: f64,
    pub view_rss_delta: f64,
}

pub fn append_csv2<T>(
    filename: &str,
    row: &T,
)
where
    T: Serialize,
{
    let file = OpenOptions::new()
        .append(true)
        .create(true)
        .open(filename)
        .unwrap();

    let mut writer =
        WriterBuilder::new()
            .has_headers(false)
            .from_writer(file);

    writer
        .serialize(row)
        .unwrap();

    writer.flush().unwrap();
}