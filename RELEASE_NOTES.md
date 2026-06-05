# LIL SKRRT RELEASE NOTES

VERSION:
- v1.0.0
- release tag: v1.0.0

STATUS:
- FULL TEST SUITE GREEN
- 26,418 passed
- 127 skipped
- 0 failures
- NO SECRETS INCLUDED IN THE RELEASE NOTES

WHAT'S IN THIS RELEASE:
- Broad Hermes-to-Lil Skrrt rebrand across docs, CLI/UI text, installer flow, and website copy.
- Gateway/test isolation fixes for suite-order leaks, including Telegram fixture cache cleanup and env restoration around config tests.
- Send-message target handling fixes, including explicit email target parsing and the email-specific home-address hint.
- Qwen auth/runtime credential handling now respects the expected env override path while remaining isolated in tests.
- Additional cleanup across status, skin, plugins, tooling, and docs to keep the suite and visible strings aligned.

VALIDATION:
- Full suite run with xdist: `./.venv/bin/python -m pytest -q -x -n 4 --dist loadfile`
- Result: `26,418 passed, 127 skipped, 246 warnings`

RELEASE NOTES ARCHIVE:
- The previous clean baseline is preserved below for reference.

---

## Historical clean baseline

VERSION:
- Based on Lil Skrrt v0.14.0 (2026.5.16)
- commit febc4cfec
- release tag: v0.14.0-clean

STATUS:
- CLEAN BASELINE VERIFIED
- NO USER SECRETS INCLUDED
- NO CHAT SESSIONS INCLUDED
- NO PERSONAL CUSTOMIZATIONS INCLUDED
- NO UNVERIFIED UPGRADES

WHY THIS VERSION:
- This is the stable baseline for this machine.
- Newer releases have known issues on this setup.
- Keep this build in service unless a later build is proven stable.

OPERATOR DIRECTIVE:
- Do not drift.
- Do not contaminate.
- Do not upgrade without verification.

INSTALL PATH:
1. Clone the private repo.
2. Checkout v0.14.0-clean.
3. Run scripts/install.sh.
4. Use the example config files only as needed.
