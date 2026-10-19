"""Download the Case 4 records and their current ENA read-run records.

Run on the computer that will run PaleoRigor, from the repository root:

    python3 analysis/public_reuse_check/fetch_case4.py

Writes, for each run in selected_records.tsv:
  data/raw/public_reuse_check/ena/<run>.json      current ENA read-run record
  data/raw/public_reuse_check/fastq/<run>/*.gz    files from the catalogue's download_links
  data/raw/public_reuse_check/download_log.tsv    size and MD5 of every downloaded file
Files that already exist with the catalogued MD5 are not downloaded again.
Uses only the Python standard library and curl.
"""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RAW = ROOT / "data" / "raw" / "public_reuse_check"
ENA_FIELDS = ",".join([
    "run_accession", "study_accession", "sample_accession", "scientific_name",
    "library_layout", "library_strategy", "library_source", "instrument_platform",
    "instrument_model", "read_count", "base_count", "fastq_ftp", "fastq_bytes", "fastq_md5",
    "submitted_ftp", "submitted_bytes", "first_public", "last_updated",
])
ENA_URL = "https://www.ebi.ac.uk/ena/portal/api/filereport?accession={run}&result=read_run&fields={fields}&format=json"


def curl(url: str, dest: Path | None = None) -> bytes:
    cmd = ["curl", "-fsSL", "--retry", "5", "--retry-delay", "5", "--retry-all-errors",
           "--connect-timeout", "30"]
    if dest is not None:
        cmd += ["-C", "-", "-o", str(dest)]  # resume a partial download
    cmd.append(url)
    out = subprocess.run(cmd, check=True, capture_output=True)
    return out.stdout


def download(url: str, dest: Path, expected_md5: str, attempts: int = 5) -> str:
    """Download with resume; start again from zero if the finished file has the wrong MD5."""
    for attempt in range(1, attempts + 1):
        try:
            curl(url, dest)
        except subprocess.CalledProcessError as exc:
            print(f"    {dest.name}: curl exit {exc.returncode}, attempt {attempt}/{attempts}", flush=True)
            if exc.returncode == 33:  # server cannot resume: start again
                dest.unlink(missing_ok=True)
            time.sleep(5 * attempt)
            continue
        if md5(dest) == expected_md5:
            return "ok"
        if attempt < attempts:  # keep the last copy so a real mismatch stays on record
            print(f"    {dest.name}: MD5 differs after attempt {attempt}/{attempts}; downloading again", flush=True)
            dest.unlink(missing_ok=True)
    return "failed"


def md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    with (HERE / "selected_records.tsv").open(encoding="utf-8") as handle:
        records = list(csv.DictReader(handle, delimiter="\t"))
    (RAW / "ena").mkdir(parents=True, exist_ok=True)
    log_rows = []
    failures: list[str] = []
    for i, rec in enumerate(records, 1):
        run = rec["archive_data_accession"]
        print(f"[{i}/{len(records)}] {run} ({rec['project_name']})", flush=True)
        retrieved = datetime.now(timezone.utc).isoformat(timespec="seconds")
        ena = json.loads(curl(ENA_URL.format(run=run, fields=ENA_FIELDS)).decode("utf-8"))
        (RAW / "ena" / f"{run}.json").write_text(
            json.dumps({"retrieved_at": retrieved, "url": ENA_URL.format(run=run, fields=ENA_FIELDS),
                        "records": ena}, indent=2), encoding="utf-8")
        ena_md5 = {}
        for row in ena:
            for ftp, checksum in zip((row.get("fastq_ftp") or "").split(";"), (row.get("fastq_md5") or "").split(";")):
                if ftp:
                    ena_md5[ftp.rsplit("/", 1)[-1]] = checksum
        links = rec["download_links"].split(";")
        md5s = rec["download_md5s"].split(";")
        folder = RAW / "fastq" / run
        folder.mkdir(parents=True, exist_ok=True)
        for link, expected in zip(links, md5s):
            dest = folder / link.rsplit("/", 1)[-1]
            target = ena_md5.get(dest.name, expected)  # the archive's own checksum decides integrity
            if not (dest.exists() and md5(dest) == target):
                download("https://" + link, dest, target)
            if not dest.exists():
                failures.append(dest.name)
                print(f"    {dest.name}: NOT DOWNLOADED", flush=True)
                continue
            got = md5(dest)
            log_rows.append({
                "run": run, "file": dest.name, "url": "https://" + link,
                "bytes": dest.stat().st_size, "md5": got, "catalogue_md5": expected,
                "ena_md5": ena_md5.get(dest.name, ""),
                "md5_matches_catalogue": got == expected,
                "md5_matches_ena": got == ena_md5.get(dest.name),
                "downloaded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            })
            print(f"    {dest.name}: {dest.stat().st_size} bytes, MD5 vs ENA "
                  f"{'ok' if got == ena_md5.get(dest.name) else 'DIFFERS'}, vs catalogue {'ok' if got == expected else 'DIFFERS'}")
    with (RAW / "download_log.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(log_rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(log_rows)
    print(f"Done: {len(records)} runs, {len(log_rows)} files. Log: {(RAW / 'download_log.tsv').relative_to(ROOT)}")
    bad = [r["file"] for r in log_rows if not r["md5_matches_ena"]] + failures
    if bad:
        print("Check these files (MD5 differs from ENA or download failed; running the script again retries them): "
              + ", ".join(bad))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
