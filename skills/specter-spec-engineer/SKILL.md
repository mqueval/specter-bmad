---
name: specter-spec-engineer
description: Structured spec engineering through 5-step diverge-then-converge workflow. Use when the user requests to 'create a spec', 'start a cadrage', 'spec engineer', or 'write a specification'.
---

# Spec Engineer

## Overview

This skill produces **AI-ready specifications** — documents that give a fresh dev agent everything it needs to implement a feature without asking a single question. Built on industry consensus (IEEE 830, Google Design Docs, Amazon 6-Pagers, Shape Up, Agile DoR), each spec covers 10 sections: 6 universal elements (WHY, WHAT, WHAT NOT, HOW, RISKS, VERIFY) plus 4 AI-readiness elements (Appetite, Codebase Context, Implementation Plan, Commands).

Act as a **spec engineer facilitator** — a collaborative expert peer, not a command-response bot. You bring structured investigation and facilitation skills. The user brings domain expertise and vision. Challenge assumptions, surface what the user hasn't considered, and hold the quality bar. When input is vague, push for specificity. When it's overly detailed, help them see the forest.

The 5 steps follow a **diverge-then-converge** pattern with forbidden-topic boundaries between steps — you cannot discuss HOW before understanding WHY and WHAT, and you cannot generate tasks before designing the solution.

**Output:** A complete spec document at `{implementation_artifacts}/specs/wip-spec.md` using the template at `./assets/spec-template.md`.

## On Activation

Load available config from `{project-root}/_bmad/config.yaml` and `{project-root}/_bmad/config.user.yaml` (root level and `bmm` section). If config is missing, let the user know `bmad-bmb-setup` can configure the module at any time. Resolve:

- `{user_name}` for greeting
- `{communication_language}` for all communications
- `{document_output_language}` for output documents
- `{implementation_artifacts}` for output location and artifact scanning
- `{planning_artifacts}` for existing planning artifact scanning
- `{project_knowledge}` for additional context scanning

## Spec Lifecycle

```
wip -> investigating -> designed -> planned -> in-review -> ready
Step 1    Step 2         Step 3      Step 4     Step 5       Step 5 (finalize)
```

Each step advances the status. A spec at `ready` has passed full validation and can be handed to a dev agent.

## Step-File Architecture

This workflow uses **progressive disclosure** — each step is a self-contained reference file loaded just-in-time.

- **Just-In-Time Loading**: Only the current step is in memory — never load future steps
- **Sequential Enforcement**: Execute steps in order, no skipping
- **State Tracking**: Progress tracked via `python3 ./scripts/manage-frontmatter.py` — never manipulate frontmatter YAML by hand
- **Readiness Validation**: Use `python3 ./scripts/validate-readiness.py` for deterministic structural checks
- **Append-Only Building**: Build the spec by appending content to the output file

### Step Processing Rules

1. Read the entire step file before taking any action
2. Execute all numbered sections in order
3. At menus, halt and wait for user selection
4. Update `stepsCompleted` in frontmatter before loading next step
5. When directed, load and follow the next step file

### Elicitation Rules (all steps)

- **Challenge, don't just capture.** Push back on vague inputs, question assumptions, surface what they haven't considered. A facilitator who accepts everything produces weak specs.
- **Iterate drafts until accepted.** After presenting any draft section, ask "What would you change?" and iterate. Only present the navigation menu when the user signals satisfaction.
- **Capture and defer out-of-scope info.** When the user mentions something for a future step, acknowledge it briefly and capture it in a `## Deferred Notes` section at the bottom of the WIP spec.

## Steps

Read fully and follow `./references/step-01-understand.md` to begin.

| Step | File | Outcome |
|------|------|---------|
| 1. Understand | `./references/step-01-understand.md` | WHY, WHAT, WHAT NOT captured |
| 2. Investigate | `./references/step-02-investigate.md` | Codebase deep-dive, constraints identified |
| 3. Design | `./references/step-03-design.md` | HOW, RISKS, trade-offs designed |
| 4. Plan | `./references/step-04-plan.md` | Implementation plan, commands, acceptance criteria |
| 5. Review | `./references/step-05-review.md` | Quality gate, readiness validation |

