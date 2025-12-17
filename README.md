# BOOTCAMP Manager — refined spec

## Data model (core fields)

Describe each record as plain-text key/value pairs or small YAML/JSON documents.

Project (one record)

* `id` — short slug (string)
* `title` — human title (string)
* `tech` — comma list (e.g., `bash,fzf,busybox`)
* `status` — one of: `current, active, deferred, blocked, legacy`
* `stage` — current stage index or id
* `created_at` — ISO timestamp
* `updated_at` — ISO timestamp
* `meta` — freeform map (owner, repo, notes)

Stage (ordered block inside a project)

* `id` — slug or integer
* `title` — short title
* `goals` — array of concise objectives
* `acceptance` — array of pass/failable checks
* `weeks` — estimated weeks or effort metric

Exercise (daily drill)

* `id`
* `title`
* `tasks` — ordered todo list (shell-friendly)
* `stage_id` — link to parent stage
* `duration_min` — expected minutes
* `prereqs` — list of other exercise ids
* `tags` — keywords

System state (single machine-level file)

* `current_project`
* `stage`
* `week`
* `completed` — CSV of exercise ids
* `last_run` — ISO timestamp

Storage formats: prefer small YAML for readability; keep plain-text fallback for embedded targets.

---

## CLI commands (mapped to your utils)

All commands are POSIX-friendly and return meaningful exit codes (0 success, 1 user error, 2 system error).

* `bootmgr new project <id> --title <T> --tech <t1,t2>`
  Create a new project skeleton.

* `bootmgr new exercise <project> <id> --title <T> --duration 20`
  Create an exercise under a project.

* `bootmgr list projects`
  Tabular, sortable output; `--json` for machine use.

* `bootmgr list exercises <project> [--stage id] [--tag X]`
  Filtered lists.

* `bootmgr inspect project|exercise <id> [--format yaml|json]`
  Show full record.

* `bootmgr edit project|exercise <id>`
  Preferred editor from `$EDITOR`. Support `--inline` to apply quick field changes.

* `bootmgr status [<project>|<exercise>]`
  Show machine state and progress percentages.

* `bootmgr run [--today|--exercise id|--project id]`
  Launch daily UI. If TTY: interactive fzf selector; otherwise non-interactive picks the next due exercise. Writes run log.

* `bootmgr next` / `bootmgr prev`
  Advance or rollback week/stage with confirmation.

* `bootmgr export <project> > file.yaml` / `bootmgr import file.yaml`
  Transportable backups.

* `bootmgr scaffold-tool <name>`
  Create a tool template: script + bats test + shellcheck header.

* `bootmgr dashboard [--week N]`
  Generate a short report: progress, stuck items, upcoming drills.

* `bootmgr completion bash|zsh`
  Emit shell completion snippet.

Flags common to many commands:

* `--ci` produce deterministic machine-friendly output
* `--dry-run` simulate changes
* `--yes` non-interactive confirmation
* `--verbose` increase log detail

---

## UI & UX behavior

Interactive:

* Use fzf for selections. Always show a preview pane (`--preview 'bootmgr inspect {} --format yaml'`).
* Keybindings: `ctrl-a` select all, `ctrl-d` deselect, `ctrl-e` open editor on selected.
* Multi-select allowed for batch operations (mark complete, export).

Non-interactive:

* Deterministic exit codes and JSON output suitable for CI.

Logging:

* Per-run logs written to `~/.bootmgr/logs/YYYYMMDD_HHMM_<exercise>.log`.
* Global audit `~/.bootmgr/activity.log`.
* Log rotation: keep last N (configurable), gzip older logs.

Notifications (optional):

* Hooks directory `~/.bootmgr/hooks/` with `on-run`, `on-complete` scripts executed with env vars.

---

## File layout (recommended)

```
~/.bootmgr/
  state                # machine state (plain key=val)
  projects/            # yaml per project: <id>.yaml
  exercises/           # yaml per exercise: <project>-<id>.yaml
  tools.d/             # discoverable tool scripts
  logs/
  activity.log
  tests/               # bats tests for bootmgr core
```

---

## Acceptance checks (quick list)

* `bootmgr new project p1` creates `projects/p1.yaml` and exits 0.
* `bootmgr list projects --json` emits valid JSON array.
* `bootmgr run` on a TTY opens fzf and writes a run log for the chosen exercise.
* `bootmgr next` increments week, persists to `state`.
* `BOOTMGR_PORTABLE=1 ./bootmgr` avoids GNU-only utilities and exits 0 on BusyBox.

---

## Minimal data examples

Project YAML:

```yaml
id: core-bash
title: "Core Bash Mastery"
tech: [bash,fzf,busybox]
status: active
stage: 1
created_at: 2025-12-17T10:00:00Z
```

Exercise YAML:

```yaml
id: safe-run
project: core-bash
title: "Implement safe-run utility"
tasks:
  - design interface: safe-run --timeout --retries
  - implement logging
  - add shellcheck header
  - write bats test
duration_min: 45
stage_id: 1
```

State file (plain text):

```
current_project=core-bash
stage=1
week=2
completed=safe-run,fs-watch
last_run=2025-12-16T09:12:00Z
```

---

## Testing & CI

* Unit: bats for each command and behavior (create, list, run dry-run).
* Lint: shellcheck; fail CI on any critical warnings.
* Portability: test under BusyBox and a modern GNU distro in CI matrix.
* Determinism: `--ci` runs must be byte-identical across runs where input is identical.

---

## Security & Ops

* Never run as root; refuse dangerous ops without explicit `--yes --allow-root`.
* Sanitize `$EDITOR` and command inputs when used as preview commands.
* Ensure atomic writes (use `mktemp` fallback) for state and project files.
* Minimal external dependencies: coreutils, bash≥4 preferred, fzf optional but strongly recommended.

---

## Implementation milestones (short)

1. Core state & `new/list/inspect` (basic CRUD).
2. `run` with non-interactive selection + logging.
3. Interactive fzf UI + previews.
4. `next/prev`, export/import, and scaffold.
5. Tests, portability mode, completions.
6. Hooks, dashboard, optional remote/run-on-host.

