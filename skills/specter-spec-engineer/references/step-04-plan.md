# Step 4: Plan — Implementation Tasks & Acceptance Criteria

**Progress: Step 4 of 5** — Next: Review

## STEP GOAL

Generate the Implementation Plan (ordered tasks with concrete file paths and actions), Acceptance Criteria in Given/When/Then format, and Testing Strategy. This step makes the spec actionable — a fresh dev agent reads this and knows exactly what to do.

## Step Rules

- Every task MUST reference specific file paths and concrete actions
- Tasks MUST be ordered by dependency (lowest-level first)
- Acceptance criteria MUST use Given/When/Then format
- FORBIDDEN to leave any placeholder or "TBD" — everything is concrete
- FORBIDDEN to skip edge cases in acceptance criteria
- Cross-reference: every file in `files_to_modify` must appear in at least one task

## Sequence of Instructions

### 1. Review Complete Spec State

Read the WIP spec at `{outputFile}` — ALL previous sections:
- WHY/WHAT/WHAT NOT — problem, goals, scope
- HOW — chosen solution direction, trade-offs, appetite
- RISKS — identified risks and mitigations
- Codebase Context — files, patterns, constraints, commands

### 2. Generate Implementation Tasks

Create an ordered task list. Each task follows this format:

```markdown
- [ ] **Task N** — [Brief title] (AC: X, Y)
  - **Files:** `path/to/file.ts` — create | modify | delete
  - **Action:** [Specific enough for a fresh agent — what to do, not how to think]
  - **Depends on:** Task X (or "None")
  - **Verify:** [How to confirm this task is done]
```

**Ordering rules:**
1. Schema / data model changes first
2. Core logic / business rules second
3. Integration / API layer third
4. UI / presentation fourth
5. Tests alongside or after their source
6. Configuration / deployment last

**Quality checks before presenting:**
- Every file in `files_to_modify` frontmatter appears in at least one task
- No task modifies more than 3-4 files (split if needed)
- Dependencies form a DAG — no circular dependencies
- Each task is completable in isolation given its dependencies are done

Present the task list, then **challenge it:**
- "Could a dev agent who has never seen this codebase start Task 1 right now without asking a question?"
- "Is any task doing too much? If it takes more than a few hours, it should be split."
- "Are there hidden subtasks inside any of these — things that look simple but aren't?"
- "If Task N fails, does it block everything downstream or can we work around it?"
- "Am I missing a task for test setup, migration, or configuration?"

Iterate until the user confirms the plan is actionable.

### 3. Generate Acceptance Criteria

For each goal from WHAT, produce Given/When/Then acceptance criteria:

```markdown
**AC-N: [Criterion title]**

**Given** [precondition — system state before the action]
**When** [action — what the user or system does]
**Then** [expected result — observable, verifiable outcome]
```

**Coverage requirements:**
- Happy path for each P0 goal (mandatory)
- Error/failure scenarios for each P0 goal
- Edge cases identified in RISKS section
- Boundary conditions (empty state, max load, concurrent access)
- State transitions (if applicable)

**Challenge the AC with the user:**
- "If all these AC pass but the feature still feels broken, what scenario did we miss?"
- "What's the worst thing a user could do that we haven't covered?"
- "Are there race conditions, concurrent access, or timing issues we should test?"
- "What happens when this feature interacts with [related feature from codebase context]?"

Iterate until the user confirms coverage is complete.

### 4. Define Testing Strategy

Aligned with test patterns discovered in step-02:

**Unit Tests:** What to test, mocking strategy (from existing patterns), key assertions
**Integration Tests:** Integration points to test, test data setup
**E2E Tests (if applicable):** Critical user flows, environment requirements
**Manual Verification:** What requires human verification, specific steps

### 5. Verify Commands

Cross-reference commands from step-02 with the actual project configuration. Check package.json, Makefile, or equivalent to confirm:
- Build & run commands are exact
- Test commands include how to run just this feature's tests
- Lint/format commands are current

Update the Commands section if anything changed.

### 6. Draft Plan Sections

Synthesize into spec sections:

**Implementation Plan > Tasks:** Ordered task list with all details
**Implementation Plan > Appetite:** Value from step-03
**VERIFY > Acceptance Criteria:** Given/When/Then for each criterion
**VERIFY > Edge Cases:** Boundary conditions
**VERIFY > Testing Strategy:** Unit, integration, e2e, manual
**Commands:** Verified build, test, lint commands

Present the complete draft. **Final challenge:**
- "Read this plan as if you're a dev agent seeing it for the first time — where would you get stuck?"
- "Is the testing strategy realistic given the appetite?"

Iterate until the user confirms.

### 7. Update WIP Spec

Write Implementation Plan, VERIFY, and Commands sections to the spec. Run: `python3 ./scripts/manage-frontmatter.py {outputFile} complete step-04-plan`

### 8. Menu

Display:

"**Select:**
- **[A] Advanced Elicitation** — deeper analysis of task decomposition or AC coverage
- **[P] Party Mode** — multi-agent review of the implementation plan
- **[C] Continue** to Review (Step 5 of 5)"

**Handling:**
- **A**: Invoke `bmad-advanced-elicitation` with plan + AC. Ask "Accept? (y/n)". Update or keep, redisplay.
- **P**: Invoke `bmad-party-mode` with full plan. Ask "Accept? (y/n)". Update or keep, redisplay.
- **C**: Run `python3 ./scripts/manage-frontmatter.py {outputFile} complete step-04-plan`, then read fully and follow: `./step-05-review.md`
- **Other**: Respond helpfully, redisplay menu.

Halt and wait for user input. Only proceed on 'C'.
