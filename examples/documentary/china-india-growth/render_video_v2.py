"""Reference-paced documentary edit: 35 voice-locked object-led shots.

Usage: python render_video_v2.py --stills | python render_video_v2.py
The first version remains in render_video.py for comparison.
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
ASSETS = ROOT / "assets" / "v2"
RENDERS = ROOT / "renders"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
SCORE = json.loads((ROOT / "score.json").read_text(encoding="utf-8"))
PLAN = json.loads((ROOT / "shot_plan_v2.json").read_text(encoding="utf-8"))
SHOTS = PLAN["shots"]
W, H, FPS = 720, 1280, 24
PAPER = (244, 234, 207)
GOLD = (245, 174, 50)
RED = (198, 47, 46)
GREEN = (83, 188, 145)
BLUE = (88, 162, 209)
FONT_PATH = Path(__file__).resolve().parents[3] / "engine" / "fonts" / "Oswald-Variable.ttf"
F57 = ImageFont.truetype(str(FONT_PATH), 57)
F48 = ImageFont.truetype(str(FONT_PATH), 48)
F38 = ImageFont.truetype(str(FONT_PATH), 38)
F27 = ImageFont.truetype(str(FONT_PATH), 27)
F22 = ImageFont.truetype(str(FONT_PATH), 22)

ASSET_FILES = {
    "opening-diorama": ROOT / "assets" / "opening-diorama.png",
    "world-bank-page": ROOT / "evidence" / "world-bank-data-page-tall.png",
    "farm": ASSETS / "farm.png",
    "coastal-globe": ASSETS / "coastal-globe.png",
    "factory-line": ASSETS / "factory-line.png",
    "cargo-lift": ASSETS / "cargo-lift.png",
    "growth-loop": ASSETS / "growth-loop.png",
    "reform-file": ASSETS / "reform-file.png",
    "it-office": ASSETS / "it-office.png",
    "worker-gap": ASSETS / "worker-gap.png",
    "speed-distance": ASSETS / "speed-distance.png",
    "jobs-choice": ASSETS / "jobs-choice.png",
}
SOURCE = {key: Image.open(path).convert("RGB") for key, path in ASSET_FILES.items()}
WB = SOURCE["world-bank-page"]
WB_INCOME = WB.crop((47, 1285, 750, 1464))


def clamp(value, low=0.0, high=1.0):
    return max(low, min(high, value))


def ease(value):
    value = clamp(value)
    return value * value * (3 - 2 * value)


def shot_at(t):
    for shot in SHOTS:
        if t < shot["end"]:
            return shot
    return SHOTS[-1]


CAMERA = {
    "gauge-left": (0.30, 0.69, 1.13, -0.02, 0.01),
    "gauge-right": (0.69, 0.69, 1.13, 0.02, 0.01),
    "needle-india": (0.30, 0.69, 1.13, -0.02, 0.01),
    "rise-india": (0.68, 0.70, 1.06, -0.02, -0.02),
    "seedling": (0.53, 0.74, 1.10, 0.02, -0.02),
    "farm-hand": (0.59, 0.77, 1.18, -0.02, -0.02),
    "ports": (0.59, 0.68, 1.10, 0.01, -0.02),
    "factory-light": (0.57, 0.70, 1.07, 0.01, 0.02),
    "conveyor": (0.55, 0.80, 1.17, -0.01, 0.01),
    "container": (0.58, 0.68, 1.13, 0.01, -0.02),
    "ship-route": (0.57, 0.70, 1.05, 0.02, -0.02),
    "loop-first": (0.50, 0.72, 1.05, 0.02, -0.02),
    "loop-second": (0.66, 0.65, 1.13, -0.02, 0.02),
    "loop-full": (0.50, 0.72, 1.04, 0.01, -0.02),
    "file-open": (0.42, 0.75, 1.10, 0.02, -0.02),
    "gate": (0.73, 0.64, 1.13, -0.03, -0.01),
    "data-cables": (0.52, 0.70, 1.08, 0.02, -0.02),
    "office": (0.46, 0.75, 1.17, 0.02, -0.02),
    "worker": (0.40, 0.78, 1.17, 0.02, -0.01),
    "bridge": (0.66, 0.67, 1.15, -0.03, 0.01),
    "choice-book": (0.32, 0.76, 1.14, 0.01, -0.02),
    "choice-machine": (0.53, 0.68, 1.14, 0.01, -0.02),
    "choice-truck": (0.73, 0.76, 1.14, -0.02, -0.02),
}


def camera_image(shot, progress):
    src = SOURCE[shot["asset"]]
    if shot["asset"] == "world-bank-page":
        return Image.new("RGBA", (W, H), (23, 34, 34, 255))
    cx, cy, zoom, dx, dy = CAMERA.get(shot["action"], (0.52, 0.66, 1.05, 0.015, -0.015))
    # 9:16 crop, then a small perspective push; each shot has its own target.
    sw, sh = src.size
    ratio = W / H
    crop_h = min(sh, int(sh / zoom))
    crop_w = min(sw, int(crop_h * ratio))
    if crop_w > sw:
        crop_w = sw
        crop_h = int(crop_w / ratio)
    cx = clamp(cx + dx * progress, 0.20, 0.80)
    cy = clamp(cy + dy * progress, 0.27, 0.78)
    x = int(clamp(sw * cx - crop_w / 2, 0, sw - crop_w))
    y = int(clamp(sh * cy - crop_h / 2, 0, sh - crop_h))
    img = src.crop((x, y, x + crop_w, y + crop_h)).resize((W, H), Image.Resampling.BICUBIC)
    # Darken the headline corner while preserving the lit object.
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for yy in range(470):
        d.line((0, yy, W, yy), fill=(3, 7, 9, int(66 * (1 - yy / 470))))
    out = img.convert("RGBA")
    out.alpha_composite(layer)
    return out


def halo(draw, x, y, radius, color, alpha=150):
    for r, a in [(radius + 18, 25), (radius + 8, 45), (radius, alpha)]:
        draw.ellipse((x-r, y-r, x+r, y+r), outline=(*color, a), width=4)


def path(draw, points, progress, color=GOLD, width=8):
    if progress <= 0:
        return
    lengths = [math.dist(points[i], points[i+1]) for i in range(len(points)-1)]
    remaining = sum(lengths) * clamp(progress)
    out = [points[0]]
    for i, length in enumerate(lengths):
        if remaining >= length:
            out.append(points[i+1])
            remaining -= length
        else:
            q = remaining / max(length, 1)
            out.append((int(points[i][0] * (1-q) + points[i+1][0] * q), int(points[i][1] * (1-q) + points[i+1][1] * q)))
            break
    if len(out) > 1:
        draw.line(out, fill=(*color, 48), width=width+17, joint="curve")
        draw.line(out, fill=(*color, 230), width=width, joint="curve")
        x, y = out[-1]
        draw.ellipse((x-9, y-9, x+9, y+9), fill=(*PAPER, 255))


def pillar(draw, x, bottom, height, color, label=None):
    width, depth = 88, 22
    y = bottom - height
    draw.polygon([(x, y), (x+width, y), (x+width+depth, y-depth), (x+depth, y-depth)], fill=(*PAPER, 215))
    draw.polygon([(x+width, y), (x+width+depth, y-depth), (x+width+depth, bottom-depth), (x+width, bottom)], fill=(*color, 137))
    draw.rectangle((x, y, x+width, bottom), fill=(*color, 232))
    if label:
        draw.text((x-3, bottom+17), label, font=F27, fill=PAPER)


def heading(draw, shot, p):
    value = shot["headline"]
    if not value or shot["action"] == "evidence":
        return
    words = value.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=F57) > 588 and current:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    font = F57 if len(lines) <= 2 else F48
    offset = int(-28 * (1 - ease(p / 0.17)))
    for i, line in enumerate(lines):
        col = PAPER if i == 0 else (RED if "DOWN" in value or "GAP" in value else GOLD)
        y = 182 + i * (73 if font == F57 else 64)
        draw.text((68+offset+2, y+3), line, font=font, fill=(5, 7, 7, 200))
        draw.text((68+offset, y), line, font=font, fill=col)


def action_overlay(shot, p, base):
    act = shot["action"]
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    q = ease(p)
    if act in ("gauge-left", "gauge-right", "needle-india"):
        x = 205 if act != "gauge-right" else 530
        y = 905
        angle = math.radians(165 - 110*q if act == "needle-india" else 150 - 70*q)
        x2 = x + 94 * math.cos(angle)
        y2 = y - 94 * math.sin(angle)
        halo(d, x, y, 89, GREEN if act == "needle-india" else GOLD, 75)
        d.line((x, y, x2, y2), fill=(*(GREEN if act == "needle-india" else GOLD), 250), width=8)
    elif act in ("rise-india", "pillars"):
        if act == "rise-india":
            path(d, [(490, 1020), (517, 951), (545, 882)], q, GREEN, 7)
        else:
            pillar(d, 165, 1060, int(360*q), GOLD, "CHINA")
            pillar(d, 452, 1060, int(230*q), GREEN, "INDIA")
    elif act in ("bars-1990", "bars-2025"):
        d.rounded_rectangle((65, 655, 657, 1087), radius=17, fill=(9, 16, 19, 212))
        d.text((91, 684), "GDP PER PERSON  ·  CURRENT US$", font=F27, fill=PAPER)
        if act == "bars-1990":
            pillar(d, 175, 988, int(190*q), GOLD, "CHINA")
            pillar(d, 440, 988, int(217*q), GREEN, "INDIA")
            if q > .66:
                d.text((169, 756), "$319", font=F38, fill=PAPER)
                d.text((436, 731), "$371", font=F38, fill=PAPER)
        else:
            pillar(d, 175, 988, int(326*q), GOLD, "CHINA")
            pillar(d, 440, 988, int(72*q), GREEN, "INDIA")
            if q > .66:
                d.text((140, 617), "$13,862", font=F38, fill=PAPER)
                d.text((436, 861), "$2,703", font=F38, fill=PAPER)
    elif act == "evidence":
        d.rectangle((0, 0, W, H), fill=(14, 11, 9, 110))
        d.rounded_rectangle((35, 331, 685, 1007), radius=12, fill=(243, 239, 229, 250))
        d.text((69, 363), "WORLD BANK GROUP  /  DATA", font=F27, fill=(15, 51, 73))
        d.text((69, 409), "GDP PER PERSON", font=F38, fill=(19, 29, 34))
        crop = ImageOps.contain(WB_INCOME, (600, 210), Image.Resampling.LANCZOS).convert("RGBA")
        base.alpha_composite(layer)
        base.alpha_composite(crop, (60, 493))
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        d.line((69, 706, 649, 706), fill=(*GOLD, 220), width=4)
        d.text((69, 737), "CHINA", font=F27, fill=(34, 42, 43))
        d.text((69, 780), "$13,862", font=F48, fill=(165, 63, 35))
        d.text((387, 737), "INDIA", font=F27, fill=(34, 42, 43))
        d.text((387, 780), "$2,703", font=F48, fill=(28, 105, 92))
        d.text((69, 927), "CURRENT US$  ·  2025", font=F27, fill=(34, 42, 43))
    elif act == "scale":
        d.rounded_rectangle((65, 720, 653, 1009), radius=17, fill=(23, 28, 24, 205))
        d.text((101, 761), "GDP / PERSON", font=F38, fill=GOLD)
        d.line((101, 831, 601, 831), fill=(*PAPER, 155), width=3)
        d.text((101, 854), "ONE ECONOMIC MEASURE", font=F27, fill=PAPER)
    elif act in ("seedling", "farm-hand"):
        for n, x in enumerate((174, 266, 360, 458, 558)):
            height = int((35 + 20*n) * ease((p - n*.11)/.57))
            d.line((x, 1130, x+8, 1130-height), fill=(*GREEN, 190), width=5)
            d.ellipse((x+2, 1127-height, x+16, 1141-height), fill=(*GREEN, 170))
    elif act == "ports":
        for n, (x,y) in enumerate(((318,712),(392,795),(451,859),(490,951))):
            if p > n*.17:
                halo(d, x, y, 9, GOLD, 240)
    elif act == "factory-light":
        for n in range(5):
            x = 83+n*124
            y = int(865+40*math.sin((p*2+n/4)*math.pi))
            halo(d,x,y,9,GOLD,185)
    elif act == "conveyor":
        x = int(70+500*q)
        y = int(1010-100*q)
        d.polygon([(x,y),(x+64,y-14),(x+105,y+2),(x+42,y+18)],fill=(210,156,86,238))
        d.polygon([(x,y),(x+42,y+18),(x+42,y+67),(x,y+48)],fill=(140,80,43,240))
        d.polygon([(x+42,y+18),(x+105,y+2),(x+105,y+52),(x+42,y+67)],fill=(185,105,55,240))
    elif act == "container":
        # Trace the suspended container already present in the source plate.
        # A second painted container looked like a floating UI box.
        y = int(760-18*q)
        d.line((387, 474, 387, y), fill=(239, 190, 113, 100), width=3)
        d.line((235, 758, 539, 758), fill=(*GOLD, int(80+130*q)), width=5)
    elif act in ("loop-first", "loop-second", "loop-full"):
        pts=[(115,978),(235,890),(392,842),(591,741)]
        path(d,pts,q,GOLD,7)
        if act != "loop-first":
            path(d,[(591,741),(527,559),(325,611),(115,978)],ease((p-.22)/.77),GOLD,5)
    elif act == "ship-route":
        path(d,[(155,922),(311,843),(485,690),(609,581)],q,GOLD,7)
    elif act == "file-open":
        yy=int(900-170*q)
        d.polygon([(210,yy),(486,yy),(511,yy+219),(232,yy+219)], fill=(230,205,154,215),outline=(90,58,33,235))
        d.text((280,yy+55),"1991",font=F57,fill=(110,53,36))
    elif act == "gate":
        for n in range(5):
            x=390+n*45
            d.line((x,586,x+42*q,1027),fill=(*GOLD,int(150*q)),width=5)
    elif act in ("data-cables", "office"):
        pts=[(150,996),(271,911),(352,783),(507,637),(563,486)]
        path(d,pts,q,BLUE,7)
    elif act == "worker":
        halo(d,392,928,int(28+23*q),GOLD,105)
    elif act == "bridge":
        path(d,[(62,846),(215,843),(342,782)],q,RED,7)
        halo(d,356,769,20,RED,230)
    elif act in ("bar-india", "bar-china", "bars-current"):
        d.rounded_rectangle((65,642,655,1072),radius=16,fill=(11,21,26,221))
        subtitle="2000–2019  ·  REAL GDP GROWTH" if act != "bars-current" else "2025  ·  REAL GDP GROWTH"
        d.text((88,675),subtitle,font=F27,fill=PAPER)
        a,b=(6.7,9.1) if act != "bars-current" else (7.6,5.0)
        for idx,(x,val,col,name) in enumerate(((156,a,GREEN,"INDIA"),(431,b,GOLD,"CHINA"))):
            h=int(val/10*270*q)
            pillar(d,x,962,h,col,name)
            if p>.58:
                d.text((x-7,896-h),f"{val:.1f}%",font=F38,fill=PAPER)
    elif act == "distance":
        pillar(d,163,1080,int(360*q),GOLD,"CHINA")
        pillar(d,445,1080,int(106*q),GREEN,"INDIA")
        d.text((98,652),"TODAY'S SPEED",font=F27,fill=PAPER)
        d.text((98,689),"≠ DECADES OF DISTANCE",font=F27,fill=GOLD)
    elif act.startswith("choice-"):
        x,y={"choice-book":(181,880),"choice-machine":(365,743),"choice-truck":(557,913)}[act]
        halo(d,x,y,int(54+25*q),GOLD,205)
    base.alpha_composite(layer)


def frame_at(time):
    shot=shot_at(time)
    progress=clamp((time-shot["start"])/max(shot["end"]-shot["start"],.05))
    frame=camera_image(shot,progress)
    action_overlay(shot,progress,frame)
    if shot["action"]!="evidence":
        heading(ImageDraw.Draw(frame),shot,progress)
    # The reference has a fine film crease, not a bright dividing rule.
    grain=Image.new("RGBA",(W,H),(0,0,0,0))
    gd=ImageDraw.Draw(grain)
    gd.line((360,0,360,H),fill=(234,208,165,22),width=1)
    frame.alpha_composite(grain)
    return frame.convert("RGB")


def make_audio():
    voice,sr=sf.read(ROOT/"voice"/"narration.wav",dtype="float32")
    n=len(voice)
    t=np.arange(n,dtype=np.float32)/sr
    music=np.zeros(n,dtype=np.float32)
    # Slow minor-to-major harmonic chapters; voice stays well in front.
    chapters=[(0,32.94,(110.0,164.8,220.0)),(32.94,51.48,(98.0,146.8,196.0)),(51.48,85.66,(92.5,138.6,185.0)),(85.66,117.59,(123.5,185.0,246.9))]
    for start,end,frequencies in chapters:
        a=max(0,int(start*sr)); b=min(n,int(end*sr))
        if b<=a:continue
        tt=t[a:b]
        pad=sum(np.sin(2*np.pi*f*tt)*w for f,w in zip(frequencies,(1,.5,.25)))
        envelope=.5+.5*np.sin(2*np.pi*.13*tt)
        music[a:b]+=.007*pad*envelope
    for shot in SHOTS[1:]:
        a=int(shot["start"]*sr)
        nn=min(int(.21*sr),n-a)
        if nn<=0:continue
        tt=np.arange(nn,dtype=np.float32)/sr
        click=.019*np.exp(-19*tt)*np.sin(2*np.pi*(95-50*tt)*tt)
        music[a:a+nn]+=click
    # Subtle moving factory pulse and India data shimmer, below speech.
    for start,end,period in ((32.94,51.48,.62),(51.48,73.17,.85)):
        for when in np.arange(start,end,period):
            a=int(when*sr); nn=min(int(.11*sr),n-a)
            tt=np.arange(nn,dtype=np.float32)/sr
            music[a:a+nn]+=.003*np.exp(-29*tt)*np.sin(2*np.pi*1100*tt)
    full=np.clip(voice+music,-.98,.98)
    sf.write(RENDERS/"mix-v2.wav",full,sr,subtype="PCM_16")


def stills():
    RENDERS.mkdir(exist_ok=True)
    sheet=Image.new("RGB",(7*180,5*320),(8,11,13))
    for i,shot in enumerate(SHOTS):
        mid=(shot["start"]+shot["end"])/2
        frame=frame_at(mid)
        frame.save(RENDERS/f"v2-shot-{i+1:02d}.jpg",quality=90)
        sheet.paste(frame.resize((180,320),Image.Resampling.LANCZOS),((i%7)*180,(i//7)*320))
    sheet.save(RENDERS/"v2-storyboard.jpg",quality=90)
    print("Wrote 35 shot stills and contact sheet")


def render():
    RENDERS.mkdir(exist_ok=True)
    make_audio()
    output=RENDERS/"china-india-documentary-v2.mp4"
    cmd=[FFMPEG,"-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i",str(RENDERS/"mix-v2.wav"),"-vf","scale=1080:1920:flags=lanczos","-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-movflags","+faststart","-shortest",str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    total=math.ceil(SCORE["targetSeconds"]*FPS)
    for index in range(total):
        frame=frame_at(index/FPS)
        try: proc.stdin.write(frame.tobytes())
        except BrokenPipeError: raise RuntimeError(proc.stderr.read().decode(errors="replace"))
        if index%(FPS*10)==0: print(f"v2 {index/FPS:.0f}/{SCORE['targetSeconds']:.0f}s",flush=True)
    proc.stdin.close()
    err=proc.stderr.read().decode(errors="replace")
    if proc.wait()!=0: raise RuntimeError(err)
    print(output)


if __name__=="__main__":
    stills() if "--stills" in sys.argv else render()
