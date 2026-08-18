#!/usr/bin/env bash
# UserPromptSubmit hook: tells the model to invoke the plain-language skill when
# the prompt asks for Plain Language.
#
# Reads the hook payload on stdin and greps it. The patterns require a space
# between the two words, so the hyphenated "plain-language" in a file path or
# working directory never matches.

set -u

payload=$(cat)

if printf '%s' "$payload" | grep -Eqi '(stop|end|exit|quit|disable|turn off|drop|cancel|no more)[^.?!]{0,30}plain +(language|english)|back to normal'; then
  exit 0
fi

if printf '%s' "$payload" | grep -Eqi 'plain +(language|english)|plainly worded|jargon[ -]?free|no jargon|without (the )?jargon'; then
  cat <<'MSG'
The user asked for Plain Language. Invoke the `plain-language` skill now, before answering, and hold that style for the rest of the session unless the user asks you to stop.
MSG
fi

exit 0
