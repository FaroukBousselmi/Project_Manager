# 🚀 **PROJECTMGR: THE ULTIMATE EMBEDDED PROJECT MASTER**

**You are absolutely right.** The core hierarchy of **Project → Phases → Drills** is the engine. The embedded and professional features are what make it specifically valuable for your daily work. Here's the unified, exhaustive roadmap that combines everything into a single tactical plan.

---

## **PHASE 1: THE CORE ENGINE (Data & Logic)**

**Objective:** Build the hierarchical "Brain" of the project with hardware awareness.

### **SPRINT 1: INFRASTRUCTURE** ✅
*   [x] **Config Module:** Path management & portable mode.
*   [x] **Directory Setup:** Auto-creation of `projects/` and `logs/`.

### **SPRINT 2: HIERARCHICAL MODELS** 🔄
*   [x] **Project Bundle:** The "Root" container (`BootcampProject`).
*   [x] **Phase Model:** Groups of drills (e.g., "Phase 1: Driver Development").
*   [x] **Drill Model:** Individual tasks with objectives.
*   [ ] **Hardware Profile Model (`src/models/hardware.py`):**
    *   **Task:** Create `HardwareProfile` class with fields: `id`, `name`, `mcu`, `arch`, `serial_port`, `debugger_type`.
    *   **Acceptance:** Validates serial port patterns (`/dev/tty*`, `COM*`). Has `detect_connected()` method.
    *   **Test:** Unit test for port validation and a mock detection test.
*   [ ] **Toolchain Model (`src/models/toolchain.py`):**
    *   **Task:** Create `ToolchainRequirement` class: `name`, `min_version`, `env_var`.
    *   **Acceptance:** Has `check_installed()` method that uses `subprocess` to verify version in PATH.
    *   **Test:** Test version parsing and check logic with mocked subprocess output.
*   [ ] **Model Integration & Validation:**
    *   **Task:** Update `Project` model to include `hardware: List[HardwareProfile]` and `toolchains: Dict[str, ToolchainRequirement]`.
    *   **Task:** Update `Drill` model with `build_command`, `flash_command`, `wiring_diagram_path`, `required_hardware_ids`.
    *   **Acceptance:** `@model_validator` ensures `current_drill_id` exists and a drill's `required_hardware_ids` exist in the project.
    *   **Test:** Write integration tests that fail when hardware references are broken.

### **SPRINT 3: ATOMIC STORAGE & ARTIFACTS**
*   [ ] **Crash-Proof File Operations (`src/storage/atomic_ops.py`):**
    *   **Task:** Implement `atomic_json_write(path, data)` using `tempfile` + `os.replace`.
    *   **Task:** Integrate `fcntl.flock` for Unix file locking with a `FileLock` context manager. Create a fallback for Windows/portable mode.
    *   **Acceptance:** Survives `kill -9` mid-write. Lock prevents concurrent access. Returns path to saved file.
    *   **Test:** Simulation of concurrent writes and power-fail scenarios.
*   [ ] **Artifact & Binary Analysis (`src/analysis/elf_analyzer.py`):**
    *   **Task:** Create `BinaryAnalyzer` class using `pyelftools`. Method: `analyze(elf_path)` returns `.text`, `.data`, `.bss` sizes.
    *   **Task:** Integrate analyzer into `ProjectState` to append metrics to `history` after a drill is marked completed.
    *   **Acceptance:** Calculates Flash/RAM usage percentage if MCU memory specs are in `HardwareProfile`.
    *   **Test:** Analyze a sample `.elf` file and verify metrics are stored in state.

---

## **PHASE 2: THE INVENTORY & LAB BENCH**

**Objective:** Track physical tools and knowledge required for drills.

