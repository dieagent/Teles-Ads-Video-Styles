"""Generate and lock the Hindi narrator to the documentary score.

Requires edge-tts, numpy, soundfile and imageio-ffmpeg. Run from any directory:
    python build_voice.py
The chosen voice is Microsoft's Hindi neural narrator; no voice clone is used.
"""

import asyncio
import json
import re
import subprocess
from pathlib import Path

import edge_tts
import imageio_ffmpeg
import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parent
SCORE = ROOT / "score.json"
VOICE = ROOT / "voice"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
RATE = 24000
PAUSE = 0.16


def srt_time(seconds):
    milliseconds = round(seconds * 1000)
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    secs, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"


def write_captions(score):
    """Keep the optional sidecar captions aligned when the voice is rebuilt."""
    cues = []
    for beat in score["beats"]:
        sentences = [s.strip() for s in re.findall(r"[^।?!;]+[।?!;]?", beat["voice"]) if s.strip()]
        lengths = [max(1, len(s)) for s in sentences]
        total = sum(lengths)
        start, end = beat["start"], beat["end"]
        cursor = start
        for index, (sentence, length) in enumerate(zip(sentences, lengths)):
            following = end if index == len(sentences) - 1 else cursor + (end - start) * length / total
            cues.append((cursor, following, sentence))
            cursor = following
    renders = ROOT / "renders"
    renders.mkdir(exist_ok=True)
    body = "\n\n".join(
        f"{i}\n{srt_time(start)} --> {srt_time(end)}\n{line}"
        for i, (start, end, line) in enumerate(cues, 1)
    )
    (renders / "captions.srt").write_text(body + "\n", encoding="utf-8")


async def speak(beat, sem):
    target = VOICE / f"{beat['id'].lower()}.mp3"
    async with sem:
        for attempt in range(3):
            try:
                await edge_tts.Communicate(
                    beat["voice"], "hi-IN-MadhurNeural", rate="+0%"
                ).save(str(target))
                return target
            except Exception:
                if attempt == 2:
                    raise
                await asyncio.sleep(2 + attempt * 2)


def decode_trim(path):
    result = subprocess.run(
        [FFMPEG, "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", str(RATE), "-"],
        check=True,
        capture_output=True,
    )
    audio = np.frombuffer(result.stdout, dtype="<f4").copy()
    cumulative = np.concatenate(([0.0], np.cumsum(np.abs(audio), dtype=np.float64)))
    envelope = (cumulative[240:] - cumulative[:-240]) / 240
    active = np.flatnonzero(envelope > 0.002)
    if active.size:
        a = max(0, int(active[0]) - int(0.07 * RATE))
        b = min(len(audio), int(active[-1]) + 240 + int(0.10 * RATE))
        audio = audio[a:b]
    # Edge's neural voice adds near-one-second gaps after punctuation. Retain a
    # natural breath, but close those gaps so animation stays tied to speech.
    window = 240  # 10 ms at 24 kHz
    count = len(audio) // window
    energy = np.mean(np.abs(audio[:count * window].reshape(count, window)), axis=1)
    quiet = energy < 0.003
    starts = np.flatnonzero(np.diff(np.r_[False, quiet, False].astype(np.int8)) == 1)
    ends = np.flatnonzero(np.diff(np.r_[False, quiet, False].astype(np.int8)) == -1)
    cuts = []
    for start, end in zip(starts, ends):
        if (end - start) * 0.01 > 0.55:
            mid = (start + end) // 2
            cuts.append((int((start + 14) * window), int((end - 14) * window)))
    if cuts:
        chunks = []
        cursor = 0
        for start, end in cuts:
            chunks.append(audio[cursor:start])
            cursor = end
        chunks.append(audio[cursor:])
        audio = np.concatenate(chunks)
    return audio


async def main():
    VOICE.mkdir(exist_ok=True)
    score = json.loads(SCORE.read_text(encoding="utf-8"))
    beats = score["beats"]
    sem = asyncio.Semaphore(3)
    paths = await asyncio.gather(*(speak(beat, sem) for beat in beats))
    pieces = []
    cursor = 0
    for beat, path in zip(beats, paths):
        audio = decode_trim(path)
        beat["start"] = round(cursor / RATE, 3)
        pieces.append(audio)
        cursor += len(audio)
        beat["end"] = round(cursor / RATE, 3)
        pieces.append(np.zeros(int(PAUSE * RATE), dtype=np.float32))
        cursor += int(PAUSE * RATE)
        print(f"{beat['id']}: {beat['start']:.2f}–{beat['end']:.2f}s")
    full = np.concatenate(pieces)
    peak = max(float(np.max(np.abs(full))), 1e-6)
    full = full * min(0.82 / peak, 1.0)
    sf.write(VOICE / "narration.wav", full, RATE, subtype="PCM_16")
    score["timing"] = {"status": "voice_locked", "voiceFile": "voice/narration.wav", "voice": "hi-IN-MadhurNeural", "rate": "+0%"}
    score["targetSeconds"] = round(len(full) / RATE, 3)
    SCORE.write_text(json.dumps(score, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_captions(score)
    print(f"Voice locked: {len(full)/RATE:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
