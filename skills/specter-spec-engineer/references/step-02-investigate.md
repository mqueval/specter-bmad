# Step 2: Investigate — Codebase Deep Dive

**Progress: Step 2 of 5** — Next: Design

## STEP GOAL

Deep dive into the codebase to map technical constraints, identify files to modify, discover existing patterns, and build the Codebase Context + Commands sections. This step grounds the spec in reality.

## Step Rules

- FORBIDDEN to discuss HOW (solution design) — only map the technical landscape
- Map what exists, don't propose what should change yet
- Combine code analysis with user knowledge — ask about what inspection alone can't reveal
- Batch tool calls: when scanning multiple directories or patterns, run reads/greps in parallel

## Sequence of Instructions

### 1. Review Current Spec State

Read the WIP spec at `{outputFile}` to understand:
- The problem being solved (WHY)
- The goals (WHAT)
- The scope boundaries (WHAT NOT)

This context guides which parts of the codebase to investigate.

### 2. Adapt to Work Type

Read the `work_type` from the spec frontmatter.

**If greenfield** (no existing codebase): Pivot this step. Instead of investigating existing code, facilitate:
- Tech stack decisions (languages, frameworks, DB, hosting)
- Project scaffold and directory structure planning
- Dependency selection (key libraries, tools)
- Architecture pattern selection (monolith, microservices, serverless, etc.)
- CI/CD and dev tooling setup

Then skip to section 6 (Draft Codebase Context) with "Architecture Decisions" instead of "Existing Patterns."

**For all other work types:** Proceed with investigation below.

### 3. Codebase Structure Discovery

Perform a systematic scan:

**Project Structure:**
- Project type (monorepo, frontend, backend, fullstack, library)
- Directory structure and key entry points
- Tech stack: languages, frameworks, exact versions (check package.json, Cargo.toml, go.mod, etc.)

**Relevant Areas** (guided by WHY/WHAT from step-01):
- Which modules/packages/services are involved?
- Which files will likely need modification?
- What are the entry points for the feature/change?

### 4. Pattern Discovery

Find analogous code — this is the most valuable investigation activity. Similar features already implemented are the best guide for a dev agent.

**Code Patterns:**
- How are similar features implemented? Find the closest analog.
- Architectural patterns (MVC, hexagonal, hooks, event sourcing, etc.)
- Naming conventions, state management, error handling

**Test Patterns:**
- Testing frameworks in use
- How are similar features tested? Find analogous tests.
- Test patterns (mocks, fixtures, factories), test file locations

**Build & Dev:**
- Exact dev/build/test/lint commands (from package.json scripts, Makefile, etc.)
- CI/CD configurations to be aware of

### 5. Constraint Mapping

Identify constraints that will affect the solution:

**Technical:** DB schema implications, API contracts, performance-sensitive paths, type system constraints, third-party limitations

**Integration Points:** Other systems/services touched, APIs consumed/exposed, shared state

Present findings and **challenge with the user:**
- "Are there constraints I missed — things the code won't tell me?"
- "Any technical debt or known issues that could bite us in these areas?"
- "Are there patterns you've seen fail here, or ones you want to enforce?"
- "Is there a part of this codebase that looks simple but has hidden complexity?"
- "Any tribal knowledge — things that aren't in the code or docs but everyone on the team knows?"

Iterate until the user confirms the technical landscape is complete.

### 6. Build Files-to-Modify List

Compile a concrete list from investigation:

```
files_to_modify:
  - path: 'src/foo/bar.ts'
    action: 'modify'
    reason: 'Add new handler for X'
  - path: 'src/foo/new-file.ts'
    action: 'create'
    reason: 'New module for Y'
```

Present the list to the user for validation. Ask: "Any files I missed or got wrong?"

### 7. Draft Codebase Context + Commands

Synthesize investigation into spec sections:

**Codebase Context:**
- Relevant Files & Patterns (files to modify with actions, key reference files)
- Tech Stack (languages, frameworks, exact versions)
- Existing Patterns to Follow (conventions from analogous code, architecture patterns, test patterns)

**Commands:**
- Exact build, run, test, lint commands (from package.json, Makefile, etc.)
- Include how to run just the tests relevant to this feature

Present the draft, then **challenge it:**
- "Is any file in this list unnecessary — could we achieve the goal without touching it?"
- "Am I missing a file that will need changes as a side effect?"
- "Are these the real commands, or are there wrappers/aliases the team actually uses?"

Iterate until the user confirms. Then update `files_to_modify` and `tech_stack` frontmatter.

### 8. Update WIP Spec

Write Codebase Context and Commands sections to the spec. Update `files_to_modify`, `tech_stack`, and any new `inputDocuments` in frontmatter. Run: `python3 ./scripts/manage-frontmatter.py {outputFile} complete step-02-investigate`

### 9. Menu

Display:

"**Select:**
- **[A] Advanced Elicitation** — deeper technical analysis of constraints and patterns
- **[P] Party Mode** — multi-agent review of technical landscape
- **[C] Continue** to Design (Step 3 of 5)"

**Handling:**
- **A**: Invoke `bmad-advanced-elicitation` with codebase context. Ask "Accept? (y/n)". Update or keep, redisplay.
- **P**: Invoke `bmad-party-mode` with technical findings. Ask "Accept? (y/n)". Update or keep, redisplay.
- **C**: Run `python3 ./scripts/manage-frontmatter.py {outputFile} complete step-02-investigate`, then read fully and follow: `./step-03-design.md`
- **Other**: Respond helpfully, redisplay menu.

Halt and wait for user input. Only proceed on 'C'.
