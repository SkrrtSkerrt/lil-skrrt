---
sidebar_position: 10
---

# Dependency Supply-Chain Maintenance

Lil Skrrt has multiple dependency surfaces. Treat dependency changes as supply-chain work, not as routine formatting churn.

## Protected surfaces

Checked-in lockfiles and manifests:

- `pyproject.toml`
- `uv.lock`
- `package.json`
- `package-lock.json`
- `web/package.json`
- `web/package-lock.json`
- `ui-tui/package.json`
- `ui-tui/package-lock.json`
- `ui-tui/packages/hermes-ink/package.json`
- `ui-tui/packages/hermes-ink/package-lock.json`
- `website/package.json`
- `website/package-lock.json`
- `scripts/whatsapp-bridge/package.json`
- `scripts/whatsapp-bridge/package-lock.json`

CI guardrails:

- `.github/workflows/osv-scanner.yml` scans all checked-in Python and Node lockfiles with OSV-Scanner and fails on vulnerable pins.
- `.github/workflows/uv-lockfile-check.yml` blocks stale `uv.lock` updates.
- `.github/workflows/secret-scan.yml` blocks unreviewed secret-like literals.
- `.github/workflows/supply-chain-audit.yml` scans PR diffs for high-signal supply-chain attack patterns.
- `osv-scanner.toml` holds the narrow OSV ignore policy. Keep this file small and heavily justified.

## OSV scanner policy

OSV-Scanner is detection-only. It does not open PRs, update packages, or modify lockfiles.

The workflow scans explicit lockfiles instead of recursively walking the repository. This keeps results tied to sources of truth and avoids vendored, generated, test, or worktree directories.

`fail-on-vuln: true` is intentional. The current lockfiles are expected to be clean except for overrides documented in `osv-scanner.toml`; newly vulnerable pins should block before merge.

When editing OSV behavior:

1. Prefer upgrading or removing the vulnerable package.
2. Use `osv-scanner.toml` only for false positives or upstream-pinned transitive vulnerabilities that cannot be resolved locally.
3. Scope ignores to the exact package and version when possible.
4. Add a reason that explains why the dependency cannot be fixed now.
5. Add `osv-scanner.toml` to workflow path triggers when the config affects CI behavior.
6. Reproduce the scan locally before pushing.

Local OSV reproduction:

```bash
docker run --rm \
  -v "$PWD:/github/workspace" \
  --workdir /github/workspace \
  --entrypoint /root/osv-scanner \
  ghcr.io/google/osv-scanner-action:v2.3.8 \
  --lockfile=uv.lock \
  --lockfile=package-lock.json \
  --lockfile=web/package-lock.json \
  --lockfile=ui-tui/package-lock.json \
  --lockfile=ui-tui/packages/hermes-ink/package-lock.json \
  --lockfile=website/package-lock.json \
  --lockfile=scripts/whatsapp-bridge/package-lock.json
```

## Current OSV overrides

### `hermes-agent` / PyPI

`uv.lock` records the local editable root package as `hermes-agent`. OSV can match that name to advisories for published PyPI releases that do not describe the source tree being scanned.

Policy:

- Keep the local editable package filtered out.
- Do not use this override for third-party dependencies.
- If the project package name or lockfile representation changes, re-run OSV locally and remove the override if it is no longer needed.

### `pynacl==1.5.0` / PyPI

`discord.py[voice]==2.7.1` constrains PyNaCl to `>=1.5.0,<1.6`. A fixed `PyNaCl>=1.6` is not currently resolvable while that voice extra remains pinned.

Policy:

- Keep the ignore scoped to `pynacl` version `1.5.0` only.
- Revisit this override when upgrading `discord.py` or changing the Discord voice dependency path.
- Remove the ignore immediately if a compatible `discord.py[voice]` release allows `PyNaCl>=1.6`.
- Do not silence broader PyNaCl ranges.

Recheck command:

```bash
uv lock --upgrade-package discord-py --upgrade-package pynacl
```

If resolution still fails because `discord.py[voice]` requires `pynacl<1.6`, revert the lockfile and keep the scoped ignore.

## Manual audit commands

Python production audit, excluding the editable root package:

```bash
uv export --format requirements-txt --no-hashes --no-dev > /tmp/lil-skrrt-export.txt
python - <<'PY'
from pathlib import Path
lines = [line for line in Path('/tmp/lil-skrrt-export.txt').read_text().splitlines(True) if not line.startswith('-e ')]
Path('/tmp/lil-skrrt-requirements-no-root.txt').write_text(''.join(lines))
PY
uvx --from pip-audit pip-audit -r /tmp/lil-skrrt-requirements-no-root.txt --format json > /tmp/pip-audit-prod-noroot.json
python - <<'PY'
import json
from pathlib import Path
p = Path('/tmp/pip-audit-prod-noroot.json')
data = json.loads(p.read_text()) if p.read_text().strip() else {'dependencies': []}
vulns = []
for dep in data.get('dependencies', []):
    for vuln in dep.get('vulns', []):
        vulns.append((dep.get('name'), dep.get('version'), vuln.get('id'), vuln.get('fix_versions')))
print('vuln_count', len(vulns))
for row in vulns:
    print(row)
PY
```

Node production audits for every checked-in lockfile:

```bash
set -euo pipefail
for d in . website web ui-tui ui-tui/packages/hermes-ink scripts/whatsapp-bridge; do
  if [ -f "$d/package-lock.json" ]; then
    echo "== npm audit prod: $d =="
    (cd "$d" && npm audit --omit=dev --audit-level=moderate)
  fi
done
```

## Patch rules

- Regenerate lockfiles with the package manager, not manual edits.
- Python: use `uv lock --upgrade-package <name>` after changing pins.
- Node: use `npm install --package-lock-only` in the package directory after changing overrides or manifests.
- Inspect resolver-adjacent lockfile churn before committing.
- Stage only dependency-related files for dependency maintenance commits.

## Validation before push

Run the focused checks first:

```bash
uv lock --check
python - <<'PY'
import json, tomllib, yaml
from pathlib import Path
for p in [
    'package-lock.json',
    'web/package-lock.json',
    'ui-tui/package-lock.json',
    'ui-tui/packages/hermes-ink/package-lock.json',
    'website/package-lock.json',
    'scripts/whatsapp-bridge/package-lock.json',
]:
    json.loads(Path(p).read_text())
yaml.safe_load(Path('.github/workflows/osv-scanner.yml').read_text())
tomllib.loads(Path('osv-scanner.toml').read_text())
print('dependency metadata ok')
PY
python scripts/scan_secrets.py
git diff --check
```

Then run the full suite when code or lockfiles changed:

```bash
uv run python scripts/run_tests_parallel.py -- -x --tb=short -q
```

Before reporting success, verify the pushed commit on GitHub and confirm the OSV-Scanner, uv.lock check, secret scan, lint, Nix, and test workflows completed successfully.
