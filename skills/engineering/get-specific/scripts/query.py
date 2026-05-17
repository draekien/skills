# /// script
# dependencies = ["pyyaml>=6.0"]
# ///
import argparse
import sys
import yaml


def load_dict(path):
    with open(path) as f:
        return yaml.safe_load(f) or {}


def cmd_list_contexts(data):
    contexts = data.get("contexts", {})
    if not contexts:
        print("No contexts defined.")
        return
    for name, ctx in contexts.items():
        term_count = len(ctx.get("terms", {}))
        print(f"  {name} ({term_count} term{'s' if term_count != 1 else ''})")


def cmd_lookup(data, term_name, context=None):
    contexts = data.get("contexts", {})
    if context:
        ctx = contexts.get(context, {})
        term = ctx.get("terms", {}).get(term_name)
        if term:
            _print_term(term_name, term, context)
        else:
            print(f"Term '{term_name}' not found in context '{context}'.")
    else:
        found = []
        for ctx_name, ctx_data in contexts.items():
            term = ctx_data.get("terms", {}).get(term_name)
            if term:
                found.append((ctx_name, term))
        if not found:
            print(f"Term '{term_name}' not found.")
        else:
            for ctx_name, term in found:
                _print_term(term_name, term, ctx_name)


def cmd_list(data, context, page, page_size):
    contexts = data.get("contexts", {})
    ctx = contexts.get(context)
    if not ctx:
        print(f"Context '{context}' not found.")
        return
    terms = list(ctx.get("terms", {}).items())
    total = len(terms)
    start = (page - 1) * page_size
    end = start + page_size
    page_terms = terms[start:end]
    print(f"Context: {context} — {total} term{'s' if total != 1 else ''} (page {page}, {page_size}/page)")
    for name, term in page_terms:
        definition = term.get("definition", "(no definition)")
        truncated = definition[:80] + ("..." if len(definition) > 80 else "")
        print(f"  {name}: {truncated}")
    if end < total:
        print(f"\n  (--page {page + 1} for more)")


def _print_term(name, term, context):
    print(f"\n### {name} [{context}]")
    if "aliases" in term:
        print(f"aliases: {', '.join(term['aliases'])}")
    print(term.get("definition", "(no definition)"))
    if "usage" in term:
        print(f"usage: {term['usage']}")
    if "related" in term:
        print("related:")
        for r in term["related"]:
            print(f"  - {r['term']} ({r['relationship']})")


def main():
    parser = argparse.ArgumentParser(description="Query the ubiquitous language dictionary.")
    parser.add_argument("--dict", required=True, help="Path to ubiquitous-language.yaml")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list-contexts", help="List all bounded contexts")

    lookup_p = subparsers.add_parser("lookup", help="Look up a term by name")
    lookup_p.add_argument("term", help="Term name")
    lookup_p.add_argument("--context", help="Limit search to a specific context")

    list_p = subparsers.add_parser("list", help="List terms in a context")
    list_p.add_argument("context", help="Context name")
    list_p.add_argument("--page", type=int, default=1)
    list_p.add_argument("--page-size", type=int, default=20)

    args = parser.parse_args()

    try:
        data = load_dict(args.dict)
    except FileNotFoundError:
        print(f"Dictionary not found: {args.dict}")
        sys.exit(1)

    if args.command == "list-contexts":
        cmd_list_contexts(data)
    elif args.command == "lookup":
        cmd_lookup(data, args.term, getattr(args, "context", None))
    elif args.command == "list":
        cmd_list(data, args.context, args.page, args.page_size)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
