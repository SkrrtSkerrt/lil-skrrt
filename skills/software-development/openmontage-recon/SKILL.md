---
name: openmontage-recon
description: Use when inspecting OpenMontage or any agent-first video pipeline repo. Capture the manifest, skill, tool, and governance contracts without guessing.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [openmontage, repo-inspection, pipelines, skills, provider-registry, governance]
    related_skills: [implementation-workflows, repository-drilling-synthesis, project-execution-guardrails]
---

# OpenMontage Recon

## Overview

OpenMontage is not a normal app repo. It is a contract system for agent-driven video production.

Treat it as four layers:
- manifests define pipeline stages and gates
- skills define how each stage is executed
- tools define live capabilities and provider availability
- schemas define artifact contracts and reviewer expectations

The important work is mapping the contracts, not summarizing filenames.

## When to Use

Use this skill when:
- the user wants a repo walkthrough
- you need to understand how OpenMontage-style agent systems are organized
- you need to compare pipeline stages, skills, manifests, providers, or schemas
- you want reusable governance rules from an agent-first pipeline repo

Do not use it for ordinary app repos that do not separate manifests, skills, and schemas.

## Recon Method

1. Read the top-level agent contract first.
   - AGENT_GUIDE.md
   - PROJECT_CONTEXT.md
   - skills/INDEX.md

2. Read the pipeline manifest(s).
   - pipeline_defs/<pipeline>.yaml
   - confirm stage order, artifacts, tools, approvals, and sub-stages

