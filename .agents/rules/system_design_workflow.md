# 🏗️ Automated System Design Documentation & Sync Protocol

Whenever a new System Design topic, lecture, or case study is discussed or requested, execute the following protocol autonomously:

---

## ⚡ Automated 5-Step Workflow for System Design

### Step 1: Bucket Placement & File Creation
* Create the markdown document under `content/system-design/`:
  * E.g., `content/system-design/<topic_name>.md`.
  * Structure: Core problem, 4-layer architecture diagram (ASCII), component trade-offs, and failure handling.
* If it introduces a new calculation rule or pattern archetype, update or create a quick-reference cheat sheet in `content/cheat-sheets/`.

### Step 2: Create Active Excalidraw Practice Prompt
* Add or link an Excalidraw whiteboarding challenge in `content/system-design/` with:
  * 20-25 minute timer target.
  * 4-layer drawing checklist (Edge $\to$ Compute $\to$ Storage $\to$ Async).
  * 3-4 self-grilling questions.

### Step 3: Rebuild HTML Viewer
* Run `python3 scripts/legacy/build_viewer.py` to bundle all markdown guides into `generated/legacy/viewer.html` for clean, zero-CORS local viewing.

### Step 4: Update Central Index
* Add links in `docs/study-index.md` under Section 5 (System Design & Production Infrastructure).

### Step 5: Git Auto-Commit & Push (MANDATORY)
* Stage modified and new files (`git add .`).
* Commit authored by `tsathya98` (`tsathya98@gmail.com`).
* Push immediately to `origin/main`.
