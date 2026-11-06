# Open-source director research

Reviewed 2026-11-06. These are upstream projects we studied for architecture. No upstream code or assets were copied into Teles Ads.

| Project | Relevant design | What Teles Ads uses |
|---|---|---|
| [OpenReels](https://github.com/tsensei/OpenReels) (MIT) | Topic → web research → scene script → voice → visuals → captions → assembly → critique. Its CLI supports a direction brief, a dry-run director score and replay from a saved score. | Research before scripting, an editable director score, and an optional `--direction` handoff. We still inspect its output against the chosen Teles Ads reference style. |
| [Frame / texttovideo](https://github.com/qmmughal/texttovideo) (MIT) | An editable storyboard keeps each scene's narration next to its visual prompt; voice and word-synced captions are generated after scene planning. | Every beat has exact narration, image, motion, caption and sound fields. |
| [aidemo](https://github.com/tandryukha/aidemo) (MIT) | A readable `storyboard.json` is the stable source for voice, recording and captions; composition trims dead time. | Keep `score.json` reviewable and validate it before rendering; reject unexplained voice gaps. |
| [Reel Maestro](https://github.com/spunkytensor/reel-maestro) (Apache 2.0) | Idea-to-reel CLI with editable scene and selective regeneration in Studio. | Revise a weak beat or joke without throwing away the whole story. |

The important missing piece in generic topic-to-video tools is **character-specific comedy research**: what the person has actually said, what the public has joked about, what is verified, and how an original joke changes the plot. The `/director` skill adds that research ledger and a story pass before rendering.

## Optional OpenReels handoff

The local command `node engine/director/export_direction.mjs <score.json> <direction.md>` writes a compatible **direction brief**, not an OpenReels score. If the user has OpenReels configured, its documented CLI accepts `--direction <file>` and offers `--dry-run` to inspect a proposed score before asset generation. Generated narration, timing and visual style must be checked against the Teles Ads score and chosen reference. OpenReels is not installed or bundled by this repository; API-based generation may cost money.

## Why a local score validator exists

The validator checks that a director brief has a selected style, source-linked joke motifs, setup/escalation/payoff beats, visual and sound instructions, and real timing once the voice is locked. It catches the specific failure of a long, unexplained gap between voice and picture. It cannot judge humor, source truth or visual quality; the director still reviews the draft with sound.
