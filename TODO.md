# **BOOTCAMP MANAGER: DEVELOPMENT ROADMAP**

## **PHASE 1: INFRASTRUCTURE & CORE SYSTEMS**

### **SPRINT 1: FOUNDATION SETUP**

**Objective:** Establish secure, portable foundation with zero external dependencies.

#### **Dependencies for This Sprint:**
- **Python 3.8+** (stdlib only) - Core runtime
- **pathlib** (stdlib) - Cross-platform path handling
- **json** (stdlib) - State serialization
- **os/sys** (stdlib) - Environment and system operations

#### **Tasks:**

- [ ] **FIX CONFIGURATION MODULE BUGS** - CRITICAL
   - **Description:** Current config.py has syntax errors (`p.exists != True`). Must handle all edge cases: missing directories, permissions, portable mode.
   - **Acceptance Criteria:**
     - `from src.config import get_config` doesn't crash
     - Returns valid Path objects for all required directories
     - Creates `projects/` and `logs/` directories with 755 permissions
     - Portable mode (`BOOTMGR_PORTABLE=1`) disables non-portable features
     - Clear error messages for all failure modes

- [ ] **IMPLEMENT FILE-BASED LOCKING**
   - **Description:** Prevent concurrent modifications using atomic file operations. Use `fcntl` on Unix, `msvcrt` on Windows, fallback to PID files.
   - **Acceptance Criteria:**
     - Two processes can't modify same project simultaneously
     - Lock timeout after 30 seconds (prevents deadlocks)
     - Lock files cleaned up on process exit (atexit)
     - Works on all target platforms (Linux, macOS, Windows)

- [ ] **CREATE LOGGING INFRASTRUCTURE**
   - **Description:** Structured logging with rotation. Separate audit trail from debug logs. No external logging libraries.
   - **Acceptance Criteria:**
     - Logs to `logs/activity.log` (human-readable) and `logs/debug.json` (machine-readable)
     - Automatic rotation: keep 30 days, compress older logs with gzip
     - Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
     - Each entry includes: timestamp, level, module, function, message

- [ ] **ENVIRONMENT VALIDATION**
   - **Description:** Check system requirements at startup. Validate $EDITOR, PATH, disk space, permissions.
   - **Acceptance Criteria:**
     - Reports missing requirements before any operation
     - Suggests fixes for common issues
     - `--check` flag validates environment without running
     - Returns exit code 78 (EX_CONFIG) for configuration errors

**SPRINT 1 SUCCESS METRICS:**
- Zero runtime crashes in configuration phase
- 100% test coverage for config module
- Works in Docker container with minimal base image (alpine:latest)

---

### **SPRINT 2: DATA MODEL IMPLEMENTATION**

**Objective:** Create type-safe, validated data structures with comprehensive business logic.

#### **Dependencies for This Sprint:**
- **Pydantic 2.0+** - Data validation and serialization
- **email-validator** - Optional for email validation in models
- **python-dateutil** - Enhanced date parsing (optional, fallback to datetime)

#### **Tasks:**

- [ ] **COMPLETE CORE MODELS**
   - **Description:** Implement Project, Phase, Drill, State, HistoryEntry with full validation. Use Python enums for status fields.
   - **Acceptance Criteria:**
     - All models inherit from `BaseModel` with automatic timestamps
     - Field validators reject invalid data with clear error messages
     - Enums restrict values to defined sets (current/active/deferred/etc.)
     - `model_dump_json()` produces valid JSON Schema

- [ ] **IMPLEMENT CROSS-REFERENCE INTEGRITY**
   - **Description:** Validate relationships between entities. Drill.phase_id must exist, State references must be valid.
   - **Acceptance Criteria:**
     - Loading project with broken references raises `ValidationError`
     - Only one Phase can be "active" at a time
     - Only one Drill can be "active" at a time
     - Circular dependencies in prerequisites are detected

- [ ] **ADD BUSINESS LOGIC METHODS**
   - **Description:** Progress calculation, dependency resolution, state transitions. Pure functions where possible.
   - **Acceptance Criteria:**
     - `calculate_progress()` returns accurate percentages (overall and per-phase)
     - `get_next_drill()` respects prerequisites and completion status
     - `can_advance_phase()` checks all acceptance criteria
     - All business logic has idempotent operations

- [ ] **CREATE MODEL FACTORIES FOR TESTING**
   - **Description:** Build factory functions to generate test data. Support random and deterministic modes.
   - **Acceptance Criteria:**
     - Generate valid Project with N phases and M drills
     - Create test scenarios: blocked project, completed project, circular deps
     - Factories work without database/filesystem

**SPRINT 2 SUCCESS METRICS:**
- All models pass `mypy --strict` with no errors
- 100+ validation test cases passing
- JSON Schema export for all models
- Performance: Load 1000-drill project in < 1 second

