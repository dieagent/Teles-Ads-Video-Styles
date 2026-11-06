---
name: documentary
description: Research and produce a vertical, Hindi/Hinglish, cinematic 3D illustrated explainer in the exact editing grammar of the supplied snakebite reference. Use for the documentary slash command followed by a topic.
---

# /documentary: illustrated evidence explainer

Read [the measured reference breakdown](references/STYLE_BREAKDOWN.md), [the design and animation specification](references/DESIGN_SYSTEM.md), [the research and source-insert method](references/RESEARCH_TO_VIDEO.md), and [the worked Japan example](../../../examples/documentary/japan-atomic-bombings/SCRIPT.md). Watch [the original clip](../../../examples/documentary/reference/snakebite-source.mp4) and inspect [the 24-frame sheet](../../../examples/documentary/reference/storyboard-24.jpg) before production. These files define a particular video treatment, not a generic documentary genre.

## Input and output

`/documentary <one-line question>` is enough input. Interpret an imprecise question charitably, identify the precise event or process, and research before writing. Default to a 9:16, roughly two-minute Hindi/Hinglish explainer with short English uppercase headline cards; follow another language or duration if the user gives one. Deliver a finished video, its full script, source ledger, source screenshots used, editable shot score, and a review note.

## Production sequence

1. **Define the question and answer.** Find the central misconception, the causal chain, and the important uncertainty. The opening should stage a compelling question or apparent contradiction, not a list of facts.
2. **Research.** Use current primary or authoritative sources and record URLs, publisher, date, exact claim, and limitations. For historical disputes, distinguish official rationale, documented sequence, and historians' debated interpretation. For medical or safety topics, verify against current clinical/public-health sources. Never inherit a number or claim from the reference video without independent verification.
3. **Write the full narration and score.** Use a sequence of hook → scale/context → apparent answer → mechanism or chronology → complication/reversal → evidence-based answer → human consequence → closing question. Give every narrated beat a specific visible object/action, phrase-level caption, camera/object animation, sound cue, and source ID. Use `score.json` format and run `node engine/director/validate_score.mjs <score.json>`; documentaries need no jokes. See the Japan example.
4. **Plan the evidence insert.** Use a real article, archive, data page, or document screenshot only when its provenance adds value. Capture the actual page, retain an unedited original, record URL and capture date, then use a readable crop with publisher/date and a precise claim highlight. Do not fabricate a headline, blend two pages, or use a long article as wallpaper. In the source clip, the argument is carried mainly by animated scenes and diagrams; an article screenshot is an optional proof beat.
5. **Record or generate the voice.** Use a natural original narrator voice. Read every line aloud for sense and pacing. Measure the final voice take, fill actual `start`/`end` seconds and `voiceFile` in the score, set `timing.status` to `voice_locked`, and validate again. The image must start on the phrase it explains. Rewrite or rerecord a line if the pictures cannot be made intelligible at its pace. Do not stretch dead space with an unrelated moving background.
6. **Build original visuals.** Follow the reference's layered, tactile 3D illustration, diagram transitions, color-coded chapters, and large condensed type. Animate causes and changes: a map narrows, a timeline advances, a cutaway reveals a process, a document proves a point. Reference frames are analysis assets, not frames to reuse in the new video. Use an available renderer, compositing engine, or the Arc Lab engine only where it can faithfully produce the look. Keep generated visuals and archival material clearly distinguished when the distinction matters.
7. **Render and review.** Make a draft, watch it with sound from start to finish, and check source attribution, caption timing, spoken-to-visual alignment, factual nuance, legibility on a phone, music ducking, and the ending. Fix the draft and export the final MP4. Show the user the video plus its files. If a voice or render dependency is genuinely unavailable, finish the researched script and production-ready score and identify the precise missing component; never call an unrendered plan a video.

## Style anchors

- Scene-led illustrated explanation: characters, objects, maps, anatomy/diagrams and dimensional cutaways, with gentle grain and paper/film texture.
- White and amber/red bold condensed uppercase cards, usually upper-left, limited to the key phrase being spoken; no wall of subtitles over an irrelevant backdrop.
- Warm amber for setup, green for classification or mechanism, red for danger or reversal, blue for night or uncertainty. Use the topic's semantic equivalent of these chapter changes.
- Continuous spoken explanation, with purposeful short reaction pauses and sound accents. Background music remains below the voice.
- One visual question opens; the end answers it and invites a specific viewer response without overstating certainty.

The worked example addresses the user's Hiroshima/Nagasaki prompt. It is a script and research example, not a rendered example film. Research again when the command is invoked for a new topic.
