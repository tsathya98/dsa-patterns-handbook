#!/usr/bin/env python3
"""
Generate the unified DSA Study Hub & Tracker web application:
- Separates Concept/Theory Notes from LeetCode Problem Walkthroughs & Cheat Sheets.
- Collapsible Left Sidebar (Topics) and Right Sidebar (On This Page) with keyboard shortcuts.
- Dedicated Pomodoro Focus Tracker Tab + persistent live mini-timer in the top bar +
  soothing Web Audio API harmonic chime when the timer completes.
- 4 modern developer palettes: Linear Indigo, Tokyo Night, Catppuccin Mocha, Daylight Clean.
"""

import os
import json
import re

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

CATEGORY_META = {
    "Root": {"label": "Overview & Plans", "order": 0, "icon": "🧭"},
    "00_foundations": {"label": "00. Foundations", "order": 1, "icon": "🧱"},
    "01_arrays_and_pointers": {"label": "01. Arrays & Pointers", "order": 2, "icon": "🎯"},
    "02_linked_lists": {"label": "02. Linked Lists", "order": 3, "icon": "🔗"},
    "03_stacks_and_queues": {"label": "03. Stacks & Queues", "order": 4, "icon": "🥞"},
    "04_sorting": {"label": "04. Sorting", "order": 5, "icon": "📊"},
    "05_binary_search": {"label": "05. Binary Search", "order": 6, "icon": "🔍"},
    "system_design": {"label": "System Design", "order": 7, "icon": "🏗️"},
    "cheat_sheets": {"label": "Cheat Sheets", "order": 8, "icon": "⚡"},
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

    m_title = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = m_title.group(1).strip() if m_title else filename

    m_num = re.match(r"^(\d+)_", filename)
    prefix_num = int(m_num.group(1)) if m_num else 9999

    m_lc_title = re.search(r"LeetCode\s+(\d+)", title, re.IGNORECASE)
    lc_number = int(m_lc_title.group(1)) if m_lc_title else None
    if lc_number is None and cat_raw in ("01_arrays_and_pointers", "02_linked_lists", "03_stacks_and_queues"):
        if prefix_num > 0 and not filename.startswith("00_") and not filename.startswith("01_linked_list_fundamentals"):
            lc_number = prefix_num

    short_title = re.sub(r"^(?:LeetCode\s+\d+\s*[:\-–]\s*|\d+\.\s*)", "", title, flags=re.IGNORECASE).strip()

    m_diff = re.search(r"\*\*Difficulty:\*\*\s*(Easy|Medium|Hard)", content, re.IGNORECASE)
    if m_diff:
        difficulty = m_diff.group(1).capitalize()
    elif cat_raw == "cheat_sheets":
        difficulty = "Cheat Sheet"
    elif lc_number is not None:
        difficulty = "Easy"
    else:
        difficulty = "Concept"

    m_pat = re.search(r"\*\*Pattern:\*\*\s*([^\n|]+)", content)
    pattern = m_pat.group(1).strip() if m_pat else cat_info["label"]

    m_url = re.search(r"\((https://leetcode\.com/problems/[^)]+)\)", content)
    lc_url = m_url.group(1).strip() if m_url else ""

    summary = ""
    for line in content.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith(">") or s.startswith("```") or s.startswith("|") or s.startswith("---") or s.startswith("<"):
            continue
        clean_s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
        clean_s = clean_s.replace("**", "").replace("`", "")
        if len(clean_s) > 20:
            summary = clean_s[:160] + ("..." if len(clean_s) > 160 else "")
            break

    if cat_raw == "cheat_sheets":
        doc_type = "cheat_sheet"
        sort_key = (2, prefix_num, short_title.lower())
    elif lc_number is not None:
        doc_type = "problem"
        sort_key = (1, lc_number, short_title.lower())
    else:
        doc_type = "concept"
        sort_key = (0, prefix_num, short_title.lower())

    return {
        "path": rel_path,
        "title": title,
        "shortTitle": short_title,
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


def build_html(default_view: str = "concepts") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DSA Visual Study Hub & Focus Tracker</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <link rel="stylesheet" href="static/vendor/katex.min.css">
  <script src="static/vendor/marked.min.js"></script>
  <script src="static/vendor/highlight.min.js"></script>
  <script src="static/vendor/katex.min.js"></script>
  <script src="static/vendor/auto-render.min.js"></script>
  <script src="static/vendor/mermaid.min.js"></script>
  <style>
    {hl_css}

    /* 1. LINEAR INDIGO (Default: Sleek Slate + Electric Indigo & Sky Blue) */
    body.theme-indigo {{
      --bg: #0b0d13;
      --surface: #111520;
      --surface-card: #161b28;
      --surface-hover: #1e2536;
      --border: #262f45;
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --accent: #6366f1;
      --accent-text: #818cf8;
      --accent-fg: #ffffff;
      --accent-soft: rgba(99, 102, 241, 0.14);
      --accent-border: rgba(99, 102, 241, 0.38);
      --code-bg: #080a0f;
      --code-inline-bg: #1e2538;
      --code-inline-text: #a5b4fc;
      --heading-h1: #f8fafc;
      --heading-h2: #38bdf8;
    }}

    /* 2. TOKYO NIGHT (Deep Neon Blue-Black + Cyan & Lavender) */
    body.theme-tokyo {{
      --bg: #16161e;
      --surface: #1a1b26;
      --surface-card: #212434;
      --surface-hover: #292e42;
      --border: #333952;
      --text: #c0caf5;
      --text-muted: #7aa2f7;
      --accent: #7dcfff;
      --accent-text: #7dcfff;
      --accent-fg: #0f111a;
      --accent-soft: rgba(125, 207, 255, 0.14);
      --accent-border: rgba(125, 207, 255, 0.38);
      --code-bg: #111219;
      --code-inline-bg: #282c40;
      --code-inline-text: #bb9af7;
      --heading-h1: #7dcfff;
      --heading-h2: #bb9af7;
    }}

    /* 3. CATPPUCCIN MOCHA (Cozy Pastel Mauve & Sapphire Dark) */
    body.theme-mocha {{
      --bg: #181825;
      --surface: #1e1e2e;
      --surface-card: #252538;
      --surface-hover: #313244;
      --border: #3b3d54;
      --text: #cdd6f4;
      --text-muted: #a6adc8;
      --accent: #cba6f7;
      --accent-text: #cba6f7;
      --accent-fg: #11111b;
      --accent-soft: rgba(203, 166, 247, 0.15);
      --accent-border: rgba(203, 166, 247, 0.4);
      --code-bg: #11111b;
      --code-inline-bg: #2b2c40;
      --code-inline-text: #f5c2e7;
      --heading-h1: #cba6f7;
      --heading-h2: #89b4fa;
    }}

    /* 4. DAYLIGHT CLEAN (Stripe / Linear Crisp Light Mode) */
    body.theme-daylight {{
      --bg: #f8fafc;
      --surface: #f1f5f9;
      --surface-card: #ffffff;
      --surface-hover: #e2e8f0;
      --border: #cbd5e1;
      --text: #0f172a;
      --text-muted: #475569;
      --accent: #4f46e5;
      --accent-text: #4f46e5;
      --accent-fg: #ffffff;
      --accent-soft: rgba(79, 70, 229, 0.1);
      --accent-border: rgba(79, 70, 229, 0.3);
      --code-bg: #0f172a;
      --code-inline-bg: #eef2ff;
      --code-inline-text: #4338ca;
      --heading-h1: #0f172a;
      --heading-h2: #2563eb;
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

    .ui-accent-btn {{
      background-color: var(--accent);
      color: var(--accent-fg);
    }}
    .ui-accent-soft {{
      background-color: var(--accent-soft);
      color: var(--accent-text);
      border-color: var(--accent-border);
    }}
    .ui-accent-text {{
      color: var(--accent-text);
    }}

    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 9999px; }}

    /* Markdown Reader Typography */
    .md-body {{
      color: var(--text);
      line-height: 1.75;
      font-size: 0.95rem;
    }}
    .md-body h1 {{
      font-size: 1.7rem;
      font-weight: 800;
      color: var(--heading-h1);
      margin-top: 0.25rem;
      margin-bottom: 1rem;
      padding-bottom: 0.6rem;
      border-bottom: 1px solid var(--border);
      letter-spacing: -0.02em;
    }}
    .md-body h2 {{
      font-size: 1.22rem;
      font-weight: 700;
      color: var(--heading-h2);
      margin-top: 1.85rem;
      margin-bottom: 0.65rem;
      padding-bottom: 0.35rem;
      border-bottom: 1px solid var(--border);
      scroll-margin-top: 5rem;
    }}
    .md-body h3 {{
      font-size: 1.05rem;
      font-weight: 600;
      color: var(--text);
      margin-top: 1.3rem;
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
    .md-body li {{ margin-bottom: 0.35rem; }}
    .md-body blockquote {{
      border-left: 3px solid var(--accent);
      background: var(--accent-soft);
      padding: 0.65rem 1rem;
      border-radius: 0 0.6rem 0.6rem 0;
      margin-bottom: 1.1rem;
      font-size: 0.875rem;
    }}
    .md-body blockquote p {{ margin-bottom: 0.2rem; }}
    .md-body pre {{
      background: var(--code-bg) !important;
      color: #e2e8f0;
      border: 1px solid var(--border);
      border-radius: 0.75rem;
      padding: 0.95rem 1.1rem;
      overflow-x: auto;
      margin-bottom: 1.1rem;
      font-size: 0.84rem;
      line-height: 1.55;
    }}
    .md-body code {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.84em;
    }}
    .md-body :not(pre) > code {{
      background: var(--code-inline-bg);
      border: 1px solid var(--border);
      padding: 0.14rem 0.4rem;
      border-radius: 0.35rem;
      color: var(--code-inline-text);
      font-weight: 500;
    }}
    .md-body table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 1.25rem;
      font-size: 0.85rem;
      border: 1px solid var(--border);
      border-radius: 0.5rem;
      overflow: hidden;
    }}
    .md-body th {{
      background: var(--surface);
      font-weight: 600;
      text-align: left;
      padding: 0.6rem 0.8rem;
      border-bottom: 1px solid var(--border);
    }}
    .md-body td {{
      padding: 0.55rem 0.8rem;
      border-bottom: 1px solid var(--border);
    }}
    .md-body a {{
      color: var(--accent-text);
      text-decoration: underline;
      text-underline-offset: 3px;
    }}
    .md-body details {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 0.75rem;
      padding: 0.7rem 1rem;
      margin-bottom: 1rem;
    }}
    .md-body summary {{
      cursor: pointer;
      font-weight: 600;
      color: var(--accent-text);
      user-select: none;
    }}
    .md-body details[open] summary {{
      margin-bottom: 0.75rem;
      padding-bottom: 0.45rem;
      border-bottom: 1px solid var(--border);
    }}

    .md-body.visual-focus-mode > p,
    .md-body.visual-focus-mode > ul,
    .md-body.visual-focus-mode > ol {{
      display: none;
    }}
    .md-body.hide-flowcharts-mode .mermaid-figure {{
      display: none;
    }}

    dialog::backdrop {{
      background: rgba(8, 10, 18, 0.75);
      backdrop-filter: blur(4px);
    }}
  </style>
