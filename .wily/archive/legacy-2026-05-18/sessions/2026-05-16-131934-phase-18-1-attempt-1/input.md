# Wily Phase Context

Phase: 18-1 - Claim conflict warnings

## Phase

# Phase 18-1: Claim conflict warnings

## Purpose

Warn users when another active actor already appears to be working on the same phase.

## Acceptance

- Board marks multi-actor live claims on the same phase.
- Wily CLI can report a clear warning when starting a phase with a fresh remote claim.
- Stale claims do not block or over-warn.

## Planner Adapter

# Planner

Recommended planner: manual

## Prompt

# Execution Prompt

Implement claim conflict warnings in Board and Wily CLI where appropriate.

## Verification

# Verification

Run Board and Wily CLI tests for conflict warning behavior.

## Handoff

# Handoff

Use Stage s17 freshness so stale sessions do not trigger false warnings.

## Existing Implementation Plan

# Implementation Plan

No detailed implementation plan exists yet.
