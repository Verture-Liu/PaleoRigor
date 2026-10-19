# Public-data reuse check (Case 4): protocol

Written on 19 October 2026, before any file was downloaded or any PaleoRigor run was made.
The selection rule, the request text, the checks, and the outcome measures below are fixed;
results are reported as they come out, including failures.

## Question

When a researcher takes small public ancient-metagenome records from a community catalogue
and hands them to PaleoRigor, how many can be reused exactly as catalogued, and does
PaleoRigor's decision for each record agree with what the files show?

## Source catalogue

AncientMetagenomeDir, host-associated metagenomes, `master` branch at commit
`0a390202e2f911fbbc37848253075023c2e13fbd` (16 October 2026), retrieved on 19 October 2026 through a web browser (the text of each raw file, saved as UTF-8;
the MD5 values are those of the saved copies):

| File | MD5 of saved copy |
| --- | --- |
| `ancientmetagenome-hostassociated_samples.tsv` | `4bc9bb0f0663a8069d219eac94d0793c` |
| `ancientmetagenome-hostassociated_libraries.tsv` | `f1bb6c9216f1f7dcc3961c32a2b45ea8` |

Copies are in `data/raw/public_reuse_check/amdir/`.

## Selection rule (`select_records.py`)

1. Join libraries to samples on project, sample name, and sample accession.
2. Keep libraries archived at ENA or SRA, with download links and a recorded sample age.
3. Keep libraries whose catalogued FASTQ files total 3–50 MB (download_sizes).
4. Keep one library per project: the smallest, ties broken by run accession.

This gives 17 records (`selected_records.tsv`). No record is added or removed by hand.

## Steps for each record (`run_case4.py`)

1. **Public record.** Retrieve the current ENA read-run record (read count, base count,
   library layout, FASTQ file names, sizes, and MD5 checksums).
2. **Download.** Download every FASTQ file listed in the catalogue's `download_links` over HTTPS
   and compute its size and MD5 checksum. Files are not renamed, decompressed, or changed.
3. **PaleoRigor.** In the PaleoRigor application (v0.2.1 code in this repository, with the
   planning model configured in the application), the author creates one task per record,
   uploads all downloaded files of that record, and sends one fixed request
   (`RUN_SHEET.md` gives the exact text for each record):
   - catalogue layout PAIRED: *"The uploaded FASTQ files were downloaded for ENA run {run}
     ({project}), which AncientMetagenomeDir lists as a paired-end library. Detect the file
     types, confirm the mate pairing, run FastQC, summarise the reports with MultiQC, and write
     a data quality gate report. Do not trim, filter, or otherwise change the reads."*
   - catalogue layout SINGLE: *"The uploaded FASTQ files were downloaded for ENA run {run}
     ({project}), which AncientMetagenomeDir lists as a single-end library. Detect the file
     types, run FastQC, summarise the reports with MultiQC, and write a data quality gate
     report. Do not trim, filter, or otherwise change the reads."*
4. **Expert review.** The author reads each plan and approves or rejects it before execution,
   as in normal use. Plans are not edited. Results are exported to
   `results/public_reuse_check/`. Blocked decisions, invalid plans, and rejections, which
   export nothing, are kept as screenshots of PaleoRigor's message in the same folder and
   transcribed verbatim by the summary script's author.

## Checks (`summarize_case4.py`)

| Check | Passes when |
| --- | --- |
| C1 Catalogue files = ENA | catalogue MD5 checksums and sizes equal the current ENA values for the same files |
| C2 Catalogue reads = ENA | catalogue `read_count` equals the current ENA `read_count` |
| C3 Download intact | the MD5 of every downloaded file equals the ENA value |
| C4 Layout consistent | catalogue layout equals ENA `library_layout`, and the file set fits it (single-end: one file without a mate suffix; paired-end: exactly one `_1` and one `_2` file) |
| C5 Reads reproduced | the FastQC total sequences in PaleoRigor's output equal the ENA `read_count` for every mate file; not evaluated when PaleoRigor did not run |
| C6 Processing state (descriptive) | from FastQC sequence lengths: a single read length in every file of an Illumina run is recorded as *unprocessed*; a range of lengths as *length-variable* (adapter-trimmed, quality-trimmed, or merged before deposition); 454 and Ion Torrent runs, whose raw reads vary in length, are recorded as *not assessable* |

## Outcome measures

- **Primary:** the percentage of records that pass C1–C5 (reusable exactly as catalogued),
  with a 95% Wilson interval. A record that was not run by PaleoRigor does not pass C5.
- **PaleoRigor outcome:** the number of records executed, blocked (with reason code), with an
  invalid plan, failed in execution, or rejected at review.
- **Processing state:** the percentage of assessable records whose deposited reads are
  length-variable, that is, already processed and not directly comparable with raw reads
  from another study. C6 does not enter the primary measure, because a processed deposit can
  still be the correct record.
- **Agreement with the file evidence:** the percentage of records for which PaleoRigor's
  decision matches C4, that is, it executed a record with a consistent layout, or it blocked
  or flagged a record with an inconsistent one.
- **Descriptive only:** mean read length and GC content from FastQC, plotted against sample age
  and material. With 17 records and one library per project, no trend is tested or claimed.
