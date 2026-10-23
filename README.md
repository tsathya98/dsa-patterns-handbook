# Interview Atlas

A Next.js study workspace for Senior and Staff AI engineering interviews. The curriculum covers 28 topics across deep learning, GenAI, computer vision, and classical ML. Each guide starts with a directly embedded article or paper figure with attribution, then follows the same six-block layout: brief, mathematics, execution trace, failure modes, and a runnable Python core example.

The homepage starts with three subjects: coding interviews, system design, and AI/ML. Company preparation and study planning follow below. The workspace retains 237 coding problems, LeetCode 75, Top Interview 150, 30 course exercises, 29 DSA concept guides, 21 system design guides, 5 AI/ML field guides, 24 cheat sheets, and the study roadmap. The company directory contains 561 question banks with 14,666 recorded question rows and 62 saved pay/role profiles. Company data retains its original source periods and has not been reverified as current market data.

AI/ML has one learning home at `/ai-ml`: four learning tracks and five applied guides. `/curriculum` bookmarks redirect there with filters and saved views preserved. Each track page shows its own ordered lessons, progress, and a start or resume action. The guides contain 90 detailed teaching sections with worked derivations, numerical examples, and explanations of which concept to study next. See the [curriculum coverage](docs/curriculum-coverage.md) for the lesson breakdown.

## Run locally

Requires Node.js 20.9 or newer and npm.

```bash
npm ci
npm run dev
```

Open [Interview Atlas](http://127.0.0.1:3000). Search across the workspace, filter problem lists, track solved/review status, keep personal notes, and inspect company questions and role profiles. The Python playground runs 18 original templates in a browser worker with a stop control. Focus sessions continue across pages and reloads. Visual guides retain the attention-mask, KV-memory, RoPE, and convolution workbenches. Bookmarks and study progress are stored in this browser.

Use the sun/moon button in the header to switch between light and dark mode. The dark palette uses a near-black canvas and bright text. Reading text uses 16 px, controls use 14 px, and metadata starts at 12 px; all single-select controls reserve space for an inset chevron. The first visit follows your device appearance; an explicit choice persists across pages, reloads, and other tabs on the same origin.

```bash
npm test             # Content, catalogs, runtime, theme contrast, TypeScript
npm run build        # Production build
npm run check:routes # Validate a running server on port 3001
npm start            # Serve the production build
npm run build:legacy # Rebuild the original HTML hub
```

## Repository layout

```text
apps/web/                  Next.js App Router application
  app/                     Routes, layouts, and styles
  components/              Study UI, diagrams, workbenches, progress
  lib/                     Typed content loading and safe document resolution
  styles/                  Theme tokens and shared form controls
content/
  curriculum/              28 structured topic guides in four track folders
  indexes/                 Generated shared problem, note, company, and playground catalogs
  dsa/                     Numbered DSA sections and Python solutions
  system-design/           Architecture notes, LLD, and case studies
  ai-ml/                   Original AI and ML field notes
  cheat-sheets/            Pattern and architecture references
  companies/               Original company question banks
  plans/                   Preparation roadmap and pattern study guide
scripts/                   Content and math validation
  legacy/                  Original HTML generator
generated/legacy/         Original viewer, tracker, roadmap, and vendor assets
docs/                     Study index, relocation map, and platform briefs
.agents/                  Repository workflows and writing skills
notes/                    Local reference PDFs (gitignored)
```

The [original study index](docs/study-index.md) retains the detailed DSA and system design navigation. The new app exposes the original Markdown through its [study library](http://127.0.0.1:3000/library). Curriculum source files live in [content/curriculum](content/curriculum); each JSON file is the single source for its guide.

## Original viewer

Open [generated/legacy/viewer.html](generated/legacy/viewer.html), [tracker.html](generated/legacy/tracker.html), or [faang_plan.html](generated/legacy/faang_plan.html). These preserve the original HTML experience. Rebuild them with `npm run build:legacy`. Legacy document IDs and browser storage keys remain stable. Paths changed, so existing filesystem bookmarks should be updated using the [relocation map](docs/relocation-map.json).

The modern problem tracker and original hub use the same problem status, document status, personal note, and focus-log storage keys when served from the same origin. The original hub is also available at `/legacy/viewer.html`. If your previous progress lives in a local file viewer or another port, reload that original viewer, export progress, and import the JSON in the new problem tracker. AI/ML lesson completion uses its own key.

The [learner experience audit](docs/learner-experience-audit.md) records the page-by-page navigation changes and verification.

## Development

See [development notes](docs/development.md) for content conventions, Python example verification, and deployment boundaries.
