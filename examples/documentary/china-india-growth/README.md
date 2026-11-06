# China grew fast. Did India go down?

The first completed `/documentary` film: [watch the 103-second vertical MP4](renders/china-india-documentary.mp4). The one-line prompt was `/documentary how china grow so fast and indian go down`. The film treats “India went down” as a question and explains the difference between accumulated income and current annual growth.

## Project files

- [Full Hindi narration and shot instructions](SCRIPT.md)
- [Source ledger, numerical checks and limits](RESEARCH.md)
- [Voice-locked 11-beat production score](score.json)
- [Unedited World Bank data page capture](evidence/world-bank-data-page-tall.png), with a readable crop inserted in beat 2
- [Four original 3D illustrated scene plates](assets/), generated for this film and animated with code
- [Final storyboard](renders/final-storyboard.jpg), [sidecar Hindi captions](renders/captions.srt), and [narrator WAV](voice/narration.wav)
- [Voice builder](build_voice.py) and [animation renderer](render_video.py)

The uploaded snakebite reference informed the type, chapter colors, tactile illustrated scenes and cause-and-effect edit. No source-video frame appears in the output. The World Bank page is evidence for its own values; the miniature scenes are illustrations.

## Rebuild

Install `requirements.txt` into the chosen Python environment, then run `python build_voice.py` and `python render_video.py`. The voice builder uses Microsoft's `hi-IN-MadhurNeural` synthetic voice through Edge TTS, trims unusually long sentence gaps, and writes exact beat times back to `score.json`. The renderer creates charts, paths, large headline cards, ambient sound and MP4 locally using Pillow and FFmpeg through `imageio-ffmpeg`. `python render_video.py --stills` makes one still from each beat.

## QA and scope

The exported MP4 was checked at 1080 × 1920, 24 fps, 103.33 seconds, H.264/AAC. The score passed `engine/director/validate_score.mjs`. Automated audio inspection found zero silent stretches longer than 0.6 seconds at −38 dB. A rendered storyboard and key frames were inspected for the source insert, chart labels, chapter changes and legibility. The narration is synthetic and was checked for timing and continuity; no claim of a human-audited pronunciation pass is made. Data was checked on 2026-11-06 and should be refreshed for future reuse.
