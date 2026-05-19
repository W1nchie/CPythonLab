import numpy as np

from common import MiB, append_csv, benchmark, make_bytes

sizes = [1, 2, 4, 8, 16, 32, 64, 128]

for size_mib in sizes:
    size = size_mib * MiB

    data = make_bytes(size)
    mutable = bytearray(data)
    view = memoryview(mutable)
    np_view = np.frombuffer(mutable, dtype=np.uint8)

    cases = [
        ("bytes_copy", lambda: data[:]),
        ("memoryview", lambda: memoryview(mutable)),
        ("memoryview_slice", lambda: view[1:]),
        ("numpy_frombuffer", lambda: np.frombuffer(mutable, dtype=np.uint8)),
        ("numpy_copy", lambda: np.array(np_view, copy=True)),
    ]

    for name, fn in cases:
        ms = benchmark(fn)
        append_csv(
            "exp1.csv",
            {
                "language": "python",
                "experiment": "copy_vs_view",
                "operation": name,
                "size_mib": size_mib,
                "median_ms": ms,
                "throughput_mib_s": size_mib / (ms / 1e3),
            },
        )