### **SPRINT 4: HARDWARE INVENTORY SYSTEM**
*   [ ] **Global Inventory Manager (`src/inventory/manager.py`):**
    *   **Task:** Create `InventoryManager` class with dual storage: `~/.projectmgr/inventory/personal.json` and `client_assets.json`.
    *   **Task:** Model inventory items with: `id`, `name`, `type`, `serial`, `location`, `status` (`available`, `checked_out`, `maintenance`), `project_id` (if checked out).
    *   **Acceptance:** `check_out(item_id, project_id)` atomically updates status and logs.
    *   **Test:** Test check-out/check-in workflow and conflict detection.
*   [ ] **Inventory CLI (`src/cli/commands/inventory.py`):**
    *   **Task:** Commands: `pm inventory list`, `pm inventory checkout <id>`, `pm inventory locate <query>`.
    *   **Acceptance:** Tabular output with status highlighting. Prevents checkout if already in use.
*   [ ] **Serial Port Resource Locking:**
    *   **Task:** Extend file locking to manage hardware access. `ResourceLock` acquires a lock based on `serial_port` string.
    *   **Acceptance:** Prevents two processes from accessing `/dev/ttyUSB0` simultaneously.

### **SPRINT 5: KNOWLEDGE BASE & TEMPLATING**
*   [ ] **Datasheet Indexer & Searcher (`src/knowledge/datasheet_index.py`):**
    *   **Task:** Create index of PDFs in project `references/` folder. Extract metadata (title, author) and optionally text with `pdfminer`.
    *   **Task:** CLI: `pm datasheet search "i2c timing"` and `pm datasheet open <id> --page 42`.
    *   **Acceptance:** Opens system PDF viewer to the correct page. Fuzzy search works.
*   [ ] **Embedded Project Templating:**
    *   **Task:** Create `src/templates/` with directories for `stm32-blink`, `esp32-idf`, `arm-cmake`.
    *   **Task:** CLI: `pm new --template stm32-blink` generates `Makefile`, `linker.ld`, `main.c`, `wiring.md`.
    *   **Acceptance:** Generated project builds without errors.
*   [ ] **Wiring Diagram Viewer:**
    *   **Task:** Command: `pm wiring show <drill_id>` renders ASCII diagram or informs how to open image.
    *   **Acceptance:** Clearly displays pin connections before starting a drill.

---

## **PHASE 3: THE EXECUTION ENGINE (The "Drill Sergeant")**

**Objective:** Automate the embedded compile-flash-debug-monitor loop.

### **SPRINT 6: BUILD & FLASH AUTOMATION**
*   [ ] **Build Manager (`src/execution/build_manager.py`):**
    *   **Task:** Class `BuildManager` executes `drill.build_command` (e.g., `make -j4`).
    *   **Task:** Captures `stdout/stderr` to `logs/build_<timestamp>.log`. Sets env vars (`PROJECT`, `BOARD`, `MCU`).
    *   **Acceptance:** Returns success/failure. On success, triggers `BinaryAnalyzer`.
*   [ ] **Flash Manager (`src/execution/flash_manager.py`):**
    *   **Task:** Class `FlashManager` detects flasher from `HardwareProfile.debugger_type` (openocd, st-flash, esptool).
    *   **Task:** Executes appropriate command sequence. Supports `--verify` and `--reset` flags.
    *   **Acceptance:** Can flash a binary to a connected board. Provides clear error if flash fails.
*   [ ] **Integrated Serial Monitor (`src/execution/serial_monitor.py`):**
    *   **Task:** Class `SerialMonitor` using `pyserial`. Connects to port from active `HardwareProfile`.
    *   **Task:** CLI: `pm monitor` starts live monitor. Can filter lines with regex.
    *   **Acceptance:** Displays real-time UART output. Can send simple commands.

### **SPRINT 7: DRILL WORKFLOW & ANALYTICS**
*   [ ] **Drill Lifecycle Automation:**
    *   **Task:** Command `pm drill start <id>`: Acquires hardware locks, sets drill status to `active`, starts work timer.
    *   **Task:** Command `pm drill complete`: Stops timer, runs success detection on logs, updates state, releases locks.
    *   **Acceptance:** Fully automated context switching between drills.
