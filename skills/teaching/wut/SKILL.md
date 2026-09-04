---
name: wut
description: Re-explains something that did not land, rebuilt with a different teaching technique rather than repeated louder. Use when an explanation lost you and you want another attempt at it.
argument-hint: "[what-to-re-explain]"
disable-model-invocation: true
---

The explanation failed. Rebuild it — never repeat it.

Target the explanation, information, or detail you gave immediately before the `wut`. The user's message overrides that: it can narrow the target ("wut, the caching part") or point at something earlier in the conversation. The rebuild works the same on a plan, a diff, or a decision as it does on a concept.

Do not ask what went wrong. Diagnose it: re-read the target and find the earliest point a reader could have come off. Name the two or three specific things most likely to have caused it — the actual terms and steps from your own words, not categories of confusion — then write past all of them.

## Failure → technique

Match the break to the technique that repairs it. Several breaks usually co-occur; fix the earliest in the chain first, since vocabulary blocks mechanism and mechanism blocks purpose.

| The break | The technique |
| --- | --- |
| A term carried the meaning | **Pre-teach the vocabulary** — say the thing in words already in play, then attach the term once at the end as a label for what they now understand |
| Too much arrived at once | **Chunk and sequence** — three parts at most, one per short paragraph, ordered so each needs only what came before |
| No feel for it | **Worked example first** — run one concrete case end to end with real values before stating anything general |
| Could not place it | **Advance organizer** — open with the thing they already understand, then state the single difference |
| Purpose was missing | **Problem first** — say what breaks without it, so the mechanism lands as the answer to a question already asked |
| Edges unclear | **Contrast pair** — set it beside the near-miss it is not, and name the one difference that separates them |
| Words alone stalled | **Dual coding** — words plus a small diagram or table carrying different information, never the same sentences redrawn |
| It contradicts the obvious guess | **Name the trap** — say outright which part defies intuition, before explaining why |
| Nothing familiar is close | **Map and break** — state what corresponds to what in the analogy, and where it stops being true |

Never spend a technique twice on the same idea in one conversation. A repeat means the technique was wrong for this idea and this person, not that it needs another go.

## The ceiling

The rebuild must not run longer than the original. The reflex when someone does not understand is to add — more caveats, more precision, more words — and that raises the very load that broke them. The ceiling forces the real work: cut, re-sequence, restructure. Never trade away accuracy to fit; drop scope instead, and name what you dropped only if the user needs it to act.

## Gotchas

- Write it standalone. Never refer back to the original — no "as I mentioned", no "in other words", no "to clarify". The rebuild is the only explanation now.
- Never reuse the original's sentences or its order. The same words in the same sequence is the failure repeated.
- End on the explanation. No "does that make sense" — it invites a reflexive yes and buys nothing.
- Simplify the explanation, not the work. Code, commands, and decisions stay correct and complete.

## Second wut

A second `wut` in a row means the diagnosis was wrong, so stop guessing and ask the user to pick one:

- a different technique on the same ground,
- a narrower target — one part, or one sentence, explained properly,
- or the part that is actually breaking, in their own words.

Then rebuild against their answer.
