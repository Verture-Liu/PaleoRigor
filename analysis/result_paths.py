"""Locations of the archived results and figures.

Results and figures were reorganised on 14 October 2026: `Final data/` was split
into `results/` (the run folders of the dataset-level cases) and `figures/`.
The scripts below still use the original run labels ("1"-"9", "group 4-5 new",
"group 7 new", "retracted_result") as keys, so their logic is unchanged;
`results/README.md` lists the same mapping for readers of older records.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
MANUSCRIPT_FIGURES = FIGURES / "manuscript"

RUN_FOLDERS = {
    "1": RESULTS / "peptide_table_curation",
    "2": RESULTS / "sequencing_source_checks" / "ERR15682270_R1",
    "3": RESULTS / "sequencing_source_checks" / "ERR15682270_R2",
    "4": RESULTS / "earlier_runs" / "ERR10114877_R1_single_file",
    "5": RESULTS / "earlier_runs" / "ERR10114877_R2_single_file",
    "6": RESULTS / "sequencing_source_checks" / "ERR3250149",
    "7": RESULTS / "earlier_runs" / "ERR10114867_first_run",
    "8": RESULTS / "sequencing_source_checks" / "ERR10114861",
    "9": RESULTS / "sequencing_source_checks" / "ERR15682267",
    "group 4-5 new": RESULTS / "sequencing_source_checks" / "ERR10114877",
    "group 7 new": RESULTS / "sequencing_source_checks" / "ERR10114867",
    "retracted_result": RESULTS / "retraction_associated_audit",
}


def run_folder(label: str) -> Path:
    """Folder of the run that the original label referred to."""
    return RUN_FOLDERS[label]