</head>
<body class="theme-indigo min-h-screen flex flex-col antialiased">

  <!-- 1. UNIFIED TOP NAVIGATION BAR -->
  <header class="sticky top-0 z-30 ui-surface border-b px-3 sm:px-5 py-2.5 flex items-center justify-between gap-2">
    <div class="flex items-center gap-2">
      <!-- Left Sidebar Collapse Button (Always visible when in Reader) -->
      <button type="button" id="toggle-left-sidebar-btn" onclick="toggleLeftSidebar()" class="p-1.5 rounded-lg ui-card border ui-text-muted hover:text-[var(--text)] transition-colors" title="Toggle Left Topic Sidebar (Shortcut: b)">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h10M4 18h16"/></svg>
      </button>

      <div class="flex items-center gap-2">
        <span class="text-base font-extrabold tracking-tight ui-accent-text whitespace-nowrap">DSA Hub</span>
        <span id="global-progress-pill" class="hidden xl:inline-flex items-center gap-1 text-xs font-mono px-2.5 py-0.5 rounded-full ui-card border ui-text-muted" title="LeetCode Problems Solved">
          0 Solved
        </span>
      </div>
    </div>

    <!-- 6 Primary Views: Concepts | LeetCode Guides | Cheat Sheets | Tracker | Pomodoro | 12-Wk Plan -->
    <nav class="flex items-center gap-1 ui-card p-1 rounded-xl border overflow-x-auto" aria-label="Primary sections">
      <button type="button" onclick="switchView('concepts')" id="nav-btn-concepts" class="px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 whitespace-nowrap">
        <span aria-hidden="true">📘</span> Concepts
      </button>
      <button type="button" onclick="switchView('problems')" id="nav-btn-problems" class="px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 whitespace-nowrap">
        <span aria-hidden="true">🧩</span> LeetCode Guides
      </button>
      <button type="button" onclick="switchView('cheatsheets')" id="nav-btn-cheatsheets" class="px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 whitespace-nowrap">
        <span aria-hidden="true">⚡</span> Cheat Sheets
      </button>
      <button type="button" onclick="switchView('tracker')" id="nav-btn-tracker" class="px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 whitespace-nowrap">
        <span aria-hidden="true">✅</span> Tracker
      </button>
      <button type="button" onclick="switchView('pomodoro')" id="nav-btn-pomodoro" class="px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 whitespace-nowrap">
        <span aria-hidden="true">⏱️</span> <span id="nav-pomo-label">Pomodoro</span>
      </button>
      <button type="button" onclick="switchView('roadmap')" id="nav-btn-roadmap" class="px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 whitespace-nowrap">
        <span aria-hidden="true">🗺️</span> 12-Wk Plan
      </button>
    </nav>

    <!-- Right Controls: Search (Cmd+K), Palette Switcher & Right Sidebar Collapse Button -->
    <div class="flex items-center gap-1.5">
      <button type="button" id="open-cmdk-btn" class="px-2.5 py-1.5 rounded-lg ui-card border text-xs ui-text-muted hover:opacity-90 flex items-center gap-1.5 transition-colors" aria-label="Search all notes and problems">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        <kbd class="px-1.5 py-0.5 text-xs font-mono ui-surface rounded border">⌘K</kbd>
      </button>

      <!-- Palette Switcher: Indigo | Tokyo Night | Catppuccin Mocha | Daylight -->
      <div class="hidden md:flex items-center ui-card rounded-lg p-0.5 border text-xs" role="group" aria-label="Color palette">
        <button type="button" onclick="setTheme('indigo')" id="btn-theme-indigo" class="px-2 py-1 rounded font-medium transition-all" title="Linear Indigo">⚡ Indigo</button>
        <button type="button" onclick="setTheme('tokyo')" id="btn-theme-tokyo" class="px-2 py-1 rounded font-medium transition-all" title="Tokyo Night">🌃 Tokyo</button>
        <button type="button" onclick="setTheme('mocha')" id="btn-theme-mocha" class="px-2 py-1 rounded font-medium transition-all" title="Catppuccin Mocha">🌸 Mocha</button>
        <button type="button" onclick="setTheme('daylight')" id="btn-theme-daylight" class="px-2 py-1 rounded font-medium transition-all" title="Daylight Clean">☀️ Light</button>
      </div>

      <!-- Right Sidebar Collapse Button -->
      <button type="button" id="toggle-right-sidebar-btn" onclick="toggleRightSidebar()" class="p-1.5 rounded-lg ui-card border ui-text-muted hover:text-[var(--text)] transition-colors" title="Toggle Right 'On This Page' Column (Shortcut: o)">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7"/></svg>
      </button>
    </div>
  </header>

  <!-- ===================================================================== -->
  <!-- READER WORKSPACE (Used by both 📘 Concepts and 🧩 LeetCode Guides)    -->
  <!-- ===================================================================== -->
  <main id="view-reader" class="flex-1 flex overflow-hidden">
    
    <!-- Left Collapsible Sidebar -->
    <aside id="reader-sidebar" class="w-76 shrink-0 ui-surface border-r flex flex-col h-[calc(100vh-53px)] sticky top-[53px]">
      <div class="p-3 border-b ui-border space-y-2.5">
        <div class="flex items-center justify-between gap-2">
          <div class="grid grid-cols-3 gap-1 ui-card p-1 rounded-lg border text-xs flex-1" role="group" aria-label="Sidebar filter">
            <button type="button" onclick="setSidebarScope('concept')" id="sb-scope-concept" class="py-1 rounded font-semibold transition-colors">📘 Concepts</button>
            <button type="button" onclick="setSidebarScope('problem')" id="sb-scope-problem" class="py-1 rounded font-semibold transition-colors">🧩 Problems</button>
            <button type="button" onclick="setSidebarScope('all')" id="sb-scope-all" class="py-1 rounded font-semibold transition-colors">All (94)</button>
          </div>
          <button type="button" onclick="toggleLeftSidebar()" class="p-1.5 rounded-lg ui-card border ui-text-muted hover:text-[var(--text)]" title="Collapse left sidebar (b)">
            «
          </button>
        </div>

        <search>
          <input id="sidebar-filter-input" type="search" placeholder="Filter current list..." aria-label="Filter sidebar items" class="w-full ui-card border rounded-lg px-3 py-1.5 text-xs focus:outline-none">
        </search>

        <div class="flex items-center justify-between text-xs ui-text-muted px-1">
          <span id="sidebar-count-label">Showing items</span>
          <button type="button" id="toggle-all-cats-btn" class="hover:underline ui-accent-text">Collapse all</button>
        </div>
      </div>

      <div id="sidebar-tree" class="flex-1 overflow-y-auto p-2.5 space-y-2">
      </div>
    </aside>

    <!-- Center Markdown & Visual Flowchart Canvas -->
    <div id="reader-scroll-container" class="flex-1 overflow-y-auto h-[calc(100vh-53px)] px-4 sm:px-8 py-6">
      <div id="reader-inner-wrap" class="max-w-3xl mx-auto space-y-5 pb-16 transition-all">

        <!-- Document Control Bar -->
        <div class="ui-card border rounded-xl p-3.5 flex flex-wrap items-center justify-between gap-3 shadow-sm">
          <div class="flex items-center gap-2 flex-wrap">
            <span id="doc-type-badge" class="text-xs font-semibold px-2.5 py-0.5 rounded-full border ui-accent-soft">Type</span>
            <span id="doc-cat-badge" class="text-xs font-medium px-2.5 py-0.5 rounded-full ui-surface border ui-text-muted">Module</span>
            <span id="doc-diff-badge" class="text-xs font-semibold px-2.5 py-0.5 rounded-full">Difficulty</span>
            <a id="doc-lc-link" href="#" target="_blank" rel="noopener noreferrer" class="hidden text-xs font-semibold ui-accent-text hover:underline flex items-center gap-1">
              LeetCode ↗
            </a>
          </div>

          <div class="flex items-center gap-2 flex-wrap">
            <div class="flex items-center ui-surface rounded-lg p-0.5 border text-xs" role="group" aria-label="Reading mode">
              <button type="button" onclick="setReaderMode('full')" id="mode-btn-full" class="px-2.5 py-1 rounded font-semibold ui-accent-soft border">
                Text + Diagrams
              </button>
              <button type="button" onclick="setReaderMode('visual')" id="mode-btn-visual" class="px-2.5 py-1 rounded font-medium ui-text-muted" title="Hide paragraphs and show only flowcharts, arrow traces, tables, and code">
                ⚡ Diagrams Only
              </button>
            </div>

            <button type="button" onclick="toggleFlowcharts()" id="btn-toggle-flowcharts" class="px-2.5 py-1 rounded-lg border ui-accent-soft text-xs font-semibold" title="Show or hide Mermaid flowcharts">
              📊 Flowcharts: ON
            </button>

            <div class="flex items-center ui-surface rounded-lg p-0.5 border text-xs" role="group" aria-label="Study status">
              <button type="button" onclick="setCurrentDocStatus('todo')" id="status-btn-todo" class="px-2 py-1 rounded font-medium">○ Todo</button>
              <button type="button" onclick="setCurrentDocStatus('review')" id="status-btn-review" class="px-2 py-1 rounded font-medium">🔁 Review</button>
              <button type="button" onclick="setCurrentDocStatus('solved')" id="status-btn-solved" class="px-2 py-1 rounded font-medium">✓ Done</button>
            </div>
          </div>
        </div>

        <!-- Rendered Document Content -->
        <article id="rendered-content" class="md-body ui-card border rounded-2xl p-5 sm:p-8 shadow-sm">
        </article>

        <!-- Personal Takeaway Note -->
        <section class="ui-card border rounded-xl p-4 space-y-2" aria-label="Personal notes">
          <div class="flex items-center justify-between">
            <label for="doc-personal-note" class="text-xs font-bold uppercase tracking-wider ui-accent-text">📌 Personal Takeaway / Mistake to Remember</label>
            <span id="note-saved-indicator" class="text-xs ui-text-muted">Auto-saves locally</span>
          </div>
          <textarea id="doc-personal-note" rows="2" placeholder="Write your 1-sentence mental trigger or edge case for this topic..." class="w-full ui-surface border rounded-lg p-2.5 text-xs focus:outline-none"></textarea>
        </section>

        <!-- Prev / Next Navigation Footer -->
        <nav class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2" aria-label="Document pagination">
          <button type="button" id="prev-doc-btn" class="ui-card border rounded-xl p-3.5 text-left hover:opacity-90 transition-all group">
            <div class="text-xs ui-text-muted">← Previous in List</div>
            <div id="prev-doc-title" class="text-sm font-semibold mt-0.5 ui-accent-text truncate">-</div>
          </button>
          <button type="button" id="next-doc-btn" class="ui-card border rounded-xl p-3.5 text-right hover:opacity-90 transition-all group">
            <div class="text-xs ui-text-muted">Next in List →</div>
            <div id="next-doc-title" class="text-sm font-semibold mt-0.5 ui-accent-text truncate">-</div>
          </button>
        </nav>

      </div>
    </div>

    <!-- Right Collapsible Table of Contents Rail -->
    <aside id="reader-toc-sidebar" class="w-64 shrink-0 ui-surface border-l p-4 h-[calc(100vh-53px)] sticky top-[53px] flex flex-col justify-between overflow-y-auto">
      <div class="space-y-3">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold uppercase tracking-wider ui-text-muted">On This Page</span>
          <button type="button" onclick="toggleRightSidebar()" class="px-1.5 py-0.5 rounded ui-card border text-xs ui-text-muted hover:text-[var(--text)]" title="Collapse right sidebar (o)">
            »
          </button>
        </div>
        <nav id="toc-list" class="space-y-1.5 text-xs" aria-label="Table of contents">
        </nav>
      </div>
      <div class="ui-card border rounded-xl p-3 space-y-1.5 text-xs">
        <div class="font-semibold ui-accent-text">Keyboard Shortcuts</div>
        <div class="flex justify-between ui-text-muted"><span>Search all docs</span><kbd class="font-mono">⌘K / /</kbd></div>
        <div class="flex justify-between ui-text-muted"><span>Left / Right sidebar</span><kbd class="font-mono">b / o</kbd></div>
        <div class="flex justify-between ui-text-muted"><span>Prev / Next doc</span><kbd class="font-mono">[ / ]</kbd></div>
        <div class="flex justify-between ui-text-muted"><span>Diagrams Only</span><kbd class="font-mono">v</kbd></div>
      </div>
    </aside>

  </main>

  <!-- ===================================================================== -->
  <!-- VIEW 2: CHEAT SHEETS DECK (21 Quick-Reference Cards)                  -->
  <!-- ===================================================================== -->
  <section id="view-cheatsheets" class="hidden flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 py-6 space-y-5">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b ui-border pb-4">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold ui-accent-text">⚡ Pattern Cheat Sheets Deck (21)</h1>
        <p class="text-xs ui-text-muted mt-0.5">Quick-reference pattern triggers, decision flowcharts, and copy-paste templates.</p>
      </div>
      <search>
        <input id="cs-search-input" type="search" placeholder="Filter cheat sheets..." aria-label="Filter cheat sheets" class="ui-card border rounded-xl px-3.5 py-2 text-xs w-full sm:w-64 focus:outline-none">
      </search>
    </div>

    <div id="cheatsheets-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    </div>
  </section>

  <!-- ===================================================================== -->
  <!-- VIEW 3: PROBLEM TRACKER (Strictly separates LeetCode Problems)        -->
  <!-- ===================================================================== -->
  <section id="view-tracker" class="hidden flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 py-6 space-y-5">
    
    <div class="grid grid-cols-2 sm:grid-cols-5 gap-3">
      <div class="ui-card border rounded-xl p-3.5">
        <div class="text-xs ui-text-muted">Problems Solved</div>
        <div class="text-2xl font-black ui-accent-text mt-0.5" id="stat-solved">0</div>
        <div class="text-xs ui-text-muted mt-0.5" id="stat-total-label">of 40 repo problems</div>
      </div>
      <div class="ui-card border rounded-xl p-3.5">
        <div class="text-xs ui-text-muted">Needs Review</div>
        <div class="text-2xl font-black text-amber-400 mt-0.5" id="stat-review">0</div>
        <div class="text-xs ui-text-muted mt-0.5">Spaced repetition queue</div>
      </div>
      <div class="ui-card border rounded-xl p-3.5">
        <div class="text-xs ui-text-muted">Easy Solved</div>
        <div class="text-2xl font-black text-sky-400 mt-0.5" id="stat-easy">0</div>
        <div class="text-xs ui-text-muted mt-0.5">Speed & accuracy</div>
      </div>
      <div class="ui-card border rounded-xl p-3.5">
        <div class="text-xs ui-text-muted">Medium / Hard</div>
        <div class="text-2xl font-black text-purple-400 mt-0.5" id="stat-medium">0</div>
        <div class="text-xs ui-text-muted mt-0.5">Interview core</div>
      </div>
      <div class="ui-card border rounded-xl p-3.5 col-span-2 sm:col-span-1 flex flex-col justify-between">
        <div class="text-xs ui-text-muted">Log New Problem</div>
        <button type="button" id="open-log-dialog-btn" class="mt-2 w-full py-1.5 px-3 rounded-lg ui-accent-btn font-semibold text-xs transition-all hover:opacity-90">
          + Log Problem
        </button>
      </div>
    </div>

    <div class="ui-card border rounded-xl p-3 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">
      <div class="flex items-center gap-2 flex-1">
        <div class="flex items-center ui-surface rounded-lg p-0.5 border text-xs shrink-0" role="group" aria-label="Tracker item type">
          <button type="button" onclick="setTrackerTypeFilter('problem')" id="trk-type-problem" class="px-2.5 py-1 rounded font-semibold ui-accent-soft border">🧩 Problems Only</button>
          <button type="button" onclick="setTrackerTypeFilter('concept')" id="trk-type-concept" class="px-2.5 py-1 rounded font-medium ui-text-muted">📘 Concepts</button>
        </div>

        <search class="flex-1">
          <input id="tracker-search-input" type="search" placeholder="Search by LC #, title, pattern, or takeaway..." aria-label="Search tracker items" class="w-full ui-surface border rounded-lg px-3 py-1.5 text-xs focus:outline-none">
        </search>
      </div>

      <div class="flex flex-wrap items-center gap-2">
        <select id="tracker-cat-filter" aria-label="Filter by module" class="ui-surface border rounded-lg px-2.5 py-1.5 text-xs focus:outline-none">
          <option value="ALL">All Topic Folders</option>
          <option value="01_arrays_and_pointers">01. Arrays & Pointers</option>
          <option value="02_linked_lists">02. Linked Lists</option>
          <option value="03_stacks_and_queues">03. Stacks & Queues</option>
          <option value="04_sorting">04. Sorting</option>
          <option value="05_binary_search">05. Binary Search</option>
          <option value="00_foundations">00. Foundations</option>
          <option value="system_design">System Design</option>
        </select>

        <div class="flex items-center ui-surface rounded-lg p-0.5 border text-xs" role="group" aria-label="Filter by status">
          <button type="button" onclick="setTrackerStatusFilter('ALL')" data-status="ALL" class="tracker-status-btn px-2.5 py-1 rounded font-semibold ui-accent-soft border">All</button>
          <button type="button" onclick="setTrackerStatusFilter('solved')" data-status="solved" class="tracker-status-btn px-2.5 py-1 rounded font-medium ui-text-muted">✓ Solved</button>
          <button type="button" onclick="setTrackerStatusFilter('review')" data-status="review" class="tracker-status-btn px-2.5 py-1 rounded font-medium ui-text-muted">🔁 Review</button>
          <button type="button" onclick="setTrackerStatusFilter('todo')" data-status="todo" class="tracker-status-btn px-2.5 py-1 rounded font-medium ui-text-muted">○ Todo</button>
        </div>
      </div>
    </div>

    <div class="ui-card border rounded-2xl overflow-hidden shadow-sm">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="ui-surface border-b ui-border ui-text-muted uppercase tracking-wider">
              <th class="py-3 px-3 w-28">Status</th>
              <th class="py-3 px-3">Problem / Topic</th>
              <th class="py-3 px-3 hidden sm:table-cell">Pattern</th>
              <th class="py-3 px-3 hidden lg:table-cell">Core Trick / Takeaway</th>
              <th class="py-3 px-3 text-right w-40">Actions</th>
            </tr>
          </thead>
          <tbody id="tracker-tbody" class="divide-y ui-border">
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- ===================================================================== -->
  <!-- VIEW 4: POMODORO FOCUS TRACKER (With Smooth Harmonic Chime Alarm)     -->
  <!-- ===================================================================== -->
  <section id="view-pomodoro" class="hidden flex-1 max-w-4xl w-full mx-auto px-4 sm:px-6 py-8 space-y-6">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b ui-border pb-4">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold ui-accent-text">⏱️ Pomodoro & Interview Sprint Timer</h1>
        <p class="text-xs ui-text-muted mt-0.5">Runs in the background while you read notes • Plays a warm harmonic singing-bowl chime on completion.</p>
      </div>
      <div class="flex items-center gap-2">
        <select id="pomo-sound-select" aria-label="Alarm sound style" class="ui-card border rounded-lg px-2.5 py-1.5 text-xs focus:outline-none">
          <option value="chime">🔔 Warm Singing Bowl Chime</option>
          <option value="marimba">🎶 Soft Marimba Triad</option>
          <option value="crystal">✨ Crystal Bell Arpeggio</option>
        </select>
        <button type="button" onclick="playSmoothAlarm()" class="px-3 py-1.5 rounded-lg ui-card border text-xs font-semibold ui-accent-text hover:opacity-90">
          🔊 Test Chime
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-5 gap-6">
      
      <!-- Left 3 Cols: Timer Ring & Controls -->
      <div class="md:col-span-3 ui-card border rounded-2xl p-6 flex flex-col items-center justify-between space-y-6 shadow-sm">
        
        <!-- Mode Presets -->
        <div class="flex flex-wrap items-center justify-center gap-1.5 ui-surface p-1.5 rounded-xl border text-xs w-full">
          <button type="button" onclick="setPomodoroPreset(25, 'Pomodoro Focus')" id="pomo-preset-25" class="pomo-preset-btn px-3 py-1.5 rounded-lg font-semibold ui-accent-btn">
            🍅 25m Focus
          </button>
          <button type="button" onclick="setPomodoroPreset(45, 'FAANG Mock Sprint')" id="pomo-preset-45" class="pomo-preset-btn px-3 py-1.5 rounded-lg font-medium ui-text-muted hover:text-[var(--text)]">
            ⚡ 45m FAANG Mock
          </button>
          <button type="button" onclick="setPomodoroPreset(5, 'Short Break')" id="pomo-preset-5" class="pomo-preset-btn px-3 py-1.5 rounded-lg font-medium ui-text-muted hover:text-[var(--text)]">
            ☕ 5m Break
          </button>
          <button type="button" onclick="setPomodoroPreset(15, 'Long Break')" id="pomo-preset-15" class="pomo-preset-btn px-3 py-1.5 rounded-lg font-medium ui-text-muted hover:text-[var(--text)]">
            🌿 15m Break
          </button>
        </div>

        <!-- SVG Circular Countdown Ring -->
        <div class="relative w-56 h-56 flex items-center justify-center">
          <svg class="w-full h-full -rotate-90" viewBox="0 0 120 120" aria-hidden="true">
            <circle cx="60" cy="60" r="52" fill="none" stroke="var(--border)" stroke-width="6"></circle>
            <circle id="pomo-ring-circle" cx="60" cy="60" r="52" fill="none" stroke="var(--accent)" stroke-width="6" stroke-linecap="round" stroke-dasharray="326.7" stroke-dashoffset="0" class="transition-all duration-500"></circle>
          </svg>
          <div class="absolute inset-0 flex flex-col items-center justify-center text-center">
            <span id="pomo-mode-label" class="text-xs font-semibold uppercase tracking-wider ui-accent-text">Pomodoro Focus</span>
            <div id="pomo-time-display" class="text-5xl font-black font-mono tracking-tight my-1">25:00</div>
            <span id="pomo-status-sub" class="text-xs ui-text-muted">Ready to start</span>
          </div>
        </div>

        <!-- Focus Target Selector -->
        <div class="w-full space-y-1">
          <label for="pomo-task-input" class="text-xs ui-text-muted block">Focusing on topic / problem:</label>
          <input id="pomo-task-input" type="text" placeholder="e.g. 2D Matrices & Spiral Traversal (LC 54)" class="w-full ui-surface border rounded-xl px-3.5 py-2 text-xs focus:outline-none">
        </div>

        <!-- Start / Pause / Reset + Custom Duration -->
        <div class="flex items-center justify-between gap-3 w-full pt-2 border-t ui-border">
          <div class="flex items-center gap-2">
            <button type="button" onclick="togglePomodoroStart()" id="pomo-start-btn" class="px-5 py-2 rounded-xl ui-accent-btn font-bold text-xs shadow-sm hover:opacity-90 transition-all">
              ▶ Start Focus
            </button>
            <button type="button" onclick="resetPomodoro()" class="px-3.5 py-2 rounded-xl ui-surface border text-xs font-semibold ui-text-muted hover:text-[var(--text)]">
              Reset
            </button>
          </div>

          <div class="flex items-center gap-1.5 text-xs">
            <label for="pomo-custom-min" class="ui-text-muted">Custom:</label>
            <input id="pomo-custom-min" type="number" min="1" max="180" value="25" class="w-14 ui-surface border rounded-lg px-2 py-1 text-center font-mono">
            <button type="button" onclick="applyCustomPomodoro()" class="px-2.5 py-1 rounded-lg ui-card border font-medium hover:opacity-90">Set</button>
          </div>
        </div>

      </div>

      <!-- Right 2 Cols: Daily Focus Stats & Session History -->
      <div class="md:col-span-2 flex flex-col justify-between space-y-4">
        <div class="grid grid-cols-2 gap-3">
          <div class="ui-card border rounded-2xl p-4">
            <div class="text-xs ui-text-muted">Sessions Today</div>
            <div id="pomo-stat-sessions" class="text-2xl font-black ui-accent-text mt-1">0</div>
            <div class="text-xs ui-text-muted mt-0.5">Completed blocks</div>
          </div>
          <div class="ui-card border rounded-2xl p-4">
            <div class="text-xs ui-text-muted">Focus Minutes</div>
            <div id="pomo-stat-minutes" class="text-2xl font-black text-sky-400 mt-1">0m</div>
            <div class="text-xs ui-text-muted mt-0.5">Deep work logged</div>
          </div>
        </div>

        <div class="ui-card border rounded-2xl p-4 flex-1 flex flex-col justify-between space-y-3">
          <div class="flex items-center justify-between border-b ui-border pb-2">
            <h2 class="text-xs font-bold uppercase tracking-wider ui-accent-text">Completed Focus Log</h2>
            <button type="button" onclick="clearPomodoroLog()" class="text-xs ui-text-muted hover:underline">Clear</button>
          </div>
          <div id="pomo-history-list" class="space-y-2 max-h-60 overflow-y-auto text-xs flex-1">
          </div>
        </div>
      </div>

    </div>
  </section>

  <!-- ===================================================================== -->
  <!-- VIEW 5: 12-WEEK FAANG ROADMAP (With hidden="until-found" support)     -->
  <!-- ===================================================================== -->
  <section id="view-roadmap" class="hidden flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 py-6 space-y-5">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b ui-border pb-4">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold ui-accent-text">🗺️ 12-Week FAANG Preparation Roadmap</h1>
        <p class="text-xs ui-text-muted mt-0.5">2 problems/day on weekdays • 5/day on weekends • Click any topic to open its study note.</p>
      </div>
      <button type="button" onclick="openDocInReader('faang_preparation_plan.md')" class="px-3 py-1.5 rounded-lg ui-card border text-xs font-semibold ui-accent-text hover:opacity-90">
        Read Full Plan Doc →
      </button>
    </div>

    <div id="roadmap-accordion">
      <div class="flex items-center gap-2 overflow-x-auto pb-3" role="tablist">
        <button type="button" onclick="selectRoadmapPhase('rm-phase-1')" id="btn-rm-phase-1" aria-expanded="true" aria-controls="rm-phase-1" class="rm-tab-btn px-3.5 py-2 rounded-xl text-xs font-semibold ui-accent-soft border whitespace-nowrap">
          Phase 1: Arrays, Pointers & Windows (W1–3)
        </button>
        <button type="button" onclick="selectRoadmapPhase('rm-phase-2')" id="btn-rm-phase-2" aria-expanded="false" aria-controls="rm-phase-2" class="rm-tab-btn px-3.5 py-2 rounded-xl text-xs font-semibold ui-card border ui-text-muted whitespace-nowrap">
          Phase 2: Linked Lists, Stacks & Binary Search (W4–6)
        </button>
        <button type="button" onclick="selectRoadmapPhase('rm-phase-3')" id="btn-rm-phase-3" aria-expanded="false" aria-controls="rm-phase-3" class="rm-tab-btn px-3.5 py-2 rounded-xl text-xs font-semibold ui-card border ui-text-muted whitespace-nowrap">
          Phase 3: Pattern Cheat Sheets (W7–9)
        </button>
        <button type="button" onclick="selectRoadmapPhase('rm-phase-4')" id="btn-rm-phase-4" aria-expanded="false" aria-controls="rm-phase-4" class="rm-tab-btn px-3.5 py-2 rounded-xl text-xs font-semibold ui-card border ui-text-muted whitespace-nowrap">
          Phase 4: System Design & Architecture (W10–12)
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
        <input id="cmdk-input" type="search" placeholder="Search any concept, LC #, pattern, or keyword..." aria-label="Search all study guides" class="w-full bg-transparent text-sm focus:outline-none">
      </search>
      <form method="dialog">
        <button type="submit" class="px-2 py-0.5 rounded text-xs ui-surface border ui-text-muted">Esc</button>
      </form>
    </div>
    <div id="cmdk-results" class="max-h-96 overflow-y-auto p-2 space-y-1">
    </div>
  </dialog>

  <!-- ===================================================================== -->
  <!-- NATIVE DIALOG 2: QUICK-PEEK STUDY DRAWER                              -->
  <!-- ===================================================================== -->
  <dialog id="peek-dialog" closedby="any" class="ui-card border rounded-2xl w-full max-w-3xl p-0 text-[var(--text)] shadow-2xl max-h-[88vh]">
    <div class="sticky top-0 z-10 ui-surface border-b px-5 py-3 flex items-center justify-between gap-3">
      <div class="flex items-center gap-2 truncate">
        <span id="peek-title" class="font-bold text-sm truncate">Study Guide</span>
      </div>
      <div class="flex items-center gap-2 shrink-0">
        <button type="button" id="peek-open-full-btn" class="px-3 py-1 rounded-lg ui-accent-btn font-semibold text-xs">
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
        <button type="submit" class="px-3.5 py-1.5 rounded-lg ui-accent-btn font-semibold">Save Problem</button>
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
    const THEME_KEY = 'dsa_hub_palette_v3';
    const LEFT_SB_KEY = 'dsa_hub_left_sb_open';
    const RIGHT_SB_KEY = 'dsa_hub_right_sb_open';
    const POMO_LOG_KEY = 'dsa_hub_pomo_log_v1';

    let docStatusMap = {{}};
    let docNotesMap = {{}};
    let customProblems = [];
    let pomoHistory = [];
    let currentView = DEFAULT_INITIAL_VIEW;
    let sidebarScope = 'concept';
    let currentDocPath = "00_foundations/01_algorithms_correctness_efficiency.md";
    let readerMode = 'full';
    let showFlowcharts = true;
    let trackerStatusFilter = 'ALL';
    let trackerTypeFilter = 'problem';
    let isLeftSidebarOpen = true;
    let isRightSidebarOpen = true;

    // 1. Initialize Storage
    function initState() {{
      try {{
        const savedStatus = localStorage.getItem(STATUS_STORAGE_KEY);
        if (savedStatus) {{
          docStatusMap = JSON.parse(savedStatus);
        }} else {{
          DOC_KEYS.forEach(k => {{
            if (DOCS_DATA[k].defaultSolved) docStatusMap[k] = 'solved';
          }});
          localStorage.setItem(STATUS_STORAGE_KEY, JSON.stringify(docStatusMap));
        }}

        const savedNotes = localStorage.getItem(NOTES_STORAGE_KEY);
        if (savedNotes) docNotesMap = JSON.parse(savedNotes);

        const savedCustom = localStorage.getItem(CUSTOM_PROBS_KEY);
        if (savedCustom) customProblems = JSON.parse(savedCustom);

        const savedPomo = localStorage.getItem(POMO_LOG_KEY);
        if (savedPomo) pomoHistory = JSON.parse(savedPomo);

        const savedLeft = localStorage.getItem(LEFT_SB_KEY);
        if (savedLeft !== null) isLeftSidebarOpen = savedLeft === 'true';

        const savedRight = localStorage.getItem(RIGHT_SB_KEY);
        if (savedRight !== null) isRightSidebarOpen = savedRight === 'true';
      }} catch (e) {{
        console.warn(e);
      }}
    }}

    // 2. Collapsible Left & Right Sidebars
    function applySidebarVisibility() {{
      const leftSb = document.getElementById('reader-sidebar');
      const rightSb = document.getElementById('reader-toc-sidebar');
      const leftBtn = document.getElementById('toggle-left-sidebar-btn');
      const rightBtn = document.getElementById('toggle-right-sidebar-btn');
      const innerWrap = document.getElementById('reader-inner-wrap');

      if (leftSb) {{
        if (isLeftSidebarOpen) {{
          leftSb.classList.remove('hidden');
          leftBtn.classList.add('ui-accent-soft');
        }} else {{
          leftSb.classList.add('hidden');
          leftBtn.classList.remove('ui-accent-soft');
        }}
      }}

      if (rightSb) {{
        if (isRightSidebarOpen) {{
          rightSb.classList.remove('hidden');
          rightBtn.classList.add('ui-accent-soft');
        }} else {{
          rightSb.classList.add('hidden');
          rightBtn.classList.remove('ui-accent-soft');
        }}
      }}

      // Expand center reading width slightly when both sidebars are collapsed
      if (innerWrap) {{
        if (!isLeftSidebarOpen && !isRightSidebarOpen) {{
          innerWrap.className = 'max-w-4xl mx-auto space-y-5 pb-16 transition-all';
        }} else {{
          innerWrap.className = 'max-w-3xl mx-auto space-y-5 pb-16 transition-all';
        }}
      }}
    }}

    function toggleLeftSidebar() {{
      isLeftSidebarOpen = !isLeftSidebarOpen;
      localStorage.setItem(LEFT_SB_KEY, String(isLeftSidebarOpen));
      applySidebarVisibility();
    }}

    function toggleRightSidebar() {{
      isRightSidebarOpen = !isRightSidebarOpen;
      localStorage.setItem(RIGHT_SB_KEY, String(isRightSidebarOpen));
      applySidebarVisibility();
    }}

    // 3. Pomodoro Timer & Smooth Web Audio Harmonic Chime
    let pomoTotalSeconds = 25 * 60;
    let pomoRemainingSeconds = 25 * 60;
    let pomoModeTitle = 'Pomodoro Focus';
    let pomoInterval = null;
    let audioCtx = null;

    function playSmoothAlarm() {{
      try {{
        if (!audioCtx) {{
          const AudioContextClass = window.AudioContext || window.webkitAudioContext;
          audioCtx = new AudioContextClass();
        }}
        if (audioCtx.state === 'suspended') audioCtx.resume();

        const style = document.getElementById('pomo-sound-select')?.value || 'chime';
        const now = audioCtx.currentTime;

        // Harmonic frequencies (Hz) for C major 9th / Singing Bowl intervals
        const presets = {{
          chime:   {{ freqs: [523.25, 659.25, 783.99, 987.77, 1046.50], wave: 'sine',     gap: 0.22, dur: 2.4 }},
          marimba: {{ freqs: [440.00, 554.37, 659.25, 880.00],          wave: 'triangle', gap: 0.14, dur: 1.4 }},
          crystal: {{ freqs: [587.33, 880.00, 1174.66, 1479.98],        wave: 'sine',     gap: 0.18, dur: 2.0 }}
        }};
        const cfg = presets[style] || presets.chime;

        cfg.freqs.forEach((freq, idx) => {{
          const start = now + idx * cfg.gap;
          const osc = audioCtx.createOscillator();
          const overtone = audioCtx.createOscillator();
          const gain = audioCtx.createGain();

          osc.type = cfg.wave;
          osc.frequency.setValueAtTime(freq, start);

          overtone.type = 'sine';
          overtone.frequency.setValueAtTime(freq * 2, start);

          // Smooth bell envelope: soft attack (0.04s) + long warm exponential decay
          gain.gain.setValueAtTime(0.0001, start);
          gain.gain.linearRampToValueAtTime(0.16, start + 0.04);
          gain.gain.exponentialRampToValueAtTime(0.0001, start + cfg.dur);

          osc.connect(gain);
          overtone.connect(gain);
          gain.connect(audioCtx.destination);

          osc.start(start);
          overtone.start(start);
          osc.stop(start + cfg.dur + 0.05);
          overtone.stop(start + cfg.dur + 0.05);
        }});
      }} catch (e) {{
        console.warn('Audio chime error:', e);
      }}
    }}

    function formatMMSS(sec) {{
      const m = Math.floor(sec / 60);
      const s = sec % 60;
      return `${{String(m).padStart(2, '0')}}:${{String(s).padStart(2, '0')}}`;
    }}

    function updatePomodoroUI() {{
      const timeStr = formatMMSS(pomoRemainingSeconds);
      const disp = document.getElementById('pomo-time-display');
      if (disp) disp.textContent = timeStr;

      const modeLbl = document.getElementById('pomo-mode-label');
      if (modeLbl) modeLbl.textContent = pomoModeTitle;

      // Update circular SVG progress ring (circumference = 2 * pi * 52 = 326.7)
      const ring = document.getElementById('pomo-ring-circle');
      if (ring && pomoTotalSeconds > 0) {{
        const fraction = 1 - (pomoRemainingSeconds / pomoTotalSeconds);
        ring.style.strokeDashoffset = String(326.7 * fraction);
      }}

      // Update top navbar live badge so user can see countdown while reading notes!
      const navLbl = document.getElementById('nav-pomo-label');
      if (navLbl) {{
        if (pomoInterval) {{
          navLbl.textContent = timeStr;
        }} else if (pomoRemainingSeconds < pomoTotalSeconds && pomoRemainingSeconds > 0) {{
          navLbl.textContent = `${{timeStr}} (Paused)`;
        }} else {{
          navLbl.textContent = 'Pomodoro';
        }}
      }}
    }}

    function setPomodoroPreset(minutes, label) {{
      if (pomoInterval) {{
        clearInterval(pomoInterval);
        pomoInterval = null;
      }}
      pomoTotalSeconds = minutes * 60;
      pomoRemainingSeconds = pomoTotalSeconds;
      pomoModeTitle = label;
      document.getElementById('pomo-custom-min').value = minutes;
      document.getElementById('pomo-start-btn').textContent = '▶ Start Focus';
      document.getElementById('pomo-status-sub').textContent = 'Ready to start';

      [25, 45, 5, 15].forEach(m => {{
        const btn = document.getElementById(`pomo-preset-${{m}}`);
        if (!btn) return;
        if (m === minutes) {{
          btn.className = 'pomo-preset-btn px-3 py-1.5 rounded-lg font-semibold ui-accent-btn';
        }} else {{
          btn.className = 'pomo-preset-btn px-3 py-1.5 rounded-lg font-medium ui-text-muted hover:text-[var(--text)]';
        }}
      }});

      updatePomodoroUI();
    }}

    function applyCustomPomodoro() {{
      const mins = Math.max(1, Math.min(180, parseInt(document.getElementById('pomo-custom-min').value, 10) || 25));
      setPomodoroPreset(mins, `Custom ${{mins}}m Focus`);
    }}

    function togglePomodoroStart() {{
      const startBtn = document.getElementById('pomo-start-btn');
      const sub = document.getElementById('pomo-status-sub');

      // Warm up AudioContext on user click so browser allows chime when timer ends
      if (!audioCtx) {{
        try {{
          const AudioContextClass = window.AudioContext || window.webkitAudioContext;
          audioCtx = new AudioContextClass();
        }} catch (e) {{}}
      }}

      if (pomoInterval) {{
        clearInterval(pomoInterval);
        pomoInterval = null;
        startBtn.textContent = '▶ Resume';
        sub.textContent = 'Paused';
        updatePomodoroUI();
        return;
      }}

      if (pomoRemainingSeconds <= 0) {{
        pomoRemainingSeconds = pomoTotalSeconds;
      }}

      startBtn.textContent = '⏸ Pause';
      sub.textContent = 'Focusing... (stays active across tabs)';

      pomoInterval = setInterval(() => {{
        pomoRemainingSeconds -= 1;
        updatePomodoroUI();

        if (pomoRemainingSeconds <= 0) {{
          clearInterval(pomoInterval);
          pomoInterval = null;
          startBtn.textContent = '▶ Start Again';
          sub.textContent = '🎉 Session Complete!';
          playSmoothAlarm();

          // Log session
          const minsCompleted = Math.round(pomoTotalSeconds / 60);
          const taskField = document.getElementById('pomo-task-input');
          const taskName = (taskField && taskField.value.trim()) || DOCS_DATA[currentDocPath]?.shortTitle || pomoModeTitle;
          pomoHistory.unshift({{
            id: 'pomo-' + Date.now(),
            title: taskName,
            minutes: minsCompleted,
            mode: pomoModeTitle,
            time: new Date().toLocaleTimeString([], {{ hour: '2-digit', minute: '2-digit' }})
          }});
          localStorage.setItem(POMO_LOG_KEY, JSON.stringify(pomoHistory));
          renderPomodoroHistory();
          updatePomodoroUI();
        }}
      }}, 1000);

      updatePomodoroUI();
    }}

    function resetPomodoro() {{
      if (pomoInterval) {{
        clearInterval(pomoInterval);
        pomoInterval = null;
      }}
      pomoRemainingSeconds = pomoTotalSeconds;
      document.getElementById('pomo-start-btn').textContent = '▶ Start Focus';
      document.getElementById('pomo-status-sub').textContent = 'Ready to start';
      updatePomodoroUI();
    }}

    function renderPomodoroHistory() {{
      const totalSessions = pomoHistory.length;
      const totalMins = pomoHistory.reduce((acc, s) => acc + (s.minutes || 0), 0);
      const sessEl = document.getElementById('pomo-stat-sessions');
      const minEl = document.getElementById('pomo-stat-minutes');
      const listEl = document.getElementById('pomo-history-list');

      if (sessEl) sessEl.textContent = totalSessions;
      if (minEl) minEl.textContent = `${{totalMins}}m`;
      if (!listEl) return;

      if (pomoHistory.length === 0) {{
        listEl.innerHTML = '<div class="ui-text-muted py-6 text-center">No completed sessions yet today. Start a 25m focus block above!</div>';
        return;
      }}

      listEl.innerHTML = pomoHistory.map(item => `
        <div class="ui-surface border rounded-xl p-2.5 flex items-center justify-between gap-2">
          <div class="truncate">
            <div class="font-semibold truncate">${{item.title}}</div>
            <div class="ui-text-muted">${{item.mode}} • ${{item.time}}</div>
          </div>
          <span class="px-2 py-0.5 rounded ui-accent-soft border font-mono shrink-0">+${{item.minutes}}m</span>
        </div>
      `).join('');
    }}

    function clearPomodoroLog() {{
      pomoHistory = [];
      localStorage.setItem(POMO_LOG_KEY, JSON.stringify(pomoHistory));
      renderPomodoroHistory();
    }}

    // 4. Status & Theme Helpers
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
      const problemKeys = DOC_KEYS.filter(k => DOCS_DATA[k].docType === 'problem');
      const solvedProbs = problemKeys.filter(k => getDocStatus(k) === 'solved').length + customProblems.length;
      const pill = document.getElementById('global-progress-pill');
      if (pill) pill.textContent = `🧩 ${{solvedProbs}} / ${{problemKeys.length + customProblems.length}} Problems Solved`;
    }}

    function setTheme(theme) {{
      const valid = ['indigo', 'tokyo', 'mocha', 'daylight'];
      if (!valid.includes(theme)) theme = 'indigo';
      document.body.className = `theme-${{theme}} min-h-screen flex flex-col antialiased`;
      localStorage.setItem(THEME_KEY, theme);

      valid.forEach(t => {{
        const btn = document.getElementById(`btn-theme-${{t}}`);
        if (!btn) return;
        if (t === theme) {{
          btn.className = 'px-2 py-1 rounded font-semibold transition-all ui-accent-soft border';
        }} else {{
          btn.className = 'px-2 py-1 rounded font-medium transition-all ui-text-muted hover:opacity-100';
        }}
      }});

      if (typeof mermaid !== 'undefined') {{
        mermaid.initialize({{
          startOnLoad: false,
          theme: theme === 'daylight' ? 'neutral' : 'dark',
          flowchart: {{ curve: 'basis', padding: 12 }},
          securityLevel: 'loose'
        }});
        if ((currentView === 'concepts' || currentView === 'problems') && currentDocPath) {{
          renderMermaidDiagrams(document.getElementById('rendered-content'));
        }}
      }}
    }}

    function setSidebarScope(scope) {{
      sidebarScope = scope;
      ['concept', 'problem', 'all'].forEach(s => {{
        const btn = document.getElementById(`sb-scope-${{s}}`);
        if (!btn) return;
        if (s === scope) {{
          btn.className = 'py-1 rounded font-semibold transition-colors ui-accent-btn shadow-sm';
        }} else {{
          btn.className = 'py-1 rounded font-medium transition-colors ui-text-muted hover:text-[var(--text)]';
        }}
      }});
      renderSidebarTree();
    }}

    // 5. Primary Navigation Switcher (6 Views)
    function switchView(view) {{
      currentView = view;
      ['concepts', 'problems', 'cheatsheets', 'tracker', 'pomodoro', 'roadmap'].forEach(v => {{
        const btn = document.getElementById(`nav-btn-${{v}}`);
        if (!btn) return;
        if (v === view) {{
          btn.className = 'px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 whitespace-nowrap ui-accent-btn shadow-sm';
        }} else {{
          btn.className = 'px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 whitespace-nowrap ui-text-muted hover:text-[var(--text)]';
        }}
      }});

      const readerEl = document.getElementById('view-reader');
      const csEl = document.getElementById('view-cheatsheets');
      const trkEl = document.getElementById('view-tracker');
      const pomoEl = document.getElementById('view-pomodoro');
      const rmEl = document.getElementById('view-roadmap');

      [readerEl, csEl, trkEl, pomoEl, rmEl].forEach(el => el.classList.add('hidden'));

      if (view === 'concepts') {{
        readerEl.classList.remove('hidden');
        setSidebarScope('concept');
        if (DOCS_DATA[currentDocPath]?.docType === 'problem') {{
          renderDoc("00_foundations/01_algorithms_correctness_efficiency.md");
        }}
      }} else if (view === 'problems') {{
        readerEl.classList.remove('hidden');
        setSidebarScope('problem');
        if (DOCS_DATA[currentDocPath]?.docType !== 'problem') {{
          renderDoc("01_arrays_and_pointers/3_longest_substring_without_repeating_characters.md");
        }}
      }} else if (view === 'cheatsheets') {{
        csEl.classList.remove('hidden');
        renderCheatSheetsGrid();
      }} else if (view === 'tracker') {{
        trkEl.classList.remove('hidden');
        renderTrackerTable();
      }} else if (view === 'pomodoro') {{
        pomoEl.classList.remove('hidden');
        const taskInput = document.getElementById('pomo-task-input');
        if (taskInput && !taskInput.value && DOCS_DATA[currentDocPath]) {{
          taskInput.value = DOCS_DATA[currentDocPath].title;
        }}
        renderPomodoroHistory();
      }} else if (view === 'roadmap') {{
        rmEl.classList.remove('hidden');
        renderRoadmapGrids();
      }}

      const url = new URL(window.location);
      url.searchParams.set('view', view);
      window.history.replaceState({{}}, '', url);
    }}

    function openDocInReader(docPath) {{
      const key = resolveDocKey(docPath);
      const doc = DOCS_DATA[key];
      const targetTab = doc?.docType === 'problem' ? 'problems' : 'concepts';
      currentDocPath = key;
      switchView(targetTab);
      if (doc?.docType === 'cheat_sheet') {{
        setSidebarScope('all');
      }}
      renderDoc(key);
    }}

    // 6. Markdown + KaTeX + Mermaid Pipeline
    function renderMarkdownInto(containerEl, markdownText, basePath) {{
      if (typeof marked !== 'undefined') {{
        containerEl.innerHTML = marked.parse(markdownText, {{ breaks: true, gfm: true }});
      }} else {{
        containerEl.innerHTML = '<pre><code>' + markdownText + '</code></pre>';
      }}

      containerEl.querySelectorAll('pre code.language-mermaid').forEach((codeEl) => {{
        const pre = codeEl.parentElement;
        const graphDef = codeEl.textContent;
        const fig = document.createElement('figure');
        fig.className = 'mermaid-figure my-4 ui-surface border rounded-xl p-4 overflow-x-auto';
        fig.innerHTML = `
          <figcaption class="flex items-center justify-between text-xs ui-text-muted mb-2 pb-1.5 border-b ui-border">
            <span class="font-semibold ui-accent-text flex items-center gap-1.5">📊 Decision Flowchart</span>
            <span>Follow arrows step-by-step</span>
          </figcaption>
          <div class="mermaid-render flex justify-center py-1" data-graph="${{encodeURIComponent(graphDef)}}"></div>
        `;
        pre.replaceWith(fig);
      }});

      containerEl.querySelectorAll('pre').forEach(pre => {{
        pre.setAttribute('tabindex', '0');
        if (typeof hljs !== 'undefined') {{
          const code = pre.querySelector('code');
          if (code) hljs.highlightElement(code);
        }}
      }});

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

      renderMermaidDiagrams(containerEl);

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

    // 7. Render Active Document in Reader
    function resolveDocKey(docPath) {{
      if (!docPath) return "00_foundations/01_algorithms_correctness_efficiency.md";
      const clean = docPath.replace(/^(\\.\\/|\\/)/, '');
      if (DOCS_DATA[clean]) return clean;
      const match = DOC_KEYS.find(k => k.endsWith(clean) || clean.endsWith(k));
      return match || "00_foundations/01_algorithms_correctness_efficiency.md";
    }}

    function getFilteredSidebarDocs() {{
      return DOC_KEYS.map(k => DOCS_DATA[k]).filter(d => {{
        if (sidebarScope === 'concept') return d.docType === 'concept';
        if (sidebarScope === 'problem') return d.docType === 'problem';
        return true;
      }});
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
      document.getElementById('doc-type-badge').textContent = doc.docType === 'problem' ? '🧩 LeetCode Walkthrough' : (doc.docType === 'cheat_sheet' ? '⚡ Cheat Sheet' : '📘 Concept Guide');
      document.getElementById('doc-cat-badge').textContent = `${{doc.categoryIcon}} ${{doc.categoryLabel}}`;

      const diffBadge = document.getElementById('doc-diff-badge');
      diffBadge.textContent = doc.difficulty;
      if (doc.difficulty === 'Easy') {{
        diffBadge.className = 'text-xs font-semibold px-2.5 py-0.5 rounded-full bg-sky-500/15 text-sky-400 border border-sky-500/30';
      }} else if (doc.difficulty === 'Medium') {{
        diffBadge.className = 'text-xs font-semibold px-2.5 py-0.5 rounded-full bg-amber-500/15 text-amber-400 border border-amber-500/30';
      }} else if (doc.difficulty === 'Hard') {{
        diffBadge.className = 'text-xs font-semibold px-2.5 py-0.5 rounded-full bg-rose-500/15 text-rose-400 border border-rose-500/30';
      }} else {{
        diffBadge.className = 'hidden';
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

      const noteInput = document.getElementById('doc-personal-note');
      noteInput.value = docNotesMap[targetKey] || doc.summary || '';

      const scopedList = getFilteredSidebarDocs();
      const curIdx = scopedList.findIndex(d => d.path === targetKey);
      const prevDoc = curIdx > 0 ? scopedList[curIdx - 1] : scopedList[scopedList.length - 1] || doc;
      const nextDoc = curIdx >= 0 && curIdx < scopedList.length - 1 ? scopedList[curIdx + 1] : scopedList[0] || doc;

      document.getElementById('prev-doc-title').textContent = prevDoc.title;
      document.getElementById('prev-doc-btn').onclick = () => renderDoc(prevDoc.path);
      document.getElementById('next-doc-title').textContent = nextDoc.title;
      document.getElementById('next-doc-btn').onclick = () => renderDoc(nextDoc.path);

      document.querySelectorAll('.sidebar-doc-link').forEach(el => {{
        if (el.dataset.path === targetKey) {{
          el.className = 'sidebar-doc-link flex items-center justify-between gap-2 px-2.5 py-1.5 rounded-lg text-xs font-semibold ui-accent-soft border';
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
          ? 'block pl-3 py-1 ui-text-muted hover:text-[var(--accent-text)] truncate transition-colors'
          : 'block py-1 font-medium ui-text-muted hover:text-[var(--accent-text)] truncate transition-colors';
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
        btnVis.className = 'px-2.5 py-1 rounded font-semibold ui-accent-soft border';
        btnFull.className = 'px-2.5 py-1 rounded font-medium ui-text-muted';
      }} else {{
        contentEl.classList.remove('visual-focus-mode');
        btnFull.className = 'px-2.5 py-1 rounded font-semibold ui-accent-soft border';
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
        btn.className = 'px-2.5 py-1 rounded-lg border ui-accent-soft text-xs font-semibold';
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
          const activeColor = k === 'solved' ? 'ui-accent-soft border' : (k === 'review' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' : 'ui-card text-[var(--text)] border');
          map[k].className = `px-2 py-1 rounded font-semibold ${{activeColor}}`;
        }} else {{
          map[k].className = 'px-2 py-1 rounded font-medium ui-text-muted hover:opacity-100';
        }}
      }});
    }}

    function setCurrentDocStatus(status) {{
      setDocStatus(currentDocPath, status);
    }}

    function renderSidebarTree() {{
      const container = document.getElementById('sidebar-tree');
      const q = (document.getElementById('sidebar-filter-input')?.value || '').toLowerCase().trim();
      container.innerHTML = '';

      const scopedDocs = getFilteredSidebarDocs().filter(d => {{
        if (!q) return true;
        return d.title.toLowerCase().includes(q) || d.pattern.toLowerCase().includes(q) || d.path.toLowerCase().includes(q);
      }});

      const scopeLabel = sidebarScope === 'concept' ? 'Concept Guides' : (sidebarScope === 'problem' ? 'LeetCode Problems' : 'Total Docs');
      document.getElementById('sidebar-count-label').textContent = `${{scopedDocs.length}} ${{scopeLabel}}`;

      const groups = {{}};
      scopedDocs.forEach(d => {{
        if (!groups[d.category]) groups[d.category] = [];
        groups[d.category].push(d);
      }});

      Object.keys(groups).forEach(cat => {{
        const items = groups[cat];
        const first = items[0];
        const doneCount = items.filter(i => getDocStatus(i.path) === 'solved').length;

        const details = document.createElement('details');
        details.open = true;
        details.className = 'group';

        const summary = document.createElement('summary');
        summary.className = 'flex items-center justify-between px-2 py-1.5 rounded-lg text-xs font-bold uppercase tracking-wider ui-text-muted hover:text-[var(--text)] cursor-pointer select-none';
        summary.innerHTML = `
          <span>${{first.categoryIcon}} ${{first.categoryLabel}}</span>
          <span class="font-mono text-xs px-1.5 py-0.5 rounded ui-card border">${{doneCount}}/${{items.length}}</span>
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
            ? 'sidebar-doc-link flex items-center justify-between gap-2 px-2.5 py-1.5 rounded-lg text-xs font-semibold ui-accent-soft border'
            : 'sidebar-doc-link flex items-center justify-between gap-2 px-2.5 py-1.5 rounded-lg text-xs ui-text-muted hover:text-[var(--text)] hover:bg-[var(--surface-hover)] transition-colors';

          const st = getDocStatus(item.path);
          const statusIcon = st === 'solved'
            ? '<span class="ui-accent-text font-bold shrink-0">✓</span>'
            : (st === 'review' ? '<span class="text-amber-400 shrink-0">🔁</span>' : '');

          const shortLabel = item.lcNumber
            ? `<span class="truncate"><span class="font-mono opacity-60 mr-1.5">#${{item.lcNumber}}</span>${{item.shortTitle}}</span>`
            : `<span class="truncate">${{item.shortTitle}}</span>`;

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

    function renderCheatSheetsGrid() {{
      const grid = document.getElementById('cheatsheets-grid');
      const q = (document.getElementById('cs-search-input')?.value || '').toLowerCase().trim();
      const sheets = DOC_KEYS.map(k => DOCS_DATA[k]).filter(d => d.category === 'cheat_sheets' || d.path === 'dsa_patterns_study_guide.md');

      const filtered = sheets.filter(d => !q || d.title.toLowerCase().includes(q) || d.summary.toLowerCase().includes(q));
      grid.innerHTML = filtered.map(d => `
        <div class="ui-card border rounded-2xl p-4 flex flex-col justify-between gap-3 hover:border-[var(--accent)] transition-all">
          <div class="space-y-2">
            <div class="flex items-center justify-between gap-2">
              <span class="text-xs font-mono px-2 py-0.5 rounded ui-surface border ui-accent-text">${{d.categoryIcon}} ${{d.categoryLabel}}</span>
              ${{d.hasMermaid ? '<span class="text-xs px-2 py-0.5 rounded ui-accent-soft border">📊 Flowchart</span>' : ''}}
            </div>
            <h2 class="text-base font-bold">${{d.title}}</h2>
            <p class="text-xs ui-text-muted leading-relaxed">${{d.summary || 'Complete pattern triggers, visual arrows, and Python templates.'}}</p>
          </div>
          <div class="pt-3 border-t ui-border flex items-center justify-between">
            <button type="button" onclick="openPeekDialog('${{d.path}}')" class="text-xs ui-text-muted hover:text-[var(--text)]">Quick Peek</button>
            <button type="button" onclick="openDocInReader('${{d.path}}')" class="px-3 py-1.5 rounded-lg ui-accent-soft border text-xs font-semibold hover:opacity-90 transition-all">
              Open Sheet →
            </button>
          </div>
        </div>
      `).join('');
    }}

    function setTrackerTypeFilter(t) {{
      trackerTypeFilter = t;
      const btnProb = document.getElementById('trk-type-problem');
      const btnConc = document.getElementById('trk-type-concept');
      if (t === 'problem') {{
        btnProb.className = 'px-2.5 py-1 rounded font-semibold ui-accent-soft border';
        btnConc.className = 'px-2.5 py-1 rounded font-medium ui-text-muted';
      }} else {{
        btnConc.className = 'px-2.5 py-1 rounded font-semibold ui-accent-soft border';
        btnProb.className = 'px-2.5 py-1 rounded font-medium ui-text-muted';
      }}
      renderTrackerTable();
    }}

    function setTrackerStatusFilter(st) {{
      trackerStatusFilter = st;
      document.querySelectorAll('.tracker-status-btn').forEach(btn => {{
        if (btn.dataset.status === st) {{
          btn.className = 'tracker-status-btn px-2.5 py-1 rounded font-semibold ui-accent-soft border';
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

      const allProblems = DOC_KEYS.map(k => DOCS_DATA[k]).filter(d => d.docType === 'problem');
      const solvedProblems = allProblems.filter(d => getDocStatus(d.path) === 'solved');
      const reviewProblems = allProblems.filter(d => getDocStatus(d.path) === 'review');
      const easySolved = solvedProblems.filter(d => d.difficulty === 'Easy').length;
      const medHardSolved = solvedProblems.filter(d => d.difficulty === 'Medium' || d.difficulty === 'Hard').length;

      document.getElementById('stat-solved').textContent = solvedProblems.length + customProblems.length;
      document.getElementById('stat-total-label').textContent = `of ${{allProblems.length + customProblems.length}} LeetCode problems`;
      document.getElementById('stat-review').textContent = reviewProblems.length;
      document.getElementById('stat-easy').textContent = easySolved;
      document.getElementById('stat-medium').textContent = medHardSolved;

      const baseItems = DOC_KEYS.map(k => DOCS_DATA[k]).filter(d => d.docType === trackerTypeFilter);

      const rows = baseItems.filter(d => {{
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
          ? '<span class="px-2.5 py-1 rounded-lg font-semibold ui-accent-soft border">✓ Solved</span>'
          : (st === 'review'
            ? '<span class="px-2.5 py-1 rounded-lg font-semibold bg-amber-500/20 text-amber-400 border border-amber-500/30">🔁 Review</span>'
            : '<span class="px-2.5 py-1 rounded-lg font-medium ui-surface border ui-text-muted">○ Todo</span>');

        const diffColor = d.difficulty === 'Easy' ? 'text-sky-400' : (d.difficulty === 'Medium' ? 'text-amber-400' : (d.difficulty === 'Hard' ? 'text-rose-400' : 'ui-text-muted'));
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
                ${{d.lcNumber ? `<span class="font-mono text-xs px-1.5 py-0.5 rounded ui-surface border ui-accent-text">#${{d.lcNumber}}</span>` : ''}}
                <button type="button" onclick="openPeekDialog('${{d.path}}')" class="text-left hover:underline transition-colors">
                  ${{d.shortTitle}}
                </button>
              </div>
              <div class="text-xs ${{diffColor}} mt-0.5">${{d.difficulty}} • ${{d.categoryLabel}}</div>
            </td>
            <td class="py-3 px-3 hidden sm:table-cell">
              <span class="px-2 py-0.5 rounded ui-surface border text-xs">${{d.pattern}}</span>
            </td>
            <td class="py-3 px-3 hidden lg:table-cell max-w-md">
              <p class="text-xs ui-text-muted line-clamp-2">${{noteText}}</p>
            </td>
            <td class="py-3 px-3 text-right whitespace-nowrap space-x-1.5">
              <button type="button" onclick="openPeekDialog('${{d.path}}')" class="px-2.5 py-1 rounded-lg ui-surface border text-xs hover:opacity-80">
                Peek
              </button>
              <button type="button" onclick="openDocInReader('${{d.path}}')" class="px-2.5 py-1 rounded-lg ui-accent-soft border text-xs font-semibold hover:opacity-90">
                Study →
              </button>
            </td>
          </tr>
        `;
      }}).join('');
    }}

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
          ? 'rm-tab-btn px-3.5 py-2 rounded-xl text-xs font-semibold ui-accent-soft border whitespace-nowrap'
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
            <div class="ui-card border rounded-xl p-3 flex items-center justify-between gap-2">
              <div class="truncate">
                <button type="button" onclick="openDocInReader('${{d.path}}')" class="text-xs font-semibold hover:underline truncate block text-left">
                  ${{d.lcNumber ? '#' + d.lcNumber + ' ' + d.shortTitle : d.shortTitle}}
                </button>
                <span class="text-xs ui-text-muted">${{d.docType === 'problem' ? '🧩 Problem' : '📘 Concept'}} • ${{d.categoryLabel}}</span>
              </div>
              <button type="button" onclick="cycleDocStatus('${{d.path}}')" class="shrink-0 text-xs px-2 py-1 rounded border ${{isSolved ? 'ui-accent-soft' : 'ui-surface ui-text-muted'}}">
                ${{isSolved ? '✓ Done' : '○ Todo'}}
              </button>
            </div>
          `;
        }}).join('');
      }});
    }}

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
          <span class="text-xs font-mono px-2 py-0.5 rounded ui-surface border shrink-0">${{d.docType === 'problem' ? '🧩 Problem' : (d.docType === 'cheat_sheet' ? '⚡ Sheet' : '📘 Concept')}}</span>
        </button>
      `).join('');
    }}

    document.getElementById('open-cmdk-btn').addEventListener('click', openCmdK);
    cmdkInput.addEventListener('input', (e) => renderCmdKResults(e.target.value));

    window.addEventListener('keydown', (e) => {{
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {{
        e.preventDefault();
        openCmdK();
      }} else if (e.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName)) {{
        e.preventDefault();
        openCmdK();
      }} else if ((currentView === 'concepts' || currentView === 'problems') && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName)) {{
        if (e.key === '[') document.getElementById('prev-doc-btn').click();
        if (e.key === ']') document.getElementById('next-doc-btn').click();
        if (e.key === 'v') setReaderMode(readerMode === 'full' ? 'visual' : 'full');
        if (e.key === 'b') toggleLeftSidebar();
        if (e.key === 'o') toggleRightSidebar();
      }}
    }});

    document.getElementById('doc-personal-note').addEventListener('input', (e) => {{
      docNotesMap[currentDocPath] = e.target.value;
      localStorage.setItem(NOTES_STORAGE_KEY, JSON.stringify(docNotesMap));
      const ind = document.getElementById('note-saved-indicator');
      ind.textContent = 'Saved ✓';
      setTimeout(() => {{ ind.textContent = 'Auto-saves locally'; }}, 1200);
    }});

    document.getElementById('sidebar-filter-input').addEventListener('input', renderSidebarTree);
    document.getElementById('toggle-all-cats-btn').addEventListener('click', (e) => {{
      const detailsList = document.querySelectorAll('#sidebar-tree details');
      const anyOpen = Array.from(detailsList).some(d => d.open);
      detailsList.forEach(d => {{ d.open = !anyOpen; }});
      e.target.textContent = anyOpen ? 'Expand all' : 'Collapse all';
    }});

    document.getElementById('cs-search-input').addEventListener('input', renderCheatSheetsGrid);
    document.getElementById('tracker-search-input').addEventListener('input', renderTrackerTable);
    document.getElementById('tracker-cat-filter').addEventListener('change', renderTrackerTable);

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
    const savedTheme = localStorage.getItem(THEME_KEY) || 'indigo';
    setTheme(savedTheme);
    applySidebarVisibility();
    updateGlobalProgressPill();
    updatePomodoroUI();

    const params = new URLSearchParams(window.location.search);
    const paramDoc = params.get('doc');
    const paramView = params.get('view');

    if (paramDoc) {{
      openDocInReader(paramDoc);
    }} else if (paramView && ['concepts', 'problems', 'cheatsheets', 'tracker', 'pomodoro', 'roadmap'].includes(paramView)) {{
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
    ("viewer.html", "concepts"),
    ("tracker.html", "tracker"),
    ("faang_plan.html", "roadmap"),
]:
    out_path = os.path.join(ROOT_DIR, filename)
    with open(out_path, "w", encoding="utf-8") as fp:
        fp.write(build_html(default_view))
    print(f"Generated {out_path} (default_view={default_view})")
