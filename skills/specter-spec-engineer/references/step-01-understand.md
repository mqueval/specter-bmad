# Step 1: Understand — Problem & Scope Discovery

**Progress: Step 1 of 5** — Next: Investigate

## STEP GOAL

Initialize the spec workflow, capture the WHY (problem & context), WHAT (goals), and WHAT NOT (non-goals) through collaborative dialogue. Create the WIP spec file. Optionally accept a seed document to fast-track.

## Step Rules

- FORBIDDEN to discuss HOW (solution) — only WHY, WHAT, and WHAT NOT
- FORBIDDEN to look ahead to future steps
- Push for specificity: vague problems produce vague specs
- You bring structured thinking — the user brings domain expertise
- If the user's input is already rich, don't ask questions you can answer from context

## Sequence of Instructions

### 1. Check for Existing WIP

Look for file at `{outputFile}`:

- **If exists with `stepsCompleted` but NOT `step-05-review` in the list:** Report what exists and which steps are completed. Ask: "Resume from where we left off, or start fresh?" If resume: load the next step file based on stepsCompleted. If fresh: proceed to section 2.
- **If exists with `step-05-review` in stepsCompleted:** This spec is complete. Proceed to section 2 for a new spec.
- **If not exists:** Proceed to section 2.

### 2. Greet & Detect Entry Mode

**Greeting:**

"Welcome {user_name}! Let's engineer a spec together.

You can start in different ways:
- **Describe your idea** — a few sentences is perfect, I'll guide you from there
- **Paste existing content** — a draft spec, ticket description, or notes — I'll parse and fill gaps
- **Point to a file** — give me a path to an existing document and I'll extract the intent

What are you working on?"

**Wait for user response.**

### 3. Route by Input Type

**If the user provides a rough idea/description:**
Proceed to section 4 (standard discovery path).

**If the user pastes substantial content or references a file/ticket:**
This is the **seed path** — extract structure from their input:

- Parse the content for existing WHY, WHAT, WHAT NOT, HOW, RISKS, VERIFY, Codebase Context, Implementation Plan elements
- Map what's covered vs what's missing
- Present a gap analysis: "Here's what I extracted from your input: [summary]. Here's what's missing: [list]."
- **If all 10 sections are substantially covered:** Offer an express lane: "This looks like a near-complete spec. Want to [V] fast-validate — jump straight to Review (Step 5), or [G] go through the full guided workflow?" If V: create the WIP spec, populate all sections, mark steps 1-4 as completed, then load `./step-05-review.md` directly.
- **If partial coverage:** For missing elements, ask targeted questions (not the full discovery sequence). Once gaps are filled, skip to section 6 (Draft).

### 4. Quick Context Scan

After the user describes their intent, perform a rapid scan:

**Scan Locations (in parallel where possible):**
- `{planning_artifacts}/**` — existing planning artifacts
- `{implementation_artifacts}/**` — existing specs
- `{project_knowledge}/**` — project docs
- `docs/**` — general docs

**Look For:**
- Existing specs related to the same topic
- Product briefs or PRDs that provide context
- Project documentation (README, architecture docs)
- Project context file (`**/project-context.md`)
- For sharded content: if `*foo*.md` not found, also check `*foo*/index.md`

**Report findings:**
- "I found [N] related documents: [list]. I'll use these as context."
- Or: "No existing documents found related to this topic."

Load relevant documents for context. Track in `inputDocuments` frontmatter.

### 5. Collaborative Discovery

Based on the user's pitch AND discovered context, fill gaps through conversation. Ask about what you DON'T know — not what you can see in the codebase or documents.

**Round 1 — WHY (Problem & Context):**
- What exists today? What's wrong with it?
- What's the trigger — why now, not last month?
- Who is affected and how?
- What happens if we do nothing?

Ask 3-5 focused questions in a single message. Wait for response.

**Round 2 — WHAT & WHAT NOT (Goals & Scope):**
- What does "done" look like concretely? What are the measurable outcomes?
- What are we explicitly NOT doing? What adjacent problems are tempting but out of scope?
- Any hard constraints (time, tech, team)?

Ask 3-5 focused questions. Wait for response.

**Soft gate:** After each round, instead of a hard menu: "Anything else on this topic, or shall we move on?"

### 6. Draft WHY / WHAT / WHAT NOT Sections

Synthesize the conversation into draft content. Apply quality standards from the template:

- **WHY**: Current State (factual), Problem Statement (specific, with who/how), Why Now (trigger)
- **WHAT**: Goals with P0/P1/P2 priorities, measurable Success Criteria
- **WHAT NOT**: Non-obvious exclusions with brief justification (not trivial things)

Present the draft, then **challenge it with the user:**

- "Is the problem statement something we can observe today, or is it aspirational?"
- "If we do nothing for 6 months, what concretely goes wrong?"
- "Is [goal X] measurable? How would we know it's achieved — what number changes?"
- "Would anyone reasonably expect [non-goal Y] to be in scope? If not, it's too obvious — replace it."
- "Are the P0 goals the ones where failure means the whole thing is worthless?"

Iterate the draft until the user confirms it reflects their intent. Only then proceed to section 7.

### 7. Detect Work Type

Based on the conversation, classify the work type. This shapes vocabulary and emphasis in later steps:

- **Feature** (default) — user-facing functionality. Goals use P0/P1/P2, AC use Given/When/Then, tasks follow schema→logic→API→UI ordering.
- **Infrastructure** — backend, DevOps, platform work. Goals become operational targets (latency, throughput, availability). AC become precondition/action/verification. No UI layer in task ordering.
- **Refactoring** — restructuring without behavior change. Goals are structural (reduced coupling, improved testability). AC focus on behavior preservation. Risks focus on regression.
- **Greenfield** — no existing codebase. Step 2 pivots from investigation to tech stack decisions and scaffold planning. Codebase Context becomes Architecture Decisions.

Note the detected type in the spec frontmatter (add `work_type` field). If unclear, ask the user. This classification travels with the spec — later steps adapt their behavior accordingly.

### 8. Create WIP Spec File

- Copy template from `./assets/spec-template.md` to `{outputFile}`
- Fill in frontmatter: slug, title, status (`wip`), created date, author, work_type, tech_stack (if known)
- Fill in WHY, WHAT, WHAT NOT sections with drafted content
- Run: `python3 ./scripts/manage-frontmatter.py {outputFile} complete step-01-understand`
- Track loaded documents in `inputDocuments`

### 9. Menu

Display:

"**Select:**
- **[A] Advanced Elicitation** — deeper critique to sharpen problem definition and scope
- **[P] Party Mode** — multi-agent perspectives on the problem framing
- **[C] Continue** to Investigation (Step 2 of 5)"

**Handling:**
- **A**: Invoke `bmad-advanced-elicitation` with WHY/WHAT/WHAT NOT content. Ask "Accept refinements? (y/n)". If yes, update spec and redisplay menu. If no, redisplay.
- **P**: Invoke `bmad-party-mode` with problem & scope. Ask "Accept changes? (y/n)". Update or keep, redisplay.
- **C**: Run `python3 ./scripts/manage-frontmatter.py {outputFile} complete step-01-understand`, then read fully and follow: `./step-02-investigate.md`
- **Other**: Respond helpfully, redisplay menu.

Halt and wait for user input. Only proceed on 'C'.
