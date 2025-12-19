# 🚀 **PROJECTMGR: MASTER TODO LIST**

## **PHASE 1: THE CORE ENGINE (Data & Logic)**

### **SPRINT 1: INFRASTRUCTURE** ✅

* [x] **Config Module:** `src/config.py` handles path management and portable mode.
* [x] **Directory Setup:** `ensure_dirs()` creates `projects/` and `logs/`.
* [x] **Basic Persistence:** `src/pm.py` handles saving and loading `ProjectBundle`.

### **SPRINT 2: HIERARCHICAL MODELS** 🔄

* [x] **Project Bundle:** `src/models/bundle.py` (Root container).
* [x] **Phase & Drill Models:** Defined within the bundle and project models.
* [ ] **REFRESH: Hardware Profile Model (`src/models/hardware.py`):**
* [ ] Create `HardwareProfile` class: `id`, `name`, `mcu`, `arch`, `serial_port`, `debugger_type`.
* [ ] Add regex validation for ports (`/dev/tty*`, `COM*`).


* [ ] **REFRESH: Toolchain Model (`src/models/toolchain.py`):**
* [ ] Create `ToolchainRequirement` class: `name`, `min_version`, `env_var`.
* [ ] Implement `check_installed()` method using `subprocess`.


* [ ] **REFRESH: Client Model (`src/models/client.py`):**
* [ ] Create `Client` class: `name`, `company`, `hourly_rate`, `contact_info`.


* [ ] **ARCH UPDATE: Model Integration:**
* [ ] Update `Project` in `src/models/project.py` to include `hardware`, `toolchains`, and `client_info`.
* [ ] Update `Drill` in `src/models/bundle.py` with `build_command`, `flash_command`, and `required_hardware_ids`.



### **SPRINT 3: ATOMIC STORAGE & ARTIFACTS**

* [ ] **ARCH UPDATE: Atomic Operations (`src/storage.py`):**
* [ ] Move logic from `pm.py` to `storage.py`.
* [ ] Implement `atomic_json_write` using `tempfile` + `os.replace`.
* [ ] Integrate `fcntl.flock` for Unix file locking.


* [ ] **Binary Analysis (`src/utils/elf_analyzer.py`):**
* [ ] Create `BinaryAnalyzer` using `pyelftools` to return `.text`, `.data`, `.bss`.
* [ ] Integrate into `ProjectState` to store history metrics.



---

## **PHASE 2: THE INVENTORY & LAB BENCH**

### **SPRINT 4: HARDWARE INVENTORY SYSTEM**

* [ ] **Inventory Manager (`src/inventory_mgr.py`):**
* [ ] Dual storage: `personal.json` and `client_assets.json`.
* [ ] Track: `id`, `serial`, `location`, `status` (`available`, `checked_out`).


* [ ] **Resource Locking:**
* [ ] Prevent two projects from opening the same `serial_port` simultaneously.



### **SPRINT 5: KNOWLEDGE & TEMPLATING**

* [ ] **Datasheet Indexer (`src/utils/pdf_helper.py`):**
* [ ] CLI to search and open PDFs to a specific page.


* [ ] **Embedded Project Templating:**
* [ ] `pm new --template stm32` (generates Makefile, linker script, main.c).


* [ ] **Wiring Diagram Viewer:**
* [ ] `pm wiring show <drill_id>` (renders ASCII/PNG).



---

## **PHASE 3: THE EXECUTION ENGINE (Build & Flash)**

### **SPRINT 6: BUILD & FLASH AUTOMATION**

* [ ] **Build Manager (`src/build_mgr.py`):**
* [ ] Execute `drill.build_command` and capture logs to `logs/`.


* [ ] **Flash Manager (`src/flash_mgr.py`):**
* [ ] Execute `openocd`, `st-flash`, etc., based on `HardwareProfile`.


* [ ] **Integrated Serial Monitor:**
* [ ] Live `pyserial` monitor inside the CLI.



### **SPRINT 7: DRILL WORKFLOW & ANALYTICS**

* [ ] **Drill Lifecycle:** `pm drill start` (acquires locks, starts timer) and `pm drill complete` (stops timer, updates state).
* [ ] **Success Detection:** Auto-mark drill complete if "SUCCESS" regex is found in UART logs.
* [ ] **Regression Tracking:** Alert if `.text` (binary size) grows > 10% between builds.

---

## **PHASE 4: THE MISSION CONTROL (TUI Dashboard)**

### **SPRINT 8: DASHBOARD UI**

* [ ] **ARCH UPDATE: `src/dashboard.py`:**
* [ ] Refactor existing file to use **Textual** or **Rich**.
* [ ] Pane 1: Project/Phase/Drill Tree.
* [ ] Pane 2: Active Drill Objectives & Wiring.
* [ ] Pane 3: Memory Gauges (Flash/RAM usage).
* [ ] Pane 4: Live Serial Monitor output.



---

## **PHASE 5: PROFESSIONAL TOOLS & REPORTING**

### **SPRINT 9: TIME TRACKING & BILLING**

* [ ] **Session Logging:** Integrate work timer with `ProjectState.history`.
* [ ] **Invoice Generator:** Create PDF invoices using `Client` hourly rates.

### **SPRINT 10: SKILL ANALYTICS & REPORTS**

* [ ] **Skill Matrix:** Generate visual charts based on drill tags (`spi`, `i2c`, `can`).
* [ ] **Weekly Lab Report:** Export Markdown summary of work for clients.

---

## **PHASE 6: DISTRIBUTION**

### **SPRINT 11: PACKAGING & CI/CD**

* [ ] **Docker Toolchain:** Create a container with ARM-GCC and ProjectMgr pre-installed.
* [ ] **Shell Completion:** Add autocomplete for `project_id` and `drill_id`.

