#!/usr/bin/env python3
"""Append one session's feedback items to the feedback log.

Assigns IDs and stable participant pseudonyms, validates every field against
the schema, refuses rows that still contain a known real name, and prints a
session summary.

Usage:
  python append_feedback.py --items items.json --log feedback-log.csv \
      --map participants.private.json [--dry-run]
"""
import argparse
import csv
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

COLUMNS = [
    "id", "session_date", "session_type", "build", "source_ref", "participant",
    "area", "type", "basis", "severity_hint", "paraphrase", "evidence",
    "needs_clarification", "status", "logged_at",
]
SESSION_TYPES = {"stakeholder-demo", "user-test"}
TYPES = {"bug", "friction", "request", "question", "praise"}
BASES = {"stated", "observed"}
SEVERITIES = {"blocker", "major", "minor", "none"}
ROLES = {"stakeholder": "S", "user": "U"}
TEXT_FIELDS = ("paraphrase", "evidence", "needs_clarification")
EVIDENCE_WORD_LIMIT = 25

AREAS_FILE = Path(__file__).resolve().parent.parent / "references" / "app-areas.md"


def load_areas():
    """Allowed areas come from the reference table, so editing it updates validation."""
    areas = set()
    for line in AREAS_FILE.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\|\s*`([a-z0-9-]+)`\s*\|", line)
        if m:
            areas.add(m.group(1))
    if not areas:
        sys.exit(f"Could not read any areas from {AREAS_FILE}")
    return areas


def load_map(path):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def find_label(pmap, name):
    key = name.strip().lower()
    for label, entry in pmap.items():
        names = [entry.get("name", "")] + entry.get("aliases", [])
        if key in (n.strip().lower() for n in names if n):
            return label
    return None


def next_label(pmap, role):
    prefix = ROLES[role]
    nums = [int(k.split("-")[1]) for k in pmap if k.startswith(prefix + "-")]
    return f"{prefix}-{(max(nums) + 1) if nums else 1:02d}"


def all_names(pmap):
    names = []
    for entry in pmap.values():
        names.append(entry.get("name", ""))
        names.extend(entry.get("aliases", []))
    return [n for n in names if n and n.strip()]


def contains_name(text, names):
    for n in names:
        if re.search(r"(?<!\w)" + re.escape(n) + r"(?!\w)", text, flags=re.IGNORECASE):
            return n
    return None


def next_id(rows):
    nums = [int(r["id"].split("-")[1]) for r in rows if r.get("id", "").startswith("FB-")]
    return (max(nums) + 1) if nums else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", required=True, type=Path)
    ap.add_argument("--log", required=True, type=Path)
    ap.add_argument("--map", required=True, type=Path)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    payload = json.loads(args.items.read_text(encoding="utf-8"))
    session = payload.get("session", {})
    items = payload.get("items", [])
    areas = load_areas()
    errors, warnings = [], []

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", session.get("date", "")):
        errors.append("session.date must be YYYY-MM-DD")
    if session.get("type") not in SESSION_TYPES:
        errors.append(f"session.type must be one of {sorted(SESSION_TYPES)}")
    if not items:
        errors.append("no items to log")

    existing = []
    if args.log.exists():
        with args.log.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames and reader.fieldnames != COLUMNS:
                errors.append(f"log columns don't match schema: {reader.fieldnames}")
            existing = list(reader)

    pmap = load_map(args.map)
    new_people = []
    rows = []
    counter = next_id(existing)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # Resolve pseudonyms first so the name check covers people new in this session.
    for i, it in enumerate(items, 1):
        role = it.get("role")
        if role not in ROLES:
            errors.append(f"item {i}: role must be 'stakeholder' or 'user'")
            continue
        name = (it.get("participant") or "").strip()
        if not name:
            errors.append(f"item {i}: participant is empty")
            continue
        if find_label(pmap, name) is None:
            label = next_label(pmap, role)
            pmap[label] = {"name": name, "aliases": [], "role": role}
            new_people.append(label)

    names = all_names(pmap)

    for i, it in enumerate(items, 1):
        name = (it.get("participant") or "").strip()
        label = find_label(pmap, name) if name else None
        if label and pmap[label]["role"] != it.get("role"):
            errors.append(f"item {i}: {label} is a {pmap[label]['role']} in the map but item says {it.get('role')}")
        for field, allowed in (("area", areas), ("type", TYPES), ("basis", BASES), ("severity_hint", SEVERITIES)):
            if it.get(field) not in allowed:
                errors.append(f"item {i}: {field}={it.get(field)!r} not in {sorted(allowed)}")
        if not (it.get("paraphrase") or "").strip():
            errors.append(f"item {i}: paraphrase is empty")
        for field in TEXT_FIELDS:
            hit = contains_name(it.get(field) or "", names)
            if hit:
                errors.append(f"item {i}: {field} contains a real name from the map ({hit!r}); anonymize it")
        if len((it.get("evidence") or "").split()) > EVIDENCE_WORD_LIMIT:
            warnings.append(f"item {i}: evidence is over {EVIDENCE_WORD_LIMIT} words; trim to the key phrase")
        rows.append({
            "id": f"FB-{counter:04d}",
            "session_date": session.get("date", ""),
            "session_type": session.get("type", ""),
            "build": session.get("build", ""),
            "source_ref": session.get("source_ref", ""),
            "participant": label or "",
            "area": it.get("area", ""),
            "type": it.get("type", ""),
            "basis": it.get("basis", ""),
            "severity_hint": it.get("severity_hint", ""),
            "paraphrase": (it.get("paraphrase") or "").strip(),
            "evidence": (it.get("evidence") or "").strip(),
            "needs_clarification": (it.get("needs_clarification") or "").strip(),
            "status": "new",
            "logged_at": now,
        })
        counter += 1

    for w in warnings:
        print("WARNING:", w)
    if errors:
        print("NOT WRITTEN. Fix these and rerun:")
        for e in errors:
            print(" -", e)
        sys.exit(1)

    if not args.dry_run:
        new_file = not args.log.exists()
        args.log.parent.mkdir(parents=True, exist_ok=True)
        with args.log.open("a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=COLUMNS)
            if new_file:
                w.writeheader()
            w.writerows(rows)
        args.map.write_text(json.dumps(pmap, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    verb = "Would log" if args.dry_run else "Logged"
    print(f"{verb} {len(rows)} items ({rows[0]['id']}–{rows[-1]['id']}) from {session['type']} on {session['date']}.")
    if new_people:
        print("New participants:", ", ".join(f"{l} ({pmap[l]['role']})" for l in new_people))
    print("By type:", dict(Counter(r["type"] for r in rows)))
    print("By area:", dict(Counter(r["area"] for r in rows)))
    sev = Counter(r["severity_hint"] for r in rows if r["severity_hint"] in ("blocker", "major"))
    if sev:
        print("Blocker/major:", dict(sev))
    clar = [r for r in rows if r["needs_clarification"]]
    if clar:
        print("Needs clarification:")
        for r in clar:
            print(f"  {r['id']}: {r['needs_clarification']}")
    other = [r["id"] for r in rows if r["area"] == "other"]
    if other:
        print("Area 'other' (consider updating app-areas.md):", ", ".join(other))


if __name__ == "__main__":
    main()
