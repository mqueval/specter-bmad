# Step 3: Design — Solution Direction & Risk Assessment

**Progress: Step 3 of 5** — Next: Plan

## STEP GOAL

Define the HOW (solution direction with alternatives and trade-offs), identify RISKS (rabbit holes, dependencies, unknowns), and set the Appetite (time/scope budget). This step turns understanding into a design decision.

## Step Rules

- Focus on DESIGN DECISIONS — not implementation details
- Always present at least 2 alternatives, never just one approach
- Every trade-off must have explicit justification
- FORBIDDEN to skip risk identification — no spec ships without risks documented
- FORBIDDEN to generate implementation tasks — that's step 4
- Challenge assumptions: surface what the user hasn't considered
- Present options with clear trade-offs, let the user decide

## Sequence of Instructions

### 1. Review Current Spec State

Read the WIP spec at `{outputFile}` to ground yourself in:
- WHY/WHAT/WHAT NOT (the problem and scope)
- Codebase Context (technical landscape, constraints, patterns)
- Files to modify and patterns to follow

### 2. Solution Direction Exploration

Based on the problem (WHY), goals (WHAT), and constraints (Codebase Context), propose 2-3 solution approaches.

For each approach, present:

| | Approach A | Approach B | Approach C |
|---|---|---|---|
| **Summary** | one-line | one-line | one-line |
| **Pros** | advantages | advantages | advantages |
| **Cons** | disadvantages | disadvantages | disadvantages |
| **Pattern fit** | how well it aligns with existing code | ... | ... |

Ask:
- "Which approach resonates? Or do you see a hybrid?"
- "Are there approaches I haven't considered?"
- "What's your instinct telling you?"

Wait for response.

### 3. Refine Chosen Approach

Once the user selects or proposes an approach:

- Detail the chosen approach — enough specificity that the WHY behind each decision is clear
- Document explicitly what was rejected and why (this prevents future re-discussion)
- Identify the key trade-offs being accepted

**Challenge the chosen approach:**
- "What's the weakest part of this approach — where does it bend first under pressure?"
- "If this was someone else's design and you were reviewing it, what would you push back on?"
- "Is this the simplest approach that could work, or are we over-engineering?"
- "In 6 months, what will we regret about this choice?"

Iterate until the user is confident in the direction.

### 4. Risk Identification

Systematically surface risks across three categories:

**Rabbit Holes** — complexity traps:
- What parts could expand unexpectedly?
- Where might we discover hidden complexity?
- What seems simple but probably isn't?

**Dependencies** — external factors:
- External services, APIs, or teams
- Data migrations or schema changes
- Feature flags or rollout dependencies

**Unknown Unknowns** — assumptions that could be wrong:
- What questions don't we have answers to yet?
- What assumptions are we making?
- What would make us abandon this approach?

**Challenge risks with the user:**
- "What risks am I missing — what's kept you up at night about this?"
- "Which of these would make you abandon the approach entirely if it materialized?"
- "Have you seen a similar project fail? What killed it?"
- "Is there a dependency here that someone else controls — and what's our plan B if they don't deliver?"

Iterate until the user confirms the risk landscape is honest and complete.

### 5. Define Mitigations

For each identified risk, assign a strategy:
- **Accept** — low impact, unlikely, conscious choice
- **Mitigate** — specific action to reduce likelihood or impact
- **Avoid** — change approach to eliminate the risk
- **Transfer** — someone else handles this

### 6. Set Appetite

Appetite is a Shape Up concept: not an estimate but a **decision** that constrains the solution. If we can't solve it in this budget, we cut scope — not extend time.

Present concrete options based on the complexity you see:

"Based on what we've scoped:
- **Small batch** (1-2 days): [what would fit at this budget — what gets cut]
- **Medium batch** (3-5 days): [what would fit]
- **Large batch** (1-2 weeks): [what would fit]

What appetite feels right?"

Wait for response. The appetite shapes what's realistic for step 4.

### 7. Draft HOW / RISKS / Appetite

Synthesize into spec sections:

**HOW — Solution Direction:**
- Chosen Approach (detailed description with rationale)
- Alternatives Considered (table: alternative | rejected because)
- Trade-offs & Justification (what we're consciously accepting)

**RISKS — Rabbit Holes & Dependencies:**
- Identified Risks (with category, severity, likelihood)
- Dependencies (blocking vs informational)
- Mitigations (strategy for each risk)

Present the draft, then **challenge it:**
- "Does the Alternatives table make it obvious why we chose this path? Would a newcomer understand?"
- "Are the trade-offs honest — or are we hiding a risk in the 'acceptable' column?"
- "Does the appetite feel like a real constraint that shapes the solution, or just a number?"

Iterate until the user confirms.

### 8. Update WIP Spec

Write HOW and RISKS sections. Update `appetite` in frontmatter. Run: `python3 ./scripts/manage-frontmatter.py {outputFile} complete step-03-design`

### 9. Menu

Display:

"**Select:**
- **[A] Advanced Elicitation** — deeper trade-off analysis or risk probing
- **[P] Party Mode** — multi-agent debate on solution direction
- **[C] Continue** to Planning (Step 4 of 5)"

**Handling:**
- **A**: Invoke `bmad-advanced-elicitation` with design + risks. Ask "Accept? (y/n)". Update or keep, redisplay.
- **P**: Invoke `bmad-party-mode` with design decisions. Ask "Accept? (y/n)". Update or keep, redisplay.
- **C**: Run `python3 ./scripts/manage-frontmatter.py {outputFile} complete step-03-design`, then read fully and follow: `./step-04-plan.md`
- **Other**: Respond helpfully, redisplay menu.

Halt and wait for user input. Only proceed on 'C'.
