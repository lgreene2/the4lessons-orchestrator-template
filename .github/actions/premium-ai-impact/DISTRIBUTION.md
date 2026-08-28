# 4L Premium + AI Impact Gate — Distribution Mirror

This package is a **public distribution mirror**, not the governance authority.

Canonical authority remains the private repository `lgreene2/the4lessons-orchestrator`, hardened `staging` lineage, where the 4L Premium + AI Impact Production Standard, rubric, validator, governance boundary, and owner-release rules are maintained.

Mirrored source baseline at publication:

- canonical Orchestrator staging commit: `72f48cb7e7abf2104bb1c422b4f7f1ddf13b9b0d`
- standard version: `1.0.0`
- operating model: `automation-first, exception-driven, human-governed`
- candidate threshold: `90/100`
- public-release readiness threshold: `92/100` plus all hard gates and explicit owner approval
- `release-authority` output: always `false`

Purpose: allow sibling private 4L repositories to execute the non-sensitive quality gate without requiring private cross-repository GitHub Actions sharing. Consumer workflows should pin this action to an exact commit SHA.

This mirror must not be used to weaken thresholds, remove gates, create independent release authority, or become a competing control plane. Any future mirror update should trace to an approved canonical Orchestrator commit.
