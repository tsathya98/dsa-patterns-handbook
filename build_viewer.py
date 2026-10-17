#!/usr/bin/env python3
"""
Generate the unified DSA Study Hub & Tracker web application:
- Bundles all 94 markdown study guides, cheat sheets, and system design docs as JSON.
- Renders Markdown (marked.js), Syntax Highlighting (highlight.js), Math (KaTeX),
  and Flowcharts (Mermaid.js) locally via static/vendor/ with zero CORS issues on file://.
- Outputs viewer.html (defaults to Reader view), tracker.html (defaults to Tracker view),
  and index.html (defaults to Reader/Tracker hub).
"""

import os
import json
import re

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

CATEGORY_META = {
    "Root": {"label": "Overview & Plans", "order": 0, "icon": "🧭"},
    "cheat_sheets": {"label": "Cheat Sheets", "order": 1, "icon": "⚡"},
    "00_foundations": {"label": "00. Foundations", "order": 2, "icon": "🧱"},
    "01_arrays_and_pointers": {"label": "01. Arrays & Pointers", "order": 3, "icon": "🎯"},
    "02_linked_lists": {"label": "02. Linked Lists", "order": 4, "icon": "🔗"},
    "03_stacks_and_queues": {"label": "03. Stacks & Queues", "order": 5, "icon": "🥞"},
    "04_sorting": {"label": "04. Sorting", "order": 6, "icon": "📊"},
    "05_binary_search": {"label": "05. Binary Search", "order": 7, "icon": "🔍"},
    "system_design": {"label": "System Design", "order": 8, "icon": "🏗️"},
}

DEFAULT_SOLVED_PATHS = [
    "01_arrays_and_pointers/88_merge_sorted_array.md",
    "01_arrays_and_pointers/27_remove_element.md",
    "01_arrays_and_pointers/26_remove_duplicates_from_sorted_array.md",
    "01_arrays_and_pointers/80_remove_duplicates_from_sorted_array_ii.md",
    "01_arrays_and_pointers/169_majority_element.md",
    "01_arrays_and_pointers/189_rotate_array.md",
    "01_arrays_and_pointers/121_best_time_to_buy_and_sell_stock.md",
    "01_arrays_and_pointers/122_best_time_to_buy_and_sell_stock_ii.md",
    "01_arrays_and_pointers/55_jump_game.md",
    "01_arrays_and_pointers/274_h_index.md",
    "03_stacks_and_queues/678_valid_parenthesis_string.md",
    "03_stacks_and_queues/20_valid_parentheses.md",
    "01_arrays_and_pointers/125_valid_palindrome.md",
    "01_arrays_and_pointers/392_is_subsequence.md",
    "01_arrays_and_pointers/167_two_sum_ii_input_array_is_sorted.md",
    "01_arrays_and_pointers/11_container_with_most_water.md",
    "01_arrays_and_pointers/15_3sum.md",
    "01_arrays_and_pointers/238_product_of_array_except_self.md",
    "01_arrays_and_pointers/3_longest_substring_without_repeating_characters.md",
    "01_arrays_and_pointers/5_longest_palindromic_substring.md",
    "01_arrays_and_pointers/283_move_zeroes.md",
    "01_arrays_and_pointers/66_plus_one.md",
    "01_arrays_and_pointers/724_find_pivot_index.md",
    "01_arrays_and_pointers/643_maximum_average_subarray_i.md",
    "01_arrays_and_pointers/1456_maximum_number_of_vowels_in_a_substring_of_given_length.md",
    "01_arrays_and_pointers/228_summary_ranges.md",
    "01_arrays_and_pointers/290_word_pattern.md",
    "01_arrays_and_pointers/12_integer_to_roman.md",
    "01_arrays_and_pointers/13_roman_to_integer.md",
    "01_arrays_and_pointers/53_maximum_subarray.md",
    "02_linked_lists/206_reverse_linked_list.md",
    "02_linked_lists/21_merge_two_sorted_lists.md",
    "02_linked_lists/2_add_two_numbers.md",
    "02_linked_lists/19_remove_nth_node_from_end.md",
    "02_linked_lists/83_remove_duplicates_from_sorted_list.md",
    "02_linked_lists/141_linked_list_cycle.md",
    "02_linked_lists/143_reorder_list.md",
    "02_linked_lists/234_palindrome_linked_list.md",
    "02_linked_lists/1290_convert_binary_number_in_a_linked_list_to_integer.md",
    "02_linked_lists/1721_swapping_nodes_in_a_linked_list.md",
]


def parse_doc_metadata(rel_path: str, filename: str, content: str) -> dict:
    cat_raw = rel_path.split("/")[0] if "/" in rel_path else "Root"
    cat_info = CATEGORY_META.get(cat_raw, {"label": cat_raw, "order": 99, "icon": "📄"})

    # Title
    m_title = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = m_title.group(1).strip() if m_title else filename

    # Check if filename starts with a number (either LC number or 00/01 prefix)
    m_num = re.match(r"^(\d+)_", filename)
    prefix_num = int(m_num.group(1)) if m_num else 9999

    # Determine if it's a LeetCode problem
    m_lc_title = re.search(r"LeetCode\s+(\d+)", title, re.IGNORECASE)
    lc_number = int(m_lc_title.group(1)) if m_lc_title else None
    if lc_number is None and cat_raw in ("01_arrays_and_pointers", "02_linked_lists", "03_stacks_and_queues"):
        if prefix_num > 0 and not filename.startswith("00_") and not filename.startswith("01_linked_list_fundamentals"):
            lc_number = prefix_num

    # Difficulty
    m_diff = re.search(r"\*\*Difficulty:\*\*\s*(Easy|Medium|Hard)", content, re.IGNORECASE)
    difficulty = m_diff.group(1).capitalize() if m_diff else ("Cheat Sheet" if cat_raw == "cheat_sheets" else "Concept")

    # Pattern
    m_pat = re.search(r"\*\*Pattern:\*\*\s*([^\n|]+)", content)
    pattern = m_pat.group(1).strip() if m_pat else cat_info["label"]

    # LeetCode URL
    m_url = re.search(r"\((https://leetcode\.com/problems/[^)]+)\)", content)
    lc_url = m_url.group(1).strip() if m_url else ""

    # Short 1-line summary (first normal paragraph line)
    summary = ""
    for line in content.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith(">") or s.startswith("```") or s.startswith("|") or s.startswith("---") or s.startswith("<"):
            continue
        # Clean markdown formatting
        clean_s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
        clean_s = clean_s.replace("**", "").replace("`", "")
        if len(clean_s) > 20:
            summary = clean_s[:160] + ("..." if len(clean_s) > 160 else "")
            break

    # Doc type & sort key
    if cat_raw == "cheat_sheets":
        doc_type = "cheat_sheet"
        sort_key = (0, prefix_num, title.lower())
    elif cat_raw == "system_design":
        doc_type = "system_design"
        sort_key = (0, prefix_num, title.lower())
    elif cat_raw == "Root":
        doc_type = "overview"
        sort_key = (0, prefix_num, title.lower())
    elif lc_number is not None:
        doc_type = "problem"
        sort_key = (1, lc_number, title.lower())
    else:
        doc_type = "concept"
        sort_key = (0, prefix_num, title.lower())

    return {
        "path": rel_path,
        "title": title,
        "category": cat_raw,
        "categoryLabel": cat_info["label"],
        "categoryOrder": cat_info["order"],
        "categoryIcon": cat_info["icon"],
        "lcNumber": lc_number,
        "difficulty": difficulty,
        "pattern": pattern,
        "lcUrl": lc_url,
        "summary": summary,
        "docType": doc_type,
        "hasMermaid": "```mermaid" in content,
        "defaultSolved": rel_path in DEFAULT_SOLVED_PATHS,
        "sortOrder": sort_key,
        "content": content,
    }


raw_docs = []
for root, dirs, files in os.walk(ROOT_DIR):
    if any(x in root for x in (".git", "static", ".gemini", ".agents", "notes")):
        continue
    for f in sorted(files):
        if f.endswith(".md"):
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, ROOT_DIR)
            with open(full_path, "r", encoding="utf-8", errors="ignore") as fp:
                content = fp.read()
            raw_docs.append(parse_doc_metadata(rel_path, f, content))

# Sort deterministically by category order, then doc_type (concepts before LC problems), then LC number
raw_docs.sort(key=lambda d: (d["categoryOrder"], d["sortOrder"][0], d["sortOrder"][1], d["sortOrder"][2]))

docs = {}
for idx, d in enumerate(raw_docs):
    d["index"] = idx
    del d["sortOrder"]
    docs[d["path"]] = d

print(f"Bundled {len(docs)} markdown documents.")

hl_css_path = os.path.join(ROOT_DIR, "static/vendor/highlight-github-dark.min.css")
hl_css = open(hl_css_path, "r", encoding="utf-8").read() if os.path.exists(hl_css_path) else ""

docs_json_str = json.dumps(docs)


