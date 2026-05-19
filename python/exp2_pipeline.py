import numpy as np

from common import MiB, append_csv, benchmark, make_bytes

HEADER = 64
sizes = [1, 2, 4, 8, 16, 32, 64]


def copy_pipeline(packet, body_size):
    payload = packet[HEADER:HEADER + body_size]
    middle = payload[body_size // 4:]
    copied = bytearray(middle)
    arr = np.frombuffer(copied, dtype=np.uint8).copy()
    return int(arr.sum())


def view_pipeline(packet, body_size):
    view = memoryview(packet)
    payload = view[HEADER:HEADER + body_size]
    middle = payload[body_size // 4:]
    arr = np.frombuffer(middle, dtype=np.uint8)
    return int(arr.sum())


for size_mib in sizes:
    body_size = size_mib * MiB
    packet = make_bytes(body_size + HEADER)

    for name, fn in [
        ("copy_pipeline", lambda: copy_pipeline(packet, body_size)),
        ("view_pipeline", lambda: view_pipeline(packet, body_size)),
    ]:
        ms = benchmark(fn)

        append_csv(
            "exp2.csv",
            {
                "language": "python",
                "experiment": "pipeline",
                "operation": name,
                "size_mib": size_mib,
                "median_ms": ms,
                "throughput_mib_s": size_mib / (ms / 1e3),
            },
        )