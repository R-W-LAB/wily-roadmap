# Phase 19-1: Risk signal model and scoring

## Purpose

Define the risk signals Board should rank before implementing UI.

## Acceptance

- Risk signals include blockers, dependency bottlenecks, stale sessions, awaiting-push local completions, and unclaimed ready work.
- Each signal has a deterministic severity and explanation.
- Scoring does not require LLM calls or external analytics.
