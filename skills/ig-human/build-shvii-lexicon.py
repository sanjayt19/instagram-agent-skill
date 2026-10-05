#!/usr/bin/env python3
"""Build slop-shvii.json: base lexicon + the Shvii VOICE.md ban list.

Run from this folder:
    python3 build-shvii-lexicon.py
Writes slop-shvii.json next to slop.json. Idempotent: re-running rebuilds
from slop.json, so base updates flow through. Use it with:
    python3 humanize.py draft.txt --lexicon slop-shvii.json --report
    python3 detect.py draft.txt --lexicon slop-shvii.json
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# (find, replace) - replace "" means delete the term outright.
SHVII_WORDS = [
    ("unlock", "open"),
    ("elevate", "improve"),
    ("supercharge", "speed up"),
    ("utilize", "use"),
    ("leverage", "use"),
    ("cutting-edge", "new"),
    ("holistic", "full"),
    ("synergy", ""),
    ("ecosystem", "system"),
    ("embark", "start"),
    ("foster", "build"),
    ("boasts", "has"),
    ("paramount", "key"),
    ("vibrant", "lively"),
    ("bustling", "busy"),
    ("furthermore", "also"),
    ("moreover", "also"),
    ("additionally", "also"),
]

SHVII_PHRASES = [
    ("in today's competitive job market", "right now"),
    ("game-changer", "a big change"),
    ("streamline your", "simplify your"),
    ("navigate the job market", "get through the job market"),
    ("it's important to note", ""),
    ("remember that", ""),
    ("in conclusion", ""),
    ("ready to take your career to the next level", ""),
    ("take your career to the next level", ""),
    ("your dream job awaits", ""),
    ("land your dream job", ""),
    ("stand out from the crowd", "get noticed"),
    ("showcase your skills", "show your skills"),
    ("craft a compelling resume", "write a solid resume"),
]

SHVII_STRUCTURES = [
    {
        "id": "as-an-ai",
        "regex": r"(?im)^as an ai\b.*$",
        "name": "\"As an AI...\" opener",
        "fix": "Delete the sentence. Nobody needs the disclaimer.",
    },
]


def main():
    with open(os.path.join(HERE, "slop.json"), encoding="utf-8") as fh:
        lex = json.load(fh)

    existing = {e["find"].lower() for e in lex["words"] + lex["phrases"]}
    added_w = added_p = skipped = 0
    for find, replace in SHVII_WORDS:
        if find.lower() in existing:
            skipped += 1
            continue
        lex["words"].append({"find": find, "replace": replace, "family": "shvii"})
        existing.add(find.lower())
        added_w += 1
    for find, replace in SHVII_PHRASES:
        if find.lower() in existing:
            skipped += 1
            continue
        lex["phrases"].append({"find": find, "replace": replace, "family": "shvii"})
        existing.add(find.lower())
        added_p += 1

    existing_ids = {s["id"] for s in lex["structures"]}
    added_s = 0
    for s in SHVII_STRUCTURES:
        if s["id"] not in existing_ids:
            lex["structures"].append(s)
            added_s += 1

    lex["version"] = lex.get("version", "1.0.0") + "+shvii"
    lex["note"] = (lex.get("note", "")
                   + " Shvii overlay: VOICE.md ban list merged as family 'shvii'. "
                     "Built by build-shvii-lexicon.py; do not hand-edit, re-run the script.")

    out = os.path.join(HERE, "slop-shvii.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(lex, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"wrote {out}: +{added_w} words, +{added_p} phrases, +{added_s} structures, "
          f"{skipped} already in base")


if __name__ == "__main__":
    main()
