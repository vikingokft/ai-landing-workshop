#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
design.py - a design-rendszer skill segédprogramja. Hat parancs:

  python3 design.py fontok "Playfair Display" "Inter"
      Megnézi a Google Fontsnál, hogy a betűtípus létezik-e, és tudja-e az ő, ű, Ő, Ű betűt.

  python3 design.py skala --szin "#185347" [--mod vilagos|sotet] [--arany 1.25|1.333|1.414] \
      [--alap 17] [--cim-betu talpas|talpatlan]
      Kiszámolja a tokens.css számolható részét a fő színből: a fő szín árnyalatával
      színezett semleges színeket (háttér, szegély, szövegek, sötét), a mező- és hibaszínt,
      a betűméret-skálát (mobilon kisebb, clamp), a sormagasságokat és a rétegzett árnyékokat.
      CSS-sorokat ír ki, amiket a tokens.css-be másolsz.

  python3 design.py kontraszt <mappa vagy tokens.css>
      A tokens.css színpárjait méri (WCAG AA): szöveg a háttéren, gombszöveg a gombon stb.

  python3 design.py logo --szoveg "Kiss Blanka" --font "Playfair Display" --suly 600 \
      --szin "#3A3335" --ki logo/logo.svg [--alcim "pre- és posztnatál tréning" \
      --alcim-font "Inter" --alcim-suly 500 --alcim-szin "#6B5E62"] [--jel jel.svg] \
      [--keret kor|negyzet --keret-szin "#F3D9DC"] [--meret 64]
      Szöveges logó, betűjel vagy favicon SVG-ben. A design-rendszer skill akkor használja,
      ha nincs logó: a név a címsorbetűvel, és a kezdőbetűkből favicon. A betűket görbékké alakítja, így a logó
      bárhol ugyanúgy néz ki, betűtípus nélkül is. Kell hozzá: pip install fonttools

  python3 design.py logo-valtozatok logo.svg --ki logo/ --sotet "#25151B"
      A logóból három változat: logo.svg (színes), logo-sotet.svg (egyszínű sötét, világos
      háttérre), logo-feher.svg (egyszínű fehér, sötét háttérre). PNG-ből csak másolat készül.

  python3 design.py minta <jelölt-mappa> [<jelölt-mappa> ...] -o stilus-minta.html
      Stílusmintát készít: jelöltenként egy arculati táblát (színek kontraszttal, logó, betűk,
      árnyékok, gombok normál és hover állapotban) és egy webdesign mintát (menü, hero, kártyák,
      idézet, sötét sáv, lábléc). Több jelöltnél fülekkel lehet váltani.
      Egy mappa = egy jelölt (benne tokens.css és logo/).

