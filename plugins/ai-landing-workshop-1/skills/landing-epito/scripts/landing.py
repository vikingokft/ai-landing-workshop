#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
landing.py - a landing-építő skill segédprogramja. Hat parancs:

  python3 landing.py ellenoriz index.html [--szoveg szoveg.md] [--tokens tokens.css]
      Gépi ellenőrzés: szerkezet (lang, title, description, egy H1, alt szövegek), hogy minden
      CSS-szabály a .lp burkolóra szűkül-e, külső források, űrlap és köszönőoldal, fókusz,
      mozgás. --szoveg: a címek, gombok és bekezdések szó szerint ott vannak-e.
      --tokens: a márka színei és betűi változatlanok-e, és van-e szín a tokeneken kívül.

  python3 landing.py kepernyokep index.html --ki kepernyokepek/
      Képernyőkép headless Chrome-mal (vagy Chromiummal, Edge-dzsel): asztali (1440 px) és
      mobil (390 px) méretben, külön a hero-ról és az egész oldalról. A mozgást kikapcsolja
      (prefers-reduced-motion), hogy a beúszó szakaszok is látsszanak. Az egész oldalas képet
      az oldal aljánál levágja, és szakasznyi szeletekre bontja (-01.png, -02.png …), ha van Pillow.

  python3 landing.py wp index.html -o wp-beillesztes.html [--mediatar URL] [--koszi-url URL]
      A WordPress-változat: a betűk linkje, a <style> és a <div class="lp"> tartalma, <html>,
      <head> és <body> nélkül, a mérőkód-hely nélkül. Gutenberg Egyéni HTML blokkba vagy
      Elementor HTML-widgetbe illeszthető. A képeket a wp-kepek/ mappába másolja egyedi,
      WordPress-barát névvel (ezeket kell a Médiatárba tölteni); az SVG-ket (logó) beágyazza.
      --mediatar: egy feltöltött kép címe a Médiatárból; ebből számolja az összes kép címét.

  python3 landing.py ikonok ikonlap-nyers.png --nevek kettlebell,kerdoiv,... --ki kepek/ikonok [--marka #hex,#hex]
      Generált ikonlapból (egyszínű kulcsháttéren, rácsban) külön ikonok: átlátszó PNG, és ha telepítve
      van a vtracer, színes SVG a márka színeivel. Csak a Pillow kell hozzá, a vtracer választható.

  python3 landing.py ikonlap index.html -o kepernyokepek/ikonlap.html
      Az oldal saját ikonjai (class="lp-ikon") egy lapon, 24, 48 és 96 px-en, az oldal stílusaival:
      ebből készül képernyőkép, hogy az ikonok egységét és olvashatóságát külön is látni.

  python3 landing.py ikon --lista
  python3 landing.py ikon check-circle --stilus vonalas|kitoltott|ketszinu|szinatmenetes [--meret 32]
      Tartalék: SVG-ikon a skill ikonkészletéből (Phosphor, MIT-licenc), alapnak a saját ikonokhoz:
      a szín a környezet szövegszíne (currentColor), a színátmenetes a fő szín árnyalataiból.
      A --lista kiírja az ikonok nevét és hogy mire valók.

Csak a Python beépített moduljait használja; a kepernyokep parancshoz Chrome, Chromium vagy
Edge kell a gépen.
"""
import argparse
import html
import os
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path


# ---------------------------------------------------------------- HTML beolvasás

class Bejaro(HTMLParser):
    """Összegyűjti, amit az ellenőrzéshez tudni kell."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.elemek = []          # (tag, attrs)
        self.stilusok = []        # (attrs, szöveg)
        self.szkriptek = []       # (attrs, szöveg)
        self.szoveg = []          # látható szöveg darabjai
        self.megjegyzesek = []
        self._bent = None
        self._puffer = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.elemek.append((tag, a))
        if tag in ("style", "script"):
            self._bent = (tag, a)
            self._puffer = []
        elif tag in ("p", "div", "section", "li", "h1", "h2", "h3", "h4", "br", "td", "label", "summary"):
            self.szoveg.append(" ")

    def handle_endtag(self, tag):
        if self._bent and tag == self._bent[0]:
            (self.stilusok if tag == "style" else self.szkriptek).append((self._bent[1], "".join(self._puffer)))
            self._bent = None

    def handle_data(self, data):
        if self._bent:
            self._puffer.append(data)
        else:
            self.szoveg.append(data)

    def handle_comment(self, data):
        self.megjegyzesek.append(data)


def normal(s):
    s = html.unescape(s)
    s = s.replace("\u00a0", " ").replace("\u2028", " ")
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s+([.,;:!?)”])", r"\1", s)
    s = re.sub(r"([(„])\s+", r"\1", s)
    return s.strip()


# ---------------------------------------------------------------- CSS bejárás

