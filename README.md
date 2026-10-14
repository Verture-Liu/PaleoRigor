# PaleoRigor

**A bounded research agent with a reproducible evidence trail for paleomicrobiome data processing.**

PaleoRigor turns a natural-language research request into an explicit workflow built only from predefined local analysis skills. Before anything runs, a validator checks every file reference, file format and step dependency, and a paleobiologist reviews and approves the plan. Requests that the supplied data cannot support are refused with a named reason code. Every run keeps its final outputs, intermediate files, checksums and run record, so the path from request to result can be checked afterwards.

PaleoRigor prepares and documents data before specialist analysis. It does not authenticate ancient DNA or make biological interpretations; those decisions stay with the researcher.

- **Preprint:** Liu T, Zhang H, Jia Y, Ning K. bioRxiv (2026). [doi:10.64898/2026.09.30.755547](https://doi.org/10.64898/2026.09.30.755547)
- **Project website:** <https://verture-liu.github.io/2026summerproject/> (method overview, step-by-step guide, benchmark explorer)
- **Archived releases (Zenodo):** v0.2.0, the code that produced the reported results, [10.5281/zenodo.22912729](https://doi.org/10.5281/zenodo.22912729); v0.2.2, with the complete per-run benchmark records, [10.5281/zenodo.23042955](https://doi.org/10.5281/zenodo.23042955); latest version [10.5281/zenodo.22912728](https://doi.org/10.5281/zenodo.22912728)

## Download the desktop application

| Platform | File | Notes |
| --- | --- | --- |
| macOS 13 or later, Apple Silicon | [`paleorigor/PaleoRigor-dev-arm64.dmg`](paleorigor/) | All results in the paper were produced on macOS |
| Windows 10/11 x64 | [`paleorigor/windows/PaleoRigor-Setup.exe`](paleorigor/windows/) | Verified by its automated build and tool-identity checks |

Both installers bundle the analysis tools (FastQC, MultiQC, SeqKit, seqtk, Samtools, BWA and Bowtie 2) and their runtimes. Checksums and installation notes are in [`paleorigor/README.md`](paleorigor/README.md).

## Run from source

Requires Python 3.11–3.13.

```bash
git clone https://github.com/Verture-Liu/2026summerproject.git
cd 2026summerproject
python -m venv .venv
source .venv/bin/activate
pip install -e .
research-agent
```

The application opens in your browser on a local address. The planning model is reached through an OpenAI-compatible API: enter the endpoint, model and your own key in the application's settings, or set them as the environment variables listed in `.env.example`. Only the request and summaries of the uploaded files are sent to the model; the data files are analysed on your computer.

Run the tests with `pytest tests`.

## Repository layout

| Path | Contents |
| --- | --- |
| `src/research_agent/` | Application source: planner, validator, skill registry, execution and web interface |
| `paleorigor/` | Packaged desktop applications and their checksums |
| `analysis/benchmark_v3`–`benchmark_v5`, `analysis/benchmark_multimodel/` | Benchmark manifests, per-run records, scores and verification reports |
| `Final data/` | Final and intermediate outputs of the dataset-level cases, and figure source data (`manuscript_figures/`) |
| `supplementary/file_4_system_prompts/` | Supplementary File 1: the system prompts sent to both benchmark arms |
| `study/` | Preregistrations, study plans and questions written before the benchmark runs |
| `dev-notes/` | Development plans and design notes |
| `docs/` | Source of the project website |
| `packaging/` | macOS and Windows build scripts, pinned tool manifests and licences |
| `tests/` | Unit, integration and packaging tests |

## Citation

If you use PaleoRigor, please cite the preprint (see [`CITATION.cff`](CITATION.cff)):

> Liu T, Zhang H, Jia Y, Ning K. PaleoRigor: a bounded research agent with a reproducible evidence trail for paleomicrobiome data processing. bioRxiv. 2026. doi:10.64898/2026.09.30.755547

## License

MIT (see [`LICENSE`](LICENSE)). Bundled third-party tools keep their own licences, listed in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
