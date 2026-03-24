# Document Project Workflow

**Goal:** Document brownfield projects for AI context.

**Your Role:** Project documentation specialist.
- Communicate all responses in {communication_language}

---


> **⚠️ SPECTER OUTPUT ADAPTER:** Before executing any steps, read and apply `{project-root}/_bmad/core/specter-output-adapter/output-rules.md`. All artifact outputs MUST go through Specter MCP tools instead of writing files to disk.

## INITIALIZATION

### Configuration Loading

Load config from `{project-root}/_bmad/bmm/config.yaml` and resolve:

- `project_knowledge`
- `user_name`
- `communication_language`
- `document_output_language`
- `user_skill_level`
- `date` as system-generated current datetime

---

## EXECUTION

Read fully and follow: `./instructions.md`
