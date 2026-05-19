from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams["font.family"] = "DejaVu Sans"

RESULTS_DIR = Path("results")

df = pd.read_csv(RESULTS_DIR / "exp3.csv")

languages = df["language"].unique()

fig, axes = plt.subplots(
    1,
    len(languages),
    figsize=(16, 6),
    sharey=True,
)

if len(languages) == 1:
    axes = [axes]

language_names = {
    "python": "Python",
    "cpp": "C++",
    "rust": "Rust",
}

sizes = sorted(df["size_mib"].unique())

for ax, language in zip(axes, languages):
    subset = df[df["language"] == language]

    subset = subset.sort_values("size_mib")

    ax.plot(
        subset["size_mib"],
        subset["copy_rss_delta"],
        marker="o",
        linewidth=3,
        markersize=8,
        label="Копии",
    )

    ax.plot(
        subset["size_mib"],
        subset["view_rss_delta"],
        marker="o",
        linewidth=3,
        markersize=8,
        label="Views",
    )

    ax.set_xscale("log", base=2)

    ax.set_xticks(sizes)

    ax.set_xticklabels(
        [f"{s} MiB" for s in sizes]
    )

    ax.set_title(
        language_names.get(language),
        fontsize=16,
    )

    ax.set_xlabel(
        "Размер буфера",
        fontsize=12,
    )

    ax.grid(True, which="both", alpha=0.3)

axes[0].set_ylabel(
    "Рост RSS памяти (MiB)",
    fontsize=12,
)

handles, labels = axes[0].get_legend_handles_labels()

fig.legend(
    handles,
    labels,
    loc="upper center",
    ncol=2,
    fontsize=12,
)

fig.suptitle(
    "Сравнение удержания копий и views",
    fontsize=20,
)

plt.tight_layout(rect=[0, 0, 1, 0.92])

output = RESULTS_DIR / "exp3_memory_log_ru.png"

plt.savefig(output, dpi=300)

print(f"Сохранено: {output}")

plt.show()