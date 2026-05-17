# /// script
# dependencies = ["pyyaml>=6.0"]
# ///
"""
Migrates UBIQUITOUS_LANGUAGE.md files to .draekien/ubiquitous-language.yaml.

Finds all scoped UBIQUITOUS_LANGUAGE.md files (excluding the root index),
parses terms and ambiguities from each, and writes them into the YAML dictionary
keyed by bounded context.
"""
import argparse
import os
import re
import sys
import yaml


def find_scoped_files(project_root):
    root_index = os.path.join(project_root, "UBIQUITOUS_LANGUAGE.md")
    scoped = []
    skip_dirs = {".git", ".draekien", "node_modules", ".venv", "__pycache__"}
    for dirpath, dirnames, filenames in os.walk(project_root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs and not d.startswith(".")]
        for fname in filenames:
            if fname == "UBIQUITOUS_LANGUAGE.md":
                full = os.path.join(dirpath, fname)
                if full != root_index:
                    scoped.append(full)
    return scoped, root_index if os.path.exists(root_index) else None


def parse_scoped_file(path, project_root):
    with open(path, encoding="utf-8") as f:
        content = f.read()

    heading = re.search(r"^# Ubiquitous Language\s*[—-]\s*(.+)$", content, re.MULTILINE)
    if heading:
        context_name = heading.group(1).strip()
    else:
        rel = os.path.relpath(path, project_root)
        context_name = os.path.basename(os.path.dirname(rel))

    terms = {}
    ambiguities = {}

    sections = re.split(r"^## ", content, flags=re.MULTILINE)
    for section in sections:
        if section.startswith("Terms"):
            terms = _parse_terms(section)
        elif section.startswith("Flagged Ambiguities"):
            ambiguities = _parse_ambiguities(section)

    return context_name, terms, ambiguities


def _parse_terms(section):
    terms = {}
    blocks = re.split(r"^### ", section, flags=re.MULTILINE)
    for block in blocks[1:]:
        lines = block.strip().splitlines()
        if not lines:
            continue
        name = lines[0].strip()
        body = "\n".join(lines[1:]).strip()
        term = {}

        m = re.search(r"^aliases:\s*(.+)$", body, re.MULTILINE)
        if m:
            term["aliases"] = [a.strip() for a in m.group(1).split(",")]

        m = re.search(r"^usage:\s*(.+)$", body, re.MULTILINE)
        if m:
            term["usage"] = m.group(1).strip()

        related_block = re.search(r"^related:\n((?:  - .+\n?)+)", body, re.MULTILINE)
        if related_block:
            related = []
            for line in related_block.group(1).strip().splitlines():
                rm = re.match(r"\s*-\s+(.+?)\s+\((.+)\)", line)
                if rm:
                    related.append({"term": rm.group(1), "relationship": rm.group(2)})
            if related:
                term["related"] = related

        skip = {"aliases:", "usage:", "related:"}
        def_lines = [
            l for l in body.splitlines()
            if l.strip() and not any(l.strip().startswith(p) for p in skip)
            and not l.strip().startswith("- ")
        ]
        if def_lines:
            term["definition"] = " ".join(def_lines)

        terms[name] = term
    return terms


def _parse_ambiguities(section):
    ambiguities = {}
    blocks = re.split(r"^### ", section, flags=re.MULTILINE)
    for block in blocks[1:]:
        lines = block.strip().splitlines()
        if not lines:
            continue
        name = lines[0].strip()
        note = " ".join(lines[1:]).strip()
        ambiguities[name] = {"note": note}
    return ambiguities


def load_dict(path):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {"contexts": {}}


def save_dict(path, data):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def main():
    parser = argparse.ArgumentParser(
        description="Migrate UBIQUITOUS_LANGUAGE.md files to ubiquitous-language.yaml."
    )
    parser.add_argument("--project-root", required=True, help="Project root directory")
    parser.add_argument("--dict", required=True, help="Output path for ubiquitous-language.yaml")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    scoped_files, root_file = find_scoped_files(args.project_root)

    if not scoped_files:
        print("No scoped UBIQUITOUS_LANGUAGE.md files found.")
        sys.exit(0)

    print(f"Found {len(scoped_files)} scoped file(s):")
    for f in scoped_files:
        print(f"  {os.path.relpath(f, args.project_root)}")
    if root_file:
        print(f"  UBIQUITOUS_LANGUAGE.md (root index — skipped)")

    if args.dry_run:
        print("\n[dry-run] No files written.")
        return

    data = load_dict(args.dict)
    data.setdefault("contexts", {})

    total_terms = 0
    for path in scoped_files:
        context_name, terms, ambiguities = parse_scoped_file(path, args.project_root)
        ctx = data["contexts"].setdefault(context_name, {})
        existing_terms = ctx.get("terms", {})
        existing_terms.update(terms)
        ctx["terms"] = existing_terms
        if ambiguities:
            existing_amb = ctx.get("ambiguities", {})
            existing_amb.update(ambiguities)
            ctx["ambiguities"] = existing_amb
        total_terms += len(terms)
        print(f"Migrated: {os.path.relpath(path, args.project_root)} → '{context_name}' ({len(terms)} terms)")

    save_dict(args.dict, data)
    print(f"\nDictionary written to: {args.dict}")
    print(f"Total: {total_terms} terms across {len(scoped_files)} context(s).")
    print("\nOld files (confirm deletion with user if no longer needed):")
    for f in scoped_files:
        print(f"  {os.path.relpath(f, args.project_root)}")
    if root_file:
        print(f"  UBIQUITOUS_LANGUAGE.md (root index)")


if __name__ == "__main__":
    main()
