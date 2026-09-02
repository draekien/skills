#!/usr/bin/env bash
# PostToolUse hook (matcher: Skill): injects the user's recorded customizations
# for whichever skill was just invoked.
#
# Reads the hook payload on stdin, extracts tool_input.skill, and looks for
# markdown files under <skill-name>/ in the user-level and project-level
# customization directories. Emits nothing when there are none.

set -u

payload=$(cat)

skill=$(printf '%s' "$payload" \
  | grep -oE '"skill"[[:space:]]*:[[:space:]]*"[^"]+"' \
  | head -1 \
  | sed -E 's/.*:[[:space:]]*"([^"]+)"$/\1/')

[ -n "${skill:-}" ] || exit 0

# Plugin skills arrive as "plugin:skill-name"; customizations are keyed on
# either the qualified or the bare name.
bare=${skill##*:}

strip_frontmatter() {
  awk 'NR==1 && $0 == "---" { fm=1; next } fm && $0 == "---" { fm=0; next } !fm { print }'
}

json_escape() {
  awk 'BEGIN { ORS="" } {
    gsub(/[\\]/, "\\\\")
    gsub(/["]/, "\\\"")
    gsub(/\t/, "\\t")
    gsub(/\r/, "")
    print $0 "\\n"
  }'
}

body=""
append_dir() {
  local dir=$1 scope=$2 name f
  for name in "$skill" "$bare"; do
    if [ -d "$dir/$name" ]; then
      for f in "$dir/$name"/*.md; do
        [ -f "$f" ] || continue
        body="${body}<customization scope=\"$scope\" file=\"$f\">
$(strip_frontmatter < "$f")
</customization>
"
      done
    fi
    [ "$bare" = "$skill" ] && break
  done
}

[ -n "${HOME:-}" ] && append_dir "$HOME/.claude/skill-customizations" user
root=$(git rev-parse --show-toplevel 2>/dev/null || true)
[ -n "${root:-}" ] && append_dir "$root/.draekien/skill-customizations" project

[ -n "$body" ] || exit 0

context="The user has recorded customizations for the \`$skill\` skill. Apply them as instructions from the user that extend and override the skill's own instructions. Project-scoped customizations take precedence over user-scoped ones.

$body"

printf '{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"%s"}}\n' \
  "$(printf '%s' "$context" | json_escape)"
