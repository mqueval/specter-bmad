# Specter Output Adapter

## Prerequisite

Check if `specter_save_artifact` is available as an MCP tool.
If not, **stop here** — this adapter requires the Specter MCP server. Continue with normal BMAD file output only.

## Rule

This project uses **Specter** as its spec management system. During the workflow, write files normally as BMAD expects. **At the end of the workflow**, synchronize your results with Specter.

## During the workflow

Work normally:
- Write to `_bmad-output/`, `{planning_artifacts}/`, `{implementation_artifacts}/` as instructed by the workflow steps
- Update YAML frontmatter as normal
- Read and append to output files as normal

**Do not call Specter MCP tools during the workflow steps.** Focus on producing the best output.

## At the end of the workflow — Sync with Specter

When all workflow steps are complete, perform these two actions:

### 1. Save the artifact to Specter

Save the final document to Specter's database using `filePath` (the server reads the file directly):

```
specter_save_artifact({
  ticketRef: "{ticketRef}",
  type: "<prd|architecture|epic|story|sprint-status>",
  title: "<document title>",
  filePath: "<absolute path to the final output file>"
})
```

Map the artifact type:
- PRD / product brief → `prd`
- Architecture / tech-spec → `architecture`
- Epic or story → `epic` or `story`
- Sprint status → `sprint-status`

### 2. Update the spec with structured data

Extract key information from your work and update the spec:

```
specter_update_spec({
  ticketRef: "{ticketRef}",
  partial: {
    context: "<problem statement — why this work exists>",
    inScope: ["<what is included>", ...],
    outOfScope: ["<what is excluded>", ...],
    constraints: ["<technical or business constraints>", ...],
    acceptanceCriteria: ["<Given/When/Then or criteria>", ...],
    decisions: [
      {
        id: "<unique-id>",
        title: "<ADR title>",
        context: "<what prompted this decision>",
        pros: ["<argument for>", ...],
        cons: ["<argument against>", ...],
        decision: "<the decision made>",
        confidence: "<low|medium|high|unanimous>"
      }
    ],
    risks: [
      {
        id: "<unique-id>",
        description: "<risk description>",
        mitigation: "<how to mitigate>",
        severity: "<low|medium|high>"
      }
    ],
    steps: [
      {
        number: "01",
        title: "<implementation step>",
        description: "<what to do>"
      }
    ]
  }
})
```

**Only include fields that your workflow produced.** Don't fabricate data for fields you didn't work on.

### 3. Advance the spec status

If the workflow completed successfully:

```
specter_advance_status({
  ticketRef: "{ticketRef}",
  to: "ready"
})
```

## Error handling

If a Specter MCP call fails:
1. **Report the error clearly to the user** — include the tool name, the error message, and which artifact was affected
2. Continue with the remaining sync steps (don't stop at the first failure)
3. At the end, provide a summary of all failed sync operations so the user can act on them

The files on disk remain the source of truth as fallback, but failed syncs must be visible.

## MCP tools available

- `specter_get_spec` — Read current spec state
- `specter_update_spec` — Update spec fields (partial update)
- `specter_save_artifact` — Save artifact (use `filePath` for large documents)
- `specter_advance_status` — Transition spec status
- `specter_list_specs` — List all specs
- `specter_add_note` — Add a note to the spec timeline