def build_html(default_view: str = "reader") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DSA Visual Study Hub & Tracker</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <link rel="stylesheet" href="static/vendor/katex.min.css">
  <script src="static/vendor/marked.min.js"></script>
  <script src="static/vendor/highlight.min.js"></script>
  <script src="static/vendor/katex.min.js"></script>
  <script src="static/vendor/auto-render.min.js"></script>
  <script src="static/vendor/mermaid.min.js"></script>
  <style>
    {hl_css}

    /* THEME 1: OBSIDIAN CHARCOAL (DEFAULT) */
    body.theme-charcoal {{
      --bg: #0c0e12;
      --surface: #13171f;
      --surface-card: #181d27;
      --surface-hover: #1f2633;
      --border: #262f3f;
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --accent: #10b981;
      --accent-soft: rgba(16, 185, 129, 0.14);
      --code-bg: #090b0e;
      --heading-h1: #34d399;
      --heading-h2: #38bdf8;
    }}

    /* THEME 2: MATCHA / GRUVBOX */
    body.theme-matcha {{
      --bg: #141615;
      --surface: #1b1e1c;
      --surface-card: #222623;
      --surface-hover: #2b302c;
      --border: #333935;
      --text: #ebdbb2;
      --text-muted: #a89984;
      --accent: #a9b665;
      --accent-soft: rgba(169, 182, 101, 0.16);
      --code-bg: #0f1110;
      --heading-h1: #a9b665;
      --heading-h2: #7daea3;
    }}

    /* THEME 3: WARM PAPER (KINDLE SEPIA) */
    body.theme-sepia {{
      --bg: #f6f1e7;
      --surface: #ece4d7;
      --surface-card: #ffffff;
      --surface-hover: #e5dccb;
      --border: #d8ccb8;
      --text: #282320;
      --text-muted: #6e635d;
      --accent: #059669;
      --accent-soft: rgba(5, 150, 105, 0.12);
      --code-bg: #1e242b;
      --heading-h1: #047857;
      --heading-h2: #0369a1;
    }}

    body {{
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, sans-serif;
      letter-spacing: -0.01em;
    }}

    .ui-bg {{ background-color: var(--bg); }}
    .ui-surface {{ background-color: var(--surface); border-color: var(--border); }}
    .ui-card {{ background-color: var(--surface-card); border-color: var(--border); }}
    .ui-text {{ color: var(--text); }}
    .ui-text-muted {{ color: var(--text-muted); }}
    .ui-border {{ border-color: var(--border); }}

    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 9999px; }}

    /* Markdown Reader Typography */
    .md-body {{
      color: var(--text);
      line-height: 1.72;
      font-size: 0.95rem;
    }}
    .md-body h1 {{
      font-size: 1.65rem;
      font-weight: 800;
      color: var(--heading-h1);
      margin-top: 0.25rem;
      margin-bottom: 1rem;
      padding-bottom: 0.5rem;
      border-bottom: 1px solid var(--border);
    }}
    .md-body h2 {{
      font-size: 1.22rem;
      font-weight: 700;
      color: var(--heading-h2);
      margin-top: 1.75rem;
      margin-bottom: 0.65rem;
      padding-bottom: 0.35rem;
      border-bottom: 1px solid var(--border);
      scroll-margin-top: 5rem;
    }}
    .md-body h3 {{
      font-size: 1.05rem;
      font-weight: 600;
      color: var(--text);
      margin-top: 1.25rem;
      margin-bottom: 0.45rem;
      scroll-margin-top: 5rem;
    }}
    .md-body p {{
      margin-bottom: 0.9rem;
    }}
    .md-body ul, .md-body ol {{
      margin-bottom: 1rem;
      padding-left: 1.4rem;
    }}
    .md-body ul {{ list-style-type: disc; }}
    .md-body ol {{ list-style-type: decimal; }}
    .md-body li {{ margin-bottom: 0.3rem; }}
    .md-body blockquote {{
      border-left: 3px solid var(--accent);
      background: var(--accent-soft);
      padding: 0.6rem 1rem;
      border-radius: 0 0.5rem 0.5rem 0;
      margin-bottom: 1rem;
      font-size: 0.875rem;
    }}
    .md-body blockquote p {{ margin-bottom: 0.2rem; }}
    .md-body pre {{
      background: var(--code-bg) !important;
      color: #e2e8f0;
      border: 1px solid var(--border);
      border-radius: 0.75rem;
      padding: 0.9rem 1rem;
      overflow-x: auto;
      margin-bottom: 1rem;
      font-size: 0.84rem;
      line-height: 1.55;
    }}
    .md-body code {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.84em;
    }}
    .md-body :not(pre) > code {{
      background: var(--surface);
      border: 1px solid var(--border);
      padding: 0.12rem 0.38rem;
      border-radius: 0.35rem;
      color: var(--heading-h1);
    }}
    .md-body table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 1.2rem;
      font-size: 0.85rem;
      border: 1px solid var(--border);
      border-radius: 0.5rem;
      overflow: hidden;
    }}
    .md-body th {{
      background: var(--surface);
      font-weight: 600;
      text-align: left;
      padding: 0.55rem 0.75rem;
      border-bottom: 1px solid var(--border);
    }}
    .md-body td {{
      padding: 0.5rem 0.75rem;
      border-bottom: 1px solid var(--border);
    }}
    .md-body a {{
      color: var(--heading-h1);
      text-decoration: underline;
      text-underline-offset: 3px;
    }}
    .md-body details {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 0.75rem;
      padding: 0.65rem 1rem;
      margin-bottom: 1rem;
    }}
    .md-body summary {{
      cursor: pointer;
      font-weight: 600;
      color: var(--heading-h1);
      user-select: none;
    }}
    .md-body details[open] summary {{
      margin-bottom: 0.75rem;
      padding-bottom: 0.45rem;
      border-bottom: 1px solid var(--border);
    }}

    /* Visual-Only Focus Mode: dims paragraphs so diagrams, flowcharts, tables, and code pop */
    .md-body.visual-focus-mode > p,
    .md-body.visual-focus-mode > ul,
    .md-body.visual-focus-mode > ol {{
      display: none;
    }}

    .md-body.hide-flowcharts-mode .mermaid-figure {{
      display: none;
    }}

    /* Native Dialog Backdrop */
    dialog::backdrop {{
      background: rgba(0, 0, 0, 0.72);
      backdrop-filter: blur(4px);
    }}
  </style>
