# Specter Output Adapter

## Rule

This project uses **Specter** as its spec management system. All artifact outputs go to Specter's database via MCP tools instead of files on disk.

**When a workflow step tells you to:**
- "Append to {outputFile}" or "Save to {outputFile}" or "Write to {outputFile}"
- "Write to disk" or "Save content to file"
- Create or update any file in `_bmad-output/` or `{planning_artifacts}/` or `{implementation_artifacts}/`

**You MUST instead:**
1. Use the MCP tool `specter_save_artifact` to save the content
2. The `ticketRef` is provided in the workflow context (e.g. `{ticketRef}`)
3. Map the artifact type from the workflow context:
   - PRD workflows → type: `prd`
   - Architecture workflows → type: `architecture`
   - Epic/story workflows → type: `epic` or `story`
   - Sprint status → type: `sprint-status`

## How to save an artifact

```
specter_save_artifact({
  ticketRef: "{ticketRef}",
  type: "prd",
  title: "Product Requirements Document",
  content: "<full markdown content including all appended sections so far>",
  metadata: { stepsCompleted: ["step-01", "step-02", ...] }
})
```

**Important:** Each call to `specter_save_artifact` sends the **full accumulated content**, not just the new section. The tool does an upsert — it replaces the previous version of the artifact with the updated one.

## Tracking stepsCompleted

Instead of updating YAML frontmatter in a file, track `stepsCompleted` in the `metadata` field of `specter_save_artifact`. Each time a step completes and says "update frontmatter", add the step name to the `stepsCompleted` array in metadata.

## Reading previous content

When a step says "Read {outputFile}" or "Check frontmatter", use `specter_get_spec` to read the current spec state, and check the artifact's content from a previous `specter_save_artifact` call that you have in your conversation context.

## Other MCP tools available

- `specter_get_spec` — Read spec state (context, constraints, DoD, steps, etc.)
- `specter_update_spec` — Update spec fields (context, constraints, DoD, steps, decisions, risks, etc.)
- `specter_advance_status` — Transition spec status (draft → specifying → ready → in-progress → review → done)
- `specter_list_specs` — List all specs, optionally by status

## What NOT to do

- Do NOT write files to `_bmad-output/`, `{planning_artifacts}/`, or `{implementation_artifacts}/`
- Do NOT create markdown files in the repository for spec artifacts
- Do NOT skip saving — every time a step says "append to document", save via MCP