---

### **SPRINT 3: STORAGE LAYER**

**Objective:** Atomic, crash-proof file operations with migration support.

#### **Dependencies for This Sprint:**
- **PyYAML 6.0+** - YAML serialization (safe load/dump)
- **atomicwrites** - Cross-platform atomic file operations
- **filelock** - Portable file locking (alternative to custom implementation)

#### **Tasks:**

- [ ] **IMPLEMENT ATOMIC FILE OPERATIONS**
   - **Description:** Write to temp file, then rename. Handle power failures, disk full, permission changes.
   - **Acceptance Criteria:**
     - Kill -9 during save leaves original file intact
     - Disk full during write → clean rollback, no partial files
     - File permissions preserved (600 for sensitive files)
     - Backup created before overwrite (with timestamp)

- [ ] **CREATE YAML SERIALIZATION WITH COMMENTS**
   - **Description:** Human-readable YAML with preserved comments. Custom formatting for readability.
   - **Acceptance Criteria:**
     - Round-trip serialization preserves all data
     - Comments in template YAML are preserved
     - Output is consistently formatted (2-space indent, lists with dashes)
     - Large files (>10MB) serialize in < 5 seconds

- [ ] **BUILD STATE PERSISTENCE SYSTEM**
   - **Description:** Global and project-specific state. Conflict detection and resolution.
   - **Acceptance Criteria:**
     - State changes are transactional (all or nothing)
     - Merge conflicts detected with three-way diff
     - Manual resolution process with clear instructions
     - State survives reboot and survives corrupt file recovery

- [ ] **IMPLEMENT SCHEMA MIGRATION**
   - **Description:** Version detection and automatic upgrades. Backward compatibility for reading.
   - **Acceptance Criteria:**
     - v0.9 → v1.0 migration preserves all data
     - Migration log tracks changes for rollback
     - Cannot migrate already-migrated files (idempotent)
     - Failed migration restores backup automatically

**SPRINT 3 SUCCESS METRICS:**
- No data loss in 10,000 random crash simulations
- All file operations leave consistent state
- Migration works for at least 3 major version jumps
- Performance: 1000 writes/second for small files

---

### **SPRINT 4: COMMAND-LINE INTERFACE**

**Objective:** POSIX-compliant CLI with comprehensive help and error handling.

#### **Dependencies for This Sprint:**
- **Click 8.0+** - CLI framework with shell completion
- **rich** - Terminal formatting and tables (optional for pretty output)
- **argcomplete** - Bash completion generation

#### **Tasks:**

- [ ] **IMPLEMENT CLI FRAMEWORK WITH CLICK**
   - **Description:** Command hierarchy, help system, exit codes. Follow POSIX/GNU conventions.
   - **Acceptance Criteria:**
     - `bootmgr --help` shows all commands with descriptions
     - Exit codes: 0=success, 1=user error, 2=system error, 78=config error
     - Subcommands: `project`, `drill`, `phase`, `state`, `run`
     - Consistent argument parsing: `--flag value` and `--flag=value`

- [ ] **CREATE PROJECT CRUD OPERATIONS**
   - **Description:** Create, read, update, delete projects. Tabular and JSON output formats.
   - **Acceptance Criteria:**
     - `new project` creates valid YAML with all required fields
     - `list projects` shows table with sortable columns
     - `list projects --json` produces valid JSON array
     - `inspect project` shows YAML/JSON/markdown format
     - `edit project` opens $EDITOR, validates before saving

- [ ] **BUILD PHASE & DRILL MANAGEMENT**
   - **Description:** Add/remove phases and drills. Bulk operations via CSV/JSON import.
   - **Acceptance Criteria:**
     - `add drill` validates prerequisites exist
     - `remove phase` cascades to drills (with confirmation)
     - `import csv` creates drills from spreadsheet
     - `export markdown` generates progress report

- [ ] **IMPLEMENT SHELL COMPLETION**
   - **Description:** Bash and Zsh completion for commands and project IDs.
   - **Acceptance Criteria:**
     - `bootmgr completion bash` generates completion script
     - Tab completion suggests project IDs from filesystem
     - Dynamic completion for drill IDs within project
     - Installation instructions in --help

**SPRINT 4 SUCCESS METRICS:**
- All commands have man-style documentation
- 100% POSIX-compatible argument parsing
- Completion works in bash 4.4+ and zsh 5.8+
- Error messages are actionable and consistent

---

### **SPRINT 5: EXECUTION ENGINE**

**Objective:** Daily workflow execution with logging and progress tracking.

#### **Dependencies for This Sprint:**
- **watchdog** - File change detection (for auto-reload)
- **psutil** - Process monitoring and resource limits
- **humanize** - Human-readable durations and sizes

#### **Tasks:**

