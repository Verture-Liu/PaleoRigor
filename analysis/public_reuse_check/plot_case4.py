"""Figure 6: public-data reuse check (Case 4). Reads only the source data written by summarize_case4.py."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SRC = HERE / "source_data"
OUT = ROOT / "figures" / "manuscript" / "public_reuse_check"

COLORS = {
    "ink": "#1f2933", "muted": "#687282", "grid": "#e1e7ec", "panel": "#f8fafb",
    "blue": "#2f6f8f", "blue_light": "#eaf4f6", "green": "#4f8b6b", "green_light": "#edf7f1",
    "orange": "#c46a4a", "orange_light": "#fbefe9", "gold": "#d9a84e", "gold_light": "#fbf4df",
    "purple": "#7566a4",
}
CHECKS = [
    ("C1_catalogue_files_equal_ena", "C1\nCatalogue\nfiles = ENA"),
    ("C2_catalogue_reads_equal_ena", "C2\nCatalogue\nreads = ENA"),
    ("C3_download_intact", "C3\nDownload\nintact (MD5)"),
    ("C4_layout_consistent", "C4\nLayout\nconsistent"),
    ("C5_reads_reproduced", "C5\nReads\nreproduced"),
    ("reusable_as_catalogued", "Reusable\nas\ncatalogued"),
]
STATE = {"unprocessed": ("Single read length", COLORS["blue"], "o"),
         "length_variable": ("Length-variable", COLORS["orange"], "D"),
         "not_assessable": ("454 / Ion Torrent", COLORS["muted"], "s")}


def set_style() -> None:
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans", "sans-serif"],
        "svg.fonttype": "none", "pdf.fonttype": 42, "font.size": 8.0,
        "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.7,
        "axes.edgecolor": COLORS["ink"], "xtick.color": COLORS["ink"], "ytick.color": COLORS["ink"],
        "text.color": COLORS["ink"], "figure.facecolor": "white", "axes.facecolor": "white",
        "savefig.facecolor": "white",
    })


def panel_label(ax: plt.Axes, label: str, x: float = -0.02) -> None:
    ax.text(x, 1.02, label, transform=ax.transAxes, fontsize=12, fontweight="bold", va="bottom", ha="left")


REASONS = [  # short label, legend label, colour
    ("ENA count = both mates", "ENA read count covers both mates", COLORS["gold"]),
    ("one file, listed paired-end", "one file for a paired-end library", COLORS["orange"]),
    ("extra unpaired-read file", "extra unpaired-read file", COLORS["purple"]),
    ("catalogue entry differs from ENA", "catalogue file entry differs from ENA", COLORS["blue"]),
]


def failure_reason(r: pd.Series) -> str:
    reasons = []
    if not r.C1_catalogue_files_equal_ena:
        reasons.append(REASONS[3][0])
    if not r.C4_layout_consistent and r.n_files == 1:
        reasons.append(REASONS[1][0])
    if not r.C4_layout_consistent and r.n_files > 2:
        reasons.append(REASONS[2][0])
    if r.C4_layout_consistent and not r.C5_reads_reproduced and r.mate_ratio == 2:
        reasons.append(REASONS[0][0])
    return "; ".join(reasons)


def load() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    rec = pd.read_csv(SRC / "case4_records.csv")
    files = pd.read_csv(SRC / "case4_files.csv")
    summary = json.loads((SRC / "case4_summary.json").read_text(encoding="utf-8"))
    run_files = files.dropna(subset=["gate_records"]).copy()
    run_files["len_x_reads"] = run_files["mean_length"] * run_files["gate_records"]
    agg = run_files.groupby("run").agg(reads=("gate_records", "sum"), lx=("len_x_reads", "sum"),
                                       mate_max=("gate_records", "max"), gc=("fastqc_gc_percent", "mean"))
    agg["mean_length"] = agg["lx"] / agg["reads"]
    rec = rec.merge(agg[["mean_length", "mate_max", "gc"]], left_on="run", right_index=True, how="left")
    rec["mate_ratio"] = rec["ena_read_count"] / rec["mate_max"]
    rec["reason"] = rec.apply(failure_reason, axis=1)
    rec = rec.sort_values(["sample_age_bp", "run"]).reset_index(drop=True)
    return rec, files, summary


def draw_matrix(ax: plt.Axes, rec: pd.DataFrame) -> None:
    n = len(rec)
    ax.set_xlim(0, 1)
    ax.set_ylim(n + 2.4, -0.2)
    ax.axis("off")
    x_detail, x0, dx = 0.113, 0.442, 0.041
    heads = ["C1", "C2", "C3", "C4", "C5", "Reusable"]
    x_last = x0 + dx * (len(CHECKS) - 1) + 0.012  # the "Reusable" column sits a little apart
    x_agent = x_last + 0.085
    x_reason = x_agent + 0.075
    xs = [x0 + dx * j for j in range(len(CHECKS) - 1)] + [x_last]
    for j, title in enumerate(heads):
        ax.text(xs[j], 0.75, title, ha="center", va="center", fontsize=6.6, fontweight="bold",
                color=COLORS["ink"] if j == len(heads) - 1 else COLORS["muted"])
    ax.text(x_agent, 0.75, "PaleoRigor", ha="center", va="center", fontsize=6.6, fontweight="bold", color=COLORS["muted"])
    ax.text(x_reason, 0.75, "What did not match", ha="left", va="center", fontsize=6.6, fontweight="bold",
            color=COLORS["muted"])
    ax.text(0.0, 0.75, "Run", ha="left", va="center", fontsize=6.6, fontweight="bold", color=COLORS["muted"])
    ax.text(x_detail, 0.75, "Project · material · age (years)", ha="left", va="center", fontsize=6.6,
            fontweight="bold", color=COLORS["muted"])
    ax.plot([0, 1], [1.25, 1.25], color=COLORS["grid"], lw=0.8)
    for i, r in rec.iterrows():
        y = i + 1.85
        if i % 2 == 0:
            ax.add_patch(FancyBboxPatch((0.0, y - 0.47), 1.0, 0.94, boxstyle="square,pad=0", fc="#f6f8fa", ec="none"))
        ax.text(0.0, y, r.run, ha="left", va="center", fontsize=6.2, fontweight="bold")
        ax.text(x_detail, y, f"{r.project} · {r.material} · {r.sample_age_bp:,}", ha="left", va="center", fontsize=6.1)
        for j, (col, _) in enumerate(CHECKS):
            ok = bool(r[col])
            not_run = col == "C5_reads_reproduced" and r.paleorigor_outcome != "executed"
            if not_run:
                fc, ec, sym, sc = "#ffffff", COLORS["grid"], "–", COLORS["muted"]
            elif ok:
                fc, ec, sym, sc = COLORS["green_light"], "#c9e6d3", "✓", COLORS["green"]
            else:
                fc, ec, sym, sc = COLORS["orange_light"], "#f0cdbf", "✗", COLORS["orange"]
            w = 0.031
            ax.add_patch(FancyBboxPatch((xs[j] - w / 2, y - 0.36), w, 0.72,
                                        boxstyle="round,pad=0,rounding_size=0.008", fc=fc, ec=ec, lw=0.6))
            ax.text(xs[j], y, sym, ha="center", va="center", fontsize=7.2, color=sc, fontweight="bold",
                    fontfamily="DejaVu Sans")
        if r.paleorigor_outcome == "executed":
            ax.text(x_agent, y, "executed", ha="center", va="center", fontsize=6.3, color=COLORS["blue"])
        else:
            ax.text(x_agent, y, "blocked", ha="center", va="center",
                    fontsize=6.3, color=COLORS["orange"], fontweight="bold")
        if r.reason:
            ax.text(x_reason, y, r.reason, ha="left", va="center", fontsize=6.0, color=COLORS["orange"])
    ax.text(0.0, n + 1.55, "✓ passed   ✗ failed   – not evaluated (no PaleoRigor output).   blocked: refused before execution (missing_mate).   "
            "Records ordered by sample age.",
            ha="left", va="center", fontsize=6.2, color=COLORS["muted"], fontfamily="DejaVu Sans")
    ax.text(0.0, n + 2.2, "C1 catalogue files and sizes = ENA   C2 catalogue read count = ENA   C3 downloaded MD5 = ENA   "
                          "C4 layout consistent   C5 FastQC reads per mate = ENA read count",
            ha="left", va="center", fontsize=6.2, color=COLORS["muted"])


def draw_summary(ax: plt.Axes, rec: pd.DataFrame, summary: dict) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    n = summary["records"]
    p = summary["primary_reusable_as_catalogued"]
    ax.text(0.0, 0.97, "Records reusable exactly as catalogued", fontsize=7.6, fontweight="bold", va="top")
    ax.text(0.0, 0.89, f"{p['k']} of {n} ({p['percent']:.1f}%; Wilson 95% CI, {p['wilson95'][0]:.1f}–{p['wilson95'][1]:.1f}%)",
            fontsize=7.2, color=COLORS["muted"], va="top")
    # stacked bar: reusable, then each failure reason
    counts = [("Reusable as catalogued", int((rec.reason == "").sum()), COLORS["green"])]
    for short, label, color in REASONS:
        counts.append((label, int((rec.reason == short).sum()), color))
    assert sum(c for _, c, _ in counts) == n, counts
    left, y0, h = 0.0, 0.66, 0.11
    for label, c, color in counts:
        if c:
            ax.add_patch(FancyBboxPatch((left, y0), c / n, h, boxstyle="square,pad=0", fc=color, ec="white", lw=1.0))
            ax.text(left + c / n / 2, y0 + h / 2, str(c), ha="center", va="center", fontsize=7.4, color="white",
                    fontweight="bold")
            left += c / n
    for k, (label, c, color) in enumerate(counts):
        yy = 0.56 - k * 0.068
        ax.add_patch(FancyBboxPatch((0.0, yy - 0.022), 0.03, 0.044, boxstyle="square,pad=0", fc=color, ec="none"))
        ax.text(0.045, yy, f"{label} ({c})", va="center", fontsize=6.8)
    a = summary["decision_agrees_with_C4"]
    lv = summary["length_variable_among_assessable"]
    ax.text(0.0, -0.02, f"PaleoRigor decision matched the layout check in {a['k']} of {a['n']} records.\n"
                       f"Reads were length-variable (processed before deposition) in {lv['k']} of {lv['n']}\n"
                       f"assessable Illumina records.",
            fontsize=6.7, color=COLORS["muted"], va="bottom", linespacing=1.3)


def draw_lengths(ax: plt.Axes, rec: pd.DataFrame) -> None:
    run = rec.dropna(subset=["mean_length"])
    for state, (label, color, marker) in STATE.items():
        sub = run[run.C6_processing_state == state]
        ax.scatter(sub.sample_age_bp, sub.mean_length, s=26, color=color, marker=marker, edgecolor="white",
                   linewidth=0.5, zorder=3, label=f"{label} ({len(sub)})")
    ax.set_xscale("log")
    ax.set_xlabel("Sample age (years before present, log scale)")
    ax.set_ylabel("Mean read length (bp)")
    ax.grid(color=COLORS["grid"], lw=0.6, zorder=0)
    ax.set_ylim(0, max(run.mean_length) * 1.12)
    ax.legend(frameon=False, fontsize=6.6, loc="upper right", handletextpad=0.3, borderaxespad=0.2)
    ax.text(1.0, -0.30, "Descriptive only: one library per project; executed records only.", transform=ax.transAxes,
            ha="right", fontsize=6.4, color=COLORS["muted"])


def save(fig: mpl.figure.Figure, stem: Path) -> None:
    stem.parent.mkdir(parents=True, exist_ok=True)
    for ext in (".png", ".pdf", ".svg"):
        kwargs = {"dpi": 360} if ext == ".png" else {}
        fig.savefig(stem.with_suffix(ext), bbox_inches="tight", **kwargs)


def main() -> None:
    set_style()
    rec, _files, summary = load()
    fig = plt.figure(figsize=(7.3, 7.6))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.6, 1.0], width_ratios=[1.0, 1.0], hspace=0.28, wspace=0.28)
    ax_a = fig.add_subplot(gs[0, :])
    ax_b = fig.add_subplot(gs[1, 0])
    ax_c = fig.add_subplot(gs[1, 1])
    draw_matrix(ax_a, rec)
    draw_summary(ax_b, rec, summary)
    draw_lengths(ax_c, rec)
    panel_label(ax_a, "A")
    panel_label(ax_b, "B")
    panel_label(ax_c, "C", x=-0.2)
    save(fig, OUT / "figure6_public_reuse_check")
    rec.to_csv(OUT / "figure6_source_data.csv", index=False)
    print("written", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
