# LIL SKRRT RELEASE NOTES

VERSION:
- v1.0.1
- release tag: v1.0.1

STATUS:
- WINDOWS CLEAN INSTALL GUIDE ADDED
- LATEST MAIN BRANCH CHANGES PUSHED TO GITHUB
- 26,418 passed
- 127 skipped
- 0 failures

WHAT'S IN THIS RELEASE:
- Added a clean Windows install guide with reset, install, and verification steps.
- Linked the main installation and update docs to the new Windows guide and the correct Lil Skrrt GitHub releases page.
- Continued the visible branding sweep across installer/release/help surfaces.
- Kept the repo on the latest pushed main commit for GitHub.

VALIDATION:
- Docs checked for broken-structure issues via diff check and install-script syntax checks.
- Latest pushed commit on `main` has been verified on origin.

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
