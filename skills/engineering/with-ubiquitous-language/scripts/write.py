# /// script
# dependencies = ["pyyaml==6.0.2"]
# ///
import argparse
import os
import sys
import yaml


def load_dict(path):
    if os.path.exists(path):
        with open(path) as f:
            return yaml.safe_load(f) or {}
    return {"contexts": {}}


def save_dict(path, data):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def _ensure_context(data, context):
    data.setdefault("contexts", {}).setdefault(context, {})


def cmd_add_term(data, context, term_name, definition, aliases, usage, related):
    _ensure_context(data, context)
    data["contexts"][context].setdefault("terms", {})
    term = {"definition": definition}
    if aliases:
        term["aliases"] = aliases
    if usage:
        term["usage"] = usage
    if related:
        term["related"] = related
    data["contexts"][context]["terms"][term_name] = term
    return data


def cmd_flag_ambiguity(data, context, term_name, note):
    _ensure_context(data, context)
    data["contexts"][context].setdefault("ambiguities", {})[term_name] = {"note": note}
    return data


def cmd_resolve_ambiguity(data, context, term_name):
    ambiguities = data.get("contexts", {}).get(context, {}).get("ambiguities", {})
    if term_name not in ambiguities:
        return None
    del ambiguities[term_name]
    if not ambiguities:
        del data["contexts"][context]["ambiguities"]
    return data


def main():
    parser = argparse.ArgumentParser(description="Write terms to the ubiquitous language dictionary.")
    parser.add_argument("--dict", required=True, help="Path to ubiquitous-language.yaml")
    subparsers = parser.add_subparsers(dest="command")

    add_p = subparsers.add_parser("add-term", help="Add or update a term")
    add_p.add_argument("--context", required=True, help="Bounded context name (PascalCase)")
    add_p.add_argument("--term", required=True, help="Term name (PascalCase)")
    add_p.add_argument("--definition", required=True, help="Definition (50 words max)")
    add_p.add_argument("--aliases", nargs="*", help="Alias names")
    add_p.add_argument("--usage", help="Usage note sentence")
    add_p.add_argument("--related", nargs="*", help='Related terms as "TermName:relationship"')

    flag_p = subparsers.add_parser("flag-ambiguity", help="Flag a term as ambiguous")
    flag_p.add_argument("--context", required=True)
    flag_p.add_argument("--term", required=True)
    flag_p.add_argument("--note", required=True, help="Description of the ambiguity")

    resolve_p = subparsers.add_parser("resolve-ambiguity", help="Remove an ambiguity flag")
    resolve_p.add_argument("--context", required=True)
    resolve_p.add_argument("--term", required=True)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    data = load_dict(args.dict)

    if args.command == "add-term":
        related = None
        if args.related:
            related = []
            for r in args.related:
                parts = r.split(":", 1)
                if len(parts) == 2:
                    related.append({"term": parts[0], "relationship": parts[1]})
                else:
                    print(f"Invalid related format (expected 'Term:relationship'): {r}")
                    sys.exit(1)
        data = cmd_add_term(data, args.context, args.term, args.definition, args.aliases, args.usage, related)
        save_dict(args.dict, data)
        print(f"Added '{args.term}' to context '{args.context}'.")

    elif args.command == "flag-ambiguity":
        data = cmd_flag_ambiguity(data, args.context, args.term, args.note)
        save_dict(args.dict, data)
        print(f"Flagged '{args.term}' as ambiguous in context '{args.context}'.")

    elif args.command == "resolve-ambiguity":
        result = cmd_resolve_ambiguity(data, args.context, args.term)
        if result is None:
            print(f"Ambiguity for '{args.term}' in context '{args.context}' already resolved.")
        else:
            save_dict(args.dict, result)
            print(f"Resolved ambiguity for '{args.term}' in context '{args.context}'.")


if __name__ == "__main__":
    main()
