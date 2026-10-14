# Changelog

## Unreleased

Repository and documentation clean-up; analysis code, prompts, data and run records are unchanged.

### Added
- `README.md` at the repository root: what PaleoRigor does, downloads, running from source, repository layout and how to cite the preprint (doi:10.64898/2026.09.30.755547).
- A link to the bioRxiv preprint on the website home page, and a `preferred-citation` entry in `CITATION.cff`.

### Changed
- `CITATION.cff` and `.zenodo.json` use the manuscript title; `CITATION.cff` lists the v0.2.2 archive DOI.
- The desktop interface, its report pages, the folder-picker dialog and the user guides use the name PaleoRigor instead of "Research Agent".
- The website test checks the frozen-evaluation figures now shown on the home page (23/24, 24/24, 96/96, 6/6).
- `paleorigor/README.md` describes the current macOS and Windows builds and uses the tools' own names (seqtk, Bowtie 2).
- Preregistrations, study plans and questions moved from `docs/science-superpowers/` to `study/`; development plans and notes moved from `docs/superpowers/` and `docs/research/` to `dev-notes/`, so the website folder holds only the website.

- The repository is renamed from `2026summerproject` to `PaleoRigor`; links, clone commands, the website address
  (https://verture-liu.github.io/PaleoRigor/) and the in-app GitHub link use the new name. The user guides
  no longer show a developer's local path.
- `Final data/` is split into `results/` (run folders of the dataset-level cases, named by case and accession)
  and `figures/` (manuscript figures with their source data, and earlier drafts in `figures/development/`).
  `results/README.md` maps every earlier folder name to its new path; the files themselves are unchanged.
- The figure scripts read and write the new folders through `analysis/result_paths.py`; earlier manuscript
  builders and draft-figure scripts moved to `analysis/archive/`.
- Twelve FastQC archives under `analysis/benchmark_multimodel/v4_pro` are stored through Git LFS like the
  other `.zip` files; their content is unchanged.

### Removed
- Manuscript drafts, a temporary script and the generated `egg-info` folder are no longer tracked; they remain in the history of earlier releases.

## 0.2.2 — 2026-09-30

Archive-metadata release. Code, prompts, data and run records are identical to 0.2.1 (b1cc9c4).

### Added
- `.zenodo.json` with the author list, affiliations, ORCIDs, licence and keywords, so that the Zenodo
  GitHub integration archives the release without converting `CITATION.cff` (the automatic archive of
  0.2.1 failed during that conversion).

### Changed
- `CITATION.cff` version and release date.

## 0.2.1 — 2026-09-28

Evaluation code, prompts and reported results are unchanged from 0.2.0: both
evaluation commits (4be5f2f, 728a226) are contained in 0.2.0, and the planning
prompts and benchmark code were not changed between them and this release.

### Added
- The desktop planner runs with the same control layer as the evaluated
  PaleoRigor arm: out-of-scope requests return a blocked decision with one of
  four reason codes (`unsupported_scientific_claim`, `missing_prerequisite`,
  `file_type_mismatch`, `missing_mate`). The decision is recorded in the task's
  `planning_decision.json` and nothing is run. Tests pin the app's refusal rules
  to `supplementary/file_4_system_prompts`.
- Per-run benchmark records for rounds v3, v4 and v5 and for the incomplete
  third model configuration (`analysis/benchmark_v3`, `analysis/benchmark_v4`,
  `analysis/benchmark_v5`, `analysis/benchmark_multimodel/v4_flash_vision_exp`),
  so that every reported run label can be recomputed from the repository.
- Packaged builds of this version for both platforms under `paleorigor/`:
  `PaleoRigor-dev-arm64.dmg` (Apple Silicon, macOS 13 or later) and
  `windows/PaleoRigor-Setup.exe` (Windows 10/11 x64, built by the Windows
  installer workflow from the same source, with its native smoke-test report
  and checksum).
- A bilingual "How it works" page on the project website
  (`docs/how-it-works.html`).

### Changed
- Desktop interface redesigned ("Sequence Glass"): a skill-module shelf read
  from `/api/skills`, dataflow nodes coloured by module, the plan's task summary,
  a step-by-step run log and the refusal card.
- `paleorigor/README.md` lists the macOS Samtools version correctly (1.23.1;
  the Windows build bundles 1.24).
- The website home page reports the frozen-evaluation results (23/24 vs 19/24,
  24/24 vs 19/24, 96/96 recomputed labels, 6/6 matched records) in place of
  early development figures.