- [ ] **CREATE NON-INTERACTIVE RUNNER**
   - **Description:** Execute next due drill based on state. Time tracking, resource limits.
   - **Acceptance Criteria:**
     - `bootmgr run --today` executes exactly one drill
     - Timeout after 2x estimated duration
     - Resource limits: CPU time, memory, disk writes
     - Run log includes start, end, exit code, resource usage

- [ ] **IMPLEMENT PROGRESSION WORKFLOW**
   - **Description:** Move through phases and weeks. Validation at each transition.
   - **Acceptance Criteria:**
     - `next` only advances if current phase acceptance criteria met
     - `prev` rolls back with confirmation and creates restore point
     - `status` shows progress bar and upcoming drills
     - Automatic phase completion when all drills done

- [ ] **BUILD DEPENDENCY RESOLVER**
   - **Description:** Topological sort for prerequisites. Parallel execution where possible.
   - **Acceptance Criteria:**
     - Circular dependency detection with clear error
     - Visual dependency graph with `--graph` flag
     - Parallel execution of independent drills (with --parallel N)
     - Prerequisite chain shows estimated total time

- [ ] **CREATE EXECUTION HOOKS SYSTEM**
   - **Description:** Pre/post execution hooks. Custom scripts for notifications, logging.
   - **Acceptance Criteria:**
     - Hooks directory: `~/.bootmgr/hooks/`
     - Environment variables: `BOOTMGR_DRILL_ID`, `BOOTMGR_PROJECT_ID`
     - Hook chain: pre-run → run → post-run → on-complete
     - Hook failures don't stop execution (configurable)

**SPRINT 5 SUCCESS METRICS:**
- Daily workflow takes < 5 seconds to determine next action
- Resource usage tracking accurate within 10%
- Dependency resolver handles 1000+ drill graphs
- Hooks can be written in any language (shebang support)

---

### **SPRINT 6: TESTING & QUALITY**

**Objective:** Comprehensive test suite with CI/CD pipeline.

#### **Dependencies for This Sprint:**
- **pytest** - Test framework
- **pytest-cov** - Coverage reporting
- **pytest-mock** - Mocking
- **hypothesis** - Property-based testing
- **tox** - Multi-environment testing
- **pre-commit** - Git hooks

#### **Tasks:**

- [ ] **CREATE UNIT TEST SUITE**
   - **Description:** Test all models, validation, business logic. Mock external dependencies.
   - **Acceptance Criteria:**
     - 100% test coverage for core modules (models, storage)
     - Tests run in < 30 seconds
     - No I/O in unit tests (all mocked)
     - Property-based tests for serialization round-trip

- [ ] **IMPLEMENT INTEGRATION TESTS**
   - **Description:** Test CLI commands end-to-end. Filesystem operations, error conditions.
   - **Acceptance Criteria:**
     - Each CLI command has at least 3 integration tests
     - Tests run in isolated temporary directories
     - Clean up all test artifacts
     - Test all error conditions and edge cases

- [ ] **SETUP CI/CD PIPELINE**
   - **Description:** GitHub Actions for testing, linting, building. Multiple OS/Python versions.
   - **Acceptance Criteria:**
     - CI runs on: Ubuntu LTS, macOS latest, Windows Server
     - Python versions: 3.8, 3.9, 3.10, 3.11, 3.12
     - Steps: lint, test, build, integration test, release
     - Badges in README: tests, coverage, version

- [ ] **CREATE PERFORMANCE BENCHMARKS**
   - **Description:** Measure and track performance regressions. Large dataset handling.
   - **Acceptance Criteria:**
     - Benchmarks for: load time, save time, search, progress calc
     - Performance tracked over time (graphs)
     - Alert on >10% regression
     - Profile complex operations (dependency resolution)

**SPRINT 6 SUCCESS METRICS:**
- 95%+ overall test coverage
- CI passes on all platforms
- Zero flaky tests
- Performance benchmarks stable

---

### **SPRINT 7: PORTABILITY & DISTRIBUTION**

**Objective:** Run anywhere from embedded systems to enterprise servers.

#### **Dependencies for This Sprint:**
- **pyinstaller** - Binary packaging
- **docker** - Containerization (runtime dependency)
- **setuptools** - Python packaging
- **twine** - PyPI upload

#### **Tasks:**