</head>
<body class="theme-charcoal min-h-screen flex flex-col selection:bg-emerald-500 selection:text-black antialiased">

  <!-- 1. UNIFIED TOP NAVIGATION BAR -->
  <header class="sticky top-0 z-30 ui-surface border-b px-3 sm:px-5 py-2.5 flex items-center justify-between gap-3">
    <div class="flex items-center gap-2.5">
      <button type="button" id="mobile-sidebar-btn" class="lg:hidden p-1.5 rounded-lg ui-card border ui-text-muted hover:opacity-80" aria-label="Toggle navigation sidebar">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
      <div class="flex items-center gap-2">
        <span class="text-lg font-extrabold tracking-tight text-emerald-400">DSA Hub</span>
        <span id="global-progress-pill" class="hidden sm:inline-flex items-center gap-1 text-xs font-mono px-2 py-0.5 rounded-full ui-card border ui-text-muted">
          0 Solved
        </span>
      </div>
    </div>

    <!-- Primary View Switcher Tabs -->
    <nav class="flex items-center gap-1 ui-card p-1 rounded-xl border" aria-label="Primary views">
      <button type="button" onclick="switchView('reader')" id="nav-btn-reader" class="px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5">
        <span aria-hidden="true">📖</span> Study Notes
      </button>
      <button type="button" onclick="switchView('cheatsheets')" id="nav-btn-cheatsheets" class="px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5">
        <span aria-hidden="true">⚡</span> Cheat Sheets
      </button>
      <button type="button" onclick="switchView('tracker')" id="nav-btn-tracker" class="px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5">
        <span aria-hidden="true">✅</span> Tracker
      </button>
      <button type="button" onclick="switchView('roadmap')" id="nav-btn-roadmap" class="px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5">
        <span aria-hidden="true">🗺️</span> 12-Wk Plan
      </button>
    </nav>

    <!-- Right Controls: Quick Search (Cmd+K) & Theme Switcher -->
    <div class="flex items-center gap-2">
      <button type="button" id="open-cmdk-btn" class="px-2.5 py-1.5 rounded-lg ui-card border text-xs ui-text-muted hover:opacity-90 flex items-center gap-2 transition-colors" aria-label="Search all notes and problems">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        <span class="hidden md:inline">Search 94 docs...</span>
        <kbd class="px-1.5 py-0.5 text-xs font-mono ui-surface rounded border">⌘K</kbd>
      </button>

      <div class="hidden sm:flex items-center ui-card rounded-lg p-0.5 border text-xs" role="group" aria-label="Color theme">
        <button type="button" onclick="setTheme('charcoal')" id="btn-theme-charcoal" class="px-2 py-1 rounded font-medium transition-all" title="Obsidian Charcoal">🌑</button>
        <button type="button" onclick="setTheme('matcha')" id="btn-theme-matcha" class="px-2 py-1 rounded font-medium transition-all" title="Matcha Gruvbox">🍵</button>
        <button type="button" onclick="setTheme('sepia')" id="btn-theme-sepia" class="px-2 py-1 rounded font-medium transition-all" title="Warm Paper">📜</button>
      </div>
    </div>
  </header>

  <!-- ===================================================================== -->
  <!-- VIEW 1: STUDY READER (3-Column Clean Layout)                          -->
  <!-- ===================================================================== -->
  <main id="view-reader" class="flex-1 flex overflow-hidden">
    
    <!-- Left Categorized Sidebar -->
    <aside id="reader-sidebar" class="w-72 shrink-0 ui-surface border-r flex flex-col h-[calc(100vh-53px)] sticky top-[53px] hidden lg:flex">
      <div class="p-3 border-b ui-border space-y-2">
        <search>
          <input id="sidebar-filter-input" type="search" placeholder="Filter sidebar topics..." aria-label="Filter sidebar topics" class="w-full ui-card border rounded-lg px-3 py-1.5 text-xs focus:outline-none focus:border-emerald-500">
        </search>
        <div class="flex items-center justify-between text-xs ui-text-muted px-1">
          <span id="sidebar-count-label">94 Study Docs</span>
          <button type="button" id="toggle-all-cats-btn" class="hover:underline text-emerald-400">Collapse all</button>
        </div>
      </div>
      <div id="sidebar-tree" class="flex-1 overflow-y-auto p-2.5 space-y-2">
        <!-- Populated by JS -->
      </div>
    </aside>

    <!-- Center Markdown & Visual Flowchart Canvas -->
    <div id="reader-scroll-container" class="flex-1 overflow-y-auto h-[calc(100vh-53px)] px-4 sm:px-8 py-6">
      <div class="max-w-3xl mx-auto space-y-5 pb-16">

        <!-- Sticky Document Control Bar -->
        <div class="ui-card border rounded-xl p-3.5 flex flex-wrap items-center justify-between gap-3 shadow-sm">
          <div class="flex items-center gap-2 flex-wrap">
            <span id="doc-cat-badge" class="text-xs font-medium px-2.5 py-0.5 rounded-full ui-surface border ui-text-muted">Module</span>
            <span id="doc-diff-badge" class="text-xs font-semibold px-2.5 py-0.5 rounded-full">Difficulty</span>
            <a id="doc-lc-link" href="#" target="_blank" rel="noopener noreferrer" class="hidden text-xs font-medium text-emerald-400 hover:underline flex items-center gap-1">
              LeetCode ↗
            </a>
          </div>

          <!-- Visual Mode & Status Controls -->
          <div class="flex items-center gap-2 flex-wrap">
            <!-- Reading Mode Toggle: Text+Diagrams vs Visuals Only -->
            <div class="flex items-center ui-surface rounded-lg p-0.5 border text-xs" role="group" aria-label="Reading mode">
              <button type="button" onclick="setReaderMode('full')" id="mode-btn-full" class="px-2.5 py-1 rounded font-medium bg-emerald-500/20 text-emerald-400">
                Text + Diagrams
              </button>
              <button type="button" onclick="setReaderMode('visual')" id="mode-btn-visual" class="px-2.5 py-1 rounded font-medium ui-text-muted" title="Hide paragraphs and show only flowcharts, arrow traces, tables, and code">
                ⚡ Visuals Only
              </button>
            </div>

            <!-- Flowchart Visibility Toggle -->
            <button type="button" onclick="toggleFlowcharts()" id="btn-toggle-flowcharts" class="px-2.5 py-1 rounded-lg border ui-surface text-xs font-medium text-emerald-400" title="Show or hide Mermaid flowcharts">
              📊 Flowcharts: ON
            </button>

            <!-- 1-Click Problem Status Selector -->
            <div class="flex items-center ui-surface rounded-lg p-0.5 border text-xs" role="group" aria-label="Study status">
              <button type="button" onclick="setCurrentDocStatus('todo')" id="status-btn-todo" class="px-2 py-1 rounded font-medium">○ Todo</button>
              <button type="button" onclick="setCurrentDocStatus('review')" id="status-btn-review" class="px-2 py-1 rounded font-medium">🔁 Review</button>
              <button type="button" onclick="setCurrentDocStatus('solved')" id="status-btn-solved" class="px-2 py-1 rounded font-medium">✓ Solved</button>
            </div>
          </div>
        </div>

        <!-- Rendered Document Content -->
        <article id="rendered-content" class="md-body ui-card border rounded-2xl p-5 sm:p-8 shadow-sm">
        </article>

        <!-- Personal Takeaway Note for this Doc -->
        <section class="ui-card border rounded-xl p-4 space-y-2" aria-label="Personal notes">
          <div class="flex items-center justify-between">
            <label for="doc-personal-note" class="text-xs font-bold uppercase tracking-wider text-emerald-400">📌 Your Personal Takeaway / Mistake Log</label>
            <span id="note-saved-indicator" class="text-xs ui-text-muted">Auto-saves locally</span>
          </div>
          <textarea id="doc-personal-note" rows="2" placeholder="Write your 1-sentence mental trigger or edge case for this topic..." class="w-full ui-surface border rounded-lg p-2.5 text-xs focus:outline-none focus:border-emerald-500"></textarea>
        </section>

        <!-- Prev / Next Navigation Footer -->
        <nav class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2" aria-label="Document pagination">
          <button type="button" id="prev-doc-btn" class="ui-card border rounded-xl p-3.5 text-left hover:border-emerald-500/50 transition-all group">
            <div class="text-xs ui-text-muted">← Previous Guide</div>
            <div id="prev-doc-title" class="text-sm font-semibold mt-0.5 group-hover:text-emerald-400 truncate">-</div>
          </button>
          <button type="button" id="next-doc-btn" class="ui-card border rounded-xl p-3.5 text-right hover:border-emerald-500/50 transition-all group">
            <div class="text-xs ui-text-muted">Next Guide →</div>
            <div id="next-doc-title" class="text-sm font-semibold mt-0.5 group-hover:text-emerald-400 truncate">-</div>
          </button>
        </nav>

      </div>
    </div>

    <!-- Right Table of Contents Rail -->
    <aside class="w-60 shrink-0 ui-surface border-l p-4 h-[calc(100vh-53px)] sticky top-[53px] hidden xl:flex flex-col justify-between overflow-y-auto">
      <div class="space-y-3">
        <div class="text-xs font-bold uppercase tracking-wider ui-text-muted">On This Page</div>
        <nav id="toc-list" class="space-y-1.5 text-xs" aria-label="Table of contents">
        </nav>
      </div>
      <div class="ui-card border rounded-xl p-3 space-y-1.5 text-xs">
        <div class="font-semibold text-emerald-400">Keyboard Shortcuts</div>
        <div class="flex justify-between ui-text-muted"><span>Search all docs</span><kbd class="font-mono">⌘K / /</kbd></div>
        <div class="flex justify-between ui-text-muted"><span>Prev / Next doc</span><kbd class="font-mono">[ / ]</kbd></div>
        <div class="flex justify-between ui-text-muted"><span>Toggle Visual Mode</span><kbd class="font-mono">v</kbd></div>
      </div>
    </aside>

  </main>

  <!-- ===================================================================== -->
  <!-- VIEW 2: CHEAT SHEETS DECK (Visual Card Grid of All 21 Cheat Sheets)   -->
  <!-- ===================================================================== -->
  <section id="view-cheatsheets" class="hidden flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 py-6 space-y-5">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b ui-border pb-4">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold text-emerald-400">⚡ Pattern Cheat Sheets Deck (21)</h1>
        <p class="text-xs ui-text-muted mt-0.5">Quick-reference pattern triggers, decision flowcharts, and copy-paste templates.</p>
      </div>
      <search>
        <input id="cs-search-input" type="search" placeholder="Filter cheat sheets..." aria-label="Filter cheat sheets" class="ui-card border rounded-xl px-3.5 py-2 text-xs w-full sm:w-64 focus:outline-none focus:border-emerald-500">
      </search>
    </div>

    <div id="cheatsheets-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <!-- Populated by JS -->
    </div>
  </section>

  <!-- ===================================================================== -->
  <!-- VIEW 3: UNIFIED TRACKER (All 94 Repo Docs + Custom Logged Problems)   -->
  <!-- ===================================================================== -->
  <section id="view-tracker" class="hidden flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 py-6 space-y-5">
    
    <!-- Top Stats Row -->
    <div class="grid grid-cols-2 sm:grid-cols-5 gap-3">
      <div class="ui-card border rounded-xl p-3.5">
        <div class="text-xs ui-text-muted">Total Completed</div>
        <div class="text-2xl font-black text-emerald-400 mt-0.5" id="stat-solved">0</div>
        <div class="text-xs ui-text-muted mt-0.5" id="stat-total-label">of 94 study items</div>
      </div>
      <div class="ui-card border rounded-xl p-3.5">
        <div class="text-xs ui-text-muted">Needs Review</div>
        <div class="text-2xl font-black text-amber-400 mt-0.5" id="stat-review">0</div>
        <div class="text-xs ui-text-muted mt-0.5">Spaced repetition queue</div>
      </div>
      <div class="ui-card border rounded-xl p-3.5">
        <div class="text-xs ui-text-muted">Easy Solved</div>
        <div class="text-2xl font-black text-emerald-400 mt-0.5" id="stat-easy">0</div>
        <div class="text-xs ui-text-muted mt-0.5">Foundation builders</div>
      </div>
      <div class="ui-card border rounded-xl p-3.5">
        <div class="text-xs ui-text-muted">Medium / Hard</div>
        <div class="text-2xl font-black text-sky-400 mt-0.5" id="stat-medium">0</div>
        <div class="text-xs ui-text-muted mt-0.5">Interview core</div>
      </div>
      <div class="ui-card border rounded-xl p-3.5 col-span-2 sm:col-span-1 flex flex-col justify-between">
        <div class="text-xs ui-text-muted">Log External Problem</div>
        <button type="button" id="open-log-dialog-btn" class="mt-2 w-full py-1.5 px-3 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold text-xs transition-all">
          + Log Problem
        </button>
      </div>
    </div>

    <!-- Filter Bar -->
    <div class="ui-card border rounded-xl p-3 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">
      <search class="flex-1">
        <input id="tracker-search-input" type="search" placeholder="Search by problem #, title, pattern, or takeaway..." aria-label="Search tracker items" class="w-full ui-surface border rounded-lg px-3 py-1.5 text-xs focus:outline-none focus:border-emerald-500">
      </search>

      <div class="flex flex-wrap items-center gap-2">
        <!-- Category Filter -->
        <select id="tracker-cat-filter" aria-label="Filter by module" class="ui-surface border rounded-lg px-2.5 py-1.5 text-xs focus:outline-none focus:border-emerald-500">
          <option value="ALL">All Modules (94)</option>
          <option value="01_arrays_and_pointers">01. Arrays & Pointers</option>
          <option value="02_linked_lists">02. Linked Lists</option>
          <option value="03_stacks_and_queues">03. Stacks & Queues</option>
          <option value="04_sorting">04. Sorting</option>
          <option value="05_binary_search">05. Binary Search</option>
          <option value="00_foundations">00. Foundations</option>
          <option value="cheat_sheets">Cheat Sheets</option>
          <option value="system_design">System Design</option>
        </select>

        <!-- Status Filter -->
        <div class="flex items-center ui-surface rounded-lg p-0.5 border text-xs" role="group" aria-label="Filter by status">
          <button type="button" onclick="setTrackerStatusFilter('ALL')" data-status="ALL" class="tracker-status-btn px-2.5 py-1 rounded font-medium bg-emerald-500/20 text-emerald-400">All</button>
          <button type="button" onclick="setTrackerStatusFilter('solved')" data-status="solved" class="tracker-status-btn px-2.5 py-1 rounded font-medium ui-text-muted">✓ Solved</button>
          <button type="button" onclick="setTrackerStatusFilter('review')" data-status="review" class="tracker-status-btn px-2.5 py-1 rounded font-medium ui-text-muted">🔁 Review</button>
          <button type="button" onclick="setTrackerStatusFilter('todo')" data-status="todo" class="tracker-status-btn px-2.5 py-1 rounded font-medium ui-text-muted">○ Todo</button>
        </div>
      </div>
    </div>

    <!-- Clean Scannable Tracker Table -->
    <div class="ui-card border rounded-2xl overflow-hidden shadow-sm">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="ui-surface border-b ui-border ui-text-muted uppercase tracking-wider">
              <th class="py-3 px-3 w-28">Status</th>
              <th class="py-3 px-3">Problem / Topic</th>
              <th class="py-3 px-3 hidden sm:table-cell">Pattern / Module</th>
              <th class="py-3 px-3 hidden lg:table-cell">Core Trick / Takeaway</th>
              <th class="py-3 px-3 text-right w-36">Actions</th>
            </tr>
          </thead>
          <tbody id="tracker-tbody" class="divide-y ui-border">
            <!-- Populated by JS -->
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- ===================================================================== -->
  <!-- VIEW 4: 12-WEEK FAANG ROADMAP (With hidden="until-found" support)     -->
  <!-- ===================================================================== -->
  <section id="view-roadmap" class="hidden flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 py-6 space-y-5">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b ui-border pb-4">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold text-emerald-400">🗺️ 12-Week FAANG Preparation Roadmap</h1>
        <p class="text-xs ui-text-muted mt-0.5">2 problems/day on weekdays • 5/day on weekends • Click any topic to open its study note.</p>
      </div>
      <button type="button" onclick="openDocInReader('faang_preparation_plan.md')" class="px-3 py-1.5 rounded-lg ui-card border text-xs font-semibold text-emerald-400 hover:opacity-90">
        Read Full Plan Doc →
      </button>
    </div>

    <!-- Phase Switcher Controls -->
    <div id="roadmap-accordion">
      <div class="flex items-center gap-2 overflow-x-auto pb-3" role="tablist">
        <button type="button" onclick="selectRoadmapPhase('rm-phase-1')" id="btn-rm-phase-1" aria-expanded="true" aria-controls="rm-phase-1" class="rm-tab-btn px-3.5 py-2 rounded-xl text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 whitespace-nowrap">
          Phase 1: Arrays, Pointers & Windows (W1–3)
        </button>
        <button type="button" onclick="selectRoadmapPhase('rm-phase-2')" id="btn-rm-phase-2" aria-expanded="false" aria-controls="rm-phase-2" class="rm-tab-btn px-3.5 py-2 rounded-xl text-xs font-semibold ui-card border ui-text-muted whitespace-nowrap">
          Phase 2: Linked Lists, Stacks & Binary Search (W4–6)
        </button>
        <button type="button" onclick="selectRoadmapPhase('rm-phase-3')" id="btn-rm-phase-3" aria-expanded="false" aria-controls="rm-phase-3" class="rm-tab-btn px-3.5 py-2 rounded-xl text-xs font-semibold ui-card border ui-text-muted whitespace-nowrap">
          Phase 3: Trees, Graphs & Heaps (W7–9)
        </button>
        <button type="button" onclick="selectRoadmapPhase('rm-phase-4')" id="btn-rm-phase-4" aria-expanded="false" aria-controls="rm-phase-4" class="rm-tab-btn px-3.5 py-2 rounded-xl text-xs font-semibold ui-card border ui-text-muted whitespace-nowrap">
          Phase 4: Backtracking, DP & System Design (W10–12)
        </button>
      </div>

      <div id="rm-phase-1" class="rm-panel">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2" id="rm-phase-1-grid"></div>
      </div>
      <div id="rm-phase-2" class="rm-panel" hidden="until-found">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2" id="rm-phase-2-grid"></div>
      </div>
      <div id="rm-phase-3" class="rm-panel" hidden="until-found">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2" id="rm-phase-3-grid"></div>
      </div>
      <div id="rm-phase-4" class="rm-panel" hidden="until-found">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2" id="rm-phase-4-grid"></div>
      </div>
    </div>
  </section>

  <!-- ===================================================================== -->
  <!-- NATIVE DIALOG 1: COMMAND PALETTE SEARCH (Cmd+K)                       -->
  <!-- ===================================================================== -->
  <dialog id="cmdk-dialog" closedby="any" class="ui-card border rounded-2xl w-full max-w-xl p-0 text-[var(--text)] shadow-2xl">
    <div class="p-3.5 border-b ui-border flex items-center gap-2.5">
      <svg class="w-4 h-4 ui-text-muted shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
      <search class="flex-1">
        <input id="cmdk-input" type="search" placeholder="Search any problem #, pattern, flowchart, or keyword..." aria-label="Search all study guides" class="w-full bg-transparent text-sm focus:outline-none">
      </search>
      <form method="dialog">
        <button type="submit" class="px-2 py-0.5 rounded text-xs ui-surface border ui-text-muted">Esc</button>
      </form>
    </div>
    <div id="cmdk-results" class="max-h-96 overflow-y-auto p-2 space-y-1">
    </div>
  </dialog>

  <!-- ===================================================================== -->
  <!-- NATIVE DIALOG 2: QUICK-PEEK STUDY DRAWER (From Tracker)               -->
  <!-- ===================================================================== -->
  <dialog id="peek-dialog" closedby="any" class="ui-card border rounded-2xl w-full max-w-3xl p-0 text-[var(--text)] shadow-2xl max-h-[88vh]">
    <div class="sticky top-0 z-10 ui-surface border-b px-5 py-3 flex items-center justify-between gap-3">
      <div class="flex items-center gap-2 truncate">
        <span id="peek-title" class="font-bold text-sm truncate">Study Guide</span>
      </div>
      <div class="flex items-center gap-2 shrink-0">
        <button type="button" id="peek-open-full-btn" class="px-2.5 py-1 rounded-lg bg-emerald-500 text-slate-950 font-semibold text-xs">
          Open Full Reader ↗
        </button>
        <form method="dialog">
          <button type="submit" class="px-2.5 py-1 rounded-lg ui-card border text-xs ui-text-muted">Close (Esc)</button>
        </form>
      </div>
    </div>
    <div id="peek-body" class="p-6 overflow-y-auto max-h-[calc(88vh-56px)] md-body">
    </div>
  </dialog>

  <!-- ===================================================================== -->
  <!-- NATIVE DIALOG 3: LOG CUSTOM EXTERNAL PROBLEM                          -->
  <!-- ===================================================================== -->
  <dialog id="log-dialog" closedby="any" class="ui-card border rounded-2xl w-full max-w-md p-5 text-[var(--text)] shadow-2xl">
    <div class="flex items-center justify-between border-b ui-border pb-3 mb-4">
      <h2 class="text-base font-bold">Log Solved Problem</h2>
      <form method="dialog">
        <button type="submit" class="text-xs px-2 py-1 rounded ui-surface border ui-text-muted">Esc</button>
      </form>
    </div>
    <form id="custom-problem-form" class="space-y-3 text-xs">
      <div class="grid grid-cols-3 gap-2">
        <div>
          <label for="cp-num" class="block ui-text-muted mb-1">LC #</label>
          <input id="cp-num" type="number" required placeholder="42" class="w-full ui-surface border rounded-lg px-2.5 py-1.5">
        </div>
        <div class="col-span-2">
          <label for="cp-title" class="block ui-text-muted mb-1">Title</label>
          <input id="cp-title" type="text" required placeholder="Trapping Rain Water" class="w-full ui-surface border rounded-lg px-2.5 py-1.5">
        </div>
      </div>
      <div class="grid grid-cols-2 gap-2">
        <div>
          <label for="cp-diff" class="block ui-text-muted mb-1">Difficulty</label>
          <select id="cp-diff" class="w-full ui-surface border rounded-lg px-2.5 py-1.5">
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
          </select>
        </div>
        <div>
          <label for="cp-pattern" class="block ui-text-muted mb-1">Pattern</label>
          <input id="cp-pattern" type="text" required placeholder="Two Pointers" class="w-full ui-surface border rounded-lg px-2.5 py-1.5">
        </div>
      </div>
      <div>
        <label for="cp-note" class="block ui-text-muted mb-1">1-Line Takeaway</label>
        <textarea id="cp-note" rows="2" placeholder="Track left_max and right_max inward from the shorter wall." class="w-full ui-surface border rounded-lg px-2.5 py-1.5"></textarea>
      </div>
      <div class="flex justify-end gap-2 pt-2 border-t ui-border">
        <button type="button" onclick="document.getElementById('log-dialog').close()" class="px-3 py-1.5 rounded-lg ui-surface border">Cancel</button>
        <button type="submit" class="px-3.5 py-1.5 rounded-lg bg-emerald-500 text-slate-950 font-semibold">Save Problem</button>
      </div>
    </form>
  </dialog>

  <script>
    const DOCS_DATA = {docs_json_str};
    const DOC_KEYS = Object.keys(DOCS_DATA);
    const DEFAULT_INITIAL_VIEW = "{default_view}";

    const STATUS_STORAGE_KEY = 'dsa_hub_status_v2';
    const NOTES_STORAGE_KEY = 'dsa_hub_notes_v2';
    const CUSTOM_PROBS_KEY = 'dsa_hub_custom_probs_v2';
    const THEME_KEY = 'dsa_tracker_theme';

    let docStatusMap = {{}};
    let docNotesMap = {{}};
    let customProblems = [];
    let currentView = DEFAULT_INITIAL_VIEW;
    let currentDocPath = "dsa_patterns_study_guide.md";
    let readerMode = 'full';
    let showFlowcharts = true;
    let trackerStatusFilter = 'ALL';

    // 1. Initialize Storage & Migrate Old Tracker State
    function initState() {{
      try {{
        const savedStatus = localStorage.getItem(STATUS_STORAGE_KEY);
        if (savedStatus) {{
          docStatusMap = JSON.parse(savedStatus);
        }} else {{
          // Seed from default solved problems
          DOC_KEYS.forEach(k => {{
            if (DOCS_DATA[k].defaultSolved) docStatusMap[k] = 'solved';
          }});
          // Also migrate any old tracker entries from dsa_tracker_adhd_v17
          const legacy = localStorage.getItem('dsa_tracker_adhd_v17');
          if (legacy) {{
            const arr = JSON.parse(legacy);
            arr.forEach(item => {{
              if (item.file && DOCS_DATA[item.file]) {{
                docStatusMap[item.file] = 'solved';
                if (item.notes) docNotesMap[item.file] = item.notes;
              }}
            }});
          }}
          localStorage.setItem(STATUS_STORAGE_KEY, JSON.stringify(docStatusMap));
        }}

        const savedNotes = localStorage.getItem(NOTES_STORAGE_KEY);
        if (savedNotes) {{
          docNotesMap = {{ ...docNotesMap, ...JSON.parse(savedNotes) }};
        }}

        const savedCustom = localStorage.getItem(CUSTOM_PROBS_KEY);
        if (savedCustom) {{
          customProblems = JSON.parse(savedCustom);
        }}
      }} catch (e) {{
        console.warn(e);
      }}
    }}

    function getDocStatus(path) {{
      return docStatusMap[path] || 'todo';
    }}

    function setDocStatus(path, status) {{
      docStatusMap[path] = status;
      localStorage.setItem(STATUS_STORAGE_KEY, JSON.stringify(docStatusMap));
      updateGlobalProgressPill();
      renderSidebarTree();
      if (currentDocPath === path) updateReaderStatusButtons();
      if (currentView === 'tracker') renderTrackerTable();
      if (currentView === 'roadmap') renderRoadmapGrids();
    }}

    function updateGlobalProgressPill() {{
      const solvedCount = DOC_KEYS.filter(k => getDocStatus(k) === 'solved').length + customProblems.filter(p => p.status === 'solved').length;
      const pill = document.getElementById('global-progress-pill');
      if (pill) pill.textContent = `${{solvedCount}} / ${{DOC_KEYS.length}} Completed`;
    }}

    // 2. Theme Management (Charcoal, Matcha, Sepia) + Mermaid Theme Sync
    function setTheme(theme) {{
      document.body.className = `theme-${{theme}} min-h-screen flex flex-col selection:bg-emerald-500 selection:text-black antialiased`;
      localStorage.setItem(THEME_KEY, theme);

      ['charcoal', 'matcha', 'sepia'].forEach(t => {{
        const btn = document.getElementById(`btn-theme-${{t}}`);
        if (!btn) return;
        if (t === theme) {{
          btn.className = 'px-2 py-1 rounded font-medium transition-all bg-emerald-500/20 text-emerald-400';
        }} else {{
          btn.className = 'px-2 py-1 rounded font-medium transition-all opacity-60 hover:opacity-100';
        }}
      }});

      if (typeof mermaid !== 'undefined') {{
        mermaid.initialize({{
          startOnLoad: false,
          theme: theme === 'sepia' ? 'neutral' : 'dark',
          flowchart: {{ curve: 'basis', padding: 12 }},
          securityLevel: 'loose'
        }});
        if (currentView === 'reader' && currentDocPath) {{
          renderMermaidDiagrams(document.getElementById('rendered-content'));
        }}
      }}
    }}

    // 3. View Switching (Reader, Cheat Sheets, Tracker, Roadmap)
    function switchView(view) {{
      currentView = view;
      ['reader', 'cheatsheets', 'tracker', 'roadmap'].forEach(v => {{
        const sec = document.getElementById(`view-${{v}}`);
        const btn = document.getElementById(`nav-btn-${{v}}`);
        if (v === view) {{
          sec.classList.remove('hidden');
          btn.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 bg-emerald-500 text-slate-950 shadow-sm';
        }} else {{
          sec.classList.add('hidden');
          btn.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 ui-text-muted hover:opacity-100';
        }}
      }});

      const url = new URL(window.location);
      url.searchParams.set('view', view);
      window.history.replaceState({{}}, '', url);

      if (view === 'cheatsheets') renderCheatSheetsGrid();
      if (view === 'tracker') renderTrackerTable();
      if (view === 'roadmap') renderRoadmapGrids();
    }}

    function openDocInReader(docPath) {{
      switchView('reader');
      renderDoc(docPath);
    }}

    // 4. Markdown, Math (KaTeX), and Flowchart (Mermaid) Pipeline
    function renderMarkdownInto(containerEl, markdownText, basePath) {{
      if (typeof marked !== 'undefined') {{
        containerEl.innerHTML = marked.parse(markdownText, {{ breaks: true, gfm: true }});
      }} else {{
        containerEl.innerHTML = '<pre><code>' + markdownText + '</code></pre>';
      }}

      // Convert ```mermaid code blocks into <figure class="mermaid-figure">
      containerEl.querySelectorAll('pre code.language-mermaid').forEach((codeEl, idx) => {{
        const pre = codeEl.parentElement;
        const graphDef = codeEl.textContent;
        const fig = document.createElement('figure');
        fig.className = 'mermaid-figure my-4 ui-surface border rounded-xl p-4 overflow-x-auto';
        fig.innerHTML = `
          <figcaption class="flex items-center justify-between text-xs ui-text-muted mb-2 pb-1.5 border-b ui-border">
            <span class="font-semibold text-emerald-400 flex items-center gap-1.5">📊 Visual Flowchart</span>
            <span>Follow arrows top-to-bottom / left-to-right</span>
          </figcaption>
          <div class="mermaid-render flex justify-center py-1" data-graph="${{encodeURIComponent(graphDef)}}"></div>
        `;
        pre.replaceWith(fig);
      }});

      // Make all <pre> blocks keyboard focusable (modern-web-guidance) + add Copy button
      containerEl.querySelectorAll('pre').forEach(pre => {{
        pre.setAttribute('tabindex', '0');
        if (typeof hljs !== 'undefined') {{
          const code = pre.querySelector('code');
          if (code) hljs.highlightElement(code);
        }}
      }});

      // Render KaTeX math ($...$ and $$...$$)
      if (typeof renderMathInElement !== 'undefined') {{
        try {{
          renderMathInElement(containerEl, {{
            delimiters: [
              {{ left: '$$', right: '$$', display: true }},
              {{ left: '$', right: '$', display: false }},
              {{ left: '\\\\(', right: '\\\\)', display: false }},
              {{ left: '\\\\[', right: '\\\\]', display: true }}
            ],
            throwOnError: false
          }});
        }} catch (e) {{}}
      }}

      // Render Mermaid flowcharts
      renderMermaidDiagrams(containerEl);

      // Intercept internal .md links
      containerEl.querySelectorAll('a').forEach(anchor => {{
        const href = anchor.getAttribute('href');
        if (href && (href.endsWith('.md') || href.includes('.md#'))) {{
          anchor.addEventListener('click', (e) => {{
            e.preventDefault();
            const cleanHref = href.split('#')[0];
            let currentDir = basePath.includes('/') ? basePath.substring(0, basePath.lastIndexOf('/')) : '';
            let resolved = cleanHref.replace(/^(\\.\\/)/, '');
            if (cleanHref.startsWith('../')) {{
              resolved = cleanHref.replace(/^(\\.\\.\\/)+/, '');
            }} else if (currentDir && !cleanHref.startsWith('/')) {{
              resolved = currentDir + '/' + resolved;
            }}
            document.getElementById('peek-dialog').close();
            openDocInReader(resolved);
          }});
        }}
      }});
    }}

    async function renderMermaidDiagrams(containerEl) {{
      if (typeof mermaid === 'undefined' || !containerEl) return;
      const nodes = containerEl.querySelectorAll('.mermaid-render');
      for (let i = 0; i < nodes.length; i++) {{
        const el = nodes[i];
        const rawGraph = decodeURIComponent(el.dataset.graph || '');
        if (!rawGraph.trim()) continue;
        try {{
          const id = 'mmd-' + Date.now() + '-' + Math.random().toString(36).substring(2, 7);
          const {{ svg }} = await mermaid.render(id, rawGraph);
          el.innerHTML = svg;
        }} catch (err) {{
          el.innerHTML = `<pre class="text-xs p-2 rounded ui-card border"><code>${{rawGraph}}</code></pre>`;
        }}
      }}
    }}

    // 5. Render Active Document in Study Reader
    function resolveDocKey(docPath) {{
      if (!docPath) return "dsa_patterns_study_guide.md";
      const clean = docPath.replace(/^(\\.\\/|\\/)/, '');
      if (DOCS_DATA[clean]) return clean;
      const match = DOC_KEYS.find(k => k.endsWith(clean) || clean.endsWith(k));
      return match || "dsa_patterns_study_guide.md";
    }}

    function renderDoc(docPath) {{
      const targetKey = resolveDocKey(docPath);
      currentDocPath = targetKey;
      const doc = DOCS_DATA[targetKey];
      if (!doc) return;

      const url = new URL(window.location);
      url.searchParams.set('doc', targetKey);
      window.history.replaceState({{}}, '', url);

      document.title = `${{doc.title}} | DSA Study Hub`;
      document.getElementById('doc-cat-badge').textContent = `${{doc.categoryIcon}} ${{doc.categoryLabel}}`;

      const diffBadge = document.getElementById('doc-diff-badge');
      diffBadge.textContent = doc.difficulty;
      if (doc.difficulty === 'Easy') {{
        diffBadge.className = 'text-xs font-semibold px-2.5 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 border border-emerald-500/30';
      }} else if (doc.difficulty === 'Medium') {{
        diffBadge.className = 'text-xs font-semibold px-2.5 py-0.5 rounded-full bg-amber-500/15 text-amber-400 border border-amber-500/30';
      }} else if (doc.difficulty === 'Hard') {{
        diffBadge.className = 'text-xs font-semibold px-2.5 py-0.5 rounded-full bg-rose-500/15 text-rose-400 border border-rose-500/30';
      }} else {{
        diffBadge.className = 'text-xs font-semibold px-2.5 py-0.5 rounded-full bg-sky-500/15 text-sky-400 border border-sky-500/30';
      }}

      const lcLink = document.getElementById('doc-lc-link');
      if (doc.lcUrl) {{
        lcLink.href = doc.lcUrl;
        lcLink.classList.remove('hidden');
      }} else {{
        lcLink.classList.add('hidden');
      }}

      updateReaderStatusButtons();

      const contentEl = document.getElementById('rendered-content');
      renderMarkdownInto(contentEl, doc.content, targetKey);
      buildTableOfContents(contentEl);

      // Personal note
      const noteInput = document.getElementById('doc-personal-note');
      noteInput.value = docNotesMap[targetKey] || doc.summary || '';

      // Prev / Next buttons
      const idx = doc.index;
      const prevKey = idx > 0 ? DOC_KEYS[idx - 1] : DOC_KEYS[DOC_KEYS.length - 1];
      const nextKey = idx < DOC_KEYS.length - 1 ? DOC_KEYS[idx + 1] : DOC_KEYS[0];

      document.getElementById('prev-doc-title').textContent = DOCS_DATA[prevKey].title;
      document.getElementById('prev-doc-btn').onclick = () => renderDoc(prevKey);
      document.getElementById('next-doc-title').textContent = DOCS_DATA[nextKey].title;
      document.getElementById('next-doc-btn').onclick = () => renderDoc(nextKey);

      // Highlight active sidebar item
      document.querySelectorAll('.sidebar-doc-link').forEach(el => {{
        if (el.dataset.path === targetKey) {{
          el.className = 'sidebar-doc-link flex items-center justify-between gap-2 px-2.5 py-1.5 rounded-lg text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30';
        }} else {{
          el.className = 'sidebar-doc-link flex items-center justify-between gap-2 px-2.5 py-1.5 rounded-lg text-xs ui-text-muted hover:text-[var(--text)] hover:bg-[var(--surface-hover)] transition-colors';
        }}
      }});

      document.getElementById('reader-scroll-container').scrollTo(0, 0);
    }}

    function buildTableOfContents(contentEl) {{
      const tocList = document.getElementById('toc-list');
      tocList.innerHTML = '';
      const headings = contentEl.querySelectorAll('h2, h3');
      headings.forEach((h, i) => {{
        const id = 'sec-' + i;
        h.id = id;
        const a = document.createElement('a');
        a.href = '#' + id;
        a.textContent = h.textContent;
        a.className = h.tagName === 'H3'
          ? 'block pl-3 py-1 ui-text-muted hover:text-emerald-400 truncate transition-colors'
          : 'block py-1 font-medium ui-text-muted hover:text-emerald-400 truncate transition-colors';
        a.addEventListener('click', (e) => {{
          e.preventDefault();
          h.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
        }});
        tocList.appendChild(a);
      }});
    }}

    function setReaderMode(mode) {{
      readerMode = mode;
      const contentEl = document.getElementById('rendered-content');
      const btnFull = document.getElementById('mode-btn-full');
      const btnVis = document.getElementById('mode-btn-visual');

      if (mode === 'visual') {{
        contentEl.classList.add('visual-focus-mode');
        btnVis.className = 'px-2.5 py-1 rounded font-medium bg-emerald-500/20 text-emerald-400';
        btnFull.className = 'px-2.5 py-1 rounded font-medium ui-text-muted';
      }} else {{
        contentEl.classList.remove('visual-focus-mode');
        btnFull.className = 'px-2.5 py-1 rounded font-medium bg-emerald-500/20 text-emerald-400';
        btnVis.className = 'px-2.5 py-1 rounded font-medium ui-text-muted';
      }}
    }}

    function toggleFlowcharts() {{
      showFlowcharts = !showFlowcharts;
      const contentEl = document.getElementById('rendered-content');
      const btn = document.getElementById('btn-toggle-flowcharts');
      if (showFlowcharts) {{
        contentEl.classList.remove('hide-flowcharts-mode');
        btn.textContent = '📊 Flowcharts: ON';
        btn.className = 'px-2.5 py-1 rounded-lg border ui-surface text-xs font-medium text-emerald-400';
      }} else {{
        contentEl.classList.add('hide-flowcharts-mode');
        btn.textContent = '📊 Flowcharts: OFF';
        btn.className = 'px-2.5 py-1 rounded-lg border ui-surface text-xs font-medium ui-text-muted';
      }}
    }}

    function updateReaderStatusButtons() {{
      const st = getDocStatus(currentDocPath);
      const map = {{
        todo: document.getElementById('status-btn-todo'),
        review: document.getElementById('status-btn-review'),
        solved: document.getElementById('status-btn-solved')
      }};
      Object.keys(map).forEach(k => {{
        if (k === st) {{
          const activeColor = k === 'solved' ? 'bg-emerald-500/20 text-emerald-400' : (k === 'review' ? 'bg-amber-500/20 text-amber-400' : 'ui-card text-[var(--text)]');
          map[k].className = `px-2 py-1 rounded font-semibold ${{activeColor}}`;
        }} else {{
          map[k].className = 'px-2 py-1 rounded font-medium ui-text-muted hover:opacity-100';
        }}
      }});
    }}

    function setCurrentDocStatus(status) {{
      setDocStatus(currentDocPath, status);
    }}

    // 6. Sidebar Tree Construction (Grouped & Naturally Sorted)
    function renderSidebarTree() {{
      const container = document.getElementById('sidebar-tree');
      const q = (document.getElementById('sidebar-filter-input')?.value || '').toLowerCase().trim();
      container.innerHTML = '';

      const groups = {{}};
      DOC_KEYS.forEach(path => {{
        const d = DOCS_DATA[path];
        if (q && !d.title.toLowerCase().includes(q) && !d.pattern.toLowerCase().includes(q) && !path.toLowerCase().includes(q)) {{
          return;
        }}
        if (!groups[d.category]) groups[d.category] = [];
        groups[d.category].push(d);
      }});

      Object.keys(groups).forEach(cat => {{
        const items = groups[cat];
        const first = items[0];
        const solvedInCat = items.filter(i => getDocStatus(i.path) === 'solved').length;

        const details = document.createElement('details');
        details.open = true;
        details.className = 'group';

        const summary = document.createElement('summary');
        summary.className = 'flex items-center justify-between px-2 py-1.5 rounded-lg text-xs font-bold uppercase tracking-wider ui-text-muted hover:text-[var(--text)] cursor-pointer select-none';
        summary.innerHTML = `
          <span>${{first.categoryIcon}} ${{first.categoryLabel}}</span>
          <span class="font-mono text-xs px-1.5 py-0.5 rounded ui-card border">${{solvedInCat}}/${{items.length}}</span>
        `;
        details.appendChild(summary);

        const listDiv = document.createElement('div');
        listDiv.className = 'mt-1 space-y-0.5 pl-1';

        items.forEach(item => {{
          const a = document.createElement('a');
          a.href = `?doc=${{encodeURIComponent(item.path)}}`;
          a.dataset.path = item.path;
          const isCurrent = item.path === currentDocPath;
          a.className = isCurrent
            ? 'sidebar-doc-link flex items-center justify-between gap-2 px-2.5 py-1.5 rounded-lg text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
            : 'sidebar-doc-link flex items-center justify-between gap-2 px-2.5 py-1.5 rounded-lg text-xs ui-text-muted hover:text-[var(--text)] hover:bg-[var(--surface-hover)] transition-colors';

          const st = getDocStatus(item.path);
          const statusIcon = st === 'solved'
            ? '<span class="text-emerald-400 font-bold shrink-0">✓</span>'
            : (st === 'review' ? '<span class="text-amber-400 shrink-0">🔁</span>' : '');

          const shortLabel = item.lcNumber
            ? `<span class="truncate"><span class="font-mono opacity-60 mr-1">#${{item.lcNumber}}</span>${{item.title.replace(/^LeetCode\\s+\\d+:\\s*/i, '')}}</span>`
            : `<span class="truncate">${{item.title}}</span>`;

          a.innerHTML = `${{shortLabel}}${{statusIcon}}`;
          a.addEventListener('click', (e) => {{
            e.preventDefault();
            renderDoc(item.path);
          }});
          listDiv.appendChild(a);
        }});

        details.appendChild(listDiv);
        container.appendChild(details);
      }});
    }}

    // 7. Cheat Sheets Deck View
    function renderCheatSheetsGrid() {{
      const grid = document.getElementById('cheatsheets-grid');
      const q = (document.getElementById('cs-search-input')?.value || '').toLowerCase().trim();
      const sheets = DOC_KEYS.map(k => DOCS_DATA[k]).filter(d => d.category === 'cheat_sheets' || d.category === 'Root');

      const filtered = sheets.filter(d => !q || d.title.toLowerCase().includes(q) || d.summary.toLowerCase().includes(q));
      grid.innerHTML = filtered.map(d => `
        <div class="ui-card border rounded-2xl p-4 flex flex-col justify-between gap-3 hover:border-emerald-500/50 transition-all">
          <div class="space-y-2">
            <div class="flex items-center justify-between gap-2">
              <span class="text-xs font-mono px-2 py-0.5 rounded ui-surface border text-emerald-400">${{d.categoryIcon}} ${{d.categoryLabel}}</span>
              ${{d.hasMermaid ? '<span class="text-xs px-2 py-0.5 rounded bg-sky-500/15 text-sky-400 border border-sky-500/30">📊 Flowchart</span>' : ''}}
            </div>
            <h2 class="text-base font-bold">${{d.title}}</h2>
            <p class="text-xs ui-text-muted leading-relaxed">${{d.summary || 'Complete pattern triggers, visual arrows, and Python templates.'}}</p>
          </div>
          <div class="pt-3 border-t ui-border flex items-center justify-between">
            <button type="button" onclick="openPeekDialog('${{d.path}}')" class="text-xs ui-text-muted hover:text-[var(--text)]">Quick Peek</button>
            <button type="button" onclick="openDocInReader('${{d.path}}')" class="px-3 py-1.5 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-semibold hover:bg-emerald-500 hover:text-slate-950 transition-all">
              Open Sheet →
            </button>
          </div>
        </div>
      `).join('');
    }}

    // 8. Unified Tracker Table View
    function setTrackerStatusFilter(st) {{
      trackerStatusFilter = st;
      document.querySelectorAll('.tracker-status-btn').forEach(btn => {{
        if (btn.dataset.status === st) {{
          btn.className = 'tracker-status-btn px-2.5 py-1 rounded font-medium bg-emerald-500/20 text-emerald-400';
        }} else {{
          btn.className = 'tracker-status-btn px-2.5 py-1 rounded font-medium ui-text-muted';
        }}
      }});
      renderTrackerTable();
    }}

    function cycleDocStatus(path) {{
      const cur = getDocStatus(path);
      const next = cur === 'todo' ? 'solved' : (cur === 'solved' ? 'review' : 'todo');
      setDocStatus(path, next);
    }}

    function renderTrackerTable() {{
      const tbody = document.getElementById('tracker-tbody');
      const q = (document.getElementById('tracker-search-input')?.value || '').toLowerCase().trim();
      const catFilter = document.getElementById('tracker-cat-filter')?.value || 'ALL';

      // Update top metrics
      const allDocs = DOC_KEYS.map(k => DOCS_DATA[k]);
      const solvedDocs = allDocs.filter(d => getDocStatus(d.path) === 'solved');
      const reviewDocs = allDocs.filter(d => getDocStatus(d.path) === 'review');
      const easySolved = solvedDocs.filter(d => d.difficulty === 'Easy').length;
      const medHardSolved = solvedDocs.filter(d => d.difficulty === 'Medium' || d.difficulty === 'Hard').length;

      document.getElementById('stat-solved').textContent = solvedDocs.length + customProblems.length;
      document.getElementById('stat-review').textContent = reviewDocs.length;
      document.getElementById('stat-easy').textContent = easySolved;
      document.getElementById('stat-medium').textContent = medHardSolved;

      const rows = allDocs.filter(d => {{
        if (catFilter !== 'ALL' && d.category !== catFilter) return false;
        const st = getDocStatus(d.path);
        if (trackerStatusFilter !== 'ALL' && st !== trackerStatusFilter) return false;
        if (q) {{
          const note = (docNotesMap[d.path] || d.summary || '').toLowerCase();
          return d.title.toLowerCase().includes(q) ||
                 d.pattern.toLowerCase().includes(q) ||
                 (d.lcNumber && d.lcNumber.toString().includes(q)) ||
                 note.includes(q);
        }}
        return true;
      }});

      tbody.innerHTML = rows.map(d => {{
        const st = getDocStatus(d.path);
        const stBadge = st === 'solved'
          ? '<span class="px-2.5 py-1 rounded-lg font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">✓ Solved</span>'
          : (st === 'review'
            ? '<span class="px-2.5 py-1 rounded-lg font-semibold bg-amber-500/20 text-amber-400 border border-amber-500/30">🔁 Review</span>'
            : '<span class="px-2.5 py-1 rounded-lg font-medium ui-surface border ui-text-muted">○ Todo</span>');

        const diffColor = d.difficulty === 'Easy' ? 'text-emerald-400' : (d.difficulty === 'Medium' ? 'text-amber-400' : (d.difficulty === 'Hard' ? 'text-rose-400' : 'text-sky-400'));
        const noteText = docNotesMap[d.path] || d.summary || '-';

        return `
          <tr class="hover:bg-[var(--surface-hover)] transition-colors">
            <td class="py-3 px-3 whitespace-nowrap">
              <button type="button" onclick="cycleDocStatus('${{d.path}}')" title="Click to cycle Todo -> Solved -> Review">
                ${{stBadge}}
              </button>
            </td>
            <td class="py-3 px-3">
              <div class="font-semibold text-sm flex items-center gap-2">
                ${{d.lcNumber ? `<span class="font-mono text-xs px-1.5 py-0.5 rounded ui-surface border ui-text-muted">#${{d.lcNumber}}</span>` : ''}}
                <button type="button" onclick="openPeekDialog('${{d.path}}')" class="text-left hover:text-emerald-400 transition-colors">
                  ${{d.title.replace(/^LeetCode\\s+\\d+:\\s*/i, '')}}
                </button>
              </div>
              <div class="text-xs ${{diffColor}} mt-0.5">${{d.difficulty}} ${{d.hasMermaid ? '• 📊 Flowchart' : ''}}</div>
            </td>
            <td class="py-3 px-3 hidden sm:table-cell">
              <span class="px-2 py-0.5 rounded ui-surface border text-xs">${{d.pattern}}</span>
              <div class="text-xs ui-text-muted mt-0.5">${{d.categoryLabel}}</div>
            </td>
            <td class="py-3 px-3 hidden lg:table-cell max-w-md">
              <p class="text-xs ui-text-muted line-clamp-2">${{noteText}}</p>
            </td>
            <td class="py-3 px-3 text-right whitespace-nowrap space-x-1.5">
              <button type="button" onclick="openPeekDialog('${{d.path}}')" class="px-2.5 py-1 rounded-lg ui-surface border text-xs hover:border-emerald-500/50">
                Peek
              </button>
              <button type="button" onclick="openDocInReader('${{d.path}}')" class="px-2.5 py-1 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-semibold hover:bg-emerald-500 hover:text-slate-950">
                Study →
              </button>
            </td>
          </tr>
        `;
      }}).join('');
    }}

    // 9. Quick-Peek Modal Drawer (<dialog>)
    function openPeekDialog(docPath) {{
      const key = resolveDocKey(docPath);
      const doc = DOCS_DATA[key];
      if (!doc) return;
      const dialog = document.getElementById('peek-dialog');
      document.getElementById('peek-title').textContent = doc.title;
      document.getElementById('peek-open-full-btn').onclick = () => {{
        dialog.close();
        openDocInReader(key);
      }};
      const bodyEl = document.getElementById('peek-body');
      dialog.showModal();
      renderMarkdownInto(bodyEl, doc.content, key);
    }}

    // 10. 12-Week Roadmap View + hidden="until-found" support (modern-web-guidance)
    function selectRoadmapPhase(panelId) {{
      document.querySelectorAll('.rm-panel').forEach(panel => {{
        if (panel.id === panelId) {{
          panel.removeAttribute('hidden');
        }} else {{
          panel.setAttribute('hidden', 'until-found');
        }}
      }});
      document.querySelectorAll('.rm-tab-btn').forEach(btn => {{
        const isMatch = btn.getAttribute('aria-controls') === panelId;
        btn.setAttribute('aria-expanded', isMatch ? 'true' : 'false');
        btn.className = isMatch
          ? 'rm-tab-btn px-3.5 py-2 rounded-xl text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 whitespace-nowrap'
          : 'rm-tab-btn px-3.5 py-2 rounded-xl text-xs font-semibold ui-card border ui-text-muted whitespace-nowrap';
      }});
    }}

    function renderRoadmapGrids() {{
      const phaseMapping = {{
        'rm-phase-1-grid': ['00_foundations', '01_arrays_and_pointers'],
        'rm-phase-2-grid': ['02_linked_lists', '03_stacks_and_queues', '04_sorting', '05_binary_search'],
        'rm-phase-3-grid': ['cheat_sheets'],
        'rm-phase-4-grid': ['system_design']
      }};

      Object.keys(phaseMapping).forEach(gridId => {{
        const gridEl = document.getElementById(gridId);
        if (!gridEl) return;
        const cats = phaseMapping[gridId];
        const items = DOC_KEYS.map(k => DOCS_DATA[k]).filter(d => cats.includes(d.category));
        gridEl.innerHTML = items.map(d => {{
          const st = getDocStatus(d.path);
          const isSolved = st === 'solved';
          return `
            <div class="ui-card border rounded-xl p-3 flex items-center justify-between gap-2 ${{isSolved ? 'border-emerald-500/30' : ''}}">
              <div class="truncate">
                <button type="button" onclick="openDocInReader('${{d.path}}')" class="text-xs font-semibold hover:text-emerald-400 truncate block text-left">
                  ${{d.title}}
                </button>
                <span class="text-xs ui-text-muted">${{d.categoryLabel}} • ${{d.difficulty}}</span>
              </div>
              <button type="button" onclick="cycleDocStatus('${{d.path}}')" class="shrink-0 text-xs px-2 py-1 rounded border ${{isSolved ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' : 'ui-surface ui-text-muted'}}">
                ${{isSolved ? '✓ Done' : '○ Todo'}}
              </button>
            </div>
          `;
        }}).join('');
      }});
    }}

    // 11. Command Palette Search (Cmd+K / /)
    const cmdkDialog = document.getElementById('cmdk-dialog');
    const cmdkInput = document.getElementById('cmdk-input');
    const cmdkResults = document.getElementById('cmdk-results');

    function openCmdK() {{
      cmdkDialog.showModal();
      cmdkInput.value = '';
      renderCmdKResults('');
      cmdkInput.focus();
    }}

    function renderCmdKResults(query) {{
      const q = query.toLowerCase().trim();
      const matches = DOC_KEYS.map(k => DOCS_DATA[k]).filter(d => {{
        if (!q) return true;
        return d.title.toLowerCase().includes(q) ||
               d.pattern.toLowerCase().includes(q) ||
               d.categoryLabel.toLowerCase().includes(q) ||
               d.content.toLowerCase().includes(q);
      }}).slice(0, 25);

      cmdkResults.innerHTML = matches.map(d => `
        <button type="button" onclick="cmdkDialog.close(); openDocInReader('${{d.path}}')" class="w-full text-left px-3 py-2 rounded-xl hover:bg-[var(--surface-hover)] flex items-center justify-between gap-3 transition-colors">
          <div class="truncate">
            <div class="text-xs font-semibold">${{d.title}}</div>
            <div class="text-xs ui-text-muted truncate">${{d.categoryLabel}} • ${{d.pattern}}</div>
          </div>
          <span class="text-xs font-mono px-2 py-0.5 rounded ui-surface border shrink-0">${{d.difficulty}}</span>
        </button>
      `).join('');
    }}

    document.getElementById('open-cmdk-btn').addEventListener('click', openCmdK);
    cmdkInput.addEventListener('input', (e) => renderCmdKResults(e.target.value));

    // Global Keyboard Shortcuts
    window.addEventListener('keydown', (e) => {{
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {{
        e.preventDefault();
        openCmdK();
      }} else if (e.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName)) {{
        e.preventDefault();
        openCmdK();
      }} else if (currentView === 'reader' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName)) {{
        if (e.key === '[') document.getElementById('prev-doc-btn').click();
        if (e.key === ']') document.getElementById('next-doc-btn').click();
        if (e.key === 'v') setReaderMode(readerMode === 'full' ? 'visual' : 'full');
      }}
    }});

    // Personal Note Auto-Save
    document.getElementById('doc-personal-note').addEventListener('input', (e) => {{
      docNotesMap[currentDocPath] = e.target.value;
      localStorage.setItem(NOTES_STORAGE_KEY, JSON.stringify(docNotesMap));
      const ind = document.getElementById('note-saved-indicator');
      ind.textContent = 'Saved ✓';
      setTimeout(() => {{ ind.textContent = 'Auto-saves locally'; }}, 1200);
    }});

    // Sidebar filter & collapse toggle
    document.getElementById('sidebar-filter-input').addEventListener('input', renderSidebarTree);
    document.getElementById('toggle-all-cats-btn').addEventListener('click', (e) => {{
      const detailsList = document.querySelectorAll('#sidebar-tree details');
      const anyOpen = Array.from(detailsList).some(d => d.open);
      detailsList.forEach(d => {{ d.open = !anyOpen; }});
      e.target.textContent = anyOpen ? 'Expand all' : 'Collapse all';
    }});

    // Mobile sidebar toggle
    document.getElementById('mobile-sidebar-btn').addEventListener('click', () => {{
      const sb = document.getElementById('reader-sidebar');
      sb.classList.toggle('hidden');
      sb.classList.toggle('fixed');
      sb.classList.toggle('z-40');
    }});

    // Cheat sheets & Tracker filters
    document.getElementById('cs-search-input').addEventListener('input', renderCheatSheetsGrid);
    document.getElementById('tracker-search-input').addEventListener('input', renderTrackerTable);
    document.getElementById('tracker-cat-filter').addEventListener('change', renderTrackerTable);

    // Custom problem modal
    document.getElementById('open-log-dialog-btn').addEventListener('click', () => {{
      document.getElementById('log-dialog').showModal();
    }});
    document.getElementById('custom-problem-form').addEventListener('submit', (e) => {{
      e.preventDefault();
      customProblems.unshift({{
        id: 'cp-' + Date.now(),
        number: parseInt(document.getElementById('cp-num').value, 10),
        title: document.getElementById('cp-title').value.trim(),
        difficulty: document.getElementById('cp-diff').value,
        pattern: document.getElementById('cp-pattern').value.trim(),
        notes: document.getElementById('cp-note').value.trim(),
        status: 'solved'
      }});
      localStorage.setItem(CUSTOM_PROBS_KEY, JSON.stringify(customProblems));
      document.getElementById('custom-problem-form').reset();
      document.getElementById('log-dialog').close();
      updateGlobalProgressPill();
      renderTrackerTable();
    }});

    // hidden="until-found" beforematch synchronization & fallback (modern-web-guidance)
    const rmAccordion = document.getElementById('roadmap-accordion');
    if (rmAccordion) {{
      rmAccordion.addEventListener('beforematch', (e) => {{
        const matchedPanel = e.target.closest('.rm-panel');
        if (matchedPanel) selectRoadmapPhase(matchedPanel.id);
      }});
    }}
    if (!('onbeforematch' in HTMLElement.prototype)) {{
      document.querySelectorAll('[hidden="until-found"]').forEach((el) => {{
        el.removeAttribute('hidden');
      }});
    }}

    // Boot Application
    initState();
    const savedTheme = localStorage.getItem(THEME_KEY) || 'charcoal';
    setTheme(savedTheme);
    updateGlobalProgressPill();
    renderSidebarTree();

    const params = new URLSearchParams(window.location.search);
    const paramDoc = params.get('doc');
    const paramView = params.get('view');

    if (paramDoc) {{
      switchView('reader');
      renderDoc(paramDoc);
    }} else if (paramView && ['reader', 'cheatsheets', 'tracker', 'roadmap'].includes(paramView)) {{
      renderDoc(currentDocPath);
      switchView(paramView);
    }} else {{
      renderDoc(currentDocPath);
      switchView(DEFAULT_INITIAL_VIEW);
    }}
  </script>
</body>
</html>
"""


for filename, default_view in [
    ("viewer.html", "reader"),
    ("tracker.html", "tracker"),
    ("faang_plan.html", "roadmap"),
]:
    out_path = os.path.join(ROOT_DIR, filename)
    with open(out_path, "w", encoding="utf-8") as fp:
        fp.write(build_html(default_view))
    print(f"Generated {out_path} (default_view={default_view})")
