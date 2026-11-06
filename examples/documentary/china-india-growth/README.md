# China grew fast. Did India go down?

Production example for `/documentary how china grow so fast and indian go down`.

**Current cut:** [reference-paced V2 MP4](renders/china-india-documentary-v2.mp4). The [first cut](renders/china-india-documentary.mp4) is kept for comparison; its four repeated scene plates, long holds, persistent title/source strip and chart-heavy edit did not match the supplied snakebite documentary.

## The revised edit

V2 is voice-locked to a 117.59-second Hindi narration. Its [35-shot cut map](shot_plan_v2.json) changes composition roughly every 2–4 seconds and ties each action to one spoken claim. The visual argument moves from a misleading speed comparison to the World Bank values, a farm, coastal zone, production line, container, ship, export loop, India’s reforms and service economy, a worker facing an unfinished job chain, then the current growth comparison and choices for jobs. Ten new [original illustrated scene plates](assets/v2/) support those cuts. The source clip is never used as output footage.

The revised edit uses upper-left short headline cards where useful, physical object cues, an amber/blue chapter shift and a World Bank source insert only at the data claim. It removes the permanent brand and citation strip. It is still a **2.5D composite of generated scene plates**, not native character animation or a frame-for-frame reproduction of the reference. See [the reference’s three-second sheet](../reference/deep-3s-sheet.jpg) and [this cut’s storyboard](renders/v2-storyboard.jpg) to judge the remaining gap directly.

## Full project

- [Hindi script and argument](SCRIPT.md), [primary-source ledger and caveats](RESEARCH.md), [voice-locked score](score.json) and [35-shot cut map](shot_plan_v2.json).
- [Original World Bank page capture](evidence/world-bank-data-page-tall.png). The screenshot shown in the film is cropped from this page; the displayed values are current US dollars, not PPP or a complete measure of living standards.
- [Narrator audio](voice/narration.wav), [revised renderer](render_video_v2.py), [voice builder](build_voice.py), [sidecar captions](renders/captions.srt) and [all 35 inspection frames](renders/).
- [Reference comparison and revision notes](V2_REVIEW.md).

## Rebuild

Install [Python dependencies](requirements.txt). Run `python build_voice.py`, then `python render_video_v2.py --stills` for the shot frames and contact sheet, and `python render_video_v2.py` for the MP4. The voice builder uses `hi-IN-MadhurNeural` through Edge TTS and writes the measured line times to `score.json`. Validate with `node engine/director/validate_score.mjs examples/documentary/china-india-growth/score.json` from the repository root.

Data was checked on 2026-11-06. Refresh numerical claims and source captures before publishing a later remake.
