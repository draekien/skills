# Revision Rules

Revising a skill is not authoring a smaller one. The text already runs, and every line in it is a hypothesis someone tested — a change made without knowing which hypothesis it touches trades a known behaviour for an unknown one. Everything in the body still governs whatever gets written; these rules govern the act of changing what is already there.

## Before changing anything

**Read the skill in full — body and every reference — before the first edit.** A change that looks local rarely is: a term redefined in one section becomes a synonym everywhere else it appears, and a branch added to the body is a branch the description and argument hint do not yet cover.

**Establish what a line is doing before removing it.** A line that reads as redundant is often a countermand — an instruction that exists because the agent's default was wrong, which reads as obvious precisely because the skill already fixed it. Where a line's purpose is not recoverable from the text, ask the skill's owner rather than inferring it from style.

## While changing it

**Never silently drop process logic** — the future agent will lack that judgment without knowing it is missing. Removing a step, a caveat, or a completion criterion changes what the skill guarantees; name every such removal to the skill's owner and get agreement before it lands.

**Change what was asked and stop.** Adjacent improvement is how sediment forms: each addition is defensible alone, and the accumulation is what makes a skill unreadable. A revision that grows the skill should be able to name the branch that needed the growth.

**Keep the existing vocabulary.** A revision that introduces a synonym for a term the skill already defines breaks one term per concept across every file at once — the most expensive defect to introduce and the least visible on the diff. Grep the term before writing a new one.

**Hold the skill's position on each axis unless the position is what changed.** Loosening a prescriptive step into flexible prose, or tightening the reverse, is a design change wearing the clothes of a wording change; make it deliberately or not at all.

**Write the current instruction, not its history.** A revision that explains what used to be there leaves the reading agent to work out which version applies.

## After changing it

**Re-derive the frontmatter from the branches the skill now has.** Adding, removing, or renaming a branch invalidates the description and the argument hint even when neither was edited — a skill that grew a mode its description never mentions has a mode nothing can reach.

Done when every change traces to something the request asked for, every removal has been named to the owner, and the frontmatter matches the skill's current branches.
