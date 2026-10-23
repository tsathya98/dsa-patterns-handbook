#!/usr/bin/env python3
"""Validate curriculum contracts, Python examples, and repository-local links."""
import ast
import json
import re
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
errors = []
topics = []
expected = {"deep-learning": 9, "genai": 5, "computer-vision": 7, "classical-ml": 7}
required = {"slug", "track", "order", "title", "summary", "why", "interview", "level", "targets", "equations", "derivation", "steps", "traps", "tradeoff", "code", "variants", "sources", "lab", "figure"}
for file in sorted((ROOT / "content/curriculum").glob("*/*.json")):
    data = json.loads(file.read_text())
    topics.append(data)
    if required - data.keys():
        errors.append(f"{file.name}: missing fields {required - data.keys()}")
        continue
    if file.stem != data["slug"] or file.parent.name != data["track"]:
        errors.append(f"{file.name}: path and metadata disagree")
    for field in ("equations", "derivation", "traps", "variants", "sources"):
        if not data[field]:
            errors.append(f"{file.name}: empty {field}")
    if len(data["steps"]) < 3:
        errors.append(f"{file.name}: incomplete execution flow")
    for step in data["steps"]:
        if any(not step.get(k) for k in ("operation", "transformation", "input", "output", "note")):
            errors.append(f"{file.name}: incomplete trace step")
    for field in ("url", "source", "title", "caption"):
        if not data["figure"].get(field):
            errors.append(f"{file.name}: missing figure {field}")
    section_ids = []
    if len(data.get("explanations", [])) < 3:
        errors.append(f"{file.name}: needs architecture, derivation, and worked lesson sections")
    for section in data.get("explanations", []):
        section_ids.append(section.get("id"))
        if section.get("block") not in ("architecture", "math", "trace"):
            errors.append(f"{file.name}: invalid explanation block")
        if not section.get("title") or not section.get("paragraphs"):
            errors.append(f"{file.name}: incomplete detailed explanation")
        table = section.get("table")
        if table and any(len(row) != len(table["headers"]) for row in table["rows"]):
            errors.append(f"{file.name}: explanation table column mismatch")
    if len(section_ids) != len(set(section_ids)) or any(not value for value in section_ids):
        errors.append(f"{file.name}: duplicate or missing explanation anchors")
    for source in data["sources"]:
        if not source["url"].startswith("https://"):
            errors.append(f"{file.name}: invalid source URL")
    try:
        ast.parse(data["code"], filename=file.name)
        # Standard-library examples run without additional environment setup.
        if not re.search(r"^(?:from|import) (?:torch|numpy)\b", data["code"], re.M):
            exec(compile(data["code"], file.name, "exec"), {})
    except Exception as error:
        errors.append(f"{file.name}: Python example failed: {error}")
    if re.search("[\u2013\u2014]", file.read_text()):
        errors.append(f"{file.name}: prohibited dash character")
if Counter(t["track"] for t in topics) != Counter(expected):
    errors.append("Curriculum topic counts do not match the four requested tracks")
if len({t["slug"] for t in topics}) != len(topics):
    errors.append("Duplicate topic slugs")
topic_slugs = {topic["slug"] for topic in topics}
for topic in topics:
    if topic.get("nextTopic") and topic["nextTopic"] not in topic_slugs:
        errors.append(f"{topic['slug']}: invalid next topic")
    for related in topic.get("relatedTopics", []):
        if related["slug"] not in topic_slugs or not related.get("reason"):
            errors.append(f"{topic['slug']}: invalid topic linkage")
for track, count in expected.items():
    if sorted(t["order"] for t in topics if t["track"] == track) != list(range(1, count+1)):
        errors.append(f"{track}: order must be contiguous and unique")

link_count = 0
for file in [ROOT / "README.md", *list((ROOT / "content").rglob("*.md")), ROOT / "docs/study-index.md"]:
    for match in re.finditer(r"\[[^\]]*\]\(([^\s)]+)\)", file.read_text()):
        href = match[1].split("#")[0]
        if not href or re.match(r"[a-z]+:|/", href):
            continue
        link_count += 1
        if not (file.parent / href).exists():
            errors.append(f"{file.relative_to(ROOT)}: broken link {href}")

if "--run-examples" in sys.argv:
    for topic in topics:
        try:
            exec(compile(topic["code"], topic["slug"], "exec"), {})
        except Exception as error:
            errors.append(f"{topic['slug']}: runtime failed: {error}")
if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print(f"Validated {len(topics)} topic contracts, Python examples, and {link_count} local links.")
