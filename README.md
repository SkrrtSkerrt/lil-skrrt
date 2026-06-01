Hermes Agent clean baseline backup

Source:
- Hermes Agent v0.14.0 (2026.5.16)
- commit febc4cfec
- exported directly from the clean installed checkout

Quick install
- Clone the private repo.
- Check out the release tag: v0.14.0-clean
- Read INSTALL.md for the full deployment protocol.
- Run scripts/install.sh from the repo root.
- Copy cli-config.yaml.example to ~/.hermes/config.yaml if you need a starter config.
- Copy .env.example to ~/.hermes/.env only if you want the optional env template; do not paste secrets into this backup.

Included:
- full upstream codebase at the exact installed version
- clean install scaffolding such as cli-config.yaml.example, .env.example, and scripts/install.sh

Excluded:
- secrets
- chat/session history
- memories
- logs
- personal customizations

Purpose:
- private installable baseline for a fresh Hermes setup
- no user-specific configuration or runtime data