A tokens.css-ben egy változó hivatkozhat egy másikra (var(--ds-...)): a kontraszt és a minta
ezt feloldja. Csak a Python beépített moduljait használja, kivéve a logo parancsot (fonttools).
A fontok és a logo parancs internetet használ (Google Fonts).
"""
import argparse
import html
import io
import os
import re
import struct
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

MAGYAR = "őűŐŰ"
GF_CSS = "https://fonts.googleapis.com/css2?"


# ---------------------------------------------------------------- Google Fonts

def gf_letolt(csalad, suly=None, text=None):
    """A Google Fonts egy TTF-jét adja vissza (bájtok). Ha a család nem létezik: LookupError."""
    fam = csalad if suly is None else f"{csalad}:wght@{suly}"
    q = {"family": fam}
    if text:
        q["text"] = text
    try:
        css = urllib.request.urlopen(GF_CSS + urllib.parse.urlencode(q), timeout=20).read().decode()
    except urllib.error.HTTPError as e:
        if e.code == 400:
            raise LookupError(csalad)
        raise
    url = re.search(r"url\((.*?)\)", css)
    if not url:
        raise LookupError(csalad)
    return urllib.request.urlopen(url.group(1), timeout=30).read()


def cmap_karakterek(d):
    """A TTF cmap táblájából a lefedett karakterek (4-es és 12-es formátum)."""
    n = struct.unpack(">H", d[4:6])[0]
    base = None
    for i in range(n):
        tag, _, off, _ = struct.unpack(">4sIII", d[12 + 16 * i:28 + 16 * i])
        if tag == b"cmap":
            base = off
    if base is None:
        return set()
    kar = set()
    for i in range(struct.unpack(">H", d[base + 2:base + 4])[0]):
        _, _, so = struct.unpack(">HHI", d[base + 4 + 8 * i:base + 12 + 8 * i])
        s = base + so
        fmt = struct.unpack(">H", d[s:s + 2])[0]
        if fmt == 4:
            x2 = struct.unpack(">H", d[s + 6:s + 8])[0]
            seg = x2 // 2
            vegek = struct.unpack(">%dH" % seg, d[s + 14:s + 14 + x2])
            kezd = struct.unpack(">%dH" % seg, d[s + 16 + x2:s + 16 + 2 * x2])
            delta = struct.unpack(">%dh" % seg, d[s + 16 + 2 * x2:s + 16 + 3 * x2])
            rp = s + 16 + 3 * x2
            ro = struct.unpack(">%dH" % seg, d[rp:rp + x2])
            for k in range(seg):
                for c in range(kezd[k], vegek[k] + 1):
                    if c == 0xFFFF:
                        continue
                    if ro[k] == 0:
                        g = (c + delta[k]) & 0xFFFF
                    else:
                        p = rp + 2 * k + ro[k] + 2 * (c - kezd[k])
                        g = struct.unpack(">H", d[p:p + 2])[0]
                        g = (g + delta[k]) & 0xFFFF if g else 0
                    if g:
                        kar.add(c)
        elif fmt == 12:
            for k in range(struct.unpack(">I", d[s + 12:s + 16])[0]):
                a, b, g = struct.unpack(">III", d[s + 16 + 12 * k:s + 28 + 12 * k])
                for c in range(a, b + 1):
                    if g + (c - a):
                        kar.add(c)
    return kar


def cmd_fontok(args):
    rossz = 0
    for csalad in args.csaladok:
        try:
            d = gf_letolt(csalad, text=MAGYAR)
        except LookupError:
            print(f"✗ {csalad}: nincs ilyen család a Google Fontsban (pontos név kell, például „Playfair Display”)")
            rossz += 1
            continue
        except Exception as e:  # nincs internet, időtúllépés
            print(f"? {csalad}: nem tudtam ellenőrizni ({e}). Nézd meg kézzel: fonts.google.com, Language: Hungarian")
            rossz += 1
            continue
        hiany = [k for k in MAGYAR if ord(k) not in cmap_karakterek(d)]
        if hiany:
            print(f"✗ {csalad}: hiányzik belőle: {' '.join(hiany)}. Magyar szöveghez nem jó.")
            rossz += 1
        else:
            print(f"✓ {csalad}: létezik, és tudja az ő, ű betűt")
    sys.exit(1 if rossz else 0)


# ---------------------------------------------------------------- tokenek, kontraszt

def tokenek_olvas(utvonal):
    p = Path(utvonal)
    if p.is_dir():
        p = p / "tokens.css"
    szoveg = p.read_text(encoding="utf-8")
    valtozok = dict(re.findall(r"(--ds-[\w-]+)\s*:\s*([^;]+);", szoveg))
    meta = dict((k.lower(), v.strip()) for k, v in re.findall(r"/\*\s*([A-ZÁÉÍÓÖŐÚÜŰ-]+):\s*(.*?)\s*\*/", szoveg))
    return p, szoveg, felold({k: v.strip() for k, v in valtozok.items()}), meta


def felold(valt):
    """A var(--ds-...) hivatkozásokat a hivatkozott értékre cseréli (láncban is)."""
    ki = dict(valt)
    for _ in range(10):
        valtozott = False
        for k, v in ki.items():
            uj = re.sub(r"var\((--ds-[\w-]+)(?:\s*,\s*([^)]+))?\)",
                        lambda m: ki.get(m.group(1), m.group(2) or m.group(0)), v)
            if uj != v:
                ki[k], valtozott = uj, True
        if not valtozott:
            break
    return ki


def hex_rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        raise ValueError(h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def fenyesseg(rgb):
    def csat(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (csat(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def arany(a, b):
    la, lb = sorted((fenyesseg(hex_rgb(a)), fenyesseg(hex_rgb(b))), reverse=True)
    return (la + 0.05) / (lb + 0.05)


# (előtér, háttér, minimum, mire). Az "ALAP" az oldal alapháttere: világos módban
# a --ds-feher, sötét módban a --ds-sotet; a "PANEL" a --ds-vilagos (váltó szakasz).
PAROK = [
    ("--ds-szoveg", "ALAP", 4.5, "szöveg az alap háttéren"),
    ("--ds-szoveg", "PANEL", 4.5, "szöveg a váltó háttéren"),
    ("--ds-szoveg-vilagos", "ALAP", 4.5, "világos szöveg az alap háttéren"),
    ("--ds-szoveg-vilagos", "PANEL", 4.5, "világos szöveg a váltó háttéren"),
    ("--ds-elsodleges", "ALAP", 3.0, "kiemelt szín (alcím, ikon) az alap háttéren"),
    ("--ds-gomb-hatter", "ALAP", 3.0, "a gomb elválik a háttértől"),
    ("--ds-gomb-szoveg", "--ds-gomb-hatter", 4.5, "gombszöveg a gombon"),
    ("--ds-gomb-hover-szoveg", "--ds-gomb-hover-hatter", 4.5, "gombszöveg hoverkor"),
    ("--ds-gomb2-szin", "ALAP", 4.5, "a másodlagos gomb felirata az alap háttéren"),
    ("--ds-gomb2-hover-szoveg", "--ds-gomb2-hover-hatter", 4.5, "a másodlagos gomb felirata hoverkor"),
    ("--ds-sav-szoveg", "--ds-sav-hatter", 4.5, "szöveg a sötét sávon"),
    ("--ds-sav-gomb-hatter", "--ds-sav-hatter", 3.0, "a sáv gombja elválik a sávtól"),
    ("--ds-sav-gomb-szoveg", "--ds-sav-gomb-hatter", 4.5, "a sáv gombjának felirata"),
    ("--ds-szoveg", "--ds-mezo-hatter", 4.5, "beírt szöveg a mezőben"),
    ("--ds-mezo-keret", "ALAP", 3.0, "a mező kerete látszik"),
    ("--ds-mezo-fokusz", "ALAP", 3.0, "a fókuszkeret látszik"),
    ("--ds-hiba", "ALAP", 4.5, "hibaüzenet az alap háttéren"),
]
KOTELEZO = ["--ds-elsodleges", "--ds-sotet", "--ds-szoveg", "--ds-szoveg-vilagos", "--ds-szegely",
            "--ds-vilagos", "--ds-feher", "--ds-font-cim", "--ds-font-szoveg", "--ds-cim-suly",
            "--ds-arnyek-1", "--ds-arnyek-2", "--ds-gomb-kerekites", "--ds-gomb-hatter",
            "--ds-gomb-szoveg", "--ds-gomb-hover-hatter", "--ds-gomb-hover-szoveg", "--ds-gomb2-szin",
            "--ds-gomb2-hover-hatter", "--ds-gomb2-hover-szoveg", "--ds-sav-hatter", "--ds-sav-szoveg",
            "--ds-sav-gomb-hatter", "--ds-sav-gomb-szoveg", "--ds-sormagassag-cim",
            "--ds-mezo-hatter", "--ds-mezo-keret", "--ds-mezo-fokusz", "--ds-hiba"]


def sotet_mod(meta):
    return meta.get("mod", "vilagos").lower().startswith("s")


def kontraszt_eredmeny(valt, meta=None):
    alap = valt.get("--ds-sotet" if sotet_mod(meta or {}) else "--ds-feher")
    sorok = []
    for elo, hat, minimum, mire in PAROK:
        h = {"ALAP": alap, "PANEL": valt.get("--ds-vilagos")}.get(hat, valt.get(hat))
        if elo not in valt or not h:
            continue
        try:
            r = arany(valt[elo], h)
        except ValueError:
            sorok.append((False, f"{mire}: nem hex szín ({valt[elo]} / {h})", None, minimum))
            continue
        sorok.append((r >= minimum, mire, r, minimum))
    return sorok


def cmd_kontraszt(args):
    p, _, valt, meta = tokenek_olvas(args.tokens)
    hiba = 0
    hianyzo = [k for k in KOTELEZO if k not in valt]
    if hianyzo:
        print("✗ hiányzó változók: " + ", ".join(hianyzo))
        hiba += 1
    for ok, mire, r, minimum in kontraszt_eredmeny(valt, meta):
        if r is None:
            print(f"✗ {mire}")
        else:
            print(f"{'✓' if ok else '✗'} {mire}: {r:.2f}:1 (legalább {minimum}:1)")
        hiba += 0 if ok else 1
    print(f"\n{p}: {'rendben' if not hiba else f'{hiba} hiba'}")
    sys.exit(1 if hiba else 0)


# ---------------------------------------------------------------- skála (számolt tokenek)

def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _gam(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def hex_oklch(h):
    import math
    r, g, b = (_lin(c) for c in hex_rgb(h))
    l_ = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m_ = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s_ = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    bb = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return L, math.hypot(a, bb), math.degrees(math.atan2(bb, a)) % 360


def oklch_hex(L, C, H):
    """OKLCH -> hex; ha a szín kilóg az sRGB-ből, a telítettséget csökkenti, amíg belefér."""
    import math
    while True:
        a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
        l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
        m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
        s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
        rgb = (4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
               -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
               -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_)
        if all(-0.0005 <= c <= 1.0005 for c in rgb) or C < 0.001:
            return "#" + "".join("%02X" % round(max(0, min(1, _gam(max(0, c)))) * 255) for c in rgb)
        C *= 0.95


def kontrasztig(L, C, H, hatter, minimum, irany):
    """Addig lépteti a világosságot (irany: -1 sötétebb, +1 világosabb), amíg a kontraszt meglesz."""
    for _ in range(100):
        h = oklch_hex(L, C, H)
        if arany(h, hatter) >= minimum:
            return h
        L = max(0, min(1, L + 0.01 * irany))
    return oklch_hex(L, C, H)


def fluid(minimum, maximum, kicsi=375, nagy=1280):
    """clamp(): mobilon `minimum`, széles képernyőn `maximum` pixel, közte arányosan."""
    if maximum - minimum < 1:
        return f"{round(maximum)}px"
    meredek = (maximum - minimum) / (nagy - kicsi)
    alap = minimum - meredek * kicsi
    return f"clamp({round(minimum)}px, {alap:.1f}px + {meredek * 100:.2f}vw, {round(maximum)}px)"


def cmd_skala(args):
    L, C, H = hex_oklch(args.szin)
    sotet = args.mod.startswith("s")
    t = lambda c, maxc: min(C * c, maxc)  # a fő szín telítettségének töredéke, felülről korlátozva
    feher = "#FFFFFF"
    if not sotet:
        vilagos = oklch_hex(0.975, t(0.10, 0.012), H)
        szegely = oklch_hex(0.915, t(0.14, 0.018), H)
        sotet_sz = oklch_hex(0.22, t(0.30, 0.035), H)
        szoveg = kontrasztig(0.27, t(0.12, 0.018), H, vilagos, 9, -1)
        szoveg_vil = kontrasztig(0.52, t(0.16, 0.025), H, vilagos, 4.6, -1)
        mezo_keret = kontrasztig(0.66, t(0.14, 0.02), H, feher, 3.1, -1)
        alap, mezo_hatter = feher, "var(--ds-feher)"
        hiba = kontrasztig(0.52, 0.17, 27, feher, 4.6, -1)
    else:
        sotet_sz = oklch_hex(0.18, t(0.25, 0.03), H)
        vilagos = oklch_hex(0.235, t(0.25, 0.03), H)
        szegely = oklch_hex(0.32, t(0.22, 0.03), H)
        szoveg = kontrasztig(0.93, t(0.08, 0.012), H, vilagos, 9, 1)
        szoveg_vil = kontrasztig(0.74, t(0.10, 0.02), H, vilagos, 4.6, 1)
        mezo_keret = kontrasztig(0.50, t(0.14, 0.02), H, sotet_sz, 3.1, 1)
        alap, mezo_hatter = sotet_sz, "var(--ds-vilagos)"
        hiba = kontrasztig(0.72, 0.15, 27, sotet_sz, 4.6, 1)

    r = args.arany
    b = args.alap
    rm = 1 + (r - 1) * 0.6  # mobilon szelídebb arány
    # H4 = alap × arány, H1 = alap × arány⁴; a H1 legfeljebb 64 px, mert a landing-címek hosszúak
    meretek = {
        "h1": fluid(min(b * rm ** 4, 40), min(b * r ** 4, 64)), "h2": fluid(b * rm ** 3, min(b * r ** 3, 48)),
        "h3": fluid(b * rm ** 2, b * r ** 2), "h4": fluid(b * rm, b * r),
    }
    talpas = args.cim_betu == "talpas"
    sr, sg, sb = hex_rgb(sotet_sz if not sotet else "#000000")
    a1, a2 = (0.06, 0.10) if not sotet else (0.30, 0.45)
    print(f"""  /* --- design.py skala: --szin {args.szin} --mod {args.mod} --arany {r} --alap {b} --- */
  --ds-sotet: {sotet_sz};
  --ds-szoveg: {szoveg};
  --ds-szoveg-vilagos: {szoveg_vil};
  --ds-szegely: {szegely};
  --ds-vilagos: {vilagos};
  --ds-feher: {feher};

  --ds-cim-betukoz: {"-0.01em" if talpas else "-0.025em"};
  --ds-meret-h1: {meretek["h1"]};
  --ds-meret-h2: {meretek["h2"]};
  --ds-meret-h3: {meretek["h3"]};
  --ds-meret-h4: {meretek["h4"]};
  --ds-meret-alcim: {round(b * 0.82)}px;
  --ds-meret-body-l: {fluid(b * 1.06, b * 1.18)};
  --ds-meret-body-m: {round(b)}px;
  --ds-meret-body-s: {round(b * 0.86)}px;
  --ds-sormagassag-cim: {"1.15" if talpas else "1.08"};
  --ds-sormagassag-kiscim: 1.3;
  --ds-sormagassag: 1.6;

  --ds-arnyek-1: 0px 1px 2px 0px rgba({sr}, {sg}, {sb}, {a1}), 0px 4px 12px 0px rgba({sr}, {sg}, {sb}, {a1});
  --ds-arnyek-2: 0px 2px 4px 0px rgba({sr}, {sg}, {sb}, {a1}), 0px 16px 40px -8px rgba({sr}, {sg}, {sb}, {a2});

  --ds-mezo-hatter: {mezo_hatter};
  --ds-mezo-keret: {mezo_keret};
  --ds-mezo-fokusz: var(--ds-elsodleges);
  --ds-hiba: {hiba};""")
    print(f"\n/* A fő szín ({args.szin}) a(z) {alap} háttéren: {arany(args.szin, alap):.2f}:1. "
          "Ha 3:1 alatt van, a kiemelésekhez és a gombhoz egy sötétebb árnyalata kell. */")


# ---------------------------------------------------------------- logó

def szoveg_utvonal(font_bajt, szoveg, magassag):
    """A szöveg görbéi SVG-útvonalként; visszaad (path_d, szélesség, cap-magasság) a magassághoz skálázva."""
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen

    f = TTFont(io.BytesIO(font_bajt))
    cmap = f.getBestCmap()
    gs = f.getGlyphSet()
    upm = f["head"].unitsPerEm
    os2 = f["OS/2"]
    cap = getattr(os2, "sCapHeight", 0) or int(upm * 0.7)
    sk = magassag / cap  # a nagybetű magassága = magassag
    asc = f["hhea"].ascent
    hmtx = f["hmtx"]
    kern = {}
    if "kern" in f:
        for t in f["kern"].kernTables:
            kern.update(getattr(t, "kernTable", {}))
    pen = SVGPathPen(gs, ntos=lambda v: ("%.1f" % v).rstrip("0").rstrip("."))
    x = 0
    elozo = None
    hianyzo = []
    for k in szoveg:
        gnev = cmap.get(ord(k))
        if gnev is None:
            hianyzo.append(k)
            continue
        if elozo and (elozo, gnev) in kern:
            x += kern[(elozo, gnev)]
        tp = TransformPen(pen, (sk, 0, 0, -sk, x * sk, asc * sk))
        gs[gnev].draw(tp)
        x += hmtx[gnev][0]
        elozo = gnev
    if hianyzo:
        raise SystemExit(f"HIBA: a betűtípusból hiányzik: {' '.join(hianyzo)}")
    return pen.getCommands(), x * sk, asc * sk, magassag


def cmd_logo(args):
    try:
        import fontTools  # noqa: F401
    except ImportError:
        raise SystemExit("HIBA: ehhez kell a fonttools. Telepítsd: pip3 install fonttools (utána futtasd újra)")
    try:
        fo = gf_letolt(args.font, args.suly)
    except LookupError:
        raise SystemExit(f"HIBA: nincs ilyen Google Font: {args.font} (súly: {args.suly})")

    H = 100.0  # a nagybetű magassága belső egységben
    d, w, asc, cap = szoveg_utvonal(fo, args.szoveg, H)
    elemek = []
    alcim_h = 0
    alcim_w = 0
    if args.alcim:
        af = gf_letolt(args.alcim_font or args.font, args.alcim_suly)
        ad, alcim_w, aasc, acap = szoveg_utvonal(af, args.alcim, H * 0.32)
        alcim_h = acap

    jel_w = 0
    jel_svg = ""
    if args.jel:
        jt = Path(args.jel).read_text(encoding="utf-8")
        vb = re.search(r'viewBox="([\d.\s-]+)"', jt)
        belso = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", jt, flags=re.S)
        if vb:
            _, _, vw, vh = (float(v) for v in vb.group(1).split())
            jm = H * 1.6 if not args.alcim else H * 1.6 + alcim_h
            s = jm / vh
            jel_w = vw * s + H * 0.35
            jel_svg = f'<g transform="translate(0 {asc - H}) scale({s:.4f})">{belso}</g>'

    elemek.append(f'<path d="{d}" fill="{args.szin}" transform="translate({jel_w:.2f} 0)"/>')
    teljes_w = jel_w + max(w, alcim_w)
    teljes_h = asc + H * 0.45
    if args.alcim:
        y = asc + H * 0.42
        elemek.append(f'<path d="{ad}" fill="{args.alcim_szin or args.szin}" '
                      f'transform="translate({jel_w:.2f} {y - (aasc - acap):.2f})"/>')
        teljes_h = y + acap + H * 0.2
    if jel_svg:
        elemek.insert(0, jel_svg)

    # A szöveg teteje a viewBoxban (asc - H) körül van; a felső üres sávot levágjuk.
    fent = asc - H - H * 0.15
    vb_x, vb_y, vb_w, vb_h = 0, fent, teljes_w, teljes_h - fent

    if args.keret:
        # Betűjel vagy embléma: a felirat egy formában, négyzetes rajzlapon.
        oldal = max(vb_w, vb_h) * (1.55 if args.keret == "kor" else 1.4)
        cx, cy = vb_x + vb_w / 2, vb_y + vb_h / 2
        vb_x, vb_y, vb_w, vb_h = cx - oldal / 2, cy - oldal / 2, oldal, oldal
        if args.keret == "kor":
            forma = f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{oldal / 2:.2f}" fill="{args.keret_szin}"/>'
        else:
            forma = (f'<rect x="{vb_x:.2f}" y="{vb_y:.2f}" width="{oldal:.2f}" height="{oldal:.2f}" '
                     f'rx="{oldal * 0.2:.2f}" fill="{args.keret_szin}"/>')
        elemek.insert(0, forma)

    meret = f' width="{args.meret}" height="{args.meret}"' if args.meret else ""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb_x:.2f} {vb_y:.2f} {vb_w:.2f} {vb_h:.2f}"{meret} '
           f'role="img" aria-label="{html.escape(args.szoveg)}">\n<title>{html.escape(args.szoveg)}</title>\n'
           + "\n".join(elemek) + "\n</svg>\n")
    ki = Path(args.ki)
    ki.parent.mkdir(parents=True, exist_ok=True)
    ki.write_text(svg, encoding="utf-8")
    print(f"✓ {ki} ({len(svg) // 1024 + 1} KB)")


SZIN_ATTR = re.compile(r'\b(fill|stroke)\s*=\s*"([^"]*)"')
SZIN_STILUS = re.compile(r'\b(fill|stroke)\s*:\s*([^;"]+)')
NEM_SZIN = {"none", "transparent", "currentcolor", "inherit"}


def egyszinu(svg, szin):
    """Az SVG minden színét egyetlen színre cseréli; visszaadja (új svg, eredeti színek halmaza)."""
    talalt = set()

    def csere(m):
        ertek = m.group(2).strip()
        if ertek.lower() in NEM_SZIN or ertek.startswith("url("):
            return m.group(0)
        talalt.add(ertek.upper())
        return f'{m.group(1)}="{szin}"' if "=" in m.group(0) else f"{m.group(1)}:{szin}"

    uj = SZIN_ATTR.sub(csere, svg)
    uj = SZIN_STILUS.sub(csere, uj)
    # a szín nélküli elemek alapból feketék: a gyökérre is rákerül a szín
    uj = re.sub(r"<svg\b", f'<svg fill="{szin}"', uj, count=1)
    return uj, talalt


def cmd_logo_valtozatok(args):
    forras = Path(args.logo)
    ki = Path(args.ki)
    ki.mkdir(parents=True, exist_ok=True)
    if forras.suffix.lower() != ".svg":
        import shutil
        shutil.copyfile(forras, ki / f"logo{forras.suffix.lower()}")
        print(f"✓ {ki / ('logo' + forras.suffix.lower())} (másolat)")
        print("! Ez nem SVG: egyszínű (sötét és fehér) változat csak vektoros logóból készül jól. "
              "Kérd el a logót SVG-ben, vagy a sötét háttéren maradjon a színes logó egy világos dobozban.")
        return
    svg = forras.read_text(encoding="utf-8")
    if re.search(r"<(linearGradient|radialGradient|image|pattern|filter)\b", svg):
        (ki / "logo.svg").write_text(svg, encoding="utf-8")
        print(f"✓ {ki / 'logo.svg'} (másolat)")
        print("! A logóban színátmenet, kép vagy szűrő van: egyszínű változatot nem készítek belőle, "
              "mert torz lenne. A sötét háttéren a színes logó álljon egy világos dobozban.")
        return
    (ki / "logo.svg").write_text(svg, encoding="utf-8")
    sotet, szinek = egyszinu(svg, args.sotet)
    feher, _ = egyszinu(svg, args.feher)
    (ki / "logo-sotet.svg").write_text(sotet, encoding="utf-8")
    (ki / "logo-feher.svg").write_text(feher, encoding="utf-8")
    print(f"✓ {ki / 'logo.svg'} (színes, az eredeti)")
    print(f"✓ {ki / 'logo-sotet.svg'} (egyszínű {args.sotet}, világos háttérre)")
    print(f"✓ {ki / 'logo-feher.svg'} (egyszínű {args.feher}, sötét háttérre)")
    if len(szinek) > 1:
        print(f"! Az eredetiben {len(szinek)} szín volt ({', '.join(sorted(szinek))}), az egyszínű változatokban "
              "egy lett: nézd meg a stílusmintán, nem tűnik-e el fontos részlet (egy apró díszítés beolvadhat, "
              "ez egyszínű logónál rendben van).")


# ---------------------------------------------------------------- stílusminta
# Két rész jelöltenként: az arculati tábla (színek, logó, betűk, árnyékok, gombok)
# és egy webdesign minta (menü, hero, kártyák, idézet, sötét sáv, lábléc).

MINTA_CSS = """
*{box-sizing:border-box}
body{margin:0;background:#EDEDEA;font-family:system-ui,sans-serif;color:#1d1d1b}
.lap{max-width:1040px;margin:0 auto;padding:24px 16px 64px}
.fuls{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin:0 0 20px}
.fuls button{font:600 14px/1 system-ui;padding:10px 16px;border-radius:999px;border:1px solid #c9c9c4;background:#fff;color:#1d1d1b;cursor:pointer}
.fuls button[aria-selected=true]{background:#1d1d1b;color:#fff;border-color:#1d1d1b}
.jelolt[hidden]{display:none}
.jelolt{font-family:var(--ds-font-szoveg);color:var(--ds-szoveg)}
.tabla{background:var(--t-kulso);border-radius:16px;padding:clamp(16px,4vw,40px);display:flex;flex-direction:column;gap:24px}
.tabla-fej{text-align:center;padding:8px 0}
.tabla-fej h1{margin:0;font-family:var(--ds-font-cim);font-weight:var(--ds-cim-suly);font-size:28px;letter-spacing:.2em;text-transform:uppercase;color:var(--t-cim)}
.tabla-fej p{margin:8px 0 0;font-size:14px;color:var(--ds-szoveg-vilagos)}
.kartya{background:var(--t-kartya);border:1px solid var(--ds-szegely);border-radius:max(8px,min(var(--ds-kerekites),20px));box-shadow:var(--ds-arnyek-1);padding:clamp(16px,3vw,32px)}
.kartya>h2{margin:0 0 24px;font-family:var(--ds-font-cim);font-weight:var(--ds-cim-suly);font-size:18px;color:var(--t-cim)}
.cimke{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--ds-szoveg-vilagos)}
.kod{font:500 12px/1.4 ui-monospace,Menlo,monospace;color:var(--ds-szoveg)}
.szinek{display:grid;grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:16px}
.szinek .minta{aspect-ratio:1;border-radius:8px;border:1px solid var(--ds-szegely)}
.szinek figure{margin:0;text-align:center;display:flex;flex-direction:column;gap:6px}
.kontraszt{margin:20px 0 0;font-size:12px;color:var(--ds-szoveg-vilagos)}
.kontraszt b{color:#B3261E}
.logok{display:flex;flex-wrap:wrap;gap:16px;align-items:stretch}
.logok figure{margin:0;display:flex;flex-direction:column;gap:8px;align-items:flex-start}
.logok .hely{display:flex;align-items:center;justify-content:center;min-height:96px;padding:16px 24px;border-radius:8px;border:1px solid var(--ds-szegely);background:var(--t-alap)}
.logok .hely.sotet{background:var(--ds-sotet);border-color:var(--ds-sotet)}
.logok img{height:56px;width:auto;max-width:200px;object-fit:contain}
.logok img.kicsi{height:32px}
.sor{display:grid;grid-template-columns:72px 1fr;gap:16px;align-items:start;padding:12px 0;border-top:1px solid var(--ds-szegely)}
.sor .cimke{padding-top:8px}
.spec{font-size:10px;margin-top:4px;color:var(--ds-szoveg-vilagos)}
.cim{font-family:var(--ds-font-cim);font-weight:var(--ds-cim-suly);letter-spacing:var(--ds-cim-betukoz);text-transform:var(--ds-cim-nagybetu);color:var(--t-cim);margin:0;overflow-wrap:anywhere}
.alcim{font-family:var(--ds-font-szoveg);font-weight:var(--ds-alcim-suly);text-transform:uppercase;letter-spacing:.08em;color:var(--ds-elsodleges)}
.body{margin:0;line-height:var(--ds-sormagassag);color:var(--ds-szoveg)}
.arnyekok{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:24px}
.arnyekok>div{display:flex;gap:20px;align-items:center}
.arnyekok .doboz{width:88px;height:88px;flex:none;border-radius:max(8px,min(var(--ds-kerekites),20px));background:var(--t-kartya);border:1px solid var(--ds-szegely)}
.gomb{display:inline-block;font-family:var(--ds-font-szoveg);font-weight:700;font-size:var(--ds-gomb-betumeret);line-height:1;text-transform:var(--ds-gomb-nagybetu);letter-spacing:var(--ds-gomb-betukoz,.06em);padding:var(--ds-gomb-py) var(--ds-gomb-px);border-radius:var(--ds-gomb-kerekites);cursor:pointer;text-decoration:none;transition:all .15s ease}
.g1{background:var(--ds-gomb-hatter);color:var(--ds-gomb-szoveg);border:var(--ds-gomb-keret) solid var(--ds-gomb-hatter)}
.g1:hover,.g1.hover{background:var(--ds-gomb-hover-hatter);color:var(--ds-gomb-hover-szoveg);border-color:var(--ds-gomb-hover-hatter)}
.g2{background:transparent;color:var(--ds-gomb2-szin);border:max(1px,var(--ds-gomb-keret)) solid var(--ds-gomb2-szin)}
.g2:hover,.g2.hover{background:var(--ds-gomb2-hover-hatter);color:var(--ds-gomb2-hover-szoveg);border-color:var(--ds-gomb2-hover-hatter)}
.g3{background:var(--ds-sav-gomb-hatter);color:var(--ds-sav-gomb-szoveg);border:var(--ds-gomb-keret) solid var(--ds-sav-gomb-hatter)}
.gombok{display:grid;grid-template-columns:120px 1fr 1fr;gap:20px 24px;align-items:center;justify-items:center}
.gombok .cimke:nth-child(3n+1){justify-self:start}
.felirat{margin:40px 0 8px;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#6b6b66}
.web{background:var(--t-alap);border:1px solid var(--ds-szegely);border-radius:12px;overflow:hidden;color:var(--ds-szoveg)}
.web nav{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:18px clamp(16px,4vw,40px);border-bottom:1px solid var(--ds-szegely)}
.web nav img{height:64px;width:auto;max-width:190px;object-fit:contain;object-position:left center;margin:-8px 0}
.web nav .menu{display:flex;gap:32px;font-family:var(--ds-font-szoveg);font-weight:700;font-size:var(--ds-gomb-betumeret);text-transform:var(--ds-gomb-nagybetu);letter-spacing:var(--ds-gomb-betukoz,.06em);color:var(--ds-szoveg)}
.web nav .gomb{padding:calc(var(--ds-gomb-py) - 4px) calc(var(--ds-gomb-px) - 4px)}
.web section{padding:clamp(48px,8vw,80px) clamp(16px,4vw,40px)}
.web .hero{text-align:center}
.web .hero .cim{font-size:var(--ds-meret-h1);line-height:var(--ds-sormagassag-cim);max-width:15em;margin:16px auto 0;text-wrap:balance}
.web .hero p{max-width:580px;margin:24px auto 0;font-size:var(--ds-meret-body-l);line-height:var(--ds-sormagassag);color:var(--ds-szoveg-vilagos)}
.web .gsor{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:32px}
.web .alt{background:var(--ds-vilagos)}
.web .alt .fej{text-align:center;margin-bottom:48px}
.web .alt .fej .cim{font-size:var(--ds-meret-h2);line-height:var(--ds-sormagassag-cim);margin-top:12px}
.web .kartyak{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:24px;max-width:960px;margin:0 auto}
.web .kartyak>div{background:var(--t-alap);border:1px solid var(--ds-szegely);border-radius:max(8px,min(var(--ds-kerekites),20px));box-shadow:var(--ds-arnyek-1);padding:24px}
.web .ikon{width:40px;height:40px;display:flex;align-items:center;justify-content:center;background:var(--ds-elsodleges);color:var(--t-ikon);border-radius:min(var(--ds-gomb-kerekites),12px);margin-bottom:16px}
.web .kartyak h3{font-size:var(--ds-meret-h4);line-height:var(--ds-sormagassag-kiscim);margin:0 0 8px}
.web .kartyak p{margin:0;font-size:var(--ds-meret-body-s);line-height:var(--ds-sormagassag);color:var(--ds-szoveg-vilagos)}
.web blockquote{margin:0 auto;max-width:640px;text-align:center;font-family:var(--ds-font-cim);font-size:clamp(20px,2.5vw,26px);line-height:1.45;color:var(--t-cim)}
.web .ki{text-align:center;margin-top:24px;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--ds-szoveg-vilagos)}
.web .sav{background:var(--ds-sav-hatter);color:var(--ds-sav-szoveg);text-align:center}
.web .sav .cim{color:var(--ds-sav-szoveg);font-size:var(--ds-meret-h2);line-height:var(--ds-sormagassag-cim)}
.web .sav p{max-width:560px;margin:16px auto 32px;font-size:16px;line-height:1.55;opacity:.85}
.web .sav-logo{display:block;height:56px;width:auto;max-width:180px;object-fit:contain;margin:0 auto 24px}
.web .lab-logo{height:36px;width:auto;max-width:120px;object-fit:contain;object-position:left center;margin:-8px 0}
.web footer{display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap;padding:20px clamp(16px,4vw,40px);border-top:1px solid var(--ds-szegely);font-size:12px;color:var(--ds-szoveg-vilagos)}
.urlap{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px}
.mezo{display:flex;flex-direction:column;gap:6px;font-size:var(--ds-meret-body-s)}
.mezo label{font-weight:600;color:var(--t-cim)}
.mezo input{font:inherit;font-size:var(--ds-meret-body-m);color:var(--ds-szoveg);background:var(--ds-mezo-hatter);border:1px solid var(--ds-mezo-keret);border-radius:min(var(--ds-kerekites),12px);padding:12px 14px;outline:none;width:100%}
.mezo input:focus,.mezo input.fokusz{border-color:var(--ds-mezo-fokusz);box-shadow:0 0 0 3px color-mix(in srgb,var(--ds-mezo-fokusz) 25%,transparent)}
.mezo input.hibas{border-color:var(--ds-hiba)}
.mezo .uzenet{color:var(--ds-hiba)}
@media (max-width:640px){.web nav .menu{display:none}.gombok{grid-template-columns:1fr 1fr}.gombok .ures,.gombok .sorfej{display:none}.sor{grid-template-columns:1fr;gap:4px}}
"""

IKONOK = [
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>',
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3.5"/></svg>',
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l6-6 4 4 8-8"/><path d="M14 7h7v7"/></svg>',
]
MINTA_SZOVEG = ("Itt tudod hosszabban bemutatni saját magad vagy a problémát, következményét, fájdalompontot, "
                "célcsoport jellemzőit, vágyott végeredményt, szolgáltatást, terméket, előnyt, megoldást, "
                "folyamatot, referenciát, bizonyítékot. Ékezetek: ő, ű, Ő, Ű, á, é, í, ó, ö, ú, ü.")


def font_nev(ertek):
    m = re.match(r'\s*["\']?([^"\',]+)', ertek or "")
    return m.group(1).strip() if m else "?"


def suly_nev(w):
    try:
        w = int(w)
    except (TypeError, ValueError):
        return str(w)
    for hatar, nev in ((300, "Light"), (400, "Regular"), (500, "Medium"), (600, "SemiBold"), (700, "Bold"), (800, "ExtraBold")):
        if w <= hatar:
            return nev
    return "Black"


def arnyek_spec(ertek):
    retegek = [r.strip() for r in re.split(r",(?![^()]*\))", ertek or "") if r.strip()]
    if len(retegek) > 1:
        return "<br>".join(f"<b>{n}. réteg</b><br>" + arnyek_spec(r) for n, r in enumerate(retegek, 1))
    szamok = re.findall(r"(-?[\d.]+)px", ertek or "")
    szin = re.search(r"(rgba?\([^)]*\)|#[0-9a-fA-F]{3,8})", ertek or "")
    if len(szamok) < 3:
        return html.escape(ertek or "–")
    szamok += ["0"] * (4 - len(szamok))
    return (f"X: {szamok[0]}<br>Y: {szamok[1]}<br>Blur: {szamok[2]}<br>Spread: {szamok[3]}"
            f"<br>Szín: {html.escape(szin.group(1) if szin else '–')}")


def olvashato(hatter, jeloltek):
    """A jelöltek közül az, amelyik a háttéren a legjobban olvasható."""
    try:
        return max(jeloltek, key=lambda c: arany(c, hatter))
    except ValueError:
        return "#FFFFFF"


def jelolt_html(i, mappa, ki_mappa, egy=False):
    _, szoveg, valt, meta = tokenek_olvas(mappa)
    m = Path(mappa)
    sotet = sotet_mod(meta)
    nev = meta.get("irany", m.name)
    leiras = meta.get("leiras", "")
    v = lambda k, alap="": valt.get(k, alap)

    feluletek = {
        "--t-alap": v("--ds-sotet") if sotet else v("--ds-feher"),
        "--t-kulso": v("--ds-sotet") if sotet else v("--ds-vilagos"),
        "--t-kartya": v("--ds-vilagos") if sotet else v("--ds-feher"),
        "--t-cim": v("--ds-szoveg") if sotet else v("--ds-sotet"),
        "--t-ikon": olvashato(v("--ds-elsodleges", "#000000"),
                              [v("--ds-feher", "#FFFFFF"), v("--ds-sotet", "#000000")]),
    }
    css = re.sub(r"/\*.*?\*/", "", szoveg, flags=re.S)
    css = re.sub(r":root\b", f"#j{i}", css)
    css += f"#j{i}{{" + ";".join(f"{k}:{val}" for k, val in feluletek.items()) + "}"

    # Színek
    szin_sor = [("--ds-elsodleges", "Elsődleges / kiemelt")]
    if v("--ds-masodlagos") and v("--ds-masodlagos").lower() != v("--ds-elsodleges").lower():
        szin_sor.append(("--ds-masodlagos", "Másodlagos"))
    szin_sor += [("--ds-sotet", "Sötét"), ("--ds-szoveg", "Szöveg"), ("--ds-szoveg-vilagos", "Világos szöveg"),
                 ("--ds-szegely", "Szegély"), ("--ds-vilagos", "Világos"), ("--ds-feher", "Fehér")]
    szinek = "".join(
        f'<figure><div class="minta" style="background:{html.escape(v(k))}"></div>'
        f'<figcaption><div class="cimke">{c}</div><div class="kod">{html.escape(v(k).upper())}</div></figcaption></figure>'
        for k, c in szin_sor if v(k))
    eredmeny = kontraszt_eredmeny(valt, meta)
    rossz = [f"{mire} ({'–' if r is None else f'{r:.1f}:1'}, kell {minimum}:1)" for ok, mire, r, minimum in eredmeny if not ok]
    kontraszt = (f'<p class="kontraszt">Kontraszt (WCAG AA): {len(eredmeny) - len(rossz)}/{len(eredmeny)} rendben'
                 + (". <b>Javítandó: " + html.escape("; ".join(rossz)) + "</b>" if rossz else ".") + "</p>")

    # Logók
    logo_elemek = []
    for fajl, cimke, osztaly in (("logo.svg", "Színes", ""), ("logo-sotet.svg", "Egyszínű sötét", ""),
                                 ("logo-feher.svg", "Fehér, sötét háttérre", "sotet"),
                                 ("betujel.svg", "Betűjel", ""), ("favicon.svg", "Favicon", "")):
        lp = m / "logo" / fajl
        if lp.exists():
            src = html.escape(os.path.relpath(lp.resolve(), ki_mappa))
            kicsi = ' class="kicsi"' if fajl == "favicon.svg" else ""
            logo_elemek.append(f'<figure><div class="hely {osztaly}"><img src="{src}" alt="{cimke}"{kicsi}></div>'
                               f'<figcaption class="cimke">{cimke}</figcaption></figure>')
    if (m / "logo").exists():
        for kep in sorted((m / "logo").glob("*.png")):
            src = html.escape(os.path.relpath(kep.resolve(), ki_mappa))
            logo_elemek.append(f'<figure><div class="hely"><img src="{src}" alt="{kep.name}"></div>'
                               f'<figcaption class="cimke">{html.escape(kep.stem)}</figcaption></figure>')
    logo_kartya = (f'<section class="kartya"><h2>Logó</h2><div class="logok">{"".join(logo_elemek)}</div></section>'
                   if logo_elemek else "")
    def logo_kep(fajl, osztaly):
        lp = m / "logo" / fajl
        if not lp.exists():
            return ""
        return f'<img class="{osztaly}" src="{html.escape(os.path.relpath(lp.resolve(), ki_mappa))}" alt="Logó">'
    sav_logo = logo_kep("logo-feher.svg", "sav-logo")
    lab_logo = logo_kep("logo-sotet.svg", "lab-logo")

    nav_logo = ""
    if (m / "logo" / "logo.svg").exists():
        nav_logo = f'<img src="{html.escape(os.path.relpath((m / "logo" / "logo.svg").resolve(), ki_mappa))}" alt="Logó">'
    else:
        nav_logo = f'<span class="cim" style="font-size:20px">{html.escape(meta.get("nev", "BRAND"))}</span>'

    # Betűk
    fc, fs = font_nev(v("--ds-font-cim")), font_nev(v("--ds-font-szoveg"))
    cs = suly_nev(v("--ds-cim-suly", "600"))

    def sor(cimke, spec, tartalom):
        return (f'<div class="sor"><div class="cimke">{cimke}</div><div>{tartalom}'
                f'<div class="spec">{html.escape(spec)}</div></div></div>')

    def meret(k, alap):
        """A méret pixelben; clamp() esetén „mobil–asztali” alakban."""
        szamok = re.findall(r"([\d.]+)px", v(k, alap))
        if len(szamok) >= 2 and "clamp" in v(k, ""):
            return f"{szamok[0]}–{szamok[-1]}"
        return szamok[0] if szamok else v(k, alap)

    betuk = "".join([
        sor("H1", f"{fc} / {meret('--ds-meret-h1', '56')} / {cs}",
            '<p class="cim" style="font-size:var(--ds-meret-h1);line-height:var(--ds-sormagassag-cim)">H1 fejléc</p>'),
        sor("H2", f"{fc} / {meret('--ds-meret-h2', '40')} / {cs}",
            '<p class="cim" style="font-size:var(--ds-meret-h2);line-height:var(--ds-sormagassag-cim)">H2 fejléc</p>'),
        sor("H3", f"{fc} / {meret('--ds-meret-h3', '28')} / {cs}",
            '<p class="cim" style="font-size:var(--ds-meret-h3);line-height:var(--ds-sormagassag-kiscim)">H3 fejléc</p>'),
        sor("H4", f"{fc} / {meret('--ds-meret-h4', '24')} / {cs}",
            '<p class="cim" style="font-size:var(--ds-meret-h4);line-height:var(--ds-sormagassag-kiscim)">H4 fejléc</p>'),
        sor("Alcím", f"{fs} / {meret('--ds-meret-alcim', '18')} / {suly_nev(v('--ds-alcim-suly', '600'))}",
            '<div class="alcim" style="font-size:var(--ds-meret-alcim)">Alcím szöveg</div>'),
        sor("Body L", f"{fs} / {meret('--ds-meret-body-l', '18')} / Regular",
            f'<p class="body" style="font-size:var(--ds-meret-body-l)">{MINTA_SZOVEG}</p>'),
        sor("Body M", f"{fs} / {meret('--ds-meret-body-m', '16')} / Regular",
            f'<p class="body" style="font-size:var(--ds-meret-body-m)">{MINTA_SZOVEG}</p>'),
        sor("Body S", f"{fs} / {meret('--ds-meret-body-s', '14')} / Regular",
            f'<p class="body" style="font-size:var(--ds-meret-body-s)">{MINTA_SZOVEG}</p>'),
        sor("Gomb", f"{fs} / {meret('--ds-gomb-betumeret', '13')} / Bold",
            '<div style="font-weight:700;font-size:var(--ds-gomb-betumeret);text-transform:var(--ds-gomb-nagybetu);letter-spacing:var(--ds-gomb-betukoz,.06em)">Kattints ide</div>'),
    ])

    arnyekok = "".join(
        f'<div><div class="doboz" style="box-shadow:var({k})"></div><div class="kod">'
        f'<div style="font-family:var(--ds-font-szoveg);font-weight:600;margin-bottom:4px">{c}</div>'
        f'{arnyek_spec(v(k))}</div></div>'
        for k, c in (("--ds-arnyek-1", "Árnyék 1 · kártya"), ("--ds-arnyek-2", "Árnyék 2 · kiemelés")))

    gombok = ('<div class="gombok"><div class="ures"></div><div class="cimke">Normál</div><div class="cimke">Hover</div>'
              '<div class="cimke sorfej">Elsődleges</div><a class="gomb g1">Kattints ide</a><a class="gomb g1 hover">Kattints ide</a>'
              '<div class="cimke sorfej">Másodlagos</div><a class="gomb g2">Kattints ide</a><a class="gomb g2 hover">Kattints ide</a></div>')

    urlap = ('<div class="urlap">'
             '<div class="mezo"><label>Név</label><input placeholder="Kovács Anna"></div>'
             '<div class="mezo"><label>E-mail (fókuszban)</label><input class="fokusz" value="anna@pelda.hu"></div>'
             '<div class="mezo"><label>Telefon (hibás)</label><input class="hibas" value="06 30"><span class="uzenet">Adj meg egy teljes telefonszámot.</span></div>'
             '</div>')

    kartyak = "".join(
        f'<div><div class="ikon">{IKONOK[n]}</div><h3 class="cim">{c}</h3><p>{t}</p></div>'
        for n, (c, t) in enumerate((
            ("Gyors indulás", "Pár perc alatt készen állsz, és máris láthatod az első eredményt."),
            ("Teljes irányítás", "Minden a tiéd marad, és bármikor magaddal viheted."),
            ("Veled nő", "Ahogy növekszel, a rendszer is veled tart, hirtelen változások nélkül."),
        )))

    cimke = "végleges" if egy else f"{i}. jelölt"
    return meta.get("google-fonts", ""), f"""
<style>{css}</style>
<article class="jelolt" id="j{i}" data-nev="{html.escape(nev)}"{'' if i == 1 else ' hidden'}>
  <div class="tabla">
    <header class="tabla-fej"><h1>Arculati tábla</h1><p>{cimke} · {html.escape(nev)}{' · ' + html.escape(leiras) if leiras else ''}</p></header>
    <section class="kartya"><h2>Színek</h2><div class="szinek">{szinek}</div>{kontraszt}</section>
    {logo_kartya}
    <section class="kartya"><h2>Betűtípusok</h2>{betuk}</section>
    <section class="kartya"><h2>Árnyékok</h2><div class="arnyekok">{arnyekok}</div></section>
    <section class="kartya"><h2>Gombok</h2>{gombok}</section>
    <section class="kartya"><h2>Űrlap</h2>{urlap}</section>
  </div>
  <p class="felirat">Webdesign minta</p>
  <div class="web">
    <nav>{nav_logo}<div class="menu"><span>Szolgáltatások</span><span>Árak</span><span>Rólam</span></div><a class="gomb g1">Jelentkezem</a></nav>
    <section class="hero">
      <div class="alcim" style="font-size:12px;letter-spacing:.14em">Új ajánlat · 2026</div>
      <h2 class="cim">Egy fejléc, ami megmutatja a stílust</h2>
      <p>Itt egy bemutató szöveg jön a hero részhez, hogy lásd a törzsszöveget a helyén: a hosszát, a sortávolságát és a kontrasztját.</p>
      <div class="gsor"><a class="gomb g1">Kezdjük el</a><a class="gomb g2">Tudj meg többet</a></div>
    </section>
    <section class="alt">
      <div class="fej"><div class="alcim" style="font-size:12px;letter-spacing:.14em">Amit kapsz</div><h2 class="cim">Amit kínálok</h2></div>
      <div class="kartyak">{kartyak}</div>
    </section>
    <section>
      <blockquote>„Idézet, amely megmutatja, hogyan néz ki egy vélemény ezzel a stílussal, a saját helyén.”</blockquote>
      <div class="ki">Kovács Anna · ügyfél</div>
    </section>
    <section class="sav">
      {sav_logo}
      <h2 class="cim">Kezdd el ma!</h2>
      <p>Egy záró ajánlat, ami megerősíti az értékajánlatot, és cselekvésre késztet.</p>
      <a class="gomb g3">Jelentkezem</a>
    </section>
    <footer>{lab_logo}<span>© 2026 Minden jog fenntartva.</span><span>Adatkezelési tájékoztató</span></footer>
  </div>
</article>"""


def cmd_minta(args):
    fontok, blokkok, nevek = [], [], []
    ki_mappa = Path(args.ki).resolve().parent
    egy = len(args.mappak) == 1
    for i, m in enumerate(args.mappak, 1):
        gf, blokk = jelolt_html(i, m, ki_mappa, egy=egy)
        if gf and gf not in fontok:
            fontok.append(gf)
        blokkok.append(blokk)
        nevek.append(tokenek_olvas(m)[3].get("irany", Path(m).name))
    linkek = "".join(f'<link rel="stylesheet" href="{html.escape(u)}">' for u in fontok)
    fulek = ""
    if not egy:
        fulek = '<div class="fuls" role="tablist">' + "".join(
            f'<button role="tab" aria-selected="{"true" if i == 1 else "false"}" data-cel="j{i}">{i}. {html.escape(n)}</button>'
            for i, n in enumerate(nevek, 1)) + "</div>"
    szkript = """<script>
document.querySelectorAll('.fuls button').forEach(function(b){b.addEventListener('click',function(){
document.querySelectorAll('.fuls button').forEach(function(x){x.setAttribute('aria-selected',x===b)});
document.querySelectorAll('.jelolt').forEach(function(j){j.hidden=j.id!==b.dataset.cel});});});
</script>""" if not egy else ""
    cim = "Stílusminta" if egy else f"Stílusminta · {len(blokkok)} jelölt"
    oldal = f"""<!doctype html>
<html lang="hu"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{cim}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{linkek}<style>{MINTA_CSS}</style></head><body><main class="lap">
{fulek}{''.join(blokkok)}
</main>{szkript}</body></html>
"""
    Path(args.ki).write_text(oldal, encoding="utf-8")
    print(f"✓ {args.ki}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="parancs", required=True)

    f = sub.add_parser("fontok")
    f.add_argument("csaladok", nargs="+")
    f.set_defaults(fn=cmd_fontok)

    k = sub.add_parser("kontraszt")
    k.add_argument("tokens")
    k.set_defaults(fn=cmd_kontraszt)

    sk = sub.add_parser("skala")
    sk.add_argument("--szin", required=True, help="a fő (márka) szín hex kódja")
    sk.add_argument("--mod", default="vilagos", choices=["vilagos", "sotet"])
    sk.add_argument("--arany", type=float, default=1.333, help="betűméret-arány: 1.25 visszafogott, 1.333 kiegyensúlyozott (javasolt), 1.414 merész")
    sk.add_argument("--alap", type=float, default=17, help="a törzsszöveg mérete pixelben")
    sk.add_argument("--cim-betu", default="talpatlan", choices=["talpas", "talpatlan"])
    sk.set_defaults(fn=cmd_skala)

    lg = sub.add_parser("logo")
    lg.add_argument("--szoveg", required=True)
    lg.add_argument("--font", required=True)
    lg.add_argument("--suly", type=int, default=600)
    lg.add_argument("--szin", required=True)
    lg.add_argument("--alcim")
    lg.add_argument("--alcim-font")
    lg.add_argument("--alcim-suly", type=int, default=500)
    lg.add_argument("--alcim-szin")
    lg.add_argument("--jel", help="egy SVG-fájl a jellel, a felirat elé kerül")
    lg.add_argument("--keret", choices=["kor", "negyzet"], help="betűjelhez, faviconhoz, emblémához")
    lg.add_argument("--keret-szin", default="#000000")
    lg.add_argument("--meret", type=int, help="fix szélesség és magasság pixelben (faviconhoz)")
    lg.add_argument("--ki", required=True)
    lg.set_defaults(fn=cmd_logo)

    lv = sub.add_parser("logo-valtozatok")
    lv.add_argument("logo", help="a logófájl (SVG; PNG-ből csak másolat készül)")
    lv.add_argument("--ki", required=True, help="a cél logo/ mappa")
    lv.add_argument("--sotet", required=True, help="a sötét változat színe (a tokens.css --ds-sotet értéke)")
    lv.add_argument("--feher", default="#FFFFFF", help="a fehér változat színe (sötét háttérre)")
    lv.set_defaults(fn=cmd_logo_valtozatok)

    mn = sub.add_parser("minta")
    mn.add_argument("mappak", nargs="+")
    mn.add_argument("-o", "--ki", default="stilus-minta.html")
    mn.set_defaults(fn=cmd_minta)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
