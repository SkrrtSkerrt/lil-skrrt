Homebrew packaging notes for Lil Skrrt.

Use `packaging/homebrew/hermes-agent.rb` as a tap or `homebrew-core` starting point.

Current formula shape:
- The formula points at the current public `lil-skrrt` GitHub tag archive and pins `version` to the Python package version from `pyproject.toml`.
- If future releases attach semver-named sdist assets, prefer those over tag archives and update the formula URL/sha together.
- `faster-whisper` stays in the `voice` extra, keeping wheel-only transitive dependencies out of the base Homebrew formula.
- The wrapper exports `HERMES_BUNDLED_SKILLS`, `HERMES_OPTIONAL_SKILLS`, and `HERMES_MANAGED=homebrew` so packaged installs keep runtime assets and defer upgrades to Homebrew.
- The wrapper exposes `hermes`, `hermes-agent`, `hermes-acp`, `a`, and `lil-skrrt` when those entry points are installed.

Typical update flow:
1. Confirm the current package version in `pyproject.toml`.
2. Pick the release source URL and compute its sha256.
3. Update the formula `url`, explicit `version`, and `sha256` together.
4. Refresh Python resource stanzas with `brew update-python-resources --print-only hermes-agent` when maintaining a full Homebrew-core-ready formula.
5. Verify `brew audit --new --strict hermes-agent` and `brew test hermes-agent` on a machine with Homebrew.