def css_szabalyok(css):
    """(előtag, törzs) párok; a @media/@supports/@container belsejét is bejárja."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    ki = []
    i, n = 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0:
            break
        elotag = css[i:j].strip()
        # a hozzá tartozó záró kapcsos zárójel
        mely, k = 1, j + 1
        while k < n and mely:
            if css[k] == "{":
                mely += 1
            elif css[k] == "}":
                mely -= 1
            k += 1
        torzs = css[j + 1:k - 1]
        if elotag.startswith(("@media", "@supports", "@container", "@layer")):
            ki += css_szabalyok(torzs)
        elif elotag.startswith("@"):
            pass  # @keyframes, @font-face, @page: nem választó
        else:
            ki.append((elotag, torzs))
        i = k
    return ki


SZIN_MINTA = re.compile(r"#[0-9a-fA-F]{3,8}\b|\brgba?\([^)]*\)|\bhsla?\([^)]*\)|\boklch\([^)]*\)")


def tokenek(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    return {k: v.strip() for k, v in re.findall(r"(--ds-[\w-]+)\s*:\s*([^;]+);", css)}


# ---------------------------------------------------------------- ellenőrzés

EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\U0001F000-\U0001F2FF]")


def md_reszek(md):
    """A szoveg.md-ből a szó szerint ellenőrizhető részek: (fajta, szöveg)."""
    md = re.sub(r"^---.*?---\s*", "", md, flags=re.S)
    ki = []
    kimarad = False
    for sor in md.splitlines():
        s = sor.strip()
        if s.startswith("## "):
            kimarad = False
            continue
        if not s or s.startswith("# ") or kimarad:
            continue
        if s.startswith("Kimarad:"):
            kimarad = True
            continue
        s = re.sub(r"\[([^\]]+)\]\(\[KITÖLTENDŐ:[^\]]*\]\)", r"\1", s)  # link, aminek a címe még hiányzik
        s = re.sub(r"\[KITÖLTENDŐ:[^\]]*\]", "", s)
        s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
        s = re.sub(r"\s*\(logó\)", "", s)  # jelölés: ide logó kell, nem szöveg
        if s.startswith("### "):
            ki.append(("cím", s[4:]))
            continue
        m = re.match(r"\*\*(Gomb|Felvezető|Jelölőnégyzet):\*\*\s*(.+)", s)
        if m:
            ki.append((m.group(1).lower(), m.group(2)))
            continue
        if s.startswith("**Űrlap:**"):
            continue
        s = re.sub(r"^[-*]\s+|^\d+\.\s+", "", s)
        s = s.replace("**", "").replace("__", "")
        if len(s) > 3:
            ki.append(("szöveg", s))
    return [(f, normal(t)) for f, t in ki if normal(t)]


def cmd_ellenoriz(args):
    p = Path(args.html)
    forras = p.read_text(encoding="utf-8")
    b = Bejaro()
    b.feed(forras)
    hiba, figy = [], []
    ok = []

    def tag_ok(tag):
        return [a for t, a in b.elemek if t == tag]

    # szerkezet
    htmlek = tag_ok("html")
    (ok if htmlek and htmlek[0].get("lang", "").startswith("hu") else hiba).append('<html lang="hu">')
    (ok if tag_ok("title") else hiba).append("<title>")
    metak = tag_ok("meta")
    (ok if any(m.get("name") == "viewport" for m in metak) else hiba).append("viewport meta")
    if not args.koszi:
        (ok if any(m.get("name") == "description" and m.get("content", "").strip() for m in metak) else hiba).append("meta description")
        (ok if any(m.get("property") == "og:title" for m in metak) else figy).append("og:title (megosztáskor ez a cím)")
    h1 = len(tag_ok("h1"))
    (ok if h1 == 1 else hiba).append(f"pontosan egy <h1> (most: {h1})")
    lp = [a for t, a in b.elemek if t == "div" and "lp" in a.get("class", "").split()]
    (ok if lp else hiba).append('<div class="lp"> burkoló')

    kepek = tag_ok("img")
    alt_nelkul = [a.get("src", "?") for a in kepek if "alt" not in a]
    meret_nelkul = [a.get("src", "?") for a in kepek if not (a.get("width") and a.get("height"))]
    (hiba if alt_nelkul else ok).append("alt szöveg minden képen" + (f" (hiányzik: {', '.join(alt_nelkul[:3])})" if alt_nelkul else ""))
    if meret_nelkul:
        figy.append(f"width és height nélküli kép (betöltéskor ugrál az oldal): {', '.join(meret_nelkul[:3])}")

    # külső források
    kulso = []
    for t, a in b.elemek:
        url = a.get("src") if t in ("script", "img", "iframe") else a.get("href") if t == "link" else None
        if url and re.match(r"https?://", url) and not re.match(r"https://fonts\.(googleapis|gstatic)\.com", url):
            kulso.append(url)
    (hiba if kulso else ok).append("külső forrás csak a Google Fonts" + (f" (most: {', '.join(kulso[:3])})" if kulso else ""))

    # CSS
    fo_css = "\n".join(s for a, s in b.stilusok if "data-csak-onallo" not in a)
    szabalyok = css_szabalyok(fo_css)
    rossz_valaszto = []
    for elotag, _ in szabalyok:
        for v in elotag.split(","):
            v = v.strip()
            if v and not v.startswith(".lp"):
                rossz_valaszto.append(v)
    (hiba if rossz_valaszto else ok).append(
        "minden CSS-szabály .lp-vel kezdődik" + (f" (nem: {', '.join(rossz_valaszto[:4])})" if rossz_valaszto else ""))
    if ":focus-visible" not in fo_css:
        hiba.append("nincs :focus-visible stílus (látható fókusz a gombokon és a mezőkön)")
    else:
        ok.append(":focus-visible")
    if re.search(r"@keyframes|transition\s*:|animation\s*:", fo_css) and "prefers-reduced-motion" not in fo_css:
        hiba.append("van mozgás, de nincs prefers-reduced-motion kikapcsolás")
    vh = [m for m in re.findall(r"(?:min-)?height\s*:\s*([^;}]*\d+(?:\.\d+)?(?:s|d|l)?vh[^;}]*)", fo_css) if "min(" not in m]
    if vh:
        figy.append(f"{len(vh)} helyen vh-alapú magasság min() korlát nélkül (például {vh[0].strip()}): a képernyőkép magas "
                    "ablakában óriásira nő; írd min(100vh, 900px) alakban")
    apro = [m for m in re.findall(r"font-size\s*:\s*(\d+(?:\.\d+)?)px", fo_css) if float(m) < 16]
    if len(apro) > 3:
        figy.append(f"{len(apro)} helyen 16 px alatti betűméret: a törzsszöveg legalább 17 px legyen, apró csak címke és jogi szöveg")
    if not re.search(r"background(?:-color)?\s*:[^;]*(--ds-sotet|--ds-elsodleges|--ds-sav-hatter|--lp-szin|color-mix)", fo_css):
        figy.append("egyik szakasznak sincs színes vagy sötét háttere: az oldal valószínűleg egyforma fehér és halvány csíkok sora")
    nagybetus = len(re.findall(r"text-transform\s*:\s*uppercase", fo_css))
    if nagybetus > 3:
        figy.append(f"{nagybetus} helyen nagybetűsítés: a gombon márka, de minden cím fölötti felvezetőnél sablonjel")

    # márka: tokenek
    if args.tokens:
        tk = tokenek(Path(args.tokens).read_text(encoding="utf-8"))
        lap = tokenek(fo_css)
        elter = []
        for k, v in tk.items():
            szin = re.fullmatch(r"#[0-9a-fA-F]{3,8}", v)
            egyforma = lambda x: re.sub(r"\s+", "", x).replace("'", '"').lower()
            if (szin or k.startswith("--ds-font-")) and k in lap and egyforma(lap[k]) != egyforma(v):
                elter.append(f"{k}: {lap[k]} (a design-rendszerben {v})")
        hianyzik = [k for k in ("--ds-elsodleges", "--ds-font-cim", "--ds-font-szoveg") if k not in lap]
        (hiba if elter or hianyzik else ok).append(
            "a márka színei és betűi a design-rendszerből" +
            (f" (eltér: {'; '.join(elter[:3])})" if elter else "") +
            (f" (hiányzik: {', '.join(hianyzik)})" if hianyzik else ""))
        tokenen_kivul = set()
        for elotag, torzs in szabalyok:
            for decl in torzs.split(";"):
                if decl.strip().startswith("--ds-"):
                    continue
                tokenen_kivul.update(m.group(0) for m in SZIN_MINTA.finditer(decl))
        tokenen_kivul -= {"#fff", "#FFF", "#000"}
        if tokenen_kivul:
            figy.append(f"szín a tokeneken kívül ({len(tokenen_kivul)}): {', '.join(sorted(tokenen_kivul)[:5])}; "
                        "a színek a var(--ds-...) tokenekből vagy color-mix()-szel jöjjenek")

    # űrlap és köszönőoldal
    if not args.koszi:
        urlap = tag_ok("form")
        szkript = "\n".join(s for _, s in b.szkriptek)
        if not urlap:
            hiba.append("nincs űrlap")
        else:
            ok.append("űrlap")
            if any((a.get("method") or "").lower() == "get" for a in urlap):
                hiba.append('az űrlap method="get": a személyes adat az URL-be kerülne')
            if "koszi.html" not in szkript and not args.koszi_url:
                hiba.append("az űrlap beküldése nem visz a koszi.html-re")
            jelolo = [a for t, a in b.elemek if t == "input" and a.get("type") == "checkbox"]
            if not any("required" in a for a in jelolo):
                hiba.append("nincs kötelező (required) adatkezelési jelölőnégyzet")
        if not any("MÉRŐKÓD" in m for m in b.megjegyzesek):
            figy.append("nincs <!-- MÉRŐKÓDOK --> hely a <head>-ben")

    # szöveg
    lathato = normal("".join(b.szoveg))
    if "KITÖLTENDŐ" in forras:
        figy.append(f"{forras.count('KITÖLTENDŐ')} [KITÖLTENDŐ] hely maradt: feltöltés előtt ki kell tölteni")
    if EMOJI.search(lathato):
        figy.append("emoji a szövegben: ikonnak ne emoji legyen")
    if re.search(r"→|->", lathato):
        figy.append("nyíl (→) a szövegben: a gomb felirata szó szerint a szoveg.md-é legyen")
    if args.szoveg:
        reszek = md_reszek(Path(args.szoveg).read_text(encoding="utf-8"))
        kemeny = [(f, t) for f, t in reszek if f != "szöveg" and t not in lathato]
        puha = [t for f, t in reszek if f == "szöveg" and t not in lathato]
        (hiba if kemeny else ok).append(
            "a címek, gombok, felvezetők szó szerint" +
            (" (nincs meg: " + "; ".join(f"{f}: „{t[:50]}”" for f, t in kemeny[:4]) + ")" if kemeny else ""))
        szazalek = 100 * (1 - len(puha) / max(1, len([1 for f, _ in reszek if f == 'szöveg'])))
        if puha:
            figy.append(f"a bekezdések {szazalek:.0f}%-a szó szerint megvan; nézd meg ezeket: " +
                        "; ".join(f"„{t[:60]}”" for t in puha[:4]))
        else:
            ok.append("minden bekezdés szó szerint")

    for s in ok:
        print(f"✓ {s}")
    for s in figy:
        print(f"! {s}")
    for s in hiba:
        print(f"✗ {s}")
    print(f"\n{p}: {'rendben' if not hiba else f'{len(hiba)} hiba'}" + (f", {len(figy)} figyelmeztetés" if figy else ""))
    sys.exit(1 if hiba else 0)


# ---------------------------------------------------------------- képernyőkép

def bongeszo():
    jeloltek = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for j in jeloltek:
        if os.path.exists(j):
            return j
    for nev in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge", "msedge", "chrome"):
        w = shutil.which(nev)
        if w:
            return w
    return None


def cmd_kepernyokep(args):
    b = bongeszo()
    if not b:
        raise SystemExit("Nem találok Chrome-ot, Chromiumot vagy Edge-et. Nyisd meg az oldalt böngészőben, és nézd meg kézzel "
                         "(asztali és telefonos szélességben is).")
    p = Path(args.html).resolve()
    ki = Path(args.ki)
    ki.mkdir(parents=True, exist_ok=True)
    nev = args.nev or (p.parent.name if p.stem == "index" else p.stem)
    url = p.as_uri()
    meretek = [("asztali-hero", 1440, 900), ("asztali-teljes", 1440, args.magassag),
               ("mobil-hero", 390, 844), ("mobil-teljes", 390, min(int(args.magassag * 2.2), 30000))]
    keret = ki / f".{nev}-mobilkeret.html"
    for cimke, w, h in meretek:
        cel = ki / f"{nev}-{cimke}.png"
        cim, ablak = url, w
        if w < 500:
            # a headless Chrome ablaka legalább 500 px széles: a mobil nézet egy pontos szélességű keretben készül
            keret.write_text(f'<!doctype html><body style="margin:0;background:#888"><iframe src="{url}" '
                             f'style="border:0;display:block;background:#fff;width:{w}px;height:{h}px"></iframe></body>', encoding="utf-8")
            cim, ablak = keret.resolve().as_uri(), 500
        parancs = [b, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-prefers-reduced-motion",
                   "--allow-file-access-from-files", "--force-device-scale-factor=1", f"--window-size={ablak},{h}",
                   "--virtual-time-budget=5000", f"--screenshot={cel}", cim]
        subprocess.run(parancs, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        if cel.exists() and ablak != w:
            try:  # a keret melletti szürke sáv levágása, hogy ne tűnjön vízszintes görgetésnek
                from PIL import Image
                with Image.open(cel) as kep:
                    kep.crop((0, 0, w, kep.height)).save(cel)
            except ImportError:
                pass
        print(f"{'✓' if cel.exists() else '✗'} {cel}")
    if keret.exists():
        keret.unlink()  # a saját ideiglenes keretfájlunk
    szeletel(ki, nev)


def szeletel(ki, nev):
    """Az egész oldalas képeket levágja az oldal aljánál, és szakasznyi szeletekre bontja (Pillow kell hozzá)."""
    try:
        from PIL import Image
    except ImportError:
        print("Az egész oldalas képek szeleteléséhez a Pillow kell (pip3 install pillow); enélkül a teljes kép "
              "megvan, de nagyon hosszú. A mobil képek jobb oldalán a szürke sáv a keret széle.")
        return
    for cimke, szel, szelet in (("asztali-teljes", 1440, 1800), ("mobil-teljes", 390, 1600)):
        f = ki / f"{nev}-{cimke}.png"
        if not f.exists():
            continue
        im = Image.open(f).convert("RGB")
        im = im.crop((0, 0, min(szel, im.width), im.height))
        px = im.load()
        w, h = im.size
        alj = px[w // 2, h - 1]
        vege = h
        for y in range(h - 1, 0, -8):
            if any(px[x, y] != alj for x in range(0, w, 12)):
                vege = min(h, y + 24)
                break
        if vege >= h - 8:
            print(f"! {f.name}: az oldal hosszabb lehet a képnél; futtasd újra nagyobb --magassag értékkel")
        im = im.crop((0, 0, w, vege))
        im.save(f)
        for regi in ki.glob(f"{nev}-{cimke}-*.png"):
            regi.unlink()  # az előző futás szeletei
        db = (vege + szelet - 1) // szelet
        for i in range(db):
            im.crop((0, i * szelet, w, min(vege, (i + 1) * szelet))).save(ki / f"{nev}-{cimke}-{i + 1:02}.png")
        print(f"✓ {f.name}: {vege} px magas, {db} szeletben ({nev}-{cimke}-01.png …)")


# ---------------------------------------------------------------- WordPress

def cmd_wp(args):
    forras = Path(args.html).read_text(encoding="utf-8")
    linkek = re.findall(r'<link[^>]+fonts\.(?:googleapis|gstatic)\.com[^>]*>', forras)
    stilusok = [m.group(0) for m in re.finditer(r"<style\b(?![^>]*data-csak-onallo)[^>]*>.*?</style>", forras, re.S)]
    m = re.search(r"<body[^>]*>(.*)</body>", forras, re.S)
    if not m:
        raise SystemExit("HIBA: nincs <body> a fájlban")
    torzs = m.group(1).strip()
    if 'class="lp' not in torzs:
        raise SystemExit('HIBA: nincs <div class="lp"> burkoló a <body>-ban')
    tartalom = "\n".join(linkek + stilusok + [torzs])
    tartalom = re.sub(r"<!--\s*MÉRŐKÓD.*?-->\s*", "", tartalom, flags=re.S)
    if args.koszi_url:
        tartalom = re.sub(r"(['\"])koszi\.html\1", lambda x: f"{x.group(1)}{args.koszi_url}{x.group(1)}", tartalom)

    # A képek. Az SVG-t a WordPress alapból nem engedi feltölteni, ezért beágyazzuk; a többi
    # képet a wp-kepek/ mappába másoljuk egyedi, WordPress-barát névvel, és a Médiatár címére irányítjuk.
    import base64
    forras_mappa = Path(args.html).resolve().parent
    ki = Path(args.ki)
    kep_mappa = ki.parent / "wp-kepek"
    elotag = wp_nev(args.elotag or ajanlat_nev(Path(args.html)))
    utvonalak = sorted(set(re.findall(r"kepek/[^\"')\s?#]+", tartalom)))
    alap = mediatar_alap(args.mediatar) if args.mediatar else None
    csere, feltoltendo, hianyzik = {}, [], []
    for ut in utvonalak:
        fajl = forras_mappa / ut
        if not fajl.is_file():
            hianyzik.append(ut)
            continue
        if fajl.suffix.lower() == ".svg":
            adat = base64.b64encode(fajl.read_bytes()).decode("ascii")
            csere[ut] = "data:image/svg+xml;base64," + adat
            continue
        uj = wp_nev(f"{elotag}-{fajl.stem}") + fajl.suffix.lower()
        kep_mappa.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(fajl, kep_mappa / uj)
        feltoltendo.append(uj)
        csere[ut] = (alap + uj) if alap else ut
    for regi in sorted(csere, key=len, reverse=True):
        tartalom = re.sub(r"(?<![\w/])" + re.escape(regi) + r"(?=[\"')\s?#])", lambda _: csere[regi], tartalom)

    fej = ("<!-- Landing oldal WordPresshez: másold be a teljes tartalmat egy Gutenberg Egyéni HTML blokkba "
           "vagy egy Elementor HTML-widgetbe, fejléc és lábléc nélküli oldalsablonon. A mérőkódokat a "
           "WordPress-bővítmény adja. -->\n")
    if feltoltendo and not alap:
        fej += ("<!-- FIGYELEM: a képek címe még nincs beállítva. Töltsd fel a wp-kepek mappa képeit a "
                "Médiatárba, másold ki az egyik kép címét, és futtasd újra: landing.py wp ... --mediatar <a kép címe> -->\n")
    ki.write_text(fej + tartalom + "\n", encoding="utf-8")
    print(f"✓ {ki}")
    if feltoltendo:
        print(f"✓ {kep_mappa}/: {len(feltoltendo)} kép a Médiatárba ({', '.join(feltoltendo)})")
        if alap:
            print(f"  a képek címe: {alap}<fájlnév>")
            if args.mediatar and not re.search(r"/uploads/", args.mediatar):
                print("  ! a hónapot a mai dátumból számoltam: ha a képeket később töltöd fel, futtasd újra "
                      "a Médiatárból kimásolt képcímmel")
        else:
            print("  ! a képek címe még relatív: feltöltés után futtasd újra --mediatar <egy feltöltött kép címe>")
    if hianyzik:
        print(f"  ! nem találom: {', '.join(hianyzik)}")


def ajanlat_nev(html_ut):
    """oldalak/<ajanlat>/landing/feltoltes/index.html -> <ajanlat>; ha nem így áll, a mappa neve."""
    reszek = html_ut.resolve().parts
    if "oldalak" in reszek:
        i = reszek.index("oldalak")
        if i + 1 < len(reszek) - 1:
            return reszek[i + 1]
    return html_ut.resolve().parent.name


def wp_nev(s):
    """Ékezet nélküli, kisbetűs, kötőjeles név: a WordPress így nem nevezi át feltöltéskor."""
    import unicodedata
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "kep"


def mediatar_alap(cim):
    """A Médiatár mappájának címe. Elfogad egy feltöltött kép címét (ebből a mappát veszi),
    egy uploads-mappát, vagy csak az oldal címét (ekkor a mai év/hónap mappát feltételezi)."""
    from datetime import date
    cim = cim.strip()
    if not re.match(r"https?://", cim):
        cim = "https://" + cim
    if re.search(r"\.(jpe?g|png|webp|gif|avif)$", cim, re.I):
        return cim.rsplit("/", 1)[0] + "/"
    if "/wp-content/uploads" in cim:
        return cim.rstrip("/") + "/"
    ma = date.today()
    return f"{cim.rstrip('/')}/wp-content/uploads/{ma.year}/{ma.month:02d}/"


# ---------------------------------------------------------------- generált ikonok

def hex_rgb(h):
    h = h.strip().lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def kulcs_alfa(kep, kulcs, lo=40, hi=140):
    """Egyszínű (chroma) háttér kivágása: mennyire „kulcsszínű” egy pixel, abból az átlátszóság."""
    from PIL import ImageChops
    r, g, b = kep.convert("RGB").split()
    csat = {"r": r, "g": g, "b": b}
    kulcsban = [csat[n] for n, v in zip("rgb", kulcs) if v >= 128]
    tobbi = [csat[n] for n, v in zip("rgb", kulcs) if v < 128]
    if not kulcsban or not tobbi:
        raise SystemExit("A kulcsszín legyen élénk, egyértelmű szín (például 00FF00 vagy FF00FF).")
    min_k = kulcsban[0]
    for c in kulcsban[1:]:
        min_k = ImageChops.darker(min_k, c)
    max_t = tobbi[0]
    for c in tobbi[1:]:
        max_t = ImageChops.lighter(max_t, c)
    tobblet = ImageChops.subtract(min_k, max_t)
    lut = [255 if v <= lo else 0 if v >= hi else round(255 * (hi - v) / (hi - lo)) for v in range(256)]
    return tobblet.point(lut), max_t


def cmd_ikonok(args):
    """Generált, egyszínű hátterű ikonlapból átlátszó PNG- és (ha van vtracer) színes SVG-ikonok."""
    try:
        from PIL import Image
    except ImportError:
        raise SystemExit("Ehhez a Pillow kell: python3 -m pip install pillow")
    kulcs = hex_rgb(args.kulcs)
    osz, sor = (int(v) for v in args.racs.lower().split("x"))
    nevek = [wp_nev(n) for n in args.nevek.split(",") if n.strip()]
    if len(nevek) > osz * sor:
        raise SystemExit(f"{len(nevek)} név, de a rácsban csak {osz * sor} hely van.")
    lap = Image.open(args.lap).convert("RGB")
    W, H = lap.size
    alfa, _ = kulcs_alfa(lap, kulcs)
    ki = Path(args.ki)
    ki.mkdir(parents=True, exist_ok=True)

    # a paletta: a márka színei, vagy a lap nem háttér pixeleiből kiolvasva
    if args.marka:
        paletta = [hex_rgb(h) for h in args.marka.split(",") if h.strip()]
    else:
        kicsi = lap.resize((W // 4, H // 4))
        ka = alfa.resize(kicsi.size)
        pixelek = [p for p, a in zip(kicsi.getdata(), ka.getdata()) if a > 230]
        # a leggyakoribb, egymástól jól elkülönülő színek (a vonal és a kitöltés határán kevert pixelek kiesnek)
        from collections import Counter
        rekesz = Counter((r // 16, g // 16, b // 16) for r, g, b in pixelek)
        paletta = []
        for (r, g, b), _ in rekesz.most_common():
            c = (r * 16 + 8, g * 16 + 8, b * 16 + 8)
            if all(sum((x - y) ** 2 for x, y in zip(c, p)) > 70 ** 2 for p in paletta):
                tag = [px for px in pixelek if (px[0] // 16, px[1] // 16, px[2] // 16) == (r, g, b)]
                paletta.append(tuple(sum(v[i] for v in tag) // len(tag) for i in range(3)))
            if len(paletta) == args.szinek:
                break
    teljes = paletta + [kulcs]
    pal_kep = Image.new("P", (1, 1))
    pal_kep.putpalette([v for c in teljes for v in c] + [0] * (768 - 3 * len(teljes)))

    try:
        import vtracer
    except ImportError:
        vtracer = None
    import tempfile
    for i, nev in enumerate(nevek):
        x, y = i % osz, i // osz
        doboz = (x * W // osz, y * H // sor, (x + 1) * W // osz, (y + 1) * H // sor)
        cella, ca = lap.crop(doboz), alfa.crop(doboz)
        bb = ca.point(lambda v: 255 if v > 24 else 0).getbbox()
        if not bb:
            print(f"✗ {nev}: üres cella")
            continue
        bb = (max(bb[0] - 6, 0), max(bb[1] - 6, 0), min(bb[2] + 6, cella.width), min(bb[3] + 6, cella.height))
        cella, ca = cella.crop(bb), ca.crop(bb)
        oldal = round(max(cella.size) * 1.08)
        hely = ((oldal - cella.width) // 2, (oldal - cella.height) // 2)
        # PNG: átlátszó, a kulcsszín-szegély nélkül
        _, max_t = kulcs_alfa(cella, kulcs)
        r, g, b = cella.split()
        tisztitott = [c if v < 128 else ImageChops_darker(c, max_t) for c, v in zip((r, g, b), kulcs)]
        rgba = Image.merge("RGBA", (*tisztitott, ca))
        negyzet = Image.new("RGBA", (oldal, oldal), (0, 0, 0, 0))
        negyzet.paste(rgba, hely)
        negyzet.resize((args.meret, args.meret), Image.LANCZOS).save(ki / f"{nev}.png", optimize=True)
        sor_ki = f"✓ {nev}.png"
        # SVG: a palettára egyszerűsítve, vektorizálva, a háttér formái nélkül
        if vtracer:
            alap = Image.new("RGB", (oldal, oldal), kulcs)
            alap.paste(cella, hely)
            alap = alap.resize((360, 360), Image.LANCZOS).quantize(palette=pal_kep, dither=Image.Dither.NONE).convert("RGB")
            with tempfile.TemporaryDirectory() as tmp:
                be, svg_ut = Path(tmp) / "be.png", Path(tmp) / "ki.svg"
                alap.save(be)
                vtracer.convert_image_to_svg_py(str(be), str(svg_ut), colormode="color", hierarchical="cutout",
                                                mode="spline", filter_speckle=6, color_precision=8, layer_difference=8,
                                                corner_threshold=60, length_threshold=4.0, max_iterations=10,
                                                splice_threshold=45, path_precision=1)
                svg = svg_ut.read_text(encoding="utf-8")

            def szin(m):
                c = hex_rgb(m.group(1))
                legk = min(teljes, key=lambda p: sum((a - b) ** 2 for a, b in zip(p, c)))
                return None if legk == kulcs else '#%02X%02X%02X' % legk
            utak = []
            for m in re.finditer(r'<path[^>]*/>', svg):
                f = re.search(r'fill="#([0-9A-Fa-f]{6})"', m.group(0))
                uj = szin(f) if f else None
                if uj:
                    utak.append(m.group(0).replace(f.group(0), f'fill="{uj}"'))
            svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 360" width="360" height="360">\n'
                   + "\n".join(utak) + "\n</svg>\n")
            (ki / f"{nev}.svg").write_text(svg, encoding="utf-8")
            sor_ki += f", {nev}.svg ({len(svg) // 1024 + 1} KB)"
        print(sor_ki)
    print("  paletta: " + " ".join('#%02X%02X%02X' % c for c in paletta))
    if not vtracer:
        print("  ! SVG nem készült, mert nincs telepítve a vtracer (python3 -m pip install vtracer); a PNG-k használhatók")


def ImageChops_darker(a, b):
    from PIL import ImageChops
    return ImageChops.darker(a, b)


# ---------------------------------------------------------------- ikonlap

def cmd_ikonlap(args):
    """Az oldal saját ikonjai egy lapon, 24, 48 és 96 px-en, az oldal stílusaival."""
    forras = Path(args.html).read_text(encoding="utf-8")
    linkek = re.findall(r'<link[^>]+fonts\.(?:googleapis|gstatic)\.com[^>]*>', forras)
    stilusok = [m.group(0) for m in re.finditer(r"<style\b[^>]*>.*?</style>", forras, re.S)]
    ikonok = re.findall(r'<svg\b[^>]*class="[^"]*lp-ikon[^"]*"[^>]*>.*?</svg>', forras, re.S)
    alapmappa = Path(args.html).resolve().parent
    for m in re.finditer(r'<img\b[^>]*class="[^"]*lp-ikon[^"]*"[^>]*>', forras):
        src = re.search(r'src="([^"]+)"', m.group(0))
        if src and not re.match(r"(https?:|data:)", src.group(1)):
            ikonok.append(m.group(0).replace(src.group(0), f'src="{(alapmappa / src.group(1)).as_uri()}"'))
        else:
            ikonok.append(m.group(0))
    if not ikonok:
        raise SystemExit('Nincs ikon az oldalon (class="lp-ikon" osztályú <svg> vagy <img>).')
    egyedi = list(dict.fromkeys(ikonok))
    def meretez(svg, m):
        svg = re.sub(r'\s(width|height|style)="[^"]*"', "", svg, count=3)
        # az oldal saját .lp-ikon méretszabálya ne írja felül a lap méreteit
        tag = "<img" if svg.startswith("<img") else "<svg"
        return svg.replace(tag, f'{tag} width="{m}" height="{m}" style="width:{m}px!important;height:{m}px!important;flex:none"', 1)
    sorok = []
    for i, svg in enumerate(egyedi, 1):
        cellak = "".join(f'<div class="ik-cella">{meretez(svg, m)}<small>{m}</small></div>' for m in (24, 48, 96))
        sorok.append(f'<div class="ik-sor"><b>{i}</b>{cellak}</div>')
    lap = ("<!doctype html><html lang=\"hu\"><head><meta charset=\"utf-8\"><title>Ikonlap</title>"
           + "".join(linkek) + "".join(stilusok)
           + "<style>body{margin:0}.ik{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));"
             "gap:24px;padding:32px}.ik-sor{display:flex;align-items:center;gap:20px;padding:16px;"
             "border:1px solid rgba(0,0,0,.12)}.ik-sor b{width:24px;font:600 14px sans-serif;opacity:.5}"
             ".ik-cella{display:flex;flex-direction:column;align-items:center;gap:6px}"
             ".ik-cella small{font:12px sans-serif;opacity:.5}</style></head><body>"
           + '<div class="lp"><div class="ik">' + "".join(sorok) + "</div></div></body></html>")
    Path(args.ki).parent.mkdir(parents=True, exist_ok=True)
    Path(args.ki).write_text(lap, encoding="utf-8")
    print(f"✓ {args.ki}: {len(egyedi)} különböző ikon (összesen {len(ikonok)} az oldalon)")


# ---------------------------------------------------------------- ikonok

IKONOK = Path(__file__).resolve().parent.parent / "ikonok" / "phosphor.json"
STILUSOK = ("vonalas", "kitoltott", "ketszinu", "szinatmenetes")


def cmd_ikon(args):
    import json
    import secrets
    adat = json.loads(IKONOK.read_text(encoding="utf-8"))
    if args.lista or not args.nev:
        for nev, i in adat.items():
            print(f"{nev:22} {i['cimke']}")
        print(f"\n{len(adat)} ikon; stílusok: {', '.join(STILUSOK)}")
        return
    if args.nev not in adat:
        hasonlo = [n for n, i in adat.items() if args.nev in n or args.nev in i["cimke"]]
        raise SystemExit(f"Nincs ilyen ikon: {args.nev}." + (f" Hasonló: {', '.join(hasonlo[:8])}" if hasonlo else
                         " A nevek: landing.py ikon --lista"))
    i = adat[args.nev]
    fej = (f'<svg class="lp-ikon" viewBox="0 0 256 256" width="{args.meret}" height="{args.meret}" '
           f'aria-hidden="true" focusable="false"')
    if args.stilus == "szinatmenetes":
        gid = f"lp-g-{args.nev}-{secrets.token_hex(2)}"
        svg = (f'{fej} fill="url(#{gid})"><defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">'
               '<stop offset="0" style="stop-color:var(--lp-ikon-szin1, var(--lp-szin-fo, var(--ds-elsodleges, currentColor)))"/>'
               '<stop offset="1" style="stop-color:var(--lp-ikon-szin2, color-mix(in srgb, var(--lp-szin-fo, var(--ds-elsodleges, currentColor)) 55%, black))"/>'
               f'</linearGradient></defs>{i["kitoltott"]}</svg>')
    elif args.stilus == "ketszinu":
        belso = i["ketszinu"].replace('class="lp-ikon-hatter"',
                                       'class="lp-ikon-hatter" style="fill:var(--lp-ikon-masodik, currentColor);opacity:var(--lp-ikon-hatter-atl, .25)"')
        svg = f'{fej} fill="currentColor">{belso}</svg>'
    else:
        svg = f'{fej} fill="currentColor">{i[args.stilus]}</svg>'
    print(svg)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="parancs", required=True)

    e = sub.add_parser("ellenoriz")
    e.add_argument("html")
    e.add_argument("--szoveg", help="a szoveg.md: a címek, gombok, bekezdések szó szerint ott vannak-e")
    e.add_argument("--tokens", help="a tokens.css: a márka színei és betűi változatlanok-e")
    e.add_argument("--koszi", action="store_true", help="köszönőoldal: nincs űrlap és description-ellenőrzés")
    e.add_argument("--koszi-url", help="ha a köszönőoldal nem koszi.html")
    e.set_defaults(fn=cmd_ellenoriz)

    k = sub.add_parser("kepernyokep")
    k.add_argument("html")
    k.add_argument("--ki", required=True, help="a képek mappája")
    k.add_argument("--nev", help="a fájlnevek eleje (alapból a változat mappájának neve)")
    k.add_argument("--magassag", type=int, default=16000, help="az asztali egész oldalas kép legnagyobb magassága")
    k.set_defaults(fn=cmd_kepernyokep)

    w = sub.add_parser("wp")
    w.add_argument("html")
    w.add_argument("-o", "--ki", required=True)
    w.add_argument("--mediatar", help="egy feltöltött kép címe a Médiatárból (vagy csak az oldal címe: ekkor a mai hónap mappája)")
    w.add_argument("--elotag", help="a képek nevének eleje (alapból az ajánlat mappájának neve)")
    w.add_argument("--koszi-url", help="a köszönőoldal címe WordPressben, ha nem koszi.html")
    w.set_defaults(fn=cmd_wp)

    ig = sub.add_parser("ikonok")
    ig.add_argument("lap", help="a generált ikonlap (egyszínű kulcsháttéren, rácsban)")
    ig.add_argument("--nevek", required=True, help="az ikonok neve sorban, vesszővel (balról jobbra, fentről le)")
    ig.add_argument("--racs", default="4x2", help="oszlop x sor (alapból 4x2)")
    ig.add_argument("--ki", required=True, help="a kimeneti mappa, például kepek/ikonok")
    ig.add_argument("--kulcs", default="00FF00", help="a háttér kulcsszíne (alapból 00FF00; zöld márkánál FF00FF)")
    ig.add_argument("--szinek", type=int, default=3, help="hány színből áll az ikonkészlet (a háttér nélkül)")
    ig.add_argument("--marka", help="a márka színei vesszővel (#3D3C39,#98556E,...): az ikon színei ezekre igazodnak")
    ig.add_argument("--meret", type=int, default=256, help="a PNG mérete pixelben")
    ig.set_defaults(fn=cmd_ikonok)

    il = sub.add_parser("ikonlap")
    il.add_argument("html")
    il.add_argument("-o", "--ki", required=True, help="az ikonlap HTML-fájlja")
    il.set_defaults(fn=cmd_ikonlap)

    ik = sub.add_parser("ikon")
    ik.add_argument("nev", nargs="?", help="az ikon neve (landing.py ikon --lista)")
    ik.add_argument("--stilus", choices=STILUSOK, default="vonalas")
    ik.add_argument("--meret", type=int, default=32, help="szélesség és magasság pixelben")
    ik.add_argument("--lista", action="store_true", help="az ikonok neve és hogy mire valók")
    ik.set_defaults(fn=cmd_ikon)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
