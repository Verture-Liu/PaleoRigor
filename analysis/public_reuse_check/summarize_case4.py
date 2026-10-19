"""Summarize the public-data reuse check (Case 4) as fixed in PROTOCOL.md.

Inputs (all in the repository):
  analysis/public_reuse_check/selected_records.tsv     catalogue rows (AncientMetagenomeDir)
  data/raw/public_reuse_check/ena/<run>.json            ENA read-run records
  data/raw/public_reuse_check/download_log.tsv          size and MD5 of the downloaded files
  data/raw/public_reuse_check/fastq/<run>/              the downloaded files
  results/public_reuse_check/ResearchAgent_Result_*/    PaleoRigor exports (executed runs)
  results/public_reuse_check/<run>.jpg                  screenshots of refused requests
  analysis/public_reuse_check/refusals.tsv              the refusal messages, transcribed

Outputs (analysis/public_reuse_check/source_data/):
  case4_records.csv   one row per record: checks C1-C6 and PaleoRigor's outcome
  case4_files.csv     one row per FASTQ file: ENA, download, and PaleoRigor values
  case4_summary.json  counts, percentages, and 95% Wilson intervals
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RAW = ROOT / "data" / "raw" / "public_reuse_check"
RESULTS = ROOT / "results" / "public_reuse_check"
OUT = HERE / "source_data"
MATE = re.compile(r"_(1|2)\.f(ast)?q(\.gz)?$")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def wilson(k: int, n: int, z: float = 1.959964) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (max(0.0, centre - half), min(1.0, centre + half))


def fastqc_values(zip_path: Path) -> dict:
    with zipfile.ZipFile(zip_path) as archive:
        name = next(n for n in archive.namelist() if n.endswith("fastqc_data.txt"))
        text = archive.read(name).decode("utf-8")
    values = {}
    for line in text.splitlines():
        for key in ("Total Sequences", "Sequence length", "%GC", "Filename"):
            if line.startswith(key + "\t"):
                values[key] = line.split("\t", 1)[1]
    return values


def file_name(ref: str) -> str:
    return ref.rsplit("/", 1)[-1]


def main() -> int:
    with (HERE / "selected_records.tsv").open(encoding="utf-8") as handle:
        catalogue = list(csv.DictReader(handle, delimiter="\t"))
    with (RAW / "download_log.tsv").open(encoding="utf-8") as handle:
        downloads = {row["file"]: row for row in csv.DictReader(handle, delimiter="\t")}
    refusals = {}
    if (HERE / "refusals.tsv").exists():
        with (HERE / "refusals.tsv").open(encoding="utf-8") as handle:
            refusals = {row["run"]: row for row in csv.DictReader(handle, delimiter="\t")}

    # PaleoRigor exports, keyed by run accession from the uploaded file names in the run record
    exports = {}
    for folder in sorted(RESULTS.glob("ResearchAgent_Result_*")):
        manifest = json.loads((folder / "ResearchAgent Records" / "manifest.json").read_text(encoding="utf-8"))
        runs = {re.sub(r"_(1|2)$", "", re.sub(r"\.f(ast)?q(\.gz)?$", "", i["ref"])) for i in manifest["inputs"]}
        assert len(runs) == 1, (folder.name, runs)
        run = runs.pop()
        assert run not in exports, ("two exports for", run)
        exports[run] = (folder, manifest)

    record_rows, file_rows = [], []
    for rec in catalogue:
        run = rec["archive_data_accession"]
        ena = json.loads((RAW / "ena" / f"{run}.json").read_text(encoding="utf-8"))["records"]
        assert len(ena) == 1, run
        ena = ena[0]
        ena_files = [file_name(f) for f in ena["fastq_ftp"].split(";") if f]
        ena_md5 = dict(zip(ena_files, ena["fastq_md5"].split(";")))
        ena_bytes = dict(zip(ena_files, (int(b) for b in ena["fastq_bytes"].split(";"))))
        cat_files = [file_name(f) for f in rec["download_links"].split(";")]
        cat_md5 = dict(zip(cat_files, rec["download_md5s"].split(";")))
        cat_bytes = dict(zip(cat_files, (int(b) for b in rec["download_sizes"].split(";"))))

        c1 = set(cat_files) == set(ena_files) and all(
            cat_md5[f] == ena_md5.get(f) and cat_bytes[f] == ena_bytes.get(f) for f in cat_files)
        c2 = int(rec["read_count"]) == int(ena["read_count"])
        c3 = all(downloads[f]["md5"] == ena_md5.get(f) for f in cat_files)
        mates = sorted(f for f in cat_files if MATE.search(f))
        unsuffixed = [f for f in cat_files if not MATE.search(f)]
        layout = rec["library_layout"]
        if layout == "SINGLE":
            fits = len(cat_files) == 1 and not mates
        else:
            fits = len(cat_files) == 2 and len(mates) == 2
        c4 = layout == ena["library_layout"] and fits

        executed = run in exports
        outcome = "executed" if executed else ("blocked" if run in refusals else "not_run")
        reason = refusals.get(run, {}).get("reason_code", "")
        message = refusals.get(run, {}).get("message", "")
        uploaded_identical = ""
        per_file = {}
        if executed:
            folder, manifest = exports[run]
            uploaded = {file_name(i["path"]): i["sha256"] for i in manifest["inputs"]}
            uploaded_identical = all(
                uploaded.get(f) == sha256(RAW / "fastq" / run / f) for f in cat_files) and set(uploaded) == set(cat_files)
            gate = json.loads((folder / "final_outputs" / "data_quality_gate_report.json").read_text(encoding="utf-8"))
            gate_by_name = {g["name"]: g for g in gate["files"]}
            for f in cat_files:
                stem = re.sub(r"\.f(ast)?q(\.gz)?$", "", f)
                fq = fastqc_values(folder / "final_outputs" / f"{stem}_fastqc.zip")
                g = gate_by_name[f]
                per_file[f] = {"fastqc_total_sequences": int(fq["Total Sequences"]),
                               "fastqc_sequence_length": fq["Sequence length"],
                               "fastqc_gc_percent": float(fq["%GC"]),
                               "gate_records": g["records"], "gate_total_bases": g["total_bases"],
                               "min_length": g["min_length"], "max_length": g["max_length"],
                               "mean_length": g["mean_length"], "gate_passed": gate["gate_passed"]}
            pair_steps = list(folder.glob("step_outputs/step_*_fastq_pair_match/fastq_pair_report.json"))
            paired_ids = []
            for p in pair_steps:
                for s in json.loads(p.read_text(encoding="utf-8"))["samples"]:
                    paired_ids.append((s["layout"], file_name(s["fastq_1"]), file_name(s.get("fastq_2") or "")))
        reads = int(ena["read_count"])
        if executed:
            check_files = mates if layout == "PAIRED" and mates else cat_files
            c5 = all(per_file[f]["fastqc_total_sequences"] == reads for f in check_files)
        else:
            c5 = False
        # C6: processing state from read lengths (Illumina only)
        if ena["instrument_platform"] != "ILLUMINA":
            c6 = "not_assessable"
        elif not executed:
            c6 = "not_run"
        else:
            c6 = "unprocessed" if all(per_file[f]["min_length"] == per_file[f]["max_length"] for f in cat_files) \
                else "length_variable"
        # PaleoRigor decision agrees with C4
        if executed and c4:
            agreement, agreement_note = True, "executed a record with a consistent layout"
        elif not executed and not c4:
            agreement, agreement_note = True, "blocked a record with an inconsistent layout"
        elif executed and not c4 and unsuffixed and mates:
            # the plan named the extra file as unpaired and kept it out of the mate pair
            kept_out = executed and all(u not in {a for _, a, b in paired_ids} | {b for _, a, b in paired_ids} for u in unsuffixed)
            agreement, agreement_note = kept_out, "executed; the unpaired file was kept out of the mate pair" if kept_out else \
                "executed; the extra file was paired"
        else:
            agreement, agreement_note = False, "decision does not match the layout check"

        record_rows.append({
            "run": run, "project": rec["project_name"], "material": rec["material"], "host": rec["sample_host"],
            "sample_age_bp": int(float(rec["sample_age"])), "country": rec["geo_loc_name"],
            "platform": ena["instrument_platform"], "instrument": ena["instrument_model"],
            "catalogue_layout": layout, "ena_layout": ena["library_layout"],
            "n_files": len(cat_files), "files": ";".join(cat_files),
            "catalogue_read_count": int(rec["read_count"]), "ena_read_count": reads,
            "ena_base_count": int(ena["base_count"]),
            "catalogue_total_bytes": sum(cat_bytes.values()), "ena_total_bytes": sum(ena_bytes.values()),
            "C1_catalogue_files_equal_ena": c1, "C2_catalogue_reads_equal_ena": c2,
            "C3_download_intact": c3, "C4_layout_consistent": c4, "C5_reads_reproduced": c5,
            "reusable_as_catalogued": all([c1, c2, c3, c4, c5]),
            "C6_processing_state": c6,
            "paleorigor_outcome": outcome, "paleorigor_reason_code": reason, "paleorigor_message": message,
            "uploaded_files_identical_to_download": uploaded_identical,
            "decision_agrees_with_C4": agreement, "agreement_note": agreement_note,
            "result_folder": rel(exports[run][0]) if executed else "",
            "evidence": rel(RESULTS / f"{run}.jpg") if not executed and (RESULTS / f"{run}.jpg").exists() else "",
        })
        for f in cat_files:
            row = {"run": run, "file": f, "catalogue_bytes": cat_bytes[f], "ena_bytes": ena_bytes.get(f, ""),
                   "downloaded_bytes": int(downloads[f]["bytes"]), "catalogue_md5": cat_md5[f],
                   "ena_md5": ena_md5.get(f, ""), "downloaded_md5": downloads[f]["md5"],
                   "ena_read_count": reads}
            row.update(per_file.get(f, {}))
            file_rows.append(row)

    OUT.mkdir(exist_ok=True)
    for name, rows in (("case4_records.csv", record_rows), ("case4_files.csv", file_rows)):
        fields = list(dict.fromkeys(k for r in rows for k in r))
        with (OUT / name).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    n = len(record_rows)
    def share(key, value=True, rows=record_rows):
        k = sum(1 for r in rows if r[key] == value)
        lo, hi = wilson(k, len(rows))
        return {"k": k, "n": len(rows), "percent": round(100 * k / len(rows), 1),
                "wilson95": [round(100 * lo, 1), round(100 * hi, 1)]}
    assessable = [r for r in record_rows if r["C6_processing_state"] in ("unprocessed", "length_variable")]
    summary = {
        "records": n,
        "primary_reusable_as_catalogued": share("reusable_as_catalogued"),
        "checks": {k: share(k) for k in ["C1_catalogue_files_equal_ena", "C2_catalogue_reads_equal_ena",
                                         "C3_download_intact", "C4_layout_consistent", "C5_reads_reproduced"]},
        "processing_state_counts": {s: sum(1 for r in record_rows if r["C6_processing_state"] == s)
                                    for s in ("unprocessed", "length_variable", "not_assessable", "not_run")},
        "length_variable_among_assessable": share("C6_processing_state", "length_variable", assessable),
        "paleorigor_outcomes": {o: sum(1 for r in record_rows if r["paleorigor_outcome"] == o)
                                for o in ("executed", "blocked", "not_run")},
        "decision_agrees_with_C4": share("decision_agrees_with_C4"),
        "uploaded_files_identical_to_download": sum(1 for r in record_rows if r["uploaded_files_identical_to_download"] is True),
    }
    (OUT / "case4_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
