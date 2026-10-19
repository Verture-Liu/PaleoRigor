# Results of the dataset-level cases

Each run folder holds what PaleoRigor produced for one approved workflow:

- `final_outputs/`: the files the user asked for;
- `step_outputs/`: the intermediate files of each step;
- `ResearchAgent Records/`: the run record (workflow, manifest, checksums, timing and report). The folder name is the one the application writes.

| Folder | Case in the manuscript | Public record |
| --- | --- | --- |
| `sequencing_source_checks/ERR15682270_R1` | Sequencing source check (Figure 3) | ERR15682270, mate 1 |
| `sequencing_source_checks/ERR15682270_R2` | Sequencing source check (Figure 3) | ERR15682270, mate 2 |
| `sequencing_source_checks/ERR10114877` | Sequencing source check (Figure 3) | ERR10114877, paired-end |
| `sequencing_source_checks/ERR3250149` | Sequencing source check (Figure 3) | ERR3250149, single-end |
| `sequencing_source_checks/ERR10114867` | Sequencing source check (Figure 3) | ERR10114867, paired-end |
| `sequencing_source_checks/ERR10114861` | Sequencing source check (Figure 3) | ERR10114861, paired-end |
| `sequencing_source_checks/ERR15682267` | Sequencing source check (Figure 3) | ERR15682267, paired-end |
| `peptide_table_curation` | Peptide-table curation (Figure 4) | local `Validation.csv` |
| `retraction_associated_audit` | Retraction-associated audit (Figure 5) | SRR29088443 (SRP508771) |
| `earlier_runs/` | Earlier runs of two records; their FastQC outputs feed the Figure 3 source data (`figures/manuscript/dataset_cases/comparison_source_data/comparison_source_data.csv`) and give the same read counts and GC content as the later runs above | ERR10114877 (mates run separately), ERR10114867 (first run) |
| `public_reuse_check` | Public-data reuse check (Figure 6, Table S7) | 17 AncientMetagenomeDir records: one `ResearchAgent_Result_…` folder per executed run and `<run>.jpg` for the two refused requests; `analysis/public_reuse_check/source_data/case4_records.csv` maps each run to its folder |

## Earlier folder names

Until 14 October 2026 these folders were under `Final data/` with working names. Run records written before that date, and releases up to v0.2.2, still use the old paths.

| Earlier path | Current path |
| --- | --- |
| `Final data/1` | `results/peptide_table_curation` |
| `Final data/2` | `results/sequencing_source_checks/ERR15682270_R1` |
| `Final data/3` | `results/sequencing_source_checks/ERR15682270_R2` |
| `Final data/4` | `results/earlier_runs/ERR10114877_R1_single_file` |
| `Final data/5` | `results/earlier_runs/ERR10114877_R2_single_file` |
| `Final data/6` | `results/sequencing_source_checks/ERR3250149` |
| `Final data/7` | `results/earlier_runs/ERR10114867_first_run` |
| `Final data/8` | `results/sequencing_source_checks/ERR10114861` |
| `Final data/9` | `results/sequencing_source_checks/ERR15682267` |
| `Final data/group 4-5 new` | `results/sequencing_source_checks/ERR10114877` |
| `Final data/group 7 new` | `results/sequencing_source_checks/ERR10114867` |
| `Final data/retracted_result` | `results/retraction_associated_audit` |
| `Final data/manuscript_figures` | `figures/manuscript` |
| `Final data/task_grouped_figures` | `figures/manuscript/dataset_cases` |
| `Final data/comparison_figures` | `figures/manuscript/dataset_cases/comparison_source_data` |
| `Final data/retracted_case_figure_v2` | `figures/manuscript/retraction_audit` |
| `Final data/manuscript_figures_schemeB`, `Final data/retracted_case_figure` | `figures/development/` |

`analysis/result_paths.py` holds the same mapping for the figure scripts.
