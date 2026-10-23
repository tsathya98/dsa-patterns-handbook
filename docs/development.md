# Development notes

## Application boundaries

The app runs on Next.js with React and TypeScript. Server components read the repository's content directory; client components receive serializable guide data. The library resolves route IDs against an index of known Markdown documents. Arbitrary request paths never become filesystem reads. Markdown renders without raw HTML execution. KaTeX renders with trust disabled.

Topic pages are prerendered. The library index is generated at build time; individual document pages render on demand. Rebuild after changing content for a production deployment. Run the app from the repository's root npm scripts so its working directory resolves correctly. A deployment must include `content/`; Next.js output tracing includes it. This repository contains local application work and has not been published to a hosting service.

Browser progress synchronizes open tabs on the same origin. It has no account or cloud synchronization. AI/ML lesson completion uses `interview-atlas.progress.v1`. The restored coding tools reuse the original `dsa_hub_prob_status_v3`, `dsa_hub_status_v2`, `dsa_hub_notes_v2`, `dsa_hub_custom_probs_v2`, and `dsa_hub_pomo_log_v1` keys. Problem status changes synchronize linked document status. Progress export/import covers problems, document status, notes, custom problems, and focus history. File URLs and different ports have separate storage; use export/import to move that data.

Light and dark modes use semantic CSS variables in `apps/web/styles/tokens.css` under `data-theme` on the document root. Layout imports tokens before structural styles, then `styles/controls.css` for shared native-select appearance and control spacing. A small initial script applies `interview-atlas.theme.v1` before paint, falling back to the device color scheme when no explicit choice exists. The header toggle persists changes and synchronizes other tabs. Track and difficulty colors have theme-specific tokens. Source figures keep their original colors on a light paper canvas. Main text/color pairings are checked by `npm run check:theme`: at least 7:1 in dark mode and 4.5:1 in light mode, plus 3:1 control outlines against their surrounding surfaces. This checks named tokens, not every rendered image or syntax token. Browser checks verify the actual CSS cascade, including 44 px reserved chevron space, native keyboard selection, and responsive layouts. Typography uses shared 12/14/16 px metadata/control/reading sizes at the default root font size, with larger heading steps. Text remains scalable with browser font settings.

## Curriculum authoring

Keep one JSON file per topic under `content/curriculum/<track>/`. The `slug` matches the filename; `order` controls track progression. The four track folders contain 9, 5, 7, and 7 guides respectively. Add equations as LaTeX strings, typed input/output shapes to each step, an explicit transformation, failure modes, and primary source links. Each topic also supplies a figure URL, article URL, author attribution, and caption. The renderer directly embeds that remote image and offers a supporting tensor trace and ASCII view. Image binaries are not copied into the repository. External figures require a network connection; a failed image keeps its source link and the local trace available.

All guides include detailed `explanations` with stable section IDs, a destination block (`architecture`, `math`, or `trace`), paragraphs, equations, worked tables, and optional attributed figures. Use `order` for the next lesson in the current track. Use `nextTopic` and `nextTopicReason` for a connected learning dependency, including links to other tracks; these appear after the lesson. `relatedTopics` supplies optional prerequisites and connected applications. End-of-track pages offer another track instead of looping backward through the syllabus. The content checks validate explanation anchors, table widths, and topic targets; math checks include equations in these sections.

The homepage offers three subject paths. `/ai-ml` is the single AI/ML learning home, with four tracks and the original five applied guides. `/curriculum` and the old homepage query bookmarks redirect to `/ai-ml`, preserving query parameters. Saved lessons use `/ai-ml?saved=1`. Each `/tracks/<track>` page contains only its own ordered lessons, progress, prerequisites, and a start/resume action. Lesson details and cross-topic exploration use disclosures. The sidebar offers six main destinations, a personal study group, and tools/reference in a disclosure. The current track's lesson navigation only appears on that track and its lessons. Topic routes use the exact slug; unknown slugs return 404. Company Markdown links resolve to the corresponding interactive company page.

With a local server running, `npm run check:routes` checks all four track pages and 28 topic pages, including titles, track membership, lesson anchors, six layout blocks, forward links, and unknown-route 404s. Use `python3 scripts/check_routes.py --all-content` to additionally check every company page, reference document, and paired Python source and write `docs/learner-audit-routes.json`. Pass a different server with `python3 scripts/check_routes.py --base http://127.0.0.1:3002`.

Use plain technical language. Use ASCII hyphens in new content. Treat source-specific performance numbers as measurements with conditions, and distinguish protocol versions. Company practice lenses are editorial suggestions.

