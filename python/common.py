import csv
import statistics
import time
from pathlib import Path

MiB = 1024 * 1024

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def make_bytes(size: int) -> bytes:
    return bytes((i % 251 for i in range(size)))


def make_bytearray(size: int) -> bytearray:
    return bytearray((i % 251 for i in range(size)))


def median_ms(samples):
    return statistics.median(samples) * 1e3


def benchmark(fn, repeats=5):
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        fn()
        samples.append(time.perf_counter() - start)
    return median_ms(samples)


def append_csv(filename: str, row: dict):
    path = RESULTS_DIR / filename
    exists = path.exists()
    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        
        if not exists:
            writer.writeheader()

        writer.writerow(row)
        f.flush()