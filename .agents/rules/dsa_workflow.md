# 🤖 Automated DSA Documentation & Tracking Protocol

Whenever the user solves, discusses, or submits a new problem in this repository, ALWAYS execute the following automated synchronization workflow autonomously without being prompted.

---

## ⚡ Automated 5-Step Workflow for Every New Problem

### Step 1: Bucket Placement & File Creation
* Identify the algorithmic category and store files in the corresponding directory:
  * Arrays / Two Pointers / Sliding Window / Greedy $\to$ `01_arrays_and_pointers/`
  * Linked Lists $\to$ `02_linked_lists/`
  * Stacks & Monotonic $\to$ `03_stacks_and_queues/`
  * Sorting $\to$ `04_sorting/`
  * Binary Search $\to$ `05_binary_search/`
  * Trees & Graphs $\to$ `06_trees_and_graphs/`
  * Dynamic Programming & Backtracking $\to$ `07_dynamic_programming/`
* Create both:
  1. `<num>_<problem_name>.py`: Production Python solution with test assertions.
  2. `<num>_<problem_name>.md`: Intuitive study guide with plain English breakdown, ASCII visual diagrams, beginner traps, and FAANG interview role.

### Step 2: Auto-Update Pattern Cheat Sheets
* Review `cheat_sheets/` (e.g. `greedy_cheat_sheet.md`, `two_pointers_cheat_sheet.md`, `sliding_window_cheat_sheet.md`, `kadanes_algorithm_cheat_sheet.md`).
* If the problem reveals a new archetype, edge case, or decision rule, immediately update the relevant cheat sheet.

### Step 3: Auto-Update `tracker.html` & `faang_plan.html`
* Add the problem entry to `SCRATCH_PROBLEMS` in `tracker.html` (Title, Number, Difficulty, Pattern, Date, Study Doc link, Key Mental Model).
* Update the daily count and weekly velocity progress bar ($20$ problems/week).
* Check off the problem in `faang_plan.html`.

### Step 4: Rebuild HTML Viewer
* Run `python3 build_viewer.py` to bundle the new `.md` study guides into `viewer.html` so it opens with dark-mode formatting and syntax highlighting.

### Step 5: Update Central `README.md`
* Add the new problem entry to the appropriate section in `README.md`.

### Step 6: Git Auto-Commit & Remote Sync (MANDATORY)
* Maintain everything as an active Git repository, NOT just a local folder.
* After every problem solved, doc updated, or tracker synced:
  1. Stage all modified and new files (`git add .`).
  2. Create a descriptive commit authored by `tsathya98` (e.g. `feat(lc-134): add Gas Station study guide and tracker sync`).
  3. Push immediately to remote (`git push origin main`).
* The GitHub account for this repository is strictly **`tsathya98`** (email: `tsathya98@gmail.com`), NEVER work/corporate accounts.
* Repository remote: `https://github.com/tsathya98/dsa-patterns-handbook.git`.


