# Directing and production score

## Story pass

Write one sentence for each: protagonist's goal; obstacle; the choice that makes the problem worse; turning point; payoff. Then write a logline that connects them. A list of unrelated memes is not a story. For a short satire, one running gag and one reversal usually give the audience a better payoff than five references.

Use the research ledger to answer: what does this person actually say or do, what have audiences joked about, and which of those motifs changes the fictional situation? Give every joke an original setup and a visible consequence. Do not paste the real joke as the punch line.

## Score shape

`score.json` is the editable handoff between direction and production:

```json
{
  "title": "...",
  "premise": "...",
  "fiction": true,
  "fictionLabel": "FICTIONAL SATIRE",
  "style": "zackd",
  "styleReason": "Why this specific reference fits",
  "targetSeconds": 45,
  "story": {"goal":"...","obstacle":"...","turn":"...","payoff":"..."},
  "timing": {"status":"planned","voiceFile":null},
  "sources": [{"id":"R1","kind":"official","claim":"...","url":"https://...","published":"YYYY-MM-DD","use":"..."}],
  "jokes": [{"id":"J1","sourceIds":["R1"],"setup":"...","originalPunch":"...","storyUse":"..."}],
  "beats": [{"id":"B1","act":"setup","voice":"...","visual":"...","motion":"...","caption":"...","sound":"...","purpose":"...","sourceIds":["R1"],"jokeIds":["J1"],"start":null,"end":null,"intentionalSilence":false}]
}
```

Use `setup`, `escalation`, and `payoff` acts. `sourceIds` on a beat marks a researched motif or factual anchor; invented events can have an empty list. When the voice is locked, `start` and `end` become real seconds from the final take, and `voiceFile` points to its audio file. The validator checks references and gaps; it does not judge whether a joke is funny or a claim is true.

## Script and shot pass

- For each beat, read the voice aloud. Ask whether a viewer can understand the premise without knowing the meme. If not, add context or cut the joke.
- Give the image a verb: enters, transforms, collides, turns, reveals. A static background under several unrelated lines is a failure.
- Plan the caption on the actual spoken phrase. Keep a public-figure satire label visible in the opening so a cropped clip remains clear.
- Let a reaction shot or sound earn a pause. If there is no reaction or reveal, close the gap.
- Give the ending the best visual and the story's answer. A promotional CTA is separate and only used when requested.

## Style and render handoff

Read the chosen `.claude/skills/<style>/SKILL.md`. Its reference clip and frame sheet specify the look. Keep this score's exact story and voice while adapting the visual grammar. Existing Arc Lab engine commands are useful only when that code-drawn look fits. For an external renderer, [OpenReels](https://github.com/tsensei/OpenReels) accepts a `--direction` brief and can emit a dry-run director score; `node engine/director/export_direction.mjs <score.json> <brief.md>` produces a brief from this score. Inspect any generated score and draft before accepting it. This repo does not bundle or silently invoke OpenReels or paid providers.

Run `node engine/director/validate_score.mjs <score.json>` before voice and after locking timing. Then watch and listen to the complete export; the validator cannot replace that review.
