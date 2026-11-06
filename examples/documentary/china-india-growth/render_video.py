"""Render the /documentary China–India short from a locked score and original assets.

Run `python render_video.py`. Requires Pillow, numpy, soundfile, imageio-ffmpeg.
The compositing is code-native: scene plates, all charts, paths, typography and motion
are generated locally. Source imagery stays in evidence/ and is credited onscreen.
"""

import json
import math
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
RENDERS = ROOT / "renders"
VOICE = ROOT / "voice"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS = 720, 1280, 24
WHITE = (248, 241, 221)
AMBER = (245, 172, 46)
TEAL = (81, 215, 188)
RED = (228, 76, 65)
FONT = Path(__file__).resolve().parents[3] / "engine" / "fonts" / "Oswald-Variable.ttf"
F72 = ImageFont.truetype(str(FONT), 78)
F54 = ImageFont.truetype(str(FONT), 54)
F42 = ImageFont.truetype(str(FONT), 42)
F29 = ImageFont.truetype(str(FONT), 29)
F22 = ImageFont.truetype(str(FONT), 22)

score = json.loads((ROOT / "score.json").read_text(encoding="utf-8"))
beats = score["beats"]
duration = score["targetSeconds"]


def fitted(path):
    src = Image.open(path).convert("RGB")
    return ImageOps.fit(src, (W + 76, H + 130), method=Image.Resampling.LANCZOS)


plates = {
    "opening": fitted(ASSETS / "opening-diorama.png"),
    "reform": fitted(ASSETS / "china-reform.png"),
    "export": fitted(ASSETS / "export-chain.png"),
    "india": fitted(ASSETS / "india-path.png"),
}
plate_for = ["opening", "opening", "reform", "export", "export", "india", "india", "opening", "opening", "opening", "india"]

raw_page = Image.open(ROOT / "evidence" / "world-bank-data-page-tall.png").convert("RGB")
# Actual economic rows of the original, untouched World Bank page capture.
evidence = raw_page.crop((44, 1210, 750, 1470))
evidence = ImageOps.contain(evidence, (610, 400), method=Image.Resampling.LANCZOS)

topshade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
shade = ImageDraw.Draw(topshade)
for y in range(H):
    alpha = int(132 * max(0, 1 - y / 650) + 46 * (y / H))
    shade.line((0, y, W, y), fill=(4, 9, 16, alpha))


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def text_shadow(draw, xy, value, font, fill, stroke=0):
    x, y = xy
    draw.text((x + 3, y + 4), value, font=font, fill=(0, 0, 0, 180), stroke_width=stroke)
    draw.text((x, y), value, font=font, fill=fill, stroke_width=stroke)


def rounded_label(draw, box, label, fill, fg=WHITE, font=F22):
    draw.rounded_rectangle(box, radius=9, fill=fill, outline=(255, 255, 255, 55), width=2)
    draw.text((box[0] + 13, box[1] + 8), label, font=font, fill=fg)


def line_progress(draw, pts, progress, color=AMBER, width=8, glow=True):
    if progress <= 0:
        return
    lengths = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    target = sum(lengths) * clamp(progress)
    out = [pts[0]]
    for i, length in enumerate(lengths):
        if target >= length:
            out.append(pts[i + 1])
            target -= length
        else:
            q = target / max(length, 1)
            out.append((int(pts[i][0] * (1 - q) + pts[i + 1][0] * q), int(pts[i][1] * (1 - q) + pts[i + 1][1] * q)))
            break
    if len(out) > 1:
        if glow:
            draw.line(out, fill=(*color, 65), width=width + 14, joint="curve")
        draw.line(out, fill=(*color, 255), width=width, joint="curve")
        x, y = out[-1]
        draw.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(*WHITE, 255))


def scene_base(i, p):
    base = plates[plate_for[i]]
    x = int(38 + 13 * math.sin(p * math.pi * 2 + i))
    y = int(55 - 20 * p)
    frame = base.crop((x, y, x + W, y + H)).convert("RGBA")
    frame.alpha_composite(topshade)
    return frame


def top_card(draw, beat, p, i):
    words = beat["caption"].replace(" → ", " / ").split()
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=F72) > 610 and current:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    if len(lines) > 3:
        lines = [" ".join(words[:2]), " ".join(words[2:])]
    font = F72 if max((draw.textlength(s, font=F72) for s in lines), default=0) <= 635 else F54
    slide = int((1 - smooth(p / 0.07)) * -170)
    for n, line in enumerate(lines):
        color = WHITE if n == 0 else (TEAL if i in (5, 6, 8, 10) else AMBER)
        text_shadow(draw, (58 + slide, 146 + n * 89), line, font, color)


