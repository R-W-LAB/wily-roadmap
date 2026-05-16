# Phase 18-1: Claim conflict warnings

## Purpose

Warn users when another active actor already appears to be working on the same phase.

## Acceptance

- Board marks multi-actor live claims on the same phase.
- Wily CLI can report a clear warning when starting a phase with a fresh remote claim.
- Stale claims do not block or over-warn.
