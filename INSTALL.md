# LIL SKRRT INSTALLATION PROTOCOL

THIS REPOSITORY IS THE CLEAN BASELINE.

VERSION LOCK:
- Lil Skrrt skin based on Lil Skrrt v0.14.0 (2026.5.16)
- commit febc4cfec
- release tag: v0.14.0-clean

DIRECTIVE:
- Use this version as the stable install target.
- Do not upgrade to newer Lil Skrrt releases unless you have a verified reason to do so.
- The newer versions have issues on this machine. This baseline does not carry your secrets, chat sessions, or personal customizations.

UPDATE POLICY:
- The manual update command still exists for maintainers, but this backup is meant to stay frozen.
- Do not run `lil-skrrt update` unless you intentionally want to diverge from the clean baseline.
- If you do update, treat the result as a new fork, not this backup.

DEPLOYMENT SEQUENCE:
1. Clone the private repository.
2. Check out tag v0.14.0-clean.
3. Run: scripts/install.sh
4. If needed, copy cli-config.yaml.example to ~/.hermes/config.yaml.
5. If needed, copy .env.example to ~/.hermes/.env and add only your own credentials.
6. Launch with `a lil skrrt` or `lil-skrrt`.

OPERATOR NOTE:
- This is the version to keep in service until a future build is verified stable.
- Stay on target. No unnecessary upgrades. No drift. No contamination.
