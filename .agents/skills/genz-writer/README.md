# 🧠 Gen Z Writer Skill

A Claude skill that writes like a real person — not a language model.

Covers social media posts, blogs, essays, research, and creative writing in an authentic Gen Z voice. No AI slop. No em-dash philosophy. No hollow call-to-actions.

---

## What It Does

When triggered, this skill:

1. **Identifies the format** (social, blog, essay, research, or creative)
2. **Loads the matching branch file** with its own voice rules, structure guide, banned patterns, and worked example
3. **Applies universal anti-slop rules** that hold across every format
4. **Produces output** — then asks one follow-up question, nothing more

---

## Supported Formats

| Format | Triggers | Branch File |
|---|---|---|
| Social | tweet, thread, caption, IG, TikTok, post | `references/social.md` |
| Blog | blog, article, personal post | `references/blog.md` |
| Essay | essay, opinion piece, personal essay, reflection | `references/essay.md` |
| Research | research, paper, study, academic | `references/research.md` |
| Creative | story, fiction, poem, creative, narrative | `references/creative.md` |

---

## Trigger Phrases

This skill activates on writing requests such as:

- `"write this like a real person"`
- `"no AI slop"`
- `"gen z voice"`
- `"write a post about [topic]"`
- `"make this sound human"`
- `"write a blog / essay / caption / twitter thread"`
- `"rewrite this"`
- Any request where you hand it a topic, draft, or bullet points

---

## Input Types

The skill handles all three input types:

- **Raw topic** — `"write about burnout"` → generates from scratch
- **Rough draft / notes** — rewrites while preserving your core ideas
- **Bullet points** — expands into the target format

---

## Voice: What Gen Z Writing Actually Sounds Like

- Starts mid-thought, like you walked into the conversation late
- Sentence fragments used for rhythm. Like this.
- Specific over vague (`"4am crying to Phoebe Bridgers"` not `"feeling emotional"`)
- Self-aware humor, irony without the winking
- Emotional honesty without performing vulnerability
- Doesn't wrap things up neatly — leaves things open or unresolved on purpose
- Lowercase can be an intentional stylistic choice
- Natural use of `"like"`, `"lowkey"`, `"genuinely"`, `"actually"`, `"at this point"`

---

## Hard Bans — It Will Never Write These

Across **all** formats, no exceptions:

- `"It's not just X — it's Y"` constructions
- `"In today's fast-paced world"` or any variation
- `"There's something about X that..."` fake-profound openers
- `"Whether you're a [A] or a [B]..."` fake-inclusive intros
- `"Let's dive in"` / `"Let's explore"` / `"Let's unpack"`
- `"At the end of the day"` / `"When all is said and done"`
- Em-dash philosophy: `"— and that's what makes it special"`
- Restating the topic as if it's a revelation
- Hollow calls-to-action or motivational kickers

---

## File Structure

```
genz-writer/
├── SKILL.md                  # Core skill definition, routing logic, universal rules
└── references/
    ├── social.md             # Twitter/X, Instagram, TikTok
    ├── blog.md               # Personal blog posts, casual long-form
    ├── essay.md              # Personal, opinion, and academic essays
    ├── research.md           # Research papers, literature reviews
    └── creative.md           # Fiction, poetry, prose poetry, narrative
```

Each reference file contains: voice rules, structure guide, banned patterns, and a worked example.

---

## Example Output

**Input:** Topic — school feeling pointless (Twitter thread)

```
1/ school really feels like a side quest that somehow became the main storyline

2/ like why am I memorizing things I'll Google in 2 seconds anyway. what is this actually preparing me for

3/ the worst part is I used to genuinely like learning. somewhere between the deadlines and the grading I just. stopped caring

4/ I'm not failing. I'm doing fine technically. but I'm not there anymore and that's a different kind of exhausting
```

---

**Input:** Personal essay — feeling disconnected from school *(excerpt)*

```
I stopped caring somewhere around second semester of junior year and I can tell you the
exact moment — it was a Tuesday, 11pm, and I was memorizing the causes of a war that
ended before my grandparents were born for an exam I'd forget by Thursday.

I wasn't failing. That's the weird part.
```

---

## Installation

1. Download or clone this repository
2. Place the `genz-writer/` folder in your Claude skills directory (typically `/mnt/skills/user/`)
3. Claude will detect and load it automatically on the next session

```bash
git clone https://github.com/your-username/genz-writer-skill
cp -r genz-writer-skill/genz-writer /mnt/skills/user/
```

---

## Contributing

Found a pattern that slipped through? Have a new format branch in mind?

1. Fork the repo
2. Add your changes with a clear description of what pattern or format you're addressing
3. Open a PR — include a before/after example if you're updating voice rules

---

## License

MIT 

Copyright (c) 2026 Michael Pedemonte
