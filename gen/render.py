import os, sys, math, subprocess, shutil
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
from content import CAROUSELS, REELS, HANDLE

BG = (28, 28, 48); BOX = (42, 42, 69); OR = (255, 90, 54); PU = (80, 68, 212)
WH = (255, 255, 255); GR = (200, 200, 215)
F = "/usr/share/fonts/truetype/dejavu/"
def font(name, size): return ImageFont.truetype(F + name, size)
B = lambda s: font("DejaVuSans-Bold.ttf", s)
R = lambda s: font("DejaVuSans.ttf", s)
M = lambda s: font("DejaVuSansMono.ttf", s)

def wrap(d, text, f, width):
    out = []
    for para in text.split("\n"):
        if not para:
            out.append(""); continue
        line = ""
        for w in para.split(" "):
            t = (line + " " + w).strip()
            if d.textlength(t, font=f) <= width: line = t
            else:
                out.append(line); line = w
        out.append(line)
    return out

def draw_lines(d, x, y, lines, f, fill, gap):
    for l in lines:
        d.text((x, y), l, font=f, fill=fill); y += gap
    return y

def footer(d, i, n, W=1080, H=1350):
    d.text((60, H - 70), HANDLE, font=B(20), fill=GR)
    t = f"{i}/{n}"; d.text((W - 60 - d.textlength(t, font=B(20)), H - 70), t, font=B(20), fill=GR)

def slide(s, i, n):
    W, H = 1080, 1350
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    X, TW = 60, W - 120
    t = s["t"]
    if t in ("cover", "cta"):
        d.ellipse((W - 340, -260, W + 160, 240), fill=OR)
        if t == "cover":
            d.ellipse((W - 160, 650, W + 60, 870), fill=PU)
            d.text((X, 90), s["tag"], font=B(24), fill=WH)
            lines = wrap(d, s["title"], B(76), TW - 80)
            y = 330; y = draw_lines(d, X, y, lines, B(76), WH, 90)
            y = draw_lines(d, X, y + 30, wrap(d, s["sub"], R(36), TW - 160), R(36), GR, 48)
            d.text((X, H - 190), "Desliza  →", font=B(30), fill=OR)
        else:
            lines = wrap(d, s["title"], B(70), TW)
            y = 420; y = draw_lines(d, X, y, lines, B(70), WH, 84)
            y = draw_lines(d, X, y + 25, wrap(d, s["sub"], R(34), TW), R(34), GR, 46)
            y += 50
            d.rounded_rectangle((X, y, W - X, y + 110), radius=14, fill=OR)
            bt = "Enlace en el perfil"; f = B(40)
            d.text(((W - d.textlength(bt, font=f)) / 2, y + 30), bt, font=f, fill=WH)
    else:
        d.rectangle((0, 0, W, 12), fill=OR)
        y = 90
        if t == "prompt":
            f = B(26); bw = d.textlength(s["badge"], font=f)
            d.rounded_rectangle((X, y, X + bw + 40, y + 52), radius=8, fill=OR)
            d.text((X + 20, y + 11), s["badge"], font=f, fill=WH); y += 90
            y = draw_lines(d, X, y, wrap(d, s["h"], B(48), TW), B(48), WH, 60) + 30
            cl = wrap(d, s["code"], M(32), TW - 80)
            d.rounded_rectangle((X - 10, y, W - X + 10, max(y + 60 + len(cl) * 46, H - 180)), radius=18, fill=BOX)
            draw_lines(d, X + 30, y + 40, cl, M(32), (225, 225, 235), 46)
        else:
            y = draw_lines(d, X, y, wrap(d, s["h"], B(50), TW), B(50), OR, 62) + 40
            if t == "text":
                draw_lines(d, X, y, wrap(d, s["body"], R(38), TW), R(38), WH, 54)
            elif t == "list":
                for it in s["items"]:
                    ls = wrap(d, it, R(38), TW - 50)
                    d.ellipse((X, y + 14, X + 18, y + 32), fill=OR)
                    y = draw_lines(d, X + 45, y, ls, R(38), WH, 52) + 26
            elif t == "vs":
                for lab, txt, col in (("NO", s["no"], (120, 120, 140)), ("SÍ", s["si"], OR)):
                    d.rounded_rectangle((X, y, X + 90, y + 54), radius=8, fill=col)
                    d.text((X + 45 - d.textlength(lab, font=B(28)) / 2, y + 11), lab, font=B(28), fill=WH)
                    ls = wrap(d, txt, R(48), TW - 130)
                    y = draw_lines(d, X + 120, y - 2, ls, R(48), WH if lab == "SÍ" else GR, 64) + 90
    footer(d, i, n)
    return im

