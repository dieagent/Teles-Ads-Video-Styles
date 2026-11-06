# Research and evidence workflow for /documentary

## From a one-line prompt to a precise question

Identify the event, people, timeframe and claim hidden in casual wording. For `/documentary what happened in Japan why USA nuke him`, the question is why the United States used atomic bombs on Hiroshima and Nagasaki in August 1945 and what else shaped Japan's surrender. Do not convert a broad country into a person or imply every part of Japan was bombed. Check the expected audience's existing belief and use that as the hook.

## Build a source ledger before a script

For each source, log: stable ID, direct URL, title, publisher, publication/update date, capture/access date, precise claim, limits or perspective, beat IDs, and whether a screenshot is proposed. Prefer official archives, original documents, city records, research papers and reputable institutions. For debated history, read more than one primary/authoritative perspective and distinguish a stated government rationale from causal inference. For changing or medical topics, check current guidance. If a source disagrees with another, name the disagreement or choose a narrower claim that both support.

Use source IDs in `score.json`. The director validator permits `official` and `context` source kinds and an empty `jokes` array; documentary work does not need a comic beat. Use `fiction: false` for historical events and mark dramatized reenactments in credits or metadata when appropriate. A validated score checks structure and timing, **not** historical truth; a human source review remains required.

## Decide whether a page screenshot earns a shot

Use a screenshot when it verifies a date, a primary quote, a contemporary headline, a map, or a numerical claim that the viewer should be able to inspect. A moving diagram is often better for a causal mechanism. The snakebite reference relies on illustrations and diagrams, so do not insert an article merely because it is called a documentary.

When used:

1. Open the direct page and verify its author/publisher, date and claim. Capture the browser page at a readable resolution. Record the screenshot date and URL in `RESEARCH.md`.
2. Keep the raw screenshot unchanged in the example/project evidence folder. Make a separate cropped/styled production image; retain visible publisher/title/date, and highlight only the exact words the narration cites.
3. If the page is paywalled, unavailable, misleadingly updated, or its claim is outside the crop, use another source. Do not synthesize a fake article page or combine quotes from separate documents.
4. In the edit, introduce the source as evidence, then transition back into the dimensional scene. Put full attribution in end credits/description/source pack. Check reuse rights for archival media or use original illustrations.

## Script and voice lock

Write the entire narration, not just a visual treatment. Each paragraph must move the answer forward. Read it aloud for one thought per beat and natural Hindi/Hinglish. Reserve numbers and dates for claims with source IDs. Avoid definitive language about debated motives. For a devastating event, show human consequences respectfully; do not use spectacle as the conclusion.

Record/generate the voice, listen once without visuals, edit confusing lines, and record the final take. Mark actual phrase start/end times and any intentional pause. Only then allocate image beats and caption in/out. An optional article insert gets enough time to read; it should appear as the narrator names the source or claim. Run the score validator after timing lock, then review the rendered draft from start to finish.

## Example output folder

```
project/
  RESEARCH.md           # source ledger, claims, caveats, rights
  SCRIPT.md             # final full narration + scene instructions
  score.json            # beat-level production handoff
  evidence/             # untouched page captures and downloaded sources
  assets/                # original artwork and designed inserts
  voice/                 # final take and pronunciation notes
  renders/               # draft and final MP4, QA notes
```

The repository's [Japan example](../../../../examples/documentary/japan-atomic-bombings/) demonstrates research, script, score and a real National Archives page capture. It has no generated voice or rendered movie; a new `/documentary` invocation completes those stages for the requested topic.