3. Read the stage-director skills.
   - skills/pipelines/<pipeline>/*-director.md
   - look for the exact review focus and quality gates

4. Read the tool contract layer.
   - tools/base_tool.py
   - tools/tool_registry.py
   - config/runtime loaders
   - note how availability, fallback, and capability grouping work

5. Read schemas next.
   - schemas/artifacts/*
   - schemas/pipelines/*
   - identify the fields that are hard contracts versus optional metadata

6. Compare docs to code.
   - note drift between manifest, skill, and implementation
   - flag stale stage counts, outdated runtime rules, or hidden fallback behavior

## What to Capture

Always extract these facts:
- pipeline names and type
- stage order
- required artifacts per stage
- approval gates
- sample / preview sub-stages
- renderer/runtime rules
- provider selection rules
- decision-log requirements
- review checklist items
- any hard no-silent-fallback policy
- whether the pipeline is research-first, source-led, or harness-only
- whether the pipeline hard-locks Remotion, allows HyperFrames, or treats FFmpeg as fallback only
- whether the pipeline inserts domain-specific stages such as character_design or rig_plan

If you are comparing multiple pipelines, classify them into families first:
- research/proposal-heavy generation
- technique/runtime-heavy generation
- source-to-clips / localization / harness

## What to Copy Into Personal Operating Style

These are the reusable lessons worth keeping:
- Keep intelligence in instructions, not hidden code paths.
- Make provider/runtime decisions explicit before execution.
- Prefer live capability discovery over hardcoded tool lists.
- Use schemas and review gates to prevent drift.
- Treat approval boundaries as part of the product.
- Surface downgrade paths instead of silently taking them.
- When docs and code disagree, trust the contract source of truth and verify the implementation.
- Treat review and checkpoint as separate gates: review judges quality; checkpoint saves state and requests approval when required.
- Carry cumulative state across stages instead of restarting each stage from scratch.
- Use send-back when downstream discovery invalidates upstream work; do not hide the mismatch.
- Record every major decision in an audit trail with rejected alternatives.
- Keep runtime locked once approved; a compose-stage runtime swap is a contract breach.
- Prefer Remotion primitives when the motion can be expressed simply; escalate only when the motion genuinely needs it.
- For local-video products, assess compatibility by runtime bucket instead of one binary machine check.

## OpenMontage explainer pipeline, distilled

The explainer pipeline is a strict chain:
- research → proposal → script → scene_plan → assets → edit → compose → publish

The durable contracts are:
- research: gather evidence, data points, audience questions, and angle candidates; no creative decisions.
- proposal: present at least 3 different concepts, show music and voice implications, lock renderer/runtime choices visibly, and stop for approval.
- script: convert the selected concept into timed narration with enhancement cues and pronunciation guidance.
- scene_plan: turn sections into distinct scenes with explicit shot language, required assets, and playbook-compatible visuals.
- assets: generate real files, verify existence, manage budget, and preview expensive asset types before batch spend.
- edit: map assets to timeline, configure subtitles and ducking, and eliminate gaps or overlaps.
- compose: pre-validate, render, probe output, transcribe rendered audio, inspect frames, and confirm no silent downgrade.
- publish: build SEO metadata, chapters, thumbnail concept, export packaging, and publish log.

Cross-cutting rules:
- Every stage has review_focus and success_criteria.
- Most stages checkpoint after review.
- Human approval is mandatory at pre-production gates and publish.
- Decision_log must capture provider choice, playbook choice, music, voice, and runtime.
- If both Remotion and HyperFrames are available, both must be shown to the user.
- No silent fallback when a requested runtime or capability is unavailable.
- Every generated artifact must be schema-valid before it is trusted.
- Preflight should be presented as a capability menu, not a flat tool list.
- Show what is configured, what is missing, and what can be unlocked with a small setup fix.
- Keep render_runtime locked from proposal through edit; compose must obey it or halt and escalate.

## Pipeline family patterns

A few recurring archetypes show up across the repo:
- Explainer: research-first, proposal gate, explicit runtime choice, heavy decision-log discipline.
- Cinematic: mood-first, source-media-led, emotional pacing, color and sound coherence.
- Animation: technique-first, animation-mode selection, reuse strategy, math/diagram rigor.
- Character animation: explicit character_design and rig_plan stages, local rig reuse, sample-before-scale.
- Hybrid: source truth first, support assets second, balance gates that keep overlays from overwhelming the source.
- Avatar spokesperson: presenter-first, lip-sync and CTA landing are the main quality gates.
- Talking head: footage-led presenter workflow with strong preflight around caption placement and enhancement.
- Screen demo: capture-mode-aware brief with runtime selection constrained by the capture path.
- Clip factory: long source split into independent clips; batch failure must not sink the whole run.
- Podcast repurpose: audio-primary repackaging with episode/guest cross-linking and clip ranking.
- Localization dub: transcript truth, timing preservation, per-locale QA, and packaging by locale.
- Documentary montage: retrieval-first, source-provenance heavy, no script/publish stages.
- Framework smoke: harness-only, minimal contract validation.

These families share the same governance skeleton, but each changes what "quality" means.

## Common Pitfalls

1. Summarizing files instead of contracts.
   - Fix: map stages, artifacts, tools, approvals, and runtime choices.

2. Missing stage/skill drift.
   - Fix: compare manifest stage counts against director skill docs and actual code.

3. Assuming provider availability.
   - Fix: inspect the live registry and dependency checks.

4. Treating fallback as harmless.
   - Fix: confirm whether the repo allows silent downgrade or requires user approval.

5. Missing sample/preview gates.
   - Fix: check proposal sub-stages and reference-driven workflows.

6. Collapsing all pipelines into one mental model.
   - Fix: separate research-first, runtime-heavy, source-led, and harness-only families before drilling stage details.

7. Forgetting the structural outliers.
   - Fix: documentary-montage, character-animation, and framework-smoke do not follow the plain seven-stage pattern cleanly.

## Verification Checklist

- [ ] Top-level contract files were read first
- [ ] Pipeline manifest stage order was recorded
- [ ] Stage director skills were compared to the manifest
- [ ] Tool discovery / availability / fallback behavior was identified
- [ ] Schema contracts were checked
- [ ] Any docs-vs-code drift was noted explicitly
- [ ] Reusable lessons were separated from temporary findings
- [ ] Pipeline family was classified before details were summarized
- [ ] Any runtime lock rules were written down explicitly
- [ ] Any special stages or harness-only exceptions were called out
