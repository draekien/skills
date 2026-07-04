# /// script
# dependencies = ["pyyaml==6.0.2"]
# ///
import argparse
import json
import sys
import yaml


def load_dict(path):
    with open(path) as f:
        return yaml.safe_load(f) or {}


def cmd_list_contexts(data):
    contexts = data.get("contexts", {})
    return {
        "contexts": [
            {"name": name, "termCount": len(ctx.get("terms", {}))}
            for name, ctx in contexts.items()
        ]
    }


def cmd_lookup(data, term_name, context=None):
    contexts = data.get("contexts", {})
    results = []
    if context:
        ctx = contexts.get(context, {})
        term = ctx.get("terms", {}).get(term_name)
        if term:
            results.append(_term_result(term_name, term, context))
    else:
        for ctx_name, ctx_data in contexts.items():
            term = ctx_data.get("terms", {}).get(term_name)
            if term:
                results.append(_term_result(term_name, term, ctx_name))
    return {"term": term_name, "results": results}


def cmd_list(data, context, page, page_size):
    contexts = data.get("contexts", {})
    ctx = contexts.get(context)
    if not ctx:
        return {"context": context, "found": False, "terms": []}
    terms = list(ctx.get("terms", {}).items())
    total = len(terms)
    start = (page - 1) * page_size
    end = start + page_size
    page_terms = terms[start:end]
    return {
        "context": context,
        "found": True,
        "total": total,
        "page": page,
        "pageSize": page_size,
        "hasMore": end < total,
        "terms": [
            {"name": name, "definition": term.get("definition", "(no definition)")}
            for name, term in page_terms
        ],
    }


def _term_result(name, term, context):
    result = {"name": name, "context": context, "definition": term.get("definition", "(no definition)")}
    if "aliases" in term:
        result["aliases"] = term["aliases"]
    if "usage" in term:
        result["usage"] = term["usage"]
    if "related" in term:
        result["related"] = term["related"]
    return result


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
        print(
            f"Dictionary not found: {args.dict}. "
            "Run skillsrc.py get to resolve the configured path, "
            "or create it via write.py add-term.",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.command == "list-contexts":
        print(json.dumps(cmd_list_contexts(data)))
    elif args.command == "lookup":
        print(json.dumps(cmd_lookup(data, args.term, getattr(args, "context", None))))
    elif args.command == "list":
        print(json.dumps(cmd_list(data, args.context, args.page, args.page_size)))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
