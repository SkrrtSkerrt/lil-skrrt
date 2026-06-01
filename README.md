Lil Skrrt clean baseline backup

Source:
- Based on Lil Skrrt v0.14.0 (2026.5.16)
- commit febc4cfec
- exported directly from the clean installed checkout

Quick install
- Clone the private repo.
- Check out the release tag: v0.14.0-clean.
- Read INSTALL.md for the full deployment protocol, or see `website/docs/getting-started/installation.md` for the platform-specific Windows/macOS/Linux guide.
- Linux/macOS/WSL2: run `scripts/install.sh` from the repo root.
- Windows: open PowerShell and run `scripts/install.ps1`.
- After install, launch with `a lil skrrt` or `lil-skrrt`.
- Copy cli-config.yaml.example to ~/.hermes/config.yaml if you need a starter config.
- Copy .env.example to ~/.hermes/.env only if you want the optional env template; do not paste secrets into this backup.

Included:
- full upstream codebase at the exact installed version

Excluded:
- secrets
- chat/session history
- memories
- logs
- personal customizations

Purpose:
- private installable baseline for a fresh Lil Skrrt setup
- no user-specific configuration or runtime data

Warning:
- This repo is intentionally frozen at the clean baseline.
- The manual update path still exists, but it should not be used unless you deliberately want to fork away from the backup.
