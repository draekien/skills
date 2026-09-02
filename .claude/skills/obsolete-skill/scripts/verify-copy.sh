#!/usr/bin/env bash
# Verify a copied skill directory against what git has committed at HEAD.
set -uo pipefail

usage() {
  cat <<'USAGE'
verify-copy.sh <old-dir> <new-dir>

Compares every file git tracks at HEAD under <old-dir> against the matching
file under <new-dir>, proving a copied skill directory is byte-for-byte intact.

Output (stdout, TSV): <reason>\t<old-path>\t<new-path>
  crlf     identical apart from line endings; normalise the copy with
           find <new-dir> -name '*.md' -exec sed -i 's/\r$//' {} +
  content  genuinely different content
  missing  no such file under <new-dir>

Exit codes:
  0  every tracked file matches byte-for-byte
  1  one or more files differ
  2  usage or environment error
USAGE
}

case "${1:-}" in
  -h | --help) usage; exit 0 ;;
esac

if [ $# -ne 2 ]; then
  echo "error: expected 2 arguments, got $#. Run --help for usage." >&2
  exit 2
fi

old="${1%/}"
new="${2%/}"

git rev-parse --git-dir >/dev/null 2>&1 || {
  echo "error: not inside a git repository." >&2
  exit 2
}

[ -d "$new" ] || {
  echo "error: new directory not found: $new" >&2
  exit 2
}

mapfile -t tracked < <(git ls-tree -r --name-only HEAD "$old")
if [ "${#tracked[@]}" -eq 0 ]; then
  echo "error: git tracks no files at HEAD under: $old" >&2
  exit 2
fi

differs=0
for path in "${tracked[@]}"; do
  target="$new/${path#"$old"/}"
  if [ ! -f "$target" ]; then
    printf 'missing\t%s\t%s\n' "$path" "$target"
    differs=1
  elif git show "HEAD:$path" | diff -q - "$target" >/dev/null 2>&1; then
    continue
  elif git show "HEAD:$path" | diff -q --strip-trailing-cr - "$target" >/dev/null 2>&1; then
    printf 'crlf\t%s\t%s\n' "$path" "$target"
    differs=1
  else
    printf 'content\t%s\t%s\n' "$path" "$target"
    differs=1
  fi
done

if [ "$differs" -eq 0 ]; then
  echo "OK - ${#tracked[@]} file(s) match HEAD byte-for-byte." >&2
  exit 0
fi

echo "FAIL - copy does not match HEAD; see stdout for each file." >&2
exit 1
