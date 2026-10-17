#!/usr/bin/env python3
"""
Generate viewer.html with all markdown files pre-bundled as embedded JSON data.
This guarantees 100% reliable opening via file:// protocol without CORS errors!
"""

import os
import json
import re

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

docs = {}

for root, dirs, files in os.walk(ROOT_DIR):
    if any(x in root for x in ('.git', 'static', '.gemini', '.agents', 'notes')):
        continue
    for f in sorted(files):
        if f.endswith('.md'):
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, ROOT_DIR)
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as fp:
                content = fp.read()
            # Title extraction
            m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            title = m.group(1).strip() if m else f
            docs[rel_path] = {
                "title": title,
                "content": content,
                "category": rel_path.split('/')[0] if '/' in rel_path else 'Root'
            }

print(f"Bundled {len(docs)} markdown documents.")

# Read vendor scripts
marked_path = os.path.join(ROOT_DIR, 'static/vendor/marked.min.js')
hl_path = os.path.join(ROOT_DIR, 'static/vendor/highlight.min.js')
hl_css_path = os.path.join(ROOT_DIR, 'static/vendor/highlight-github-dark.min.css')

marked_js = open(marked_path, 'r', encoding='utf-8').read() if os.path.exists(marked_path) else ""
hl_js = open(hl_path, 'r', encoding='utf-8').read() if os.path.exists(hl_path) else ""
hl_css = open(hl_css_path, 'r', encoding='utf-8').read() if os.path.exists(hl_css_path) else ""

