from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import LogFormatterSciNotation

plt.rcParams["font.family"] = "DejaVu Sans"

RESULTS_DIR = Path("results")

df = pd.read_csv(RESULTS_DIR / "exp1.csv")

plt.figure(figsize=(13, 7))

languages = df["language"].unique()
operations = df["operation"].unique()

language_names = {
    "python": "Python",
    "cpp": "C++",
    "rust": "Rust",
}

sizes = sorted(df["size_mib"].unique())

for language in languages:
    for operation in operations:
        subset = df[
            (df["language"] == language)
            & (df["operation"] == operation)
        ].sort_values("size_mib")

        if subset.empty:
            continue

        label = (
            f"{language_names.get(language)} — "
            f"{operation}"
        )

        plt.plot(
            subset["size_mib"],
            subset["median_ms"],
            marker="o",
            linewidth=2.5,
            markersize=8,
            label=label,
        )

plt.xscale("log", base=2)
plt.yscale("log", base=10)

plt.xticks(
    sizes,
    [f"{s} MiB" for s in sizes]
)

ax = plt.gca()

ax.yaxis.set_major_formatter(
    LogFormatterSciNotation()
)

plt.title(
    "Сравнение copy и zero-copy операций",
    fontsize=20,
    pad=20,
)

plt.xlabel(
    "Размер данных",
    fontsize=14,
)

plt.ylabel(
    "Медианная задержка (мс, log10)",
    fontsize=14,
)

plt.grid(True, which="both", alpha=0.3)

plt.legend(fontsize=11)

plt.tight_layout()

output = RESULTS_DIR / "exp1_latency_log_ru.png"

plt.savefig(output, dpi=300)

print(f"Сохранено: {output}")

plt.show()