# Step 5: Review — Validation & Finalization

**Progress: Step 5 of 5** — Final Step

## STEP GOAL

Validate the complete spec against the "Ready for Development" standard, iterate on feedback, offer adversarial review, and finalize by renaming from WIP to final. No spec ships without passing all checks.

## Step Rules

- Validate EVERY section — flag ALL issues before asking for approval
- FORBIDDEN to approve a spec with placeholders, TBDs, or vague tasks
- FORBIDDEN to skip the validation checklist
- Be rigorous — the goal is a spec a fresh dev agent can execute without questions
- The user explicitly approves finalization — never auto-finalize

## Sequence of Instructions

### 1. Read Complete Spec

Read the entire WIP spec at `{outputFile}` — every section, every frontmatter field.

### 2. Present Spec Summary

"**Spec Summary: [title]**

| Section | Status | Notes |
|---------|--------|-------|
| WHY — Problem & Context | [pass/fail] | [brief note if fail] |
| WHAT — Goals & Success | [pass/fail] | |
| WHAT NOT — Non-Goals | [pass/fail] | |
| HOW — Solution Direction | [pass/fail] | |
| RISKS — Rabbit Holes | [pass/fail] | |
| VERIFY — Acceptance Criteria | [pass/fail] | |
| Codebase Context | [pass/fail] | |
| Implementation Plan | [pass/fail] | |
| Commands | [pass/fail] | |

**Appetite:** [value]
**Files to modify:** [count] files
**Tasks:** [count] tasks
**Acceptance Criteria:** [count] criteria"

### 3. Run Readiness Validation

**First, run the deterministic validation script:**

```bash
python3 ./scripts/validate-readiness.py {outputFile} --json
```

This checks structural readiness: sections present, frontmatter populated, AC in Given/When/Then, tasks with file paths, no placeholders, files_to_modify coverage. Review the script output and report findings to the user.

**Then, layer qualitative checks** that require judgment — the script handles structure, you handle semantics:

**ACTIONABLE — Can a dev agent start without asking questions?**
- [ ] Every task has a file path and a clear action
- [ ] No task references vague concepts without concrete paths
- [ ] File paths in tasks match `files_to_modify` frontmatter
- Anti-pattern: "Implement the notification system" (no file, no action)

**LOGICAL — Are tasks ordered by dependency?**
- [ ] Tasks ordered lowest-level first (schema → logic → API → UI → tests)
- [ ] No circular dependencies
- [ ] Dependencies explicitly stated per task
- Anti-pattern: UI task before the API it consumes exists

**TESTABLE — Can we verify success objectively?**
- [ ] All AC use Given/When/Then format
- [ ] Happy path covered for every P0 goal
- [ ] Edge cases from RISKS section have corresponding AC
- [ ] Testing strategy references actual test patterns from codebase
- Anti-pattern: "Test that it works" (no observable criterion)

**COMPLETE — Is everything filled in?**
- [ ] No "TBD", "TODO", or placeholder text anywhere
- [ ] No "see X for details" references — everything is inlined
- [ ] WHY answers: what exists, what's wrong, why now
- [ ] WHAT NOT has at least one non-obvious exclusion
- [ ] HOW documents at least one rejected alternative with reason
- [ ] RISKS has at least one risk with mitigation
- Anti-pattern: "Stack: same as the rest of the project" (not explicit)

**SELF-CONTAINED — Can a fresh agent implement from this document alone?**
- [ ] Tech stack documented with versions
- [ ] Existing patterns documented (not assumed)
- [ ] Build/test/lint commands are exact (not "run the tests")
- [ ] No dependency on conversation history or external context
- Anti-pattern: "See the PRD for details" (not self-contained)

Present validation results with pass/fail per criterion and specific issues flagged.

### 4. Address Issues

If any checks fail:
- Present each issue clearly with the specific text that fails
- Suggest a concrete fix for each
- Ask user to approve fixes or provide corrections

Iterate until all checks pass. Re-validate after each round of fixes.

### 5. Menu

Display only when ALL readiness checks pass:

"**The spec passes all readiness checks.**

**Select:**
- **[R] Adversarial Review** — invoke `bmad-review-adversarial-general` for a cynical critique that finds what you missed
- **[E] Edge Case Hunt** — invoke `bmad-review-edge-case-hunter` for exhaustive boundary condition analysis
- **[A] Advanced Elicitation** — deeper refinement of any section
- **[P] Party Mode** — multi-agent perspectives on the complete spec
- **[F] Finalize** — approve and ship the spec"

**Handling:**
- **R**: Invoke `bmad-review-adversarial-general` with complete spec. Present findings. Ask "Apply changes? (y/n)". If yes, apply and re-run validation. Redisplay menu.
- **E**: Invoke `bmad-review-edge-case-hunter` with complete spec. Present findings. Ask "Apply changes? (y/n)". If yes, apply and re-run validation. Redisplay menu.
- **A**: Invoke `bmad-advanced-elicitation` with the section user wants to refine. Ask "Accept? (y/n)". Update or keep, redisplay.
- **P**: Invoke `bmad-party-mode` with complete spec. Ask "Accept? (y/n)". Update or keep, re-validate, redisplay.
- **F**: Proceed to finalization (section 6).
- **Other**: Respond helpfully, redisplay menu.

Halt and wait for user input. Only finalize on 'F'.

### 6. Process Deferred Notes

Before finalization, review the `## Deferred Notes` section (if present and non-empty):

For each deferred item, decide with the user:
- **Incorporate** — the item belongs in this spec. Move it to the relevant section (WHY, RISKS, etc.) and integrate it properly.
- **Future work** — the item is valid but out of scope. Move it to WHAT NOT with a note like "Deferred to future iteration."
- **Discard** — the item is no longer relevant. Remove it.

Once all items are processed, empty or remove the Deferred Notes section. A finalized spec should not have dangling deferred items.

### 7. Finalize Spec

When user selects 'F':

**Update Frontmatter:**
Run: `python3 ./scripts/manage-frontmatter.py {outputFile} complete step-05-review`
Then set `updated: [current date]` in frontmatter.

**Rename File:**
- From `wip-spec.md` to `{slug}-spec.md` (slug from frontmatter, or derive kebab-case from title)
- Final path: `{implementation_artifacts}/specs/{slug}-spec.md`

**Confirmation:**

"**Spec finalized!**

- **File:** `{implementation_artifacts}/specs/{slug}-spec.md`
- **Status:** Ready for Development
- **Tasks:** [count] implementation tasks
- **AC:** [count] acceptance criteria
- **Appetite:** [value]

This spec is ready to hand off to a dev agent."

