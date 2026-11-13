# Proposal: prepare the audit harness for safe GitHub distribution

## Status

Implemented for review. No remote repository is created or pushed by this change.

## Problem

The working directory contains reusable harness code beside confidential candidate workspaces,
historical customer reports, raw evidence, large media and local agent/cloud configuration. A new
operator or coding agent also lacks a single root instruction file describing authority, trust
boundaries, OpenSpec workflow and the expected audit outcome.

## Proposed change

1. Exclude confidential/local material from Git without deleting it.
2. Add root instructions for Codex, Claude Code and GitHub Copilot.
3. Add a deterministic GitHub-readiness check covering files, size, secrets and tests.
4. Add contributor, security and CI documentation.
5. Rewrite onboarding so a clean clone can prepare and audit a separately supplied candidate.

## Safety impact

This strengthens the publication boundary. Candidate code, evidence, reports and secrets remain
local. The harness does not download, execute, modify, approve or upload a candidate repository.

## Non-goals

- No GitHub repository creation, commit or push.
- No candidate-source mutation or execution.
- No publication of Apple/customer proprietary artifacts.
- No automatic compliance approval or checklist update.

## Compatibility

Existing local reports and evidence remain on disk but become ignored. Reusable scripts, prompts,
policies, tests and OpenSpec changes remain eligible for Git.
