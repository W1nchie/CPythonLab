import gc
import psutil

from common import MiB, append_csv, make_bytearray

process = psutil.Process()

sizes = [1, 2, 4, 8, 16, 32, 64, 128]

for size_mib in sizes:
    size = size_mib * MiB
    base = make_bytearray(size)

    gc.collect()
    rss_before = process.memory_info().rss / MiB

    copies = [bytearray(base) for _ in range(6)]
    gc.collect()
    rss_after_copy = (process.memory_info().rss / MiB)

    del copies
    gc.collect()

    views = [memoryview(base) for _ in range(6)]
    rss_after_view = (process.memory_info().rss / MiB)

    append_csv(
        "exp3.csv",
        {
            "language": "python",
            "experiment": "memory_pressure",
            "size_mib": size_mib,
            "copy_rss_delta": rss_after_copy - rss_before,
            "view_rss_delta": rss_after_view - rss_before,
        },
    )