def source_tag(draw, label):
    draw.rounded_rectangle((52, 1184, 665, 1237), radius=8, fill=(4, 11, 17, 190))
    draw.text((66, 1193), label, font=F22, fill=WHITE)


def draw_scene(i, p, frame):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    if i == 0:
        line_progress(d, [(173, 1030), (215, 973), (247, 895)], smooth(p / 0.70), AMBER, 9)
        line_progress(d, [(530, 1030), (551, 986), (581, 935)], smooth((p - 0.10) / 0.70), TEAL, 9)
        if p > 0.64:
            rounded_label(d, (310, 770, 597, 844), "INDIA IS RISING", (12, 48, 49, 230), TEAL, F29)
    elif i == 1:
        d.rounded_rectangle((58, 540, 660, 1070), radius=24, fill=(5, 13, 18, 226))
        label = "1990  ·  CURRENT US$" if p < 0.45 else "2025  ·  CURRENT US$"
        d.text((89, 573), label, font=F29, fill=WHITE)
        first = smooth(p / 0.22)
        second = smooth((p - 0.45) / 0.26)
        h1 = int((105 * (1 - second) + 345 * second) * first)
        h2 = int((120 * (1 - second) + 68 * second) * first)
        for x, h, color, name in [(184, h1, AMBER, "CHINA"), (447, h2, TEAL, "INDIA")]:
            d.rounded_rectangle((x, 962 - h, x + 107, 962), radius=8, fill=(*color, 245))
            d.text((x - 4, 976), name, font=F29, fill=WHITE)
        value1, value2 = ("$319", "$371") if p < 0.45 else ("$13,862", "$2,703")
        d.text((168, 905 - h1), value1, font=F29, fill=WHITE)
        d.text((430, 905 - h2), value2, font=F29, fill=WHITE)
        if p > 0.68:
            appear = smooth((p - 0.68) / 0.12)
            d.rounded_rectangle((58, 540, 663, 1070), radius=13, fill=(12, 20, 25, int(255 * appear)))
            d.text((82, 572), "WORLD BANK DATA  ·  CHINA / INDIA", font=F29, fill=WHITE)
            page = evidence.convert("RGBA")
            page.putalpha(int(255 * appear))
            overlay.alpha_composite(page, (65, 680))
            d.text((82, 1005), "GDP PER PERSON  ·  CURRENT US$  ·  2025", font=F22, fill=WHITE)
        source_tag(d, "WORLD BANK WDI  ·  GDP PER PERSON")
    elif i == 2:
        line_progress(d, [(138, 1090), (292, 894), (415, 706), (582, 616)], smooth(p), AMBER, 7)
        rounded_label(d, (67, 982, 258, 1041), "1978  REFORM", (36, 32, 22, 220), WHITE, F22)
        if p > 0.48:
            rounded_label(d, (460, 638, 646, 697), "1980  ZONES", (36, 32, 22, 220), WHITE, F22)
        source_tag(d, "WORLD BANK  ·  CHINA PORTS / REFORMS")
    elif i == 3:
        line_progress(d, [(140, 1020), (350, 975), (560, 827), (608, 585)], smooth(p), AMBER, 9)
        for t, xy, label in [(0.16, (100, 1020), "MAKE"), (0.45, (319, 955), "LOAD"), (0.72, (505, 775), "SHIP")]:
            if p > t:
                rounded_label(d, (xy[0], xy[1], xy[0] + 110, xy[1] + 48), label, (20, 25, 23, 225), WHITE, F22)
    elif i == 4:
        for n, (x, y, txt) in enumerate([(88, 663, "EXPORTS"), (257, 872, "INVEST"), (487, 655, "PORTS")]):
            q = smooth((p - 0.15 * n) / 0.25)
            if q:
                d.ellipse((x - 15, y - 12, x + 160, y + 84), fill=(6, 20, 19, int(225 * q)), outline=(*AMBER, int(235 * q)), width=3)
                d.text((x + 9, y + 8), txt, font=F29, fill=(*WHITE, int(255 * q)))
        line_progress(d, [(220, 710), (329, 872), (490, 706), (220, 710)], smooth((p - 0.30) / 0.64), AMBER, 6)
        source_tag(d, "MECHANISM FROM WORLD BANK PORT STUDY")
    elif i == 5:
        line_progress(d, [(116, 1070), (250, 914), (364, 745)], smooth(p), TEAL, 7)
        rounded_label(d, (66, 962, 258, 1022), "1991  REFORM", (9, 43, 46, 230), WHITE, F22)
        if p > 0.48:
            rounded_label(d, (255, 730, 490, 793), "SERVICES + IT", (9, 43, 46, 230), TEAL, F29)
        source_tag(d, "WORLD BANK  ·  INDIA ECONOMIC MEMORANDUM")
    elif i == 6:
        d.rounded_rectangle((58, 799, 665, 1040), radius=20, fill=(6, 18, 27, 224))
        for n, (x, txt) in enumerate([(83, "SKILLS"), (294, "FACTORY"), (506, "JOBS")]):
            q = smooth((p - n * 0.15) / 0.18)
            if q:
                d.rounded_rectangle((x, 862, x + 144, 949), radius=10, fill=(23, 68, 68, int(245 * q)), outline=(*TEAL, int(255 * q)), width=3)
                d.text((x + 12, 880), txt, font=F29, fill=(*WHITE, int(255 * q)))
        line_progress(d, [(226, 906), (291, 906)], smooth((p - 0.40) / 0.25), TEAL, 4)
        if p > 0.68:
            for x in (442, 464, 486):
                d.ellipse((x, 900, x + 8, 908), fill=RED)
        source_tag(d, "WORLD BANK  ·  SERVICE-LED GROWTH")
    elif i == 7:
        d.rounded_rectangle((64, 563, 657, 1064), radius=24, fill=(9, 18, 25, 233))
        d.text((88, 585), "AVERAGE REAL GDP GROWTH", font=F29, fill=WHITE)
        d.text((88, 626), "2000–2019", font=F29, fill=AMBER)
        for n, (x, val, color, label) in enumerate([(156, 6.7, TEAL, "INDIA"), (434, 9.1, AMBER, "CHINA")]):
            h = int((val / 10) * 290 * smooth((p - 0.10 - n * 0.12) / 0.42))
            d.rounded_rectangle((x, 976 - h, x + 116, 976), radius=9, fill=(*color, 245))
            d.text((x - 1, 982), label, font=F29, fill=WHITE)
            if h > 80:
                d.text((x + 9, 920 - h), f"{val:.1f}%", font=F42, fill=WHITE)
        source_tag(d, "WORLD BANK  ·  INDIA CEM 2024")
    elif i == 8:
        d.rounded_rectangle((55, 550, 665, 1049), radius=22, fill=(5, 15, 22, 226))
        d.text((82, 570), "2025 GDP GROWTH", font=F29, fill=WHITE)
        for n, (y, val, color, name) in enumerate([(664, 7.6, TEAL, "INDIA"), (790, 5.0, AMBER, "CHINA")]):
            d.text((83, y - 12), name, font=F29, fill=WHITE)
            width = int(350 * val / 8 * smooth((p - n * 0.12) / 0.40))
            d.rounded_rectangle((220, y, 220 + width, y + 54), radius=9, fill=(*color, 245))
            d.text((568, y + 3), f"{val:.1f}%", font=F29, fill=WHITE)
        if p > 0.64:
            opacity = int(230 * smooth((p - 0.64) / 0.20))
            d.rounded_rectangle((65, 918, 653, 1032), radius=12, fill=(9, 30, 36, opacity))
            d.text((92, 944), "SPEED  ≠  DISTANCE", font=F42, fill=(*WHITE, opacity))
        source_tag(d, "WORLD BANK DATA  ·  2025 ANNUAL GROWTH")
    elif i == 9:
        line_progress(d, [(197, 992), (273, 901), (366, 747), (430, 613)], smooth(p), AMBER, 8)
        line_progress(d, [(516, 1118), (539, 1030), (581, 936)], smooth(p), TEAL, 8)
        if p > 0.57:
            rounded_label(d, (77, 1028, 641, 1091), "INDIA GREW. CHINA BUILT A LEAD.", (11, 29, 33, 232), WHITE, F29)
    elif i == 10:
        d.rounded_rectangle((64, 704, 653, 1059), radius=20, fill=(5, 22, 31, 226))
        for n, (txt, y, color) in enumerate([("SKILLS", 745, TEAL), ("FACTORIES", 840, AMBER), ("LOGISTICS", 935, WHITE)]):
            if p > n * 0.19:
                a = int(255 * smooth((p - n * 0.19) / 0.18))
                d.ellipse((93, y + 10, 117, y + 34), fill=(*color, a))
                d.text((143, y), txt, font=F42, fill=(*color, a))
        source_tag(d, "SOURCES AND SCRIPT IN PROJECT FOLDER")
    frame.alpha_composite(overlay)


