## Purpose

Single JSON document representing one bootcamp project: metadata, phases, drills, and progress. Designed for Python-first implementation, fzf-friendly CLI, and future validation.

---

## Design Principles

* Human-readable, machine-validated.
* Stable IDs (never change once created).
* Order matters for phases and drills.
* Explicit status enums.
* Extensible without breaking old versions.

---

## Top-Level Structure

```json
{
  "schema_version": "1.0",
  "project": { /* metadata */ },
  "phases": [ /* ordered */ ],
  "drills": [ /* flat list, linked to phases */ ],
  "state": { /* runtime / progress */ }
}
```

---

## project (metadata)

```json
{
  "id": "core-bash",
  "title": "Core Bash Mastery",
  "technology": ["bash", "fzf", "busybox"],
  "status": "active",
  "description": "Expert-level bash for embedded and networking",
  "created_at": "2025-12-17T10:00:00Z",
  "updated_at": "2025-12-17T10:00:00Z",
  "owner": "local",
  "tags": ["embedded", "networking", "qa"],
  "repository": null
}
```

### status (enum)

* `current`
* `active`
* `deferred`
* `blocked`
* `legacy`

---

## phases (ordered list)

Each phase represents a learning milestone.

```json
{
  "id": "phase-1",
  "index": 1,
  "title": "Bash Core Mastery",
  "objectives": [
    "Understand expansion and quoting",
    "Write safe, testable bash functions"
  ],
  "acceptance_criteria": [
    "All scripts pass shellcheck",
    "Bats tests cover failure paths"
  ],
  "estimated_weeks": 2,
  "status": "active"
}
```

### phase status (enum)

* `pending`
* `active`
* `completed`
* `blocked`

---

## drills (flat list)

Drills are atomic daily exercises. Linked to phases by `phase_id`.

```json
{
  "id": "safe-run",
  "title": "Implement safe-run utility",
  "phase_id": "phase-1",
  "todos": [
    "Design CLI interface",
    "Implement timeout and retries",
    "Add logging",
    "Write bats tests"
  ],
  "difficulty": 3,
  "estimated_minutes": 45,
  "status": "pending",
  "prerequisites": [],
  "artifacts": [
    "bin/safe-run",
    "tests/test_safe-run.bats"
  ],
  "tags": ["bash", "error-handling"]
}
```

### drill status (enum)

* `pending`
* `active`
* `completed`
* `skipped`
* `blocked`

---

## state (runtime / progress)

This section mutates during execution. Everything else is declarative.

```json
{
  "current_phase_id": "phase-1",
  "current_drill_id": "safe-run",
  "week": 1,
  "completed_drills": ["init-env"],
  "last_run": "2025-12-17T09:12:00Z",
  "history": [
    {
      "drill_id": "init-env",
      "timestamp": "2025-12-16T08:55:00Z",
      "result": "success"
    }
  ]
}
```

---

## Full Minimal Example

```json
{
  "schema_version": "1.0",
  "project": {
    "id": "core-bash",
    "title": "Core Bash Mastery",
    "technology": ["bash", "fzf"],
    "status": "active",
    "created_at": "2025-12-17T10:00:00Z",
    "updated_at": "2025-12-17T10:00:00Z"
  },
  "phases": [
    {
      "id": "phase-1",
      "index": 1,
      "title": "Bash Core",
      "objectives": ["Safe scripting"],
      "acceptance_criteria": ["Shellcheck clean"],
      "estimated_weeks": 2,
      "status": "active"
    }
  ],
  "drills": [
    {
      "id": "safe-run",
      "title": "safe-run tool",
      "phase_id": "phase-1",
      "todos": ["Implement", "Test"],
      "estimated_minutes": 45,
      "status": "pending"
    }
  ],
  "state": {
    "current_phase_id": "phase-1",
    "week": 1,
    "completed_drills": []
  }
}
```

---

## Validation Rules (to enforce in Python)

* `project.id` unique per file name.
* Phase `id` referenced by drills must exist.
* Only one phase can be `active`.
* Only one drill can be `active` at a time.
* State must not reference non-existing IDs.

---

## Planned Extensions (do not implement yet)

* Metrics (time spent, retries).
* Multi-user support.
* External tool linkage.
* Remote execution metadata.

---

## Next Steps

1. Freeze this schema.
2. Write Python dataclasses / pydantic models.
3. Implement load → validate → save cycle.
4. Add JSON Schema validator.
5. Build CLI CRUD around this structure.