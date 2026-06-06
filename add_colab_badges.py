#!/usr/bin/env python3
"""
Add Google Colab badges to all Jupyter notebooks.
Run this from INSIDE the repo root folder.

Usage:
    cd python-for-ai-engineers
    python add_colab_badges.py
"""

import json, os, glob, re

# ── EDIT THESE ─────────────────────────────────────────────────────────────
GITHUB_USERNAME = "MusaIslamFahad"
GITHUB_REPO     = "python-for-ai-engineers"
BRANCH          = "main"
# ───────────────────────────────────────────────────────────────────────────

COLAB_BASE = "https://colab.research.google.com/github"
BADGE_IMG  = "https://colab.research.google.com/assets/colab-badge.svg"

def make_badge_cell(rel_path):
    url = f"{COLAB_BASE}/{GITHUB_USERNAME}/{GITHUB_REPO}/blob/{BRANCH}/{rel_path}"
    md  = f"[![Open In Colab]({BADGE_IMG})]({url})"
    return {"cell_type": "markdown", "metadata": {}, "source": [md]}

def process(nb_path, repo_root):
    with open(nb_path, encoding="utf-8") as f:
        nb = json.load(f)
    cells = nb.get("cells", [])

    # Remove any existing Colab badge cells first
    cells = [c for c in cells
             if "colab.research.google.com" not in "".join(c.get("source", []))]

    # Relative path from repo root (forward slashes, no leading ./)
    rel = os.path.relpath(nb_path, repo_root).replace("\\", "/")

    # Insert badge after title cell (if first cell is a # heading)
    pos = 0
    if cells and cells[0].get("cell_type") == "markdown":
        if "".join(cells[0].get("source", [])).strip().startswith("#"):
            pos = 1

    cells.insert(pos, make_badge_cell(rel))
    nb["cells"] = cells

    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    return rel

def main():
    # Script must live in repo root
    repo_root = os.path.dirname(os.path.abspath(__file__))
    print(f"Repo root : {repo_root}")
    print(f"Username  : {GITHUB_USERNAME}")
    print(f"Repo      : {GITHUB_REPO}\n")

    notebooks = sorted(glob.glob(os.path.join(repo_root, "**", "*.ipynb"), recursive=True))
    print(f"Found {len(notebooks)} notebooks\n")

    for nb_path in notebooks:
        rel = process(nb_path, repo_root)
        print(f"  ✅ {rel}")

    print(f"\nDone! Commit and push:\n")
    print(f"  git add .")
    print(f"  git commit -m 'Add Colab badges'")
    print(f"  git push")

if __name__ == "__main__":
    main()
