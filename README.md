Hermes Agent clean baseline backup

Source:
- Hermes Agent v0.14.0 (2026.5.16)
- commit febc4cfec
- exported directly from the clean installed checkout

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