Runnable snippets implement a mathematical or algorithmic core. They do not claim to provide a complete production service or training pipeline. `/playground` executes the bundled Skulpt algorithm runtime in a worker with a timeout and stop control. Standard-library support is limited; NumPy and PyTorch examples need a local Python environment. The playground persists a draft and accepts allowlisted document or curriculum IDs for code loading.

The playground editor uses CodeMirror 6 with the Python language parser. It provides syntax highlighting, line numbers, four-space automatic indentation, indentation guides, folding, bracket matching/closing, search, completion, and undo/redo. Theme changes reconfigure the editor without replacing its document or undo history. Template and draft changes update the existing editor document; keyboard execution reads the current editor buffer. Escape followed by Tab releases keyboard focus from indentation handling.

## Restored study modules

`apps/web/lib/study.ts` reads `content/indexes/study-catalog.json`, which is exported from the original generator by `npm run build:legacy`. It contains the 237-problem catalog, 710 document metadata records, and 62 company profiles. That command also exports the 18 original playground templates and copies the original browser Python runtime. Update the original catalog definitions or source notes, then regenerate these indexes to avoid divergent data copies.

The overview links to `/problems`, `/concepts`, `/system-design`, `/ai-ml`, `/companies`, `/cheat-sheets`, `/roadmap`, `/tracker`, `/playground`, and `/focus`. The company directory parses all 561 Markdown banks and preserves recorded frequency/period fields. Pay profiles retain currency, location, level, equity, WLB notes, role focus, and interview focus. They are explicitly labeled as saved reference estimates. `/search` spans curriculum lessons, problems, field notes, and company profiles. The document reader adds a collapsed contents panel, contextual back and next links, study status, notes, and playground code loading. `/tracker` shows both marked coding problems and guide reviews without duplicating linked problem documents. `/library` is a secondary reference index with 30 records per page. Search omits empty groups and duplicate problem walkthroughs; short queries such as RAG match complete words. Percent-encoded route IDs are decoded before allowlist lookup, including company slugs with accented characters.

## Verification

`npm test` checks the 28 topic contracts, source syntax, standard-library examples, local Markdown links, equation rendering, restored catalog counts and paths, progress import compatibility, all 18 playground templates through the actual worker, and TypeScript. `npm run check:routes` checks the served study workspaces as well as all track and lesson pages. `npm run build` validates prerendering and production bundling. Run all tensor examples in a separate Python environment:

```bash
python3 -m venv /tmp/interview-atlas-examples
/tmp/interview-atlas-examples/bin/python -m pip install numpy torch
/tmp/interview-atlas-examples/bin/python scripts/check_content.py --run-examples
```

Browser checks should cover guide navigation, search, track filters, bookmarks, completion persistence, stage controls, workbench calculations, and the original document reader. Check narrow layouts, including tables and equations, for horizontal overflow within their scroll containers.

## Legacy hub

The original generator is in `scripts/legacy/build_viewer.py`. It reads relocated content but emits the original document IDs. This preserves its problem catalog lookups, saved document IDs, and browser storage keys. Output and vendored assets live together in `generated/legacy/`. The three HTML entry points have different default tabs and are retained for existing workflows.

The app serves those original pages and allowlisted vendor files under `/legacy/`. Generated HTML source links point to the allowlisted `/source/` reader. The original hub includes a progress export button for moving file-origin state to the new app.

Reference PDFs under `notes/` remain local and ignored. Dependency directories, Next.js output, Python bytecode, environment files, and TypeScript caches are ignored. Use `docs/relocation-map.json` to locate moved files.

## Appearance references

The darker neutral palette and consistent text/control sizes were informed by [Linear's UI redesign](https://linear.app/now/how-we-redesigned-the-linear-ui), [its 2026 refresh](https://linear.app/now/behind-the-latest-design-refresh), [VS Code's modern UI work](https://code.visualstudio.com/blogs/2026/10/15/modern-ui), [Primer's theme model](https://primer.style/product/getting-started/react/theming/), and [Material's color roles](https://m3.material.io/styles/color/roles). These are design references; the site uses its own measured palette.

The dropdown defect came from combining native appearance with 6-10 px component padding that left no explicit arrow area. All single-select controls now keep their native menu and keyboard behavior, hide the native closed-state arrow, and draw a single 12 px chevron 14 px inside the right border with 44 px of text clearance. Forced-color mode restores the native arrow. The browser probe checks computed padding after local styles have applied, including table status controls, categories, filters, the playground, and interactive labs.
