# PaleoRigor desktop applications

PaleoRigor is a local, browser-based research agent for reproducible
paleomicrobiome and ancient-DNA data processing. This folder contains the
packaged applications for Apple Silicon macOS and for Windows 10/11 x64.

## Platforms

- macOS: `PaleoRigor-dev-arm64.dmg` for Apple Silicon and macOS 13 or later.
- Windows: `windows/PaleoRigor-Setup.exe` for Windows 10/11 x64, built from the
  same 0.2.1 source by the native Windows build workflow (GitHub Actions run
  36327764584, commit e09765e) and checked by its native smoke test
  (`windows/verification.json`). Verify it against `windows/SHA256SUMS.txt`.

## Download

- `PaleoRigor-dev-arm64.dmg`
- Version: `0.2.1` (development build)
- Target: Apple Silicon (M-series Macs), macOS 13 or later

## Install and open

1. Download and open `PaleoRigor-dev-arm64.dmg`.
2. Drag `PaleoRigor.app` into the Applications folder.
3. On first launch, Control-click the app, choose **Open**, and confirm **Open**
   again if macOS reports that the developer cannot be verified.
4. PaleoRigor starts its local backend and opens the browser interface.
5. Enter the model API configuration in the web interface. API keys are stored
   in macOS Keychain and are not included in this repository.

On Windows, the same local browser interface is opened from the Start-menu or
desktop shortcut. API keys are stored through Windows Credential Manager. See
`../packaging/windows/README.md` for the build and native verification guide.

## Bundled tools

- FastQC 0.12.1
- MultiQC 1.35
- SeqKit 2.13.0
- seqtk 1.5-r133
- Samtools 1.23.1 (macOS; the Windows build bundles 1.24)
- BWA 0.7.19-r1273
- Bowtie 2 2.5.5

Users do not need to install Python, Conda, Java or these seven analysis tools
separately.

## Verification

The development build passed the project test suite, strict ad-hoc signature
verification, read-only DMG mounting, authenticated local API checks, bundled
tool checks, and native launcher lifecycle checks. See
`../packaging/macos/phase2-verification.json` for the recorded release gate.

Verify the downloaded image with:

```bash
shasum -a 256 PaleoRigor-dev-arm64.dmg
```

The expected value is listed in `SHA256SUMS.txt`.

## Development-build limitation

This build is ad-hoc signed but is not yet signed with an Apple Developer ID or
notarized by Apple. It is suitable for local development and limited testing.
Formal public distribution requires Developer ID signing and notarization.

The Windows development installer is likewise unsigned and may trigger Windows
SmartScreen. Neither build is a commercial release.