- [ ] **IMPLEMENT PORTABLE MODE**
   - **Description:** No GNU dependencies, minimal libc. BusyBox compatibility.
   - **Acceptance Criteria:**
     - `BOOTMGR_PORTABLE=1` disables all non-portable features
     - No shell commands except builtins (test, [, read, echo)
     - Works on Alpine Linux (musl libc)
     - Binary size < 10MB compressed

- [ ] **CREATE DOCKER DISTRIBUTION**
   - **Description:** Multi-architecture Docker images. Small footprint.
   - **Acceptance Criteria:**
     - Images for: linux/amd64, linux/arm64, linux/arm/v7
     - Base image: alpine:latest (< 5MB)
     - Image size < 50MB
     - Health check endpoint

- [ ] **BUILD PACKAGE DISTRIBUTION**
   - **Description:** PyPI package, Homebrew formula, Windows installer.
   - **Acceptance Criteria:**
     - `pip install bootcamp-manager` works
     - Homebrew formula passes audit
     - Windows MSI installer with GUI config
     - Digital signatures for all binaries

- [ ] **IMPLEMENT CONFIGURATION MANAGEMENT**
   - **Description:** Hierarchical config: defaults → system → user → env → CLI.
   - **Acceptance Criteria:**
     - Config files: `/etc/bootmgr.conf`, `~/.config/bootmgr.conf`
     - Environment variables: `BOOTMGR_*` override files
     - `bootmgr config show` displays effective configuration
     - Config validation with suggested fixes

**SPRINT 7 SUCCESS METRICS:**
- Runs on Raspberry Pi Zero (armv6)
- Docker image builds in < 2 minutes
- Installation takes < 30 seconds on all platforms
- Config system handles 100% of use cases

---

### **SPRINT 8: POLISH & DOCUMENTATION**

**Objective:** Production-ready system with comprehensive documentation.

#### **Dependencies for This Sprint:**
- **mkdocs** - Documentation site generation
- **mike** - Multiple version documentation
- **readthedocs** - Documentation hosting
- **sphinx** - API documentation

#### **Tasks:**

- [ ] **CREATE USER DOCUMENTATION**
   - **Description:** Tutorials, how-tos, reference. Video tutorials for complex workflows.
   - **Acceptance Criteria:**
     - Getting started guide (5 minutes to first drill)
     - Video tutorials: installation, daily workflow, project creation
     - Troubleshooting guide with common issues
     - API documentation for hooks and extensions

- [ ] **IMPLEMENT ACCESSIBILITY FEATURES**
   - **Description:** Screen reader support, high contrast, keyboard navigation.
   - **Acceptance Criteria:**
     - All output works with screen readers
     - Color-blind friendly status indicators
     - Full keyboard navigation (no mouse required)
     - Configurable font sizes and colors

- [ ] **ADD METRICS & ANALYTICS (OPT-IN)**
   - **Description:** Anonymous usage statistics. Feature usage, performance metrics.
   - **Acceptance Criteria:**
     - Opt-in only (disabled by default)
     - No personal data collected
     - Metrics: command frequency, error rates, performance
     - Local dashboard: `bootmgr metrics`

- [ ] **CREATE MIGRATION FROM OTHER SYSTEMS**
   - **Description:** Import from Trello, Asana, JIRA, spreadsheets.
   - **Acceptance Criteria:**
     - CSV import with column mapping
     - Trello export → bootcamp project
     - JIRA filter → bootcamp project
     - Validation report after import

**SPRINT 8 SUCCESS METRICS:**
- Documentation covers 100% of features
- Zero accessibility violations (WCAG 2.1 AA)
- Migration tools handle real-world data
- User satisfaction > 4.5/5 in beta testing

---

## **DEPENDENCY SUMMARY**

### **Core Runtime (Required):**
- **Python 3.8+** - Language runtime
- **Pydantic 2.0+** - Data validation
- **Click 8.0+** - CLI framework
- **PyYAML 6.0+** - YAML serialization

### **Optional Enhancements:**
- **rich** - Pretty terminal output (fallback to plain text)
- **watchdog** - File change detection
- **psutil** - Resource monitoring
- **docker** - Container runtime (for distribution)

### **Development Only:**
- **pytest + plugins** - Testing framework
- **mypy** - Type checking
- **black/isort** - Code formatting
- **pre-commit** - Git hooks

### **Build/Distribution:**
- **pyinstaller** - Binary creation
- **setuptools** - Python packaging
- **twine** - PyPI upload
- **docker** - Container builds

---

## **SUCCESS CRITERIA (PROJECT COMPLETE)**

1. **RELIABILITY:** 99.9% uptime in production use (no crashes in normal operation)
2. **PERFORMANCE:** < 100ms for common operations, < 5s for complex operations
3. **PORTABILITY:** Runs on Linux (glibc/musl), macOS, Windows, Raspberry Pi
4. **USABILITY:** New user productive in < 10 minutes
5. **MAINTAINABILITY:** 95% test coverage, all dependencies pinned, documented architecture
6. **SECURITY:** No critical vulnerabilities, principle of least privilege, secure defaults
7. **DOCUMENTATION:** All features documented, 90%+ documentation coverage
8. **COMMUNITY:** Open source, contribution guidelines, issue templates, code of conduct