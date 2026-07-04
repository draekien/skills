# ghost-writing

## Greeting-token precedence for a considered-register thread reply is unresolved

**Gap**: The Mechanics bullet "Greeting tokens by register" gives thread replies a blanket "none" independent of register, while the same bullet separately assigns a greeting token ("Hi {{name}}," / "Hi both," / "Hi Team,") to considered-or-broadcast messages. Neither the bullet nor anything else in the skill states which rule wins when both conditions apply at once - e.g. a considered-register reply that continues an existing thread.

Location: `skills/personal/ghost-writing/SKILL.md`, Mechanics bullet "Greeting tokens by register: none (close peer chat and thread replies), \"Heyo\" (working exchange), \"Hi {{name}},\" / \"Hi both,\" / \"Hi Team,\" (considered or broadcast)."

**Why it's a tradeoff, not a clear-cut fix**: Resolving this requires knowing William's actual behaviour, not just making the text internally consistent. Two equally plausible resolutions exist:

- Thread-continuation always wins (no greeting on any reply, regardless of register) - because a reply already has conversational context that makes a greeting redundant.
- Register wins for considered/broadcast messages even inside a thread - because the higher-stakes register is exactly when a greeting is least likely to read as filler and most likely to be expected (e.g. a formal escalation reply CC'ing new people).

Picking either one without evidence risks encoding a wrong default into a "fixed fact" mechanic, which principle 8's mechanics section treats as non-negotiable. This is a behavioural-precedence decision about the author's actual habits, not a wording or structure fix.

**Recommendation**: Ask William directly (or check observed thread-reply samples in considered/broadcast register) which behaviour matches his actual habit, then encode the winning rule explicitly, e.g.: "Greeting tokens by register: none for close peer, low-stakes chat, and for any reply that continues an existing thread regardless of register; ... for a first message in a working/considered/broadcast register."

**Alternative**: If no clear pattern emerges from evidence, treat thread-continuation as the tie-breaker by default (the more common case - most replies, even formal ones, don't re-greet) and note it as a low-confidence default subject to revision once more observed samples exist.
