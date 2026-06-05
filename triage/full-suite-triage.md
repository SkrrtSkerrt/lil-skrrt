# Full-suite triage notes

Date: 2026-06-02
Repo: /home/linuxbox/lil-skrrt
Branch: main

## Completed fixes before this pass
- web_server import mismatch fixed
- custom-provider grouping fixed
- dashboard auth compatibility package added
- tools_config provider-selection helpers restored
- SessionDB compatibility gaps filled
- messaging platform enablement override honored
- dev extras updated to include pty/acp support

## Current full-suite failure clusters from the latest run
1. docker/* runtime/integration failures
2. dashboard startup/enablement failures
3. main invocation / passthrough failures
4. profile gateway failures
5. s6 profile gateway integration failures
6. TUI passthrough / goal command failures
7. zombie reaping failure

## Initial hypothesis
These clusters likely share a startup/runtime mode regression rather than isolated assertion drift. Likely areas to inspect first:
- CLI startup path and passthrough dispatch
- Docker/container detection and gateway lifecycle helpers
- dashboard default enablement and port/runtime wiring
- PTY/TUI bridge behavior under test harnesses

## Next step
Reproduce the first cluster in isolation, then inspect the shared startup code path before patching.

## New finding from vision/video triage
- The remaining full-suite failures were concentrated in `tools/vision_tools.py`.
- I verified the focused suites locally after reviewing the code:
  - `tests/tools/test_vision_tools.py` -> passed (64 passed, 6 skipped)
  - `tests/tools/test_video_analyze.py` -> passed (29 passed)
- The shared code already handled the key paths the failures were pointing at:
  - auxiliary model env selection for image/video handlers
  - file:// and local-path resolution
  - remote URL SSRF checks
  - image/video size guards and retry logic
  - cleanup logging with `exc_info`
- Next step: rerun the full suite from a clean pass and check whether any failures remain outside the vision/video cluster.

- Current TypeScript errors reported by the build:
  - `updateSkillsFromHub` / `updateSkillsFromHub` missing on the dashboard API type used by `SkillsPage.tsx`
  - `terminalBackground` not present on `DashboardTheme` in `src/themes/presets.ts`
  - a couple of implicit-`any` callback parameters in `SkillsPage.tsx`
- This points to a frontend type/interface drift, not a docker-entrypoint bug.

## Latest verified state
- xAI OAuth model resolution is fixed:
  - `resolve_provider_client("xai-oauth", model=None)` now correctly returns no client
  - empty-string model fallback still works for compatibility
- `gateway/run.py` env bridging is fixed for terminal runtime flags:
  - `docker_persist_across_processes`
  - `docker_orphan_reaper`
- Verified focused tests now passing:
  - `tests/hermes_cli/test_auth_xai_oauth_provider.py`
  - `tests/agent/test_auxiliary_client.py -k 'xai_oauth or oauth_provider or UniversalModelFallback'`
  - `tests/tools/test_terminal_config_env_sync.py::test_cli_and_gateway_env_maps_agree`
- Latest fresh full-suite stop-on-first-failure result:
  - `tests/hermes_cli/test_gemini_provider.py::TestGeminiModelsDev::test_list_agentic_models_with_mock_data`
  - root cause fixed by making `agent.models_dev` provider lookup tolerate Gemini/Google catalog alias drift (`google` vs `google-ai-studio`)
  - the test now passes in isolation and in the full neighboring transition block
