"""Select the public records for the public-data reuse check (Case 4).

The rule is fixed in PROTOCOL.md and applied here without manual choice:
AncientMetagenomeDir host-associated libraries joined to their samples,
archive ENA or SRA, a download link and a sample age present,
total compressed FASTQ size 3-50 MB, and one library per project
(the smallest; ties broken by run accession).
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
AMDIR = ROOT / "data" / "raw" / "public_reuse_check" / "amdir"
SAMPLES = AMDIR / "ancientmetagenome-hostassociated_samples.tsv"
LIBRARIES = AMDIR / "ancientmetagenome-hostassociated_libraries.tsv"
OUT = Path(__file__).resolve().parent / "selected_records.tsv"

MIN_BYTES, MAX_BYTES = 3_000_000, 50_000_000


def total_bytes(value: object) -> int | None:
    try:
        return sum(int(v) for v in str(value).split(";"))
    except ValueError:
        return None


def select() -> pd.DataFrame:
    samples = pd.read_csv(SAMPLES, sep="\t", dtype=str)
    libraries = pd.read_csv(LIBRARIES, sep="\t", dtype=str)
    samples = samples.assign(acc=samples["archive_accession"].str.split(",")).explode("acc")
    keep = ["project_name", "sample_name", "acc", "sample_host", "sample_age", "community_type",
            "material", "geo_loc_name", "site_name", "publication_doi"]
    joined = libraries.merge(
        samples[keep],
        left_on=["project_name", "sample_name", "archive_sample_accession"],
        right_on=["project_name", "sample_name", "acc"],
        how="left",
    )
    joined["total_bytes"] = joined["download_sizes"].map(total_bytes)
    joined["age"] = pd.to_numeric(joined["sample_age"], errors="coerce")
    base = joined[
        joined["archive"].isin(["ENA", "SRA"])
        & joined["download_links"].notna()
        & joined["age"].notna()
        & joined["total_bytes"].between(MIN_BYTES, MAX_BYTES)
    ]
    chosen = (
        base.sort_values(["total_bytes", "archive_data_accession"])
        .groupby("project_name")
        .head(1)
        .sort_values(["age", "archive_data_accession"])
        .reset_index(drop=True)
    )
    return chosen.drop(columns=["acc"])


def main() -> int:
    for path in (SAMPLES, LIBRARIES):
        print(path.name, hashlib.md5(path.read_bytes()).hexdigest())
    chosen = select()
    chosen.to_csv(OUT, sep="\t", index=False)
    print(f"{len(chosen)} records written to {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