*   [ ] **Success/Failure Detection:**
    *   **Task:** Log parser scans serial/build logs for regex patterns defined in drill (e.g., `"ALL TESTS PASSED"`, `"HARDFAULT"`).
    *   **Acceptance:** Can auto-mark drill as `completed` or `failed` based on output.
*   [ ] **Performance Regression Tracking:**
    *   **Task:** Compare current binary metrics with previous in history. Alert if `.text` growth >10%.
    *   **Acceptance:** Warning appears in TUI dashboard and post-build summary.

---

## **PHASE 4: THE MISSION CONTROL (TUI Dashboard)**

**Objective:** A professional, interactive interface for daily work.

### **SPRINT 8: DASHBOARD UI WITH TEXTUAL**
*   [ ] **Application Scaffold (`src/ui/app.py`):**
    *   **Task:** Create main `ProjectMgrApp` with a 4-pane layout (Navigation, Workbench, Datasheet, Serial).
    *   **Acceptance:** Panes resize correctly. Basic navigation works.
*   [ ] **Core Widgets:**
    *   **Task:** `ProjectTree` widget (left): Shows Phases & Drills with status icons.
    *   **Task:** `WorkbenchPane` (center): Shows active drill objectives, wiring, commands.
    *   **Task:** `SerialPane` (bottom): Live tail of UART log with highlighting.
    *   **Task:** `MemoryGauge` widget: Live bar chart of Flash/RAM usage.
*   [ ] **Interactive Hotkeys:**
    *   **Task:** Map `Ctrl+B` to build, `Ctrl+F` to flash, `Ctrl+D` to open datasheet, `Ctrl+M` to toggle monitor.
    *   **Acceptance:** Hotkeys trigger actions instantly.

---

## **PHASE 5: PROFESSIONAL TOOLS & REPORTING**

**Objective:** Turn work into billable hours and mastery insights.

### **SPRINT 9: TIME TRACKING & BILLING**
*   [ ] **Automatic Session Logging:**
    *   **Task:** `TimeTracker` starts/stops with `drill start/complete`. Logs to `ProjectState.history`.
    *   **Task:** Integrate with `Client` model (`hourly_rate`, `company`).
    *   **Acceptance:** Accurately tracks time spent per drill/project.
*   [ ] **Invoice Generation (`src/reporting/invoice.py`):**
    *   **Task:** CLI: `pm invoice generate --period last-month` creates a PDF/markdown invoice from time logs.
    *   **Acceptance:** Includes hours, rate, total, project milestones.

### **SPRINT 10: SKILL ANALYTICS & REPORTING**
*   [ ] **Protocol & Skill Matrix:**
    *   **Task:** Analyze drill tags (`spi`, `i2c`, `rtos`) to generate a visual "Mastery Matrix".
    *   **Task:** CLI: `pm skills show` outputs a table or simple chart.
    *   **Acceptance:** Clearly shows strong and weak areas.
*   [ ] **Automated Lab Notebook:**
    *   **Task:** Command `pm report weekly` generates a Markdown file with: completed drills, code snippets, memory graphs, wiring diagrams.
    *   **Acceptance:** Creates a presentable record of work for clients or your portfolio.

---

## **PHASE 6: DISTRIBUTION & PORTABILITY**

### **SPRINT 11: PACKAGING & DEPLOYMENT**
*   [ ] **Production Packaging:**
    *   **Task:** Create `pyproject.toml` with all dependencies and entry points.
    *   **Task:** Build installable package: `pip install projectmgr`.
*   [ ] **Containerized Development Environment:**
    *   **Task:** Create `Dockerfile.toolchain` with ARM GCC, OpenOCD, Python, and ProjectMgr pre-installed.
    *   **Acceptance:** Can build and flash a project inside container with host device passthrough.

---
