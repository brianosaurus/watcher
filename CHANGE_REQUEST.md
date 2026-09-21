# Change Request

Issue 1

Seeded from [brianosaurus/watcher#1](https://github.com/brianosaurus/watcher/issues/1).

## Change Type

Feature | Bug Fix | Prototype | Refactor | Performance | Security | Upgrade

## Summary

Agentic Workflow card is wrong: rewrite it to describe uncle (github.com/unclehq/uncle)

## Motivation

## Problem

The **Agentic Workflow** card on the portfolio home page is wrong. It links to `github.com/unclehq/stagegate` and describes a hard-wired "Claude builds, Codex audits" pipeline. That is not what the project is. The project is **uncle** (https://github.com/unclehq/uncle), and the card needs to be rewritten from the actual repo.

## What the card gets wrong

- **Wrong repo.** It points at `unclehq/stagegate`. The canonical project is `unclehq/uncle`. stagegate carries the same description and appears to be the earlier name; confirm and drop the stagegate link.
- **Wrong framing.** It describes a fixed Claude/Codex pairing. Uncle is agent-agnostic: it coordinates the coding agents you already use (Cline, Claude, Codex, Kimi, OpenCode, others) and treats them as untrusted and swappable.
- **Missing the core idea.** Uncle is a terminal-native agentic software engineer that works inside your repo. You hand it requirements or a GitHub issue, talk to it while it works, and get a verified pull request. The change, not the agent, is the unit of trust.
- **Understates the integrity chain.** The card only mentions SHA-256-pinned approvals and immutable reviewer output. Uncle's chain is: approved plan, implementation, independent review, verification, human approval, GitHub PR, change evidence. Review and verification apply to an exact Git tree, not to the agent's description of the code, and trusted workflow state comes from Uncle rather than agent-authored prose.

## Where

- `static/home.html`, the `Agentic Workflow` card (around line 486): heading, URL label, body copy, `Code` link, and `tag` line.
- `AGENTIC_WORKFLOW_STRATEGY.md`: positioning notes still say "Claude builds, Codex audits". Bring them in line with uncle's agent-agnostic framing.

## Acceptance criteria

- [ ] Read the uncle README and source before writing copy. Do not derive the description from the old card.
- [ ] Card heading, URL label, and `Code` link point to `https://github.com/unclehq/uncle`.
- [ ] Body copy explains what uncle is and does in two to four concrete sentences: terminal-native, issue in / verified PR out, works with the agents you already use, independent review, human approval gates, cryptographically pinned plans and artifacts.
- [ ] No mention of a fixed Claude/Codex pairing.
- [ ] stagegate link removed unless the repo shows it is a distinct, still-maintained component.
- [ ] `tag` line updated to match the new scope.
- [ ] `AGENTIC_WORKFLOW_STRATEGY.md` updated so positioning language matches uncle.

## Observed Current Behavior

Describe what the system currently does.

## Desired Behavior

Describe what the system should do after the change.

## Reproduction

For a bug, provide exact steps to reproduce it.

For other change types, write "Not applicable."

## Constraints

List compatibility, security, performance, timing, or scope constraints.

## Known Relevant Files

List files or components if known.

## Out of Scope

List behavior or components that must not be changed.

## Success Criteria

Describe the observable evidence that proves the change works.