def frame_at(t):
    i = next((j for j, b in enumerate(beats) if t < b["end"] + 0.16), len(beats) - 1)
    beat = beats[i]
    p = clamp((t - beat["start"]) / max(beat["end"] - beat["start"], 0.1))
    frame = scene_base(i, p)
    draw_scene(i, p, frame)
    d = ImageDraw.Draw(frame)
    top_card(d, beat, p, i)
    d.rectangle((0, 0, 9, H), fill=(4, 10, 14, 125))
    d.line((365, 0, 365, H), fill=(66, 72, 70, 255), width=1)
    d.text((58, 58), "TELES ADS  /  DOCUMENTARY", font=F22, fill=(*WHITE, 210))
    d.text((601, 58), f"{i+1:02d}/11", font=F22, fill=(*WHITE, 210))
    return frame.convert("RGB")


def make_mix():
    voice, sr = sf.read(VOICE / "narration.wav", dtype="float32")
    if sr != 24000:
        raise ValueError("Voice sample rate changed")
    n = len(voice)
    t = np.arange(n, dtype=np.float32) / sr
    # Restrained original ambient pad, kept well below spoken words.
    chords = [(110.0, 164.8), (98.0, 146.8), (123.5, 185.0), (92.5, 138.6)]
    music = np.zeros(n, dtype=np.float32)
    for i, beat in enumerate(beats):
        a = int(beat["start"] * sr)
        b = min(n, int((beat["end"] + 0.16) * sr))
        local = np.arange(b - a, dtype=np.float32) / sr
        f1, f2 = chords[(i // 3) % len(chords)]
        bed = (np.sin(2 * np.pi * f1 * local) + 0.54 * np.sin(2 * np.pi * f2 * local)) * 0.0032
        bed *= np.minimum(1, local / 0.5) * np.minimum(1, (b - a - np.arange(b - a)) / (0.6 * sr))
        music[a:b] += bed
        thump_n = int(0.35 * sr)
        start = min(n - thump_n, a)
        x = np.arange(thump_n, dtype=np.float32) / sr
        music[start:start + thump_n] += 0.011 * np.sin(2 * np.pi * (70 - 35 * x) * x) * np.exp(-12 * x)
    mix = np.clip(voice + music, -0.98, 0.98)
    sf.write(RENDERS / "mix.wav", mix, sr, subtype="PCM_16")


def make_srt():
    def stamp(sec):
        ms = int(round(sec * 1000))
        return f"{ms//3600000:02d}:{(ms//60000)%60:02d}:{(ms//1000)%60:02d},{ms%1000:03d}"
    rows = []
    for i, beat in enumerate(beats, 1):
        rows.append(f"{i}\n{stamp(beat['start'])} --> {stamp(beat['end'])}\n{beat['voice']}\n")
    (RENDERS / "captions.srt").write_text("\n".join(rows), encoding="utf-8")


def render():
    RENDERS.mkdir(exist_ok=True)
    make_mix()
    make_srt()
    output = RENDERS / "china-india-documentary.mp4"
    cmd = [FFMPEG, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(RENDERS / "mix.wav"), "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-shortest", str(output)]
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    count = math.ceil(duration * FPS)
    for k in range(count):
        frame = frame_at(k / FPS)
        try:
            process.stdin.write(frame.tobytes())
        except BrokenPipeError:
            raise RuntimeError(process.stderr.read().decode(errors="replace"))
        if k % 240 == 0:
            print(f"render {k/FPS:.1f}/{duration:.1f}s", flush=True)
    process.stdin.close()
    error = process.stderr.read().decode(errors="replace")
    if process.wait() != 0:
        raise RuntimeError(error)
    print(output)


if __name__ == "__main__":
    if "--stills" in sys.argv:
        RENDERS.mkdir(exist_ok=True)
        sheet = Image.new("RGB", (6 * 216, 2 * 384), (7, 13, 19))
        for n, beat in enumerate(beats):
            middle = (beat["start"] + beat["end"]) / 2
            still = frame_at(middle)
            still.save(RENDERS / f"preview-{n+1:02d}.jpg", quality=90)
            sheet.paste(still.resize((216, 384), Image.Resampling.LANCZOS), ((n % 6) * 216, (n // 6) * 384))
        sheet.save(RENDERS / "final-storyboard.jpg", quality=90)
        print("Wrote eleven preview stills and final storyboard")
    else:
        render()
