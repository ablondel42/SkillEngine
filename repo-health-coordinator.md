Yes — build **only the coordinator first**, with a hard approval pause before fixes, strict schemas on every file, and task Create Read Update Delete built into the coordinator from day one. Approval-based agent workflows work best when they pause at a review step and resume only after explicit approval metadata is recorded, and strict JSON Schema only stays strict when you explicitly block extra keys with `additionalProperties: false` because unknown keys are otherwise allowed by default. [json-schema](https://json-schema.org/understanding-json-schema/reference/object)

## Recommended shape

For the coordinator alone, I’d keep it boring: one local service, file-based state, schema validation, and a tiny local API for task Create Read Update Delete using the normal `POST`, `GET`, `PATCH`, and `DELETE` patterns.  Do not build the real dashboard or many agents yet; just build the coordinator so it can accept one audit agent and one fix agent cleanly. [restfulapi](https://restfulapi.net/http-methods/)

## Folder structure

Use this exact starter structure:

```text
repo-health-coordinator/
├─ prompts/
│  ├─ 01-scaffold.md
│  ├─ 02-core-schemas.md
│  ├─ 03-state-machine.md
│  ├─ 04-storage-and-validation.md
│  ├─ 05-task-crud-api.md
│  ├─ 06-approval-gate.md
│  ├─ 07-subagent-contracts.md
│  ├─ 08-dashboard-projection.md
│  └─ 09-smoke-tests.md
├─ schemas/
│  ├─ health-report.schema.json
│  ├─ task-record.schema.json
│  ├─ task-crud-request.schema.json
│  ├─ task-crud-response.schema.json
│  ├─ approval-state.schema.json
│  ├─ dashboard.schema.json
│  ├─ subagent-audit-output.schema.json
│  ├─ subagent-fix-output.schema.json
│  └─ subagent-verify-output.schema.json
├─ app/
│  ├─ coordinator/
│  │  ├─ main.py
│  │  ├─ config.py
│  │  ├─ state_machine.py
│  │  ├─ validator.py
│  │  ├─ ids.py
│  │  ├─ storage.py
│  │  ├─ task_service.py
│  │  ├─ approval_service.py
│  │  ├─ report_service.py
│  │  ├─ subagent_router.py
│  │  └─ dashboard_projection.py
│  ├─ api/
│  │  ├─ routes_tasks.py
│  │  ├─ routes_runs.py
│  │  └─ routes_approval.py
│  └─ models/
│     └─ README.md
├─ state/
│  ├─ audit/
│  │  ├─ health-report.json
│  │  └─ raw-subagent-results/
│  ├─ review/
│  │  └─ approval-state.json
│  ├─ fix/
│  │  └─ repair-results.json
│  ├─ verify/
│  │  └─ verification-results.json
│  ├─ dashboard/
│  │  └─ dashboard-data.json
│  ├─ tasks/
│  │  ├─ tasks.json
│  │  ├─ requests.json
│  │  └─ responses.json
│  └─ runs/
│     └─ current-run.json
├─ tests/
│  ├─ test_state_machine.py
│  ├─ test_task_crud.py
│  ├─ test_schema_validation.py
│  ├─ test_approval_gate.py
│  └─ test_subagent_contracts.py
├─ docs/
│  └─ coordinator-workflow.md
├─ pyproject.toml
└─ README.md
```

## Prompt sequence

Run these prompts in order. The goal is to finish with a coordinator that can already receive one audit output, create tasks, let you review tasks, and later hand approved tasks to the first fix agent.

### Prompt 1 — scaffold

Save as `prompts/01-scaffold.md`.

```md
You are a senior backend engineer.

Build only the coordinator layer for a local-first repository health workflow.

Scope:
- Do not build real audit agents yet.
- Do not build real fix agents yet.
- Do not build a full dashboard UI yet.
- Build the coordinator so it is ready to accept those agents later.

Coordinator responsibilities:
1. Run state management for a 4-step workflow:
   - Step 1 audit and report
   - Step 2 user review and approval
   - Step 3 fix and report
   - Step 4 verify and report
2. Own task lifecycle management with Create, Read, Update, and Delete operations.
3. Validate all incoming and outgoing JSON files against schemas.
4. Generate derived dashboard data files.

Technical constraints:
- Use Python.
- Use a tiny local API and file-based JSON state.
- Keep the code simple, readable, and deterministic.
- Prefer boring architecture over smart architecture.

Create:
- the full folder structure
- placeholder files
- minimal README
- minimal run instructions
- no business logic yet

Return:
- full file tree
- starter file contents
```

### Prompt 2 — core schemas

Save as `prompts/02-core-schemas.md`.

```md
You are a JSON Schema architect.

Create the full schema set for a repository health coordinator.

Need these files:
- health-report.schema.json
- task-record.schema.json
- task-crud-request.schema.json
- task-crud-response.schema.json
- approval-state.schema.json
- dashboard.schema.json
- subagent-audit-output.schema.json
- subagent-fix-output.schema.json
- subagent-verify-output.schema.json

Rules:
- Use JSON Schema draft 2020-12.
- Use description on every important field.
- Use additionalProperties: false wherever possible.
- Make every schema strict and predictable.
- The system must support exactly 4 workflow steps.
- The task model must support Create, Read, Update, and Delete safely.
- A task can come from a finding or be created manually by the user.
- Approval must be required before fixes run.
- Return only valid JSON.
```

### Prompt 3 — state machine

Save as `prompts/03-state-machine.md`.

```md
You are a backend architect.

Implement only the coordinator state machine.

Workflow states:
- audit_complete
- awaiting_user_approval
- fixing_approved_items
- verifying_repairs
- completed
- failed

Rules:
- The workflow must always start with Step 1.
- It must stop after Step 1 and wait for Step 2 approval.
- It cannot enter Step 3 unless at least one task is approved.
- It cannot enter Step 4 unless at least one fix result exists.
- Invalid transitions must be rejected clearly.

Build:
- state_machine.py
- current-run.json lifecycle
- helper functions for transitions
- tests for valid and invalid transitions

Return:
- code
- test cases
- short explanation
```

### Prompt 4 — storage and validation

Save as `prompts/04-storage-and-validation.md`.

```md
You are a backend engineer.

Implement the coordinator storage and schema validation layer.

Build:
- storage.py for reading and writing JSON state files
- validator.py for schema validation
- ids.py for stable identifiers
- report_service.py for reading and updating the master health report

Rules:
- All writes must be atomic.
- All schema validation failures must return plain-English errors.
- Raw subagent files must never be trusted until validated.
- The coordinator is the only writer of normalized state files.

Support files:
- state/audit/health-report.json
- state/tasks/tasks.json
- state/review/approval-state.json
- state/fix/repair-results.json
- state/verify/verification-results.json
- state/dashboard/dashboard-data.json

Return:
- code
- example validation error objects
```

### Prompt 5 — task CRUD API

Save as `prompts/05-task-crud-api.md`.

```md
You are a backend engineer.

Implement task Create, Read, Update, and Delete support for the coordinator.

Build:
- routes_tasks.py
- task_service.py

Operations:
- POST /tasks -> create task
- GET /tasks -> list tasks with filters
- GET /tasks/{taskId} -> get one task
- PATCH /tasks/{taskId} -> update editable fields
- DELETE /tasks/{taskId} -> delete if not started, otherwise soft-delete as cancelled
- GET /tasks/{taskId}/history -> get task history

Task rules:
- A task can come from an audit finding or be manually created by the user.
- Manual tasks must include a plain-English reason.
- Once execution starts, some fields must become locked.
- Every task change must create a history event.
- Unknown fields must be rejected.
- Return plain JSON only.

Editable fields:
- title
- description
- priority
- owner
- scopeNote
- tags
- approvalState

Return:
- code
- request examples
- response examples
- tests
```

### Prompt 6 — approval gate

Save as `prompts/06-approval-gate.md`.

```md
You are a backend engineer.

Implement the user approval checkpoint for the coordinator.

Build:
- approval_service.py
- routes_approval.py

Behavior:
- Read tasks created during Step 1.
- Allow review decisions:
  - approved
  - rejected
  - deferred
  - edited
- Save review decisions to approval-state.json
- Sync approved or rejected status back into tasks.json and health-report.json
- Refuse to move into Step 3 unless approval review is complete
- Refuse to send rejected or deferred tasks to fix execution

Need endpoints:
- GET /approval
- POST /approval/submit
- POST /tasks/{taskId}/approve
- POST /tasks/{taskId}/reject
- POST /tasks/{taskId}/defer

Return:
- code
- sample approval-state.json
- tests
```

### Prompt 7 — subagent contracts

Save as `prompts/07-subagent-contracts.md`.

```md
You are designing the coordinator-facing contract for future audit, fix, and verify subagents.

Build:
- subagent_router.py
- fake test adapters for one audit agent and one fix agent
- contract validation before normalization

Rules:
- Audit subagents return only JSON matching subagent-audit-output.schema.json
- Fix subagents return only JSON matching subagent-fix-output.schema.json
- Verify subagents return only JSON matching subagent-verify-output.schema.json
- Invalid outputs must be rejected
- Accepted audit outputs must create findings and tasks
- Accepted fix outputs must update task execution state and health-report.json
- Do not implement real domain logic yet
- Use one fake “documentation” agent and one fake “security” agent stub for testing

Return:
- code
- fake subagent outputs
- tests
```

### Prompt 8 — dashboard projection

Save as `prompts/08-dashboard-projection.md`.

```md
You are a backend engineer.

Build only the dashboard projection layer, not the full UI.

Goal:
Generate one derived dashboard-data.json file from the coordinator state.

The dashboard projection must include:
- current workflow step
- repository info
- run info
- summary cards
- findings table
- tasks table
- fix table
- verification table

Rules:
- Read only normalized state files
- Never read raw subagent outputs
- Flatten nested data for easy rendering
- Keep it simple and stable

Build:
- dashboard_projection.py
- example dashboard-data.json
- tests
```

### Prompt 9 — smoke tests

Save as `prompts/09-smoke-tests.md`.

```md
You are a test engineer.

Write smoke tests for the coordinator only.

Must cover:
1. Step 1 accepts a valid fake audit output and creates findings and tasks
2. Step 1 rejects invalid audit output
3. Step 2 records review decisions
4. Step 3 refuses to run if nothing is approved
5. Task Create works
6. Task Update works
7. Task Delete hard-deletes before execution starts
8. Task Delete soft-deletes after execution starts
9. Accepted fake fix output updates tasks and report
10. Dashboard projection refreshes correctly

Return:
- test files
- test fixtures
- one sample happy-path run
```

## Core schemas

Use `additionalProperties: false` on basically every object here, because JSON Schema allows extra keys by default unless you block them. [tour.json-schema](https://tour.json-schema.org/content/03-Objects/02-Additional-Properties)

### `schemas/task-record.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://localhost/schemas/task-record.schema.json",
  "title": "Task Record",
  "description": "Canonical task object owned by the coordinator.",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "id",
    "sourceType",
    "domain",
    "title",
    "description",
    "priority",
    "approvalState",
    "executionState",
    "verificationState",
    "owner",
    "createdAt",
    "updatedAt",
    "history"
  ],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^TASK-[0-9]{4,}$",
      "description": "Unique task id."
    },
    "sourceType": {
      "type": "string",
      "enum": ["finding", "manual"],
      "description": "Where the task came from."
    },
    "findingId": {
      "type": ["string", "null"],
      "description": "Linked finding id when the task came from an audit finding."
    },
    "manualReason": {
      "type": ["string", "null"],
      "description": "Why the task was created manually."
    },
    "domain": {
      "type": "string",
      "description": "Domain such as documentation or security."
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 160,
      "description": "Short task title."
    },
    "description": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2000,
      "description": "Plain-English explanation of the task."
    },
    "priority": {
      "type": "string",
      "enum": ["P0", "P1", "P2", "P3"],
      "description": "Urgency of the task."
    },
    "severity": {
      "type": ["string", "null"],
      "enum": ["critical", "high", "medium", "low", "info", null],
      "description": "Severity inherited from a finding when available."
    },
    "approvalState": {
      "type": "string",
      "enum": ["pending_review", "approved", "rejected", "deferred", "edited"],
      "description": "Current user review state."
    },
    "executionState": {
      "type": "string",
      "enum": ["not_started", "ready", "in_progress", "done", "failed", "skipped", "cancelled"],
      "description": "Current execution state."
    },
    "verificationState": {
      "type": "string",
      "enum": ["not_applicable", "pending", "passed", "failed", "partial", "unverifiable"],
      "description": "Current verification state."
    },
    "owner": {
      "type": "string",
      "minLength": 1,
      "description": "Assigned agent or person."
    },
    "scopeNote": {
      "type": ["string", "null"],
      "description": "Optional scope limit or note."
    },
    "tags": {
      "type": "array",
      "description": "Optional task labels.",
      "items": {
        "type": "string",
        "minLength": 1,
        "maxLength": 50
      },
      "uniqueItems": true
    },
    "createdAt": {
      "type": "string",
      "format": "date-time",
      "description": "When the task was created."
    },
    "updatedAt": {
      "type": "string",
      "format": "date-time",
      "description": "When the task was last changed."
    },
    "history": {
      "type": "array",
      "description": "Audit trail of task changes.",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["at", "action", "actor", "summary"],
        "properties": {
          "at": {
            "type": "string",
            "format": "date-time",
            "description": "When the history event happened."
          },
          "action": {
            "type": "string",
            "enum": [
              "created",
              "updated",
              "approved",
              "rejected",
              "deferred",
              "deleted",
              "cancelled",
              "execution_updated",
              "verification_updated"
            ],
            "description": "What changed."
          },
          "actor": {
            "type": "string",
            "description": "Who made the change."
          },
          "summary": {
            "type": "string",
            "description": "Plain-English summary of the change."
          }
        }
      }
    }
  },
  "allOf": [
    {
      "if": {
        "properties": { "sourceType": { "const": "finding" } },
        "required": ["sourceType"]
      },
      "then": {
        "required": ["findingId"]
      }
    },
    {
      "if": {
        "properties": { "sourceType": { "const": "manual" } },
        "required": ["sourceType"]
      },
      "then": {
        "required": ["manualReason"]
      }
    }
  ]
}
```

### `schemas/health-report.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://localhost/schemas/health-report.schema.json",
  "title": "Health Report",
  "description": "Master internal report owned by the coordinator.",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schemaVersion",
    "repository",
    "run",
    "summary",
    "domains",
    "findings",
    "tasks",
    "fixes",
    "verifications"
  ],
  "properties": {
    "schemaVersion": {
      "type": "string",
      "description": "Schema version."
    },
    "repository": {
      "type": "object",
      "additionalProperties": false,
      "required": ["name", "path", "defaultBranch"],
      "properties": {
        "name": { "type": "string", "description": "Repository name." },
        "path": { "type": "string", "description": "Local repository path." },
        "defaultBranch": { "type": "string", "description": "Default branch name." }
      }
    },
    "run": {
      "type": "object",
      "additionalProperties": false,
      "required": ["runId", "status", "currentStep", "startedAt", "finishedAt"],
      "properties": {
        "runId": {
          "type": "string",
          "pattern": "^RUN-[0-9]{4,}$",
          "description": "Unique run id."
        },
        "status": {
          "type": "string",
          "enum": [
            "audit_complete",
            "awaiting_user_approval",
            "fixing_approved_items",
            "verifying_repairs",
            "completed",
            "failed"
          ],
          "description": "Current coordinator state."
        },
        "currentStep": {
          "type": "integer",
          "enum": [1, 2, 3, 4],
          "description": "Current workflow step."
        },
        "startedAt": {
          "type": "string",
          "format": "date-time",
          "description": "When the run started."
        },
        "finishedAt": {
          "type": ["string", "null"],
          "format": "date-time",
          "description": "When the run finished."
        }
      }
    },
    "summary": {
      "type": "object",
      "additionalProperties": false,
      "required": ["healthScore", "counts"],
      "properties": {
        "healthScore": {
          "type": "integer",
          "minimum": 0,
          "maximum": 100,
          "description": "Overall repository health score."
        },
        "counts": {
          "type": "object",
          "additionalProperties": false,
          "required": [
            "findings",
            "tasks",
            "approvedTasks",
            "completedFixes",
            "passedVerifications"
          ],
          "properties": {
            "findings": { "type": "integer", "minimum": 0, "description": "Total findings." },
            "tasks": { "type": "integer", "minimum": 0, "description": "Total tasks." },
            "approvedTasks": { "type": "integer", "minimum": 0, "description": "Approved tasks." },
            "completedFixes": { "type": "integer", "minimum": 0, "description": "Completed fixes." },
            "passedVerifications": { "type": "integer", "minimum": 0, "description": "Passed verifications." }
          }
        }
      }
    },
    "domains": {
      "type": "array",
      "description": "Per-domain summary blocks.",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["id", "name", "score", "status", "ownerAgent"],
        "properties": {
          "id": { "type": "string", "description": "Domain id." },
          "name": { "type": "string", "description": "Domain name." },
          "score": { "type": "integer", "minimum": 0, "maximum": 100, "description": "Domain score." },
          "status": {
            "type": "string",
            "enum": ["healthy", "needs_attention", "awaiting_approval", "fixing", "verifying", "verified"],
            "description": "Domain state."
          },
          "ownerAgent": { "type": "string", "description": "Responsible subagent." }
        }
      }
    },
    "findings": {
      "type": "array",
      "description": "Normalized findings from audit agents.",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "id",
          "domain",
          "title",
          "description",
          "severity",
          "priority",
          "status",
          "sourceAgent",
          "evidence",
          "affectedFiles",
          "suggestedFix",
          "autoFixable"
        ],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^F-[0-9]{4,}$",
            "description": "Finding id."
          },
          "domain": { "type": "string", "description": "Finding domain." },
          "title": { "type": "string", "description": "Short finding title." },
          "description": { "type": "string", "description": "Finding explanation." },
          "severity": {
            "type": "string",
            "enum": ["critical", "high", "medium", "low", "info"],
            "description": "Finding severity."
          },
          "priority": {
            "type": "string",
            "enum": ["P0", "P1", "P2", "P3"],
            "description": "Repair urgency."
          },
          "status": {
            "type": "string",
            "enum": [
              "open",
              "approved_for_fix",
              "rejected",
              "deferred",
              "fixed",
              "partially_fixed",
              "failed_verification",
              "false_positive",
              "wont_fix"
            ],
            "description": "Finding lifecycle state."
          },
          "sourceAgent": { "type": "string", "description": "Audit agent name." },
          "evidence": {
            "type": "array",
            "minItems": 1,
            "description": "Proof for the finding.",
            "items": {
              "type": "object",
              "additionalProperties": false,
              "required": ["type", "path", "snippet"],
              "properties": {
                "type": {
                  "type": "string",
                  "enum": ["file", "command", "test", "config", "log"],
                  "description": "Kind of evidence."
                },
                "path": { "type": "string", "description": "Source path." },
                "line": {
                  "type": ["integer", "null"],
                  "minimum": 1,
                  "description": "Line number if relevant."
                },
                "snippet": { "type": "string", "description": "Short proof excerpt." }
              }
            }
          },
          "affectedFiles": {
            "type": "array",
            "minItems": 1,
            "items": { "type": "string" },
            "description": "Files affected by the finding."
          },
          "suggestedFix": { "type": "string", "description": "Suggested repair." },
          "autoFixable": { "type": "boolean", "description": "Whether auto-fix is likely safe." }
        }
      }
    },
    "tasks": {
      "type": "array",
      "description": "Canonical task list.",
      "items": {
        "$ref": "task-record.schema.json"
      }
    },
    "fixes": {
      "type": "array",
      "description": "Fix reports accepted by the coordinator.",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["id", "taskId", "findingId", "fixAgent", "status", "changedFiles", "testsRun"],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^X-[0-9]{4,}$",
            "description": "Fix id."
          },
          "taskId": { "type": "string", "description": "Related task id." },
          "findingId": { "type": ["string", "null"], "description": "Related finding id." },
          "fixAgent": { "type": "string", "description": "Fix agent name." },
          "status": {
            "type": "string",
            "enum": ["applied", "partial", "failed", "skipped"],
            "description": "Fix result."
          },
          "changedFiles": {
            "type": "array",
            "items": { "type": "string" },
            "description": "Files changed by the fix."
          },
          "testsRun": {
            "type": "array",
            "items": { "type": "string" },
            "description": "Checks run after the fix."
          },
          "patchSummary": {
            "type": "string",
            "description": "Plain-English summary of the change."
          }
        }
      }
    },
    "verifications": {
      "type": "array",
      "description": "Verification results accepted by the coordinator.",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["id", "fixId", "taskId", "verifyAgent", "status", "notes"],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^V-[0-9]{4,}$",
            "description": "Verification id."
          },
          "fixId": { "type": "string", "description": "Related fix id." },
          "taskId": { "type": "string", "description": "Related task id." },
          "verifyAgent": { "type": "string", "description": "Verify agent name." },
          "status": {
            "type": "string",
            "enum": ["passed", "failed", "partial", "unverifiable"],
            "description": "Verification result."
          },
          "notes": { "type": "string", "description": "Verification notes." },
          "regressions": {
            "type": "array",
            "items": { "type": "string" },
            "description": "Any new issues introduced by the fix."
          }
        }
      }
    }
  }
}
```

### `schemas/task-crud-request.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://localhost/schemas/task-crud-request.schema.json",
  "title": "Task CRUD Request",
  "description": "Request sent to the coordinator for task Create Read Update Delete operations.",
  "type": "object",
  "additionalProperties": false,
  "required": ["requestId", "operation", "requestedAt", "actor"],
  "properties": {
    "requestId": {
      "type": "string",
      "pattern": "^REQ-[0-9]{4,}$",
      "description": "Unique request id."
    },
    "operation": {
      "type": "string",
      "enum": ["create", "read", "list", "update", "delete", "approve", "reject", "defer"],
      "description": "Requested task operation."
    },
    "requestedAt": {
      "type": "string",
      "format": "date-time",
      "description": "When the request was made."
    },
    "actor": {
      "type": "string",
      "description": "Who made the request."
    },
    "taskId": {
      "type": ["string", "null"],
      "description": "Target task id when relevant."
    },
    "payload": {
      "type": ["object", "null"],
      "additionalProperties": false,
      "description": "Fields used for create or update operations.",
      "properties": {
        "sourceType": { "type": "string", "enum": ["finding", "manual"] },
        "findingId": { "type": ["string", "null"] },
        "manualReason": { "type": ["string", "null"] },
        "domain": { "type": "string" },
        "title": { "type": "string" },
        "description": { "type": "string" },
        "priority": { "type": "string", "enum": ["P0", "P1", "P2", "P3"] },
        "owner": { "type": "string" },
        "scopeNote": { "type": ["string", "null"] },
        "tags": {
          "type": "array",
          "items": { "type": "string" }
        },
        "approvalState": {
          "type": "string",
          "enum": ["pending_review", "approved", "rejected", "deferred", "edited"]
        }
      }
    },
    "filters": {
      "type": ["object", "null"],
      "additionalProperties": false,
      "description": "Optional filters for list operations.",
      "properties": {
        "domain": { "type": "string" },
        "priority": { "type": "string", "enum": ["P0", "P1", "P2", "P3"] },
        "approvalState": { "type": "string", "enum": ["pending_review", "approved", "rejected", "deferred", "edited"] },
        "executionState": { "type": "string", "enum": ["not_started", "ready", "in_progress", "done", "failed", "skipped", "cancelled"] },
        "owner": { "type": "string" }
      }
    }
  }
}
```

### `schemas/task-crud-response.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://localhost/schemas/task-crud-response.schema.json",
  "title": "Task CRUD Response",
  "description": "Coordinator response for task Create Read Update Delete operations.",
  "type": "object",
  "additionalProperties": false,
  "required": ["requestId", "ok", "message"],
  "properties": {
    "requestId": {
      "type": "string",
      "description": "Original request id."
    },
    "ok": {
      "type": "boolean",
      "description": "Whether the operation succeeded."
    },
    "message": {
      "type": "string",
      "description": "Plain-English result message."
    },
    "task": {
      "oneOf": [
        { "$ref": "task-record.schema.json" },
        { "type": "null" }
      ],
      "description": "One returned task when relevant."
    },
    "tasks": {
      "type": ["array", "null"],
      "description": "Task list for list operations.",
      "items": {
        "$ref": "task-record.schema.json"
      }
    },
    "errors": {
      "type": "array",
      "description": "Validation or business-rule errors.",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["field", "message"],
        "properties": {
          "field": { "type": "string", "description": "Failing field or rule." },
          "message": { "type": "string", "description": "Plain-English error." }
        }
      }
    }
  }
}
```

### `schemas/approval-state.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://localhost/schemas/approval-state.schema.json",
  "title": "Approval State",
  "description": "User review decisions recorded between audit and fix.",
  "type": "object",
  "additionalProperties": false,
  "required": ["schemaVersion", "runId", "status", "reviewedAt", "taskDecisions", "summary"],
  "properties": {
    "schemaVersion": {
      "type": "string",
      "description": "Schema version."
    },
    "runId": {
      "type": "string",
      "description": "Linked run id."
    },
    "status": {
      "type": "string",
      "enum": ["awaiting_user_approval", "review_complete"],
      "description": "Whether review is still pending or done."
    },
    "reviewedAt": {
      "type": ["string", "null"],
      "format": "date-time",
      "description": "When the review finished."
    },
    "taskDecisions": {
      "type": "array",
      "description": "One user decision per task.",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["taskId", "decision"],
        "properties": {
          "taskId": {
            "type": "string",
            "description": "Target task id."
          },
          "decision": {
            "type": "string",
            "enum": ["approved", "rejected", "deferred", "edited"],
            "description": "User decision."
          },
          "note": {
            "type": ["string", "null"],
            "description": "Optional plain-English note."
          },
          "editedPriority": {
            "type": ["string", "null"],
            "enum": ["P0", "P1", "P2", "P3", null],
            "description": "Optional updated priority."
          },
          "editedOwner": {
            "type": ["string", "null"],
            "description": "Optional updated owner."
          },
          "editedScope": {
            "type": ["string", "null"],
            "description": "Optional updated scope note."
          }
        }
      }
    },
    "summary": {
      "type": "object",
      "additionalProperties": false,
      "required": ["approved", "rejected", "deferred", "edited"],
      "properties": {
        "approved": { "type": "integer", "minimum": 0, "description": "Approved task count." },
        "rejected": { "type": "integer", "minimum": 0, "description": "Rejected task count." },
        "deferred": { "type": "integer", "minimum": 0, "description": "Deferred task count." },
        "edited": { "type": "integer", "minimum": 0, "description": "Edited task count." }
      }
    }
  }
}
```

### `schemas/dashboard.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://localhost/schemas/dashboard.schema.json",
  "title": "Dashboard View",
  "description": "Small derived data model written by the coordinator for a local dashboard.",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schemaVersion",
    "generatedAt",
    "currentStep",
    "repository",
    "run",
    "summaryCards",
    "findings",
    "tasks",
    "fixes",
    "verifications"
  ],
  "properties": {
    "schemaVersion": {
      "type": "string",
      "description": "Schema version."
    },
    "generatedAt": {
      "type": "string",
      "format": "date-time",
      "description": "When this dashboard file was generated."
    },
    "currentStep": {
      "type": "integer",
      "enum": [1, 2, 3, 4],
      "description": "Current workflow step."
    },
    "repository": {
      "type": "object",
      "additionalProperties": false,
      "required": ["name", "path"],
      "properties": {
        "name": { "type": "string", "description": "Repository name." },
        "path": { "type": "string", "description": "Repository path." }
      }
    },
    "run": {
      "type": "object",
      "additionalProperties": false,
      "required": ["runId", "status"],
      "properties": {
        "runId": { "type": "string", "description": "Run id." },
        "status": { "type": "string", "description": "Workflow status." }
      }
    },
    "summaryCards": {
      "type": "object",
      "additionalProperties": false,
      "required": ["healthScore", "openFindings", "tasks", "approvedTasks", "completedFixes"],
      "properties": {
        "healthScore": { "type": "integer", "minimum": 0, "maximum": 100, "description": "Overall health score." },
        "openFindings": { "type": "integer", "minimum": 0, "description": "Open finding count." },
        "tasks": { "type": "integer", "minimum": 0, "description": "Task count." },
        "approvedTasks": { "type": "integer", "minimum": 0, "description": "Approved task count." },
        "completedFixes": { "type": "integer", "minimum": 0, "description": "Completed fix count." }
      }
    },
    "findings": {
      "type": "array",
      "description": "Flat finding rows for display.",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["id", "domain", "title", "severity", "priority", "status"],
        "properties": {
          "id": { "type": "string" },
          "domain": { "type": "string" },
          "title": { "type": "string" },
          "severity": { "type": "string" },
          "priority": { "type": "string" },
          "status": { "type": "string" }
        }
      }
    },
    "tasks": {
      "type": "array",
      "description": "Flat task rows for display.",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "id",
          "domain",
          "title",
          "priority",
          "approvalState",
          "executionState",
          "verificationState",
          "owner"
        ],
        "properties": {
          "id": { "type": "string" },
          "domain": { "type": "string" },
          "title": { "type": "string" },
          "priority": { "type": "string" },
          "approvalState": { "type": "string" },
          "executionState": { "type": "string" },
          "verificationState": { "type": "string" },
          "owner": { "type": "string" }
        }
      }
    },
    "fixes": {
      "type": "array",
      "description": "Flat fix rows for display.",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["id", "taskId", "status", "fixAgent"],
        "properties": {
          "id": { "type": "string" },
          "taskId": { "type": "string" },
          "status": { "type": "string" },
          "fixAgent": { "type": "string" }
        }
      }
    },
    "verifications": {
      "type": "array",
      "description": "Flat verification rows for display.",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["id", "taskId", "status", "verifyAgent"],
        "properties": {
          "id": { "type": "string" },
          "taskId": { "type": "string" },
          "status": { "type": "string" },
          "verifyAgent": { "type": "string" }
        }
      }
    }
  }
}
```

### `schemas/subagent-audit-output.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://localhost/schemas/subagent-audit-output.schema.json",
  "title": "Subagent Audit Output",
  "description": "Output contract for one audit subagent.",
  "type": "object",
  "additionalProperties": false,
  "required": ["domain", "agentName", "score", "findings"],
  "properties": {
    "domain": {
      "type": "string",
      "description": "Audited domain."
    },
    "agentName": {
      "type": "string",
      "description": "Audit agent name."
    },
    "score": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100,
      "description": "Domain health score."
    },
    "findings": {
      "type": "array",
      "description": "Findings produced by this audit agent.",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "title",
          "description",
          "severity",
          "priority",
          "evidence",
          "affectedFiles",
          "suggestedFix",
          "autoFixable"
        ],
        "properties": {
          "title": { "type": "string", "description": "Short finding title." },
          "description": { "type": "string", "description": "Finding explanation." },
          "severity": {
            "type": "string",
            "enum": ["critical", "high", "medium", "low", "info"],
            "description": "Finding severity."
          },
          "priority": {
            "type": "string",
            "enum": ["P0", "P1", "P2", "P3"],
            "description": "Repair urgency."
          },
          "evidence": {
            "type": "array",
            "minItems": 1,
            "items": {
              "type": "object",
              "additionalProperties": false,
              "required": ["type", "path", "snippet"],
              "properties": {
                "type": {
                  "type": "string",
                  "enum": ["file", "command", "test", "config", "log"]
                },
                "path": { "type": "string" },
                "line": { "type": ["integer", "null"] },
                "snippet": { "type": "string" }
              }
            }
          },
          "affectedFiles": {
            "type": "array",
            "minItems": 1,
            "items": { "type": "string" }
          },
          "suggestedFix": { "type": "string" },
          "autoFixable": { "type": "boolean" }
        }
      }
    }
  }
}
```

### `schemas/subagent-fix-output.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://localhost/schemas/subagent-fix-output.schema.json",
  "title": "Subagent Fix Output",
  "description": "Output contract for one fix subagent.",
  "type": "object",
  "additionalProperties": false,
  "required": ["domain", "agentName", "fixes"],
  "properties": {
    "domain": {
      "type": "string",
      "description": "Domain being repaired."
    },
    "agentName": {
      "type": "string",
      "description": "Fix agent name."
    },
    "fixes": {
      "type": "array",
      "description": "Fix results produced by this fix agent.",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["taskId", "findingId", "status", "changedFiles", "testsRun", "patchSummary"],
        "properties": {
          "taskId": { "type": "string", "description": "Target task id." },
          "findingId": { "type": ["string", "null"], "description": "Target finding id." },
          "status": {
            "type": "string",
            "enum": ["applied", "partial", "failed", "skipped"],
            "description": "Fix result."
          },
          "changedFiles": {
            "type": "array",
            "items": { "type": "string" },
            "description": "Files changed by the fix."
          },
          "testsRun": {
            "type": "array",
            "items": { "type": "string" },
            "description": "Checks run after the fix."
          },
          "patchSummary": {
            "type": "string",
            "description": "Plain-English change summary."
          }
        }
      }
    }
  }
}
```

### `schemas/subagent-verify-output.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://localhost/schemas/subagent-verify-output.schema.json",
  "title": "Subagent Verify Output",
  "description": "Output contract for one verification subagent.",
  "type": "object",
  "additionalProperties": false,
  "required": ["domain", "agentName", "verifications"],
  "properties": {
    "domain": {
      "type": "string",
      "description": "Domain being verified."
    },
    "agentName": {
      "type": "string",
      "description": "Verification agent name."
    },
    "verifications": {
      "type": "array",
      "description": "Verification results produced by this verify agent.",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["fixId", "taskId", "status", "notes"],
        "properties": {
          "fixId": { "type": "string", "description": "Related fix id." },
          "taskId": { "type": "string", "description": "Related task id." },
          "status": {
            "type": "string",
            "enum": ["passed", "failed", "partial", "unverifiable"],
            "description": "Verification result."
          },
          "notes": { "type": "string", "description": "Verification notes." },
          "regressions": {
            "type": "array",
            "items": { "type": "string" },
            "description": "New issues introduced by the fix."
          }
        }
      }
    }
  }
}
```

## CRUD and workflow rules

Use these routes for the coordinator API, because normal REST-style Create Read Update Delete maps cleanly to `POST`, `GET`, `PATCH`, and `DELETE`. [openapi](https://openapi.com/blog/http-methods-restful-apis)

- `POST /tasks`
- `GET /tasks`
- `GET /tasks/{taskId}`
- `PATCH /tasks/{taskId}`
- `DELETE /tasks/{taskId}`
- `GET /tasks/{taskId}/history`
- `GET /approval`
- `POST /approval/submit`
- `POST /tasks/{taskId}/approve`
- `POST /tasks/{taskId}/reject`
- `POST /tasks/{taskId}/defer`

Use these hard coordinator rules:
- Step 1 creates findings and tasks.
- Step 2 pauses and waits for approval.
- Step 3 can only run approved tasks.
- Step 4 can only verify tasks that produced fix results.
- Hard delete only when `executionState = not_started`.
- After execution starts, convert delete into `cancelled`.
- Every mutation writes a task history event.
- The coordinator never trusts raw subagent output until schema validation passes.

## First build target

Your first thin vertical slice should be: fake audit output in, task creation works, CRUD works, approval works, fake fix output updates task state, and the coordinator writes one clean `dashboard-data.json`. That is enough to start your first real audit agent and first real fix agent without rebuilding the coordinator later.

Build in this exact order:
1. Prompt 1.
2. Prompt 2.
3. Prompt 3.
4. Prompt 4.
5. Prompt 5.
6. Prompt 6.
7. Prompt 7.
8. Prompt 8.
9. Prompt 9.

The blunt truth: if you try to build the first audit agent before the coordinator can validate inputs, own tasks, and pause for approval, you will create a messy prototype that you will rewrite almost immediately.
