# Phase 23-1: Wily CLI draft topology event contract

## Purpose

Make `decompose-stage` emit a signed `stage_decomposed_local` event containing normalized child Phase topology.

## Scope

- Add Wily CLI tests first.
- Emit draft payload after local decomposition succeeds.
- Warn when Board live config is missing.
- Do not fail local decomposition if Board is unreachable.
