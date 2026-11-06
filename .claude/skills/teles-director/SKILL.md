---
name: teles-director
description: Turn a one-line video premise into a researched, character-specific story with original jokes, a timed director score, a selected Teles Ads style, and a reviewed video.
---

# Teles Ads director

Use for `/director <premise>`. The user supplies one line; the director finds the story, the distinctive humor, the right visual style, and the path to a finished short. Read [the research method](references/RESEARCH.md) and [the directing method](references/DIRECTING.md). See the [Modi-in-the-US example](../../../examples/director/modi-us-president/SCRIPT.md) for a complete handoff.

## Work from the idea to the video

1. Research the named people, event, setting and cultural context using current sources. For a **satirical public-figure premise**, inspect both **humor they actually used** and **jokes or memes people have made about them**. Record URLs, dates, what each source establishes and where the proposed script uses it. Treat a meme as evidence of a joke's existence, never as proof that its allegation is true. Mark counterfactual events as fiction. For factual history, science, or safety explanations, route to `/documentary` and research evidence, mechanisms and uncertainty instead of forcing jokes.
2. Decide the story engine before writing lines: who wants what, what goes wrong, how the problem escalates, what changes, and what the answer or final joke pays off. For satire, pick one main comic contradiction. Keep only researched motifs that strengthen that story. Write original setups and punch lines; do not copy a source's joke text. For a documentary, use the specific `/documentary` question → evidence → mechanism/chronology → qualified answer structure.
3. Select **one** specific style from [Teles Ads](../../../TELES_ADS.md). Read its `SKILL.md`, breakdown, source video and frame sheet. Explain why the style fits the premise. The style controls image grammar, typography, motion and sound; the director controls the story and jokes. Do not swap the visual treatment mid-video.
4. Write `RESEARCH.md`, `SCRIPT.md` and `score.json` in a project folder. `score.json` has a line for every narrated beat, the image, movement, caption, sound, story purpose and source IDs. Use the [score format](references/DIRECTING.md). Run `node engine/director/validate_score.mjs <score.json>` and fix errors.
5. Record or generate the voice, measure each take, then fill actual `start`/`end` seconds in the score and change `timing.status` to `voice_locked`. Validate again. Fit the picture to the voice, not the reverse. A pause longer than a quick reaction must have a named story or sound purpose.
6. Build original visuals according to the selected style skill. Render a draft with synchronized captions and a mix that keeps speech clear. Watch the full draft with sound; fix every weak joke, confusing action, irrelevant background, late caption and dead gap. Then render the final and deliver the file with the script, score and source ledger.

If a render tool, voice provider or asset is unavailable, complete and validate the research, script and production-ready score; report the exact missing component. If an optional provider would spend money, show the estimate before using it. Do not publish a video without the user's instruction.

For satire about real public figures, make the counterfactual and comic framing clear in the opening and metadata. Use an original narrator or obviously fictional character voice; do not present invented dialogue as a real recording or endorsement.