# ---------- Reels ----------
RW, RH, FPS = 1080, 1920, 30
def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3

def reel_frame(scene, t, dur, prog, idx):
    im = Image.new("RGB", (RW, RH), BG); d = ImageDraw.Draw(im)
    # fondo animado
    a = prog * 2 * math.pi
    cx, cy = RW - 120 + 60 * math.sin(a), 260 + 50 * math.cos(a)
    d.ellipse((cx - 330, cy - 330, cx + 330, cy + 330), fill=OR)
    px, py = 140 + 50 * math.cos(a * 1.3), RH - 420 + 60 * math.sin(a * 1.3)
    d.ellipse((px - 170, py - 170, px + 170, py + 170), fill=PU)
    # barra de progreso
    d.rectangle((0, RH - 14, int(RW * prog), RH), fill=OR)
    d.text((70, RH - 120), HANDLE, font=B(30), fill=GR)
    out = min(1, max(0, (dur - t) / 0.25))  # fade out
    X = 80
    if "code" in scene:
        d.text((X, 520), "COPIA ESTO", font=B(40), fill=OR)
        f = M(44); full = wrap(d, scene["code"], f, RW - 220)
        chars = int(len(scene["code"]) * ease(t / (dur * 0.75)))
        y = 620; d.rounded_rectangle((X - 20, y - 40, RW - X + 20, y + len(full) * 64 + 40), radius=24, fill=BOX)
        n = 0
        for l in full:
            vis = l[:max(0, chars - n)]; n += len(l) + 1
            d.text((X + 20, y), vis, font=f, fill=(230, 230, 240)); y += 64
        return im
    lines = scene["lines"]; big = B(104 if not scene.get("cta") else 92)
    lh = 128 if not scene.get("cta") else 112
    total = len(lines) * lh + (110 if scene.get("small") else 0)
    y0 = (RH - total) // 2 - 40
    for i, l in enumerate(lines):
        k = ease((t - i * 0.18) / 0.4) * out
        if k <= 0: continue
        col = OR if (scene.get("accent") == i and not scene.get("cta")) else WH
        col = tuple(int(BG[j] + (col[j] - BG[j]) * k) for j in range(3))
        dy = int((1 - k) * 60)
        w = d.textlength(l, font=big)
        x = (RW - w) / 2 if scene.get("cta") else X
        d.text((x, y0 + i * lh + dy), l, font=big, fill=col)
    if scene.get("small"):
        k = ease((t - len(lines) * 0.18) / 0.4) * out
        if k > 0:
            y = y0 + len(lines) * lh + 30
            if scene.get("cta"):
                f = B(52); w = d.textlength(scene["small"], font=f)
                bx = (RW - w) / 2 - 50
                col = tuple(int(BG[j] + (OR[j] - BG[j]) * k) for j in range(3))
                d.rounded_rectangle((bx, y, bx + w + 100, y + 120), radius=20, fill=col)
                d.text(((RW - w) / 2, y + 30), scene["small"], font=f, fill=WH)
            else:
                f = R(50)
                col = tuple(int(BG[j] + (GR[j] - BG[j]) * k) for j in range(3))
                for l in wrap(d, scene["small"], f, RW - 2 * X):
                    d.text((X, y), l, font=f, fill=col); y += 66
    return im

def render_reel(name, scenes, outdir):
    tmp = os.path.join(outdir, "_frames_" + name); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    total = sum(s["dur"] for s in scenes); fi = 0; tt = 0
    for si, s in enumerate(scenes):
        nf = int(round(s["dur"] * FPS))
        for k in range(nf):
            t = k / FPS
            reel_frame(s, t, s["dur"], (tt + t) / total, si).save(os.path.join(tmp, f"{fi:05d}.png")); fi += 1
        tt += s["dur"]
    # portada
    reel_frame(scenes[0], scenes[0]["dur"] * 0.6, scenes[0]["dur"], 0.05, 0).save(os.path.join(outdir, name + "-portada.png"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "%05d.png"),
                    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "20", "-c:a", "aac", "-b:a", "128k",
                    "-movflags", "+faststart", os.path.join(outdir, name + ".mp4")], check=True)
    shutil.rmtree(tmp)

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    only = sys.argv[2:] or None
    for k, slides in CAROUSELS.items():
        if only and k not in only: continue
        for i, s in enumerate(slides, 1):
            slide(s, i, len(slides)).save(os.path.join(out, f"{k}-{i}.png"))
    for k, sc in REELS.items():
        if only and k not in only: continue
        render_reel(k, sc, out)
    print("ok")