docs_json_str = json.dumps(docs)

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DSA Study Guide Viewer</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    {hl_css}
    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-track {{
      background: rgba(15, 23, 42, 0.6);
    }}
    ::-webkit-scrollbar-thumb {{
      background: #334155;
      border-radius: 9999px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #475569;
    }}
    /* Markdown Typography Styling */
    .md-body {{
      color: #e2e8f0;
      line-height: 1.75;
    }}
    .md-body h1 {{
      font-size: 1.875rem;
      font-weight: 800;
      color: #34d399;
      margin-top: 1.5rem;
      margin-bottom: 1rem;
      border-bottom: 1px solid #1e293b;
      padding-bottom: 0.5rem;
    }}
    .md-body h2 {{
      font-size: 1.35rem;
      font-weight: 700;
      color: #38bdf8;
      margin-top: 1.75rem;
      margin-bottom: 0.75rem;
      border-bottom: 1px solid #1e293b;
      padding-bottom: 0.35rem;
    }}
    .md-body h3 {{
      font-size: 1.15rem;
      font-weight: 600;
      color: #f1f5f9;
      margin-top: 1.25rem;
      margin-bottom: 0.5rem;
    }}
    .md-body p {{
      margin-bottom: 1rem;
      color: #cbd5e1;
    }}
    .md-body blockquote {{
      border-left: 4px solid #10b981;
      padding-left: 1rem;
      color: #94a3b8;
      background: rgba(16, 185, 129, 0.05);
      border-radius: 0 0.5rem 0.5rem 0;
      padding-top: 0.5rem;
      padding-bottom: 0.5rem;
      margin-bottom: 1rem;
    }}
    .md-body ul, .md-body ol {{
      margin-bottom: 1rem;
      padding-left: 1.5rem;
    }}
    .md-body ul {{
      list-style-type: disc;
    }}
    .md-body ol {{
      list-style-type: decimal;
    }}
    .md-body li {{
      margin-bottom: 0.35rem;
    }}
    .md-body code:not(pre code) {{
      background: #1e293b;
      color: #38bdf8;
      padding: 0.2rem 0.4rem;
      border-radius: 0.25rem;
      font-family: monospace;
      font-size: 0.875em;
    }}
    .md-body pre {{
      background: #090d16 !important;
      border: 1px solid #1e293b;
      border-radius: 0.75rem;
      padding: 1rem;
      overflow-x: auto;
      margin-bottom: 1.25rem;
    }}
    .md-body pre code {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.85rem;
      line-height: 1.5;
    }}
    .md-body table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 1.5rem;
      font-size: 0.875rem;
    }}
    .md-body th, .md-body td {{
      border: 1px solid #1e293b;
      padding: 0.6rem 0.8rem;
      text-align: left;
    }}
    .md-body th {{
      background: #0f172a;
      color: #38bdf8;
      font-weight: 600;
    }}
    .md-body tr:nth-child(even) {{
      background: rgba(30, 41, 59, 0.3);
    }}
    .md-body a {{
      color: #34d399;
      text-decoration: underline;
      text-underline-offset: 3px;
    }}
    .md-body hr {{
      border: 0;
      border-top: 1px solid #1e293b;
      margin: 2rem 0;
    }}
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col font-sans selection:bg-emerald-500 selection:text-black antialiased">

  <!-- TOP NAV BAR -->
  <header class="bg-slate-900/90 backdrop-blur border-b border-slate-800 sticky top-0 z-30 px-4 sm:px-6 py-3 flex items-center justify-between">
    <div class="flex items-center gap-3">
      <a href="tracker.html" class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs font-medium transition-colors" title="Back to Tracker">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
        Tracker
      </a>
      <a href="faang_plan.html" class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs font-medium transition-colors" title="View 10-Week Roadmap">
        🗺️ Roadmap
      </a>
      <span class="text-slate-600 hidden sm:inline">|</span>
      <h1 id="header-doc-title" class="text-sm sm:text-base font-bold text-white truncate max-w-[200px] sm:max-w-md">
        DSA Study Guide
      </h1>
    </div>

    <div class="flex items-center gap-3">
      <!-- Search Docs Dropdown / Filter -->
      <div class="relative">
        <select id="doc-selector" class="bg-slate-950 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500 max-w-[180px] sm:max-w-xs truncate">
          <!-- Populated by JS -->
        </select>
      </div>

      <button id="toggle-sidebar-btn" class="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs flex items-center gap-1 lg:hidden">
        📑 List
      </button>
    </div>
  </header>

  <!-- MAIN APP CONTAINER -->
  <div class="flex-1 flex overflow-hidden">
    
    <!-- SIDEBAR: LIST OF ALL DOCS -->
    <aside id="sidebar" class="w-72 bg-slate-900/60 border-r border-slate-800 overflow-y-auto flex-shrink-0 hidden lg:block p-4 space-y-4">
      <div class="relative">
        <input type="text" id="sidebar-search" placeholder="Search guides..." class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-300 placeholder-slate-500 focus:outline-none focus:border-emerald-500">
      </div>

      <div id="sidebar-groups" class="space-y-4 text-xs">
        <!-- Rendered by JS -->
      </div>
    </aside>

    <!-- CONTENT VIEWER -->
    <main class="flex-1 overflow-y-auto p-4 sm:p-8 lg:p-12 max-w-5xl mx-auto w-full">
      <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 sm:p-10 shadow-2xl relative">
        <div id="rendered-content" class="md-body">
          <!-- Injected dynamically -->
        </div>
      </div>
    </main>

  </div>

  <!-- EMBEDDED MARKED & HIGHLIGHT JS -->
  <script>
    {marked_js}
  </script>
  <script>
    {hl_js}
  </script>

  <!-- BUNDLED DOCS DATA & LOGIC -->
  <script>
    const DOCS_DATA = {docs_json_str};

    // Configure marked with syntax highlighting
    if (typeof marked !== 'undefined') {{
      marked.setOptions({{
        highlight: function(code, lang) {{
          if (typeof hljs !== 'undefined' && lang && hljs.getLanguage(lang)) {{
            try {{
              return hljs.highlight(code, {{ language: lang }}).value;
            }} catch (e) {{}}
          }}
          if (typeof hljs !== 'undefined') {{
            try {{
              return hljs.highlightAuto(code).value;
            }} catch (e) {{}}
          }}
          return code;
        }},
        breaks: true,
        gfm: true
      }});
    }}

    // Get active doc from URL query parameter (e.g. ?doc=01_arrays_and_pointers/88_merge_sorted_array.md)
    function getDocParam() {{
      const params = new URLSearchParams(window.location.search);
      return params.get('doc');
    }}

    function setDocParam(docPath) {{
      const url = new URL(window.location);
      url.searchParams.set('doc', docPath);
      window.history.pushState({{}}, '', url);
    }}

    // Render a given document
    function renderDoc(docPath) {{
      // Clean path
      let cleanPath = docPath ? docPath.replace(/^(\.\/|\/)/, '') : '';
      
      // Fallback matching
      let targetKey = Object.keys(DOCS_DATA).find(k => k === cleanPath);
      if (!targetKey && cleanPath) {{
        // Match by filename suffix
        targetKey = Object.keys(DOCS_DATA).find(k => k.endsWith(cleanPath) || cleanPath.endsWith(k));
      }}

      // Default to 88_merge_sorted_array.md or README.md if not found
      if (!targetKey) {{
        targetKey = "01_arrays_and_pointers/88_merge_sorted_array.md" in DOCS_DATA 
          ? "01_arrays_and_pointers/88_merge_sorted_array.md" 
          : Object.keys(DOCS_DATA)[0];
      }}

      const docObj = DOCS_DATA[targetKey];
      if (!docObj) return;

      document.getElementById('header-doc-title').textContent = docObj.title || targetKey;
      document.title = (docObj.title || targetKey) + " | DSA Guide";
      
      const contentEl = document.getElementById('rendered-content');
      
      if (typeof marked !== 'undefined') {{
        contentEl.innerHTML = marked.parse(docObj.content);
      }} else {{
        contentEl.innerHTML = '<pre>' + docObj.content + '</pre>';
      }}

      // Highlight any code blocks that marked didn't catch
      if (typeof hljs !== 'undefined') {{
        contentEl.querySelectorAll('pre code').forEach((el) => {{
          hljs.highlightElement(el);
        }});
      }}

      // Intercept local markdown links to load within viewer!
      contentEl.querySelectorAll('a').forEach(anchor => {{
        const href = anchor.getAttribute('href');
        if (href && href.endsWith('.md')) {{
          anchor.addEventListener('click', (e) => {{
            e.preventDefault();
            // Resolve relative path
            let currentDir = targetKey.includes('/') ? targetKey.substring(0, targetKey.lastIndexOf('/')) : '';
            let resolved = href.replace(/^(\.\/)/, '');
            if (href.startsWith('../')) {{
              resolved = href.replace('../', '');
            }} else if (currentDir && !href.startsWith('/')) {{
              resolved = currentDir + '/' + resolved;
            }}
            setDocParam(resolved);
            renderDoc(resolved);
            window.scrollTo(0, 0);
          }});
        }}
      }});

      // Update selector
      document.getElementById('doc-selector').value = targetKey;

      // Update active sidebar item
      document.querySelectorAll('.sidebar-item').forEach(el => {{
        if (el.dataset.path === targetKey) {{
          el.className = 'sidebar-item p-2 rounded-lg bg-emerald-500/20 text-emerald-300 font-semibold block border border-emerald-500/30';
        }} else {{
          el.className = 'sidebar-item p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/60 block transition-colors';
        }}
      }});
    }}

    // Populate Sidebar and Selector Dropdown
    function initSidebar() {{
      const selector = document.getElementById('doc-selector');
      const groupsContainer = document.getElementById('sidebar-groups');

      selector.innerHTML = '';
      groupsContainer.innerHTML = '';

      // Group docs by category
      const groups = {{}};
      Object.keys(DOCS_DATA).forEach(path => {{
        const cat = DOCS_DATA[path].category || 'Other';
        if (!groups[cat]) groups[cat] = [];
        groups[cat].push({{ path, ...DOCS_DATA[path] }});
      }});

      Object.keys(groups).sort().forEach(cat => {{
        const optGroup = document.createElement('optgroup');
        optGroup.label = cat.replace(/_/g, ' ').toUpperCase();

        const groupDiv = document.createElement('div');
        groupDiv.className = 'space-y-1';
        
        const catHeader = document.createElement('div');
        catHeader.className = 'text-[11px] font-bold uppercase tracking-wider text-slate-500 px-2 py-1';
        catHeader.textContent = cat.replace(/_/g, ' ');
        groupDiv.appendChild(catHeader);

        groups[cat].forEach(item => {{
          // Dropdown option
          const opt = document.createElement('option');
          opt.value = item.path;
          opt.textContent = item.title;
          optGroup.appendChild(opt);

          // Sidebar item
          const a = document.createElement('a');
          a.href = '#';
          a.dataset.path = item.path;
          a.className = 'sidebar-item p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/60 block transition-colors truncate';
          a.textContent = item.title;
          a.addEventListener('click', (e) => {{
            e.preventDefault();
            setDocParam(item.path);
            renderDoc(item.path);
            window.scrollTo(0, 0);
          }});
          groupDiv.appendChild(a);
        }});

        selector.appendChild(optGroup);
        groupsContainer.appendChild(groupDiv);
      }});

      selector.addEventListener('change', (e) => {{
        setDocParam(e.target.value);
        renderDoc(e.target.value);
        window.scrollTo(0, 0);
      }});

      // Sidebar search
      document.getElementById('sidebar-search').addEventListener('input', (e) => {{
        const q = e.target.value.toLowerCase().trim();
        document.querySelectorAll('.sidebar-item').forEach(item => {{
          const txt = item.textContent.toLowerCase();
          item.style.display = (!q || txt.includes(q)) ? 'block' : 'none';
        }});
      }});

      // Mobile toggle
      document.getElementById('toggle-sidebar-btn').addEventListener('click', () => {{
        const sb = document.getElementById('sidebar');
        sb.classList.toggle('hidden');
      }});
    }}

    // Init
    initSidebar();
    const initialDoc = getDocParam();
    renderDoc(initialDoc);

    // Support browser back/forward buttons
    window.addEventListener('popstate', () => {{
      renderDoc(getDocParam());
    }});
  </script>
</body>
</html>
"""

viewer_path = os.path.join(ROOT_DIR, 'viewer.html')
with open(viewer_path, 'w', encoding='utf-8') as fp:
    fp.write(html_template)

print(f"Generated {viewer_path} successfully!")
