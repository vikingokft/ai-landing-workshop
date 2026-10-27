#!/usr/bin/env python3
"""Humanizer mechanical pre-scan.


Detects two kinds of AI-writing tell that have a reliable *surface form*:

  1. FIXED-SHAPE tells — exact characters, words, or phrases (em dashes, curly
     quotes, AI vocabulary, filler phrases, chatbot artifacts, etc.).
  2. TEMPLATE-SHAPE tells — recognizable syntactic rhythms, chiefly the
     antithesis/negative-parallelism family ("isn't X. It's Y", "you don't X.
     You Y", "Not X, just Y") and the "the real <noun>" authority trope. These
     read as semantic, but their *shape* is matchable, and they are the tells
     most likely to slip past a tired manual walk precisely because the writer
     reaches for them by reflex.

It still does NOT attempt the genuinely shape-free semantic patterns
(significance inflation, superficial -ing analyses, rule-of-three, false ranges,
diff-anchored writing, etc.); those need a human/model read and live in the
structured detection pass described in SKILL.md.

Why this exists: every invocation otherwise re-derives the regexes by hand and
drifts (misses the en dash one run, the antithesis rhythm the next). This script
makes the matchable part deterministic and gives verification a single gate.

It REPORTS, it never edits. A hit is a CANDIDATE, not a verdict — a lone curly
quote from a word processor, or a single earned contrast that carries the post's
whole point ("you don't need a better prompt. You need a gate."), is not an AI
tell. Apply the clustering rule in patterns.md ("Detection guidance") before
rewriting: an isolated template hit in otherwise human prose is kept; the same
template firing several times in one piece, or across a set of sibling posts, is
the reflex worth rewriting.

Canonical source for the vocabulary list is patterns.md §7. When you change the
wordlists or template regexes here, update the matching §-section in patterns.md
and the plugin README in the same change (see AGENTS.md, "The maintenance
contract").

Usage:
    python3 "$SKILL_DIR/scripts/scan.py" <file>
        # set SKILL_DIR to the skill's "Base directory" (see SKILL.md Path Rules)
    python3 "$SKILL_DIR/scripts/scan.py" <file1> <file2> ...
        # set mode: also reports templates repeated across files
    python3 "$SKILL_DIR/scripts/scan.py"            # reads stdin
    cat draft.md | python3 "$SKILL_DIR/scripts/scan.py"

Set mode matters for sibling content (the X / LinkedIn / Threads variants of one
post): an antithesis used once is a choice, the same antithesis used in all three
variants is a crutch. Pass the related files together to surface that.

Exit code: 0 if no tells found, 1 if any found (so a verification step can gate
on it), 2 on usage/IO error.
"""

import re
import sys


# A magyar szoveg `ő` es `ű` betui NEM leteznek a Windows-konzol cp1252 kodlapjan (csak a
# kozep-europai cp1250-ben). Enelkul a print() UnicodeEncodeError-ral eldobja a szkriptet egy
# Windows-gepen — ez lappango osszeomlas volt: a doktor 25, a scanner 36 ilyen betut ir.
# A `replace` azert kell, hogy egy meg szukebb kodlapon se omoljon ossze, csak csunyabb legyen.
def _utf8_kimenet() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (ValueError, OSError):
                pass


_utf8_kimenet()


# Fixed-shape phrase/word lists, keyed to the patterns.md section they detect.
# Each entry: section label -> list of case-insensitive phrases (matched as
# whole words / phrases via word boundaries).
PHRASE_TELLS = {
    "§4 reklámnyelv": [
        "megbúvó", "megbúvva", "pezsgő", "lenyűgöző~", "kihagyhatatlan~",
        "varázslatos~", "felejthetetlen~", "szívében", "elismert", "forradalmi~", "forradalmasít~",
    ],
    "§7 AI-szókincs": [
        "kulcsfontosságú~", "elengedhetetlen~", "felbecsülhetetlen~",
        "merüljünk el", "merülj el", "merüljön el", "merüljenek el", "íme néhány", "íme egy",
        "a mai rohanó világban", "a mai rohanó", "lehetőségek tárház~",
        "holisztikus~", "szinergi~", "kihívást jelent~", "a nap végén",
        "izgalmas utazás~", "emeld új szintre", "emelje új szintre", "zökkenőmentes~", "gamechanger",
        "letéteményes~", "maradandó bizonyíték~", "kiaknáz~",
    ],
    # A markahang "Tiltott nyito-mintak" alfejezete ezeket sorolta — de ezek NEM markadontesek,
    # hanem univerzalis AI-reflexek: senkinek nem all jol. Ezert itt a helyuk, nem ott.
    "§31 AI-nyitány": [
        "a mai világban", "a mai digitális világban", "napjaink rohanó",
        "képzeld el, ahogy", "képzelje el, ahogy", "képzeld el, hogy", "képzelje el, hogy",
        "te is unod", "ön is unja", "unod már, hogy", "unja már, hogy",
        "ismerős a helyzet", "gondolkodtál már azon", "gondolkodott már azon",
        "lépésről lépésre végigvezet~",
    ],
    "§8 igei körülírás": [
        "megtestesíti", "magában foglalja", "büszkélkedik",
        "szolgál mint", "szolgál a", "képviseli a", "letéteményese",
    ],
    "§9 tagadó párhuzam": [
        "nem csupán", "nem csak", "nem kizárólag", "nem pedig",
        "nem az a kérdés", "nem arról van szó",
    ],
    "§13 szenvedő szerkezet": [
        "ásra kerül", "ésre kerül", "sor kerül rá", "megtörténik a",
        "elvégzésre", "kialakításra", "tájékoztatásra", "felhasználásra kerül",
    ],
    "§20 chatbot-maradvány": [
        "remélem, segítettem", "remélem segítettem", "szólj, ha", "szóljon, ha",
        "íme egy", "íme az", "természetesen!", "az alábbiakban bemutatom",
        "szeretnéd, hogy", "bátran kérdezz",
    ],
    "§21 tudás-korlát kifogás": [
        "a legutóbbi információim szerint", "a tudásom szerint",
        "bár a konkrét részletek korlátozottak", "a rendelkezésre álló információk alapján",
        "nyilvánosan nem elérhető", "visszafogottan kommunikál",
        "nem oszt meg részleteket",
    ],
    "§22 talpnyalás": [
        "nagyszerű kérdés", "kiváló kérdés", "teljesen igazad van",
        "kiváló észrevétel", "jó észrevétel", "szívesen segítek",
        "remek kérdés",
    ],
    "§23 töltelék": [
        "annak érdekében, hogy", "azon okból kifolyólag", "abban az esetben, ha",
        "fontos megjegyezni", "meg kell jegyezni", "mondani sem kell",
        "a jelenlegi helyzetben", "rendelkezésre áll a lehetőség",
        "azzal a céllal, hogy",
    ],
    "§24 halmozott puhítás": [
        "talán esetleg", "esetleg elképzelhető", "valószínűleg talán",
        "akár lehetséges, hogy", "elmondható, hogy",
    ],
    "§25 üres pozitív zárás": [
        "a jövő fényes", "izgalmas idők", "az úton előre",
        "jó irányba tett lépés", "a lehetőségek végtelenek",
        "összességében izgalmas",
    ],
    "§26 kötőjeles párok": [
        "adat-vezérelt", "cél-orientált", "ügyfél-központú", "érték-alapú",
        "megoldás-orientált", "eredmény-vezérelt", "élvonalbeli",
    ],
    "§27 tekintély-fordulat": [
        "a valódi kérdés az", "a lényeg az", "ami igazán számít",
        "a dolog velejére", "a mélyebb probléma", "alapvetően,",
        "a valóságban,", "az igazi kérdés",
    ],
    "§28 útjelző": [
        "merüljünk el", "nézzük meg közelebbről", "bontsuk le",
        "íme, amit tudni kell", "minden további nélkül", "most nézzük",
        "ebben a cikkben",
    ],
}


# A magyar nem csak ragoz, hanem TOHANGZOT IS NYUJT: "tarhaza" -> "tarhazABAN".
# Ezert a fix szohataros illesztes kicsuszik. A szolistaban egy zaro `~` jel azt jelenti:
# a frazis utolso szavan rag allhat — ilyenkor a TOVET kell megadni, nem a birtokos vagy
# ragozott alakot (tehat "lehetosegek tarhaz~", nem "lehetosegek tarhaza~").
#
# Szandekosan opt-in, nem blanket: igy egy "kihivas" tipusu rovid szo nem kezd
# tulilleszteni. A rag legfeljebb 6 kisbetu — ennyi elfer a magyar esetragokbol
# (-ban, -aban, -abol, -anak, -aval, -ainak).
SUFFIX_MARK = "~"
_SUFFIX = r"[a-záéíóöőúüű]{0,6}"


def _phrase_regex(phrase):
    """Return a unicode-aware boundary regex for a fixed tell phrase."""
    ragozhato = phrase.endswith(SUFFIX_MARK)
    phrase = phrase.rstrip(SUFFIX_MARK)
    parts = re.split(r"\s+", phrase.strip())
    body = r"\s+".join(re.escape(part) for part in parts)
    prefix = r"(?<![^\W_])" if phrase[:1].isalnum() else ""
    if ragozhato:
        return re.compile(prefix + body + _SUFFIX + r"(?![^\W_])", re.IGNORECASE)
    suffix = r"(?![^\W_])" if phrase[-1:].isalnum() else ""
    return re.compile(prefix + body + suffix, re.IGNORECASE)


PHRASE_PATTERNS = {
    section: [(phrase.rstrip(SUFFIX_MARK), _phrase_regex(phrase)) for phrase in phrases]
    for section, phrases in PHRASE_TELLS.items()
}

# --- Template-shape tells -------------------------------------------------
#
# The antithesis family (§9) and the "real <noun>" trope (§27) are not fixed
# phrases, but their *rhythm* is matchable. Each regex targets one reflex
# construction. These fire per-sentence; the report groups them and the
# clustering rule (in patterns.md) decides what to actually rewrite. The point
# is to make the rhythm visible, not to auto-condemn it — one earned contrast is
# human, the same beat three times is the tell.
#
# Patterns are deliberately conservative: they look for the negation + pivot
# rhythm, not every "not" in the text. Each is documented with the shape it
# catches.
TEMPLATE_TELLS = [
    # „Nem X, hanem Y" — a klasszikus kétütemű szembeállítás.
    #
    # FIGYELEM, MAGYAR KALIBRÁCIÓ: a `nem … hanem` magyarban NORMÁL nyelvtani
    # szerkezet, nem retorikai reflex. „A raktár nem a lakásban van, hanem a
    # Sorház utcában" tökéletesen természetes mondat. Ha minden előfordulást
    # jelölnénk, a scanner zajossá válna, és az angol eredetihez képest sokkal
    # több hamis pozitívot adna.
    #
    # Ezért csak akkor jelöljük, ha a szerkezet ELVONT fogalmakat állít szembe
    # (ott retorikai), nem konkrét helyet, időt, tárgyat vagy személyt.
    (
        "§9 tagadó párhuzam",
        "Nem-X-hanem-Y szembeállítás (elvont)",
        re.compile(
            r"\bnem\b[^.!?]{0,40}?\b(?:a|az)?\s*"
            r"(?:technológia|eszköz|módszer|kérdés|lényeg|cél|probléma|dolog|"
            r"pénz|idő|tudás|ember|munka|rendszer|megoldás|siker|titok)\b"
            r"[^.!?]{0,50}?\bhanem\b",
            re.IGNORECASE,
        ),
    ),
    # „Nem azért X. Hanem Y." — a kétmondatos változat. A második mondat
    # `Hanem`-mel vagy `Ez`-zel indul, és ugyanarra a tárgyra utal vissza.
    (
        "§9 tagadó párhuzam",
        "kétmondatos Nem… / Hanem… változat",
        # Csak akkor jel, ha a MÁSODIK MONDAT indul `Hanem`-mel. Az `ez`/`az`
        # kezdet csak a következő mondat, nem szembeállítás, és hamis pozitívot
        # adott természetes szövegen.
        re.compile(r"\bnem\b[^.!?]{1,80}?[.!?]\s+hanem\b", re.IGNORECASE),
    ),
    # „Nem X, csak Y" — a csonkolt fordulat. („Nem több promptolás, csak jobb jegyzet.")
    (
        "§9 tagadó párhuzam",
        "Nem-X-csak-Y csonkolt fordulat",
        re.compile(r"(?:^|[.!?]\s+)nem\s+[^.!?]{1,60}?[,.]\s*(?:csak|csupán|mindössze)\b",
                   re.IGNORECASE | re.MULTILINE),
    ),
    # „Nem arról van szó, hogy X, hanem hogy Y" — a magyar „it's not about X" megfelelője.
    (
        "§9 tagadó párhuzam",
        "Nem-arról-van-szó fordulat",
        re.compile(r"\bnem\s+(?:arról|az)\s+(?:van\s+szó|a\s+kérdés)\b", re.IGNORECASE),
    ),
    # „Nem a … -vel van baj" — rejtett tagadó párhuzam.
    (
        "§9 tagadó párhuzam",
        "Nem-a-…-vel-van-baj fordulat",
        re.compile(r"\bnem\s+a[z]?\s+[^.!?]{1,40}?\bvan\s+(?:baj|gond|probléma)\b",
                   re.IGNORECASE),
    ),
    # „A valódi/igazi <főnév> az" — tekintély-fordulat, ami a lényegre vágást ígéri (§27).
    (
        "§27 tekintély-fordulat",
        "A-valódi-<főnév> keretezés",
        re.compile(r"\ba[z]?\s+(?:valódi|igazi|tényleges)\s+"
                   r"(?:kérdés|probléma|ok|készség|munka|válasz|lényeg|különbség|történet)\b",
                   re.IGNORECASE),
    ),
    # „Ami igazán számít" / „a lényeg az" — ugyanaz a keretezés más szórenddel.
    (
        "§27 tekintély-fordulat",
        "Ami-igazán-számít keretezés",
        re.compile(r"\bami\s+(?:igazán|valóban|tényleg)\s+(?:számít|fontos|érdekes)\b",
                   re.IGNORECASE),
    ),
    # „-va/-ve" lezáró igenév a mondat végén: hamis mélység (§3).
    # Konzervatív: csak a jellemzo igek, es csak mondatveg elott.
    (
        "§3 felszínes elemzés",
        "lezáró -va/-ve igenév",
        re.compile(r",\s*(?:rávilágítva|tükrözve|bemutatva|hangsúlyozva|"
                   r"demonstrálva|illusztrálva|jelezve|kiemelve)\s*[.!?]",
                   re.IGNORECASE),
    ),
]

TEMPLATE_LABELS = {(section, label) for section, label, _rx in TEMPLATE_TELLS}


def _blank_protected(line):
    """Replace protected content with spaces, preserving newline bytes."""
    return "".join(ch if ch in "\r\n" else " " for ch in line)


INLINE_CODE_RE = re.compile(r"`+[^`\n]*`+")
FENCE_RE = re.compile(r"^\s*(```+|~~~+)")


def mask_protected_regions(text):
    """Blank code fences, inline code, and YAML frontmatter without moving lines."""
    lines = text.splitlines(keepends=True)
    masked = []
    # Only treat a leading --- as frontmatter if a closing delimiter exists
    # nearby; otherwise it's a Markdown thematic break and masking it would
    # swallow the whole document.
    in_frontmatter = bool(
        lines
        and lines[0].strip() == "---"
        and any(ln.strip() in ("---", "...") for ln in lines[1:30])
    )
    in_fence = None

    for i, line in enumerate(lines):
        stripped = line.strip()
        if in_frontmatter:
            masked.append(_blank_protected(line))
            if i > 0 and stripped in ("---", "..."):
                in_frontmatter = False
            continue

        fence = FENCE_RE.match(line)
        if in_fence:
            masked.append(_blank_protected(line))
            if fence and fence.group(1).startswith(in_fence):
                in_fence = None
            continue
        if fence:
            in_fence = fence.group(1)[:3]
            masked.append(_blank_protected(line))
            continue

        masked.append(INLINE_CODE_RE.sub(lambda m: " " * len(m.group()), line))

    return "".join(masked)


def _normalize_template_text(text):
    return text.replace("’", "'").replace("‘", "'")


def iter_paragraphs(lines):
    """Yield (start_lineno, paragraph_text) for blank-line separated paragraphs."""
    start = None
    parts = []
    for i, line in enumerate(lines, 1):
        if line.strip():
            if start is None:
                start = i
            parts.append(line.strip())
            continue
        if parts:
            yield start, " ".join(parts)
            start = None
            parts = []
    if parts:
        yield start, " ".join(parts)


def find_template_hits(lines):
    """Return {section: [(lineno, sample, text), ...]} for template-shape tells.

    These are the antithesis/authority rhythms that read as 'semantic' but have
    a matchable surface form. Reported as candidates; clustering decides.
    """
    hits = {}
    for i, paragraph in iter_paragraphs(lines):
        normalized = _normalize_template_text(paragraph)
        for section, label, rx in TEMPLATE_TELLS:
            for _m in rx.finditer(normalized):
                hits.setdefault(section, []).append((i, label, paragraph.strip()))
    return hits


# Emoji ranges (common pictographic blocks). Deliberately broad but excludes
# plain punctuation and ASCII.
EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"  # symbols & pictographs, supplemental, extended-A
    "\U00002600-\U000027BF"  # misc symbols + dingbats
    "\U0001F000-\U0001F0FF"  # mahjong/dominoes/cards
    "\U00002B00-\U00002BFF"  # arrows/stars (★ etc. used as bullets)
    "\U0001F1E6-\U0001F1FF"  # regional indicators (flags)
    "]"
)

# Az ASCII egyenes idezojel MAGYARBAN NEM JEL. A magyar billentyuzeten a „ AltGr-
# kombinacio, tehat aki gepel, "..."-t ir -- ez a normalis emberi alak. (Egy korabbi
# valtozat ezt jelezte; hibas volt, es valos emberi szovegen zajt csinalt.)
#
# A „..." szinten rendben van: ez a helyes magyar tipografia. Jelezni azt bunteti,
# aki gondosan ir.
#
# Ami VALODI jel: az ANGOL gorbe idezojel, vagyis a “ nyito (U+201C). Se nem
# billentyuzet-alak, se nem magyar tipografia -- angolra allitott Wordbol, angol
# forrasbol masolva, vagy angol tipografiai szokasu gepi szovegbol jon. A zaro ”
# (U+201D) kozos a ket nyelvben, ezert CSAK a nyitora szabad kulcsolni.
# Lasd patterns.md §19.
ENGLISH_CURLY_RE = re.compile(r'\u201C')
CURLY_RE = ENGLISH_CURLY_RE  # a jelentes-nev megtartva a hivo oldalon

# em dash, en dash; plus spaced em dash, spaced hyphen, and tight word--word.
DASH_RE = re.compile(r"—|–|\s--\s|\s-\s|(?<=[^\W\d_])--(?=[^\W\d_])")
FILENAME_LINE_RE = re.compile(r"^\S+\.[A-Za-z0-9]{1,8}$")
# A magyar ARSZABAS es NYITVATARTAS tele van nagykotojeles tartomannyal:
# "1 050 - 4 990 Ft", "9-16", "hetfo-szombat", "1-5 munkanap". Ez helyes tipografia,
# nem gondolatjel-tulzas. Ket alak zarodik ki:
#   - szam ... szam (a magyar ezres elvalaszto szokoz miatt korulotte is lehet szokoz)
#   - szo-szo szokoz NELKUL (hetfo-szombat, magyar-angol) -- ez mindig viszony, sosem irasjel
RANGE_RE = re.compile(
    r"\d\s*[\u2013\u2014]\s*\d"
    r"|[^\W\d_][\u2013\u2014][^\W\d_]"
)


def is_range(line, start, end):
    """A talalt kotojel tartomanyt jelol-e? Egy karakterrel tagitunk mind a ket iranyba."""
    for m in RANGE_RE.finditer(line):
        if m.start() <= start and end <= m.end():
            return True
    return False

BOLD_RE = re.compile(r"\*\*[^*\n]+\*\*")
INLINE_HEADER_RE = re.compile(
    r"^\s*(?:[-*]|\d+[.)])\s+"
    r"(?:\*\*[^*\n]+:\*\*|\*\*[^*\n]+\*\*:|__[^_\n]+:__|__[^_\n]+__:)"
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")

# Words that don't count toward "Title Case" (articles/conjunctions/prepositions).
SMALL_WORDS = {
    "a", "an", "the", "and", "or", "but", "nor", "for", "so", "yet", "of",
    "to", "in", "on", "at", "by", "as", "is", "vs", "via", "with", "from",
}


def find_phrase_hits(lines):
    """Return {section: [(lineno, phrase, text), ...]} for phrase/word tells."""
    hits = {}
    for section, phrases in PHRASE_PATTERNS.items():
        for i, line in enumerate(lines, 1):
            for phrase, rx in phrases:
                if rx.search(line):
                    hits.setdefault(section, []).append((i, phrase, line.strip()))
    return hits


def find_regex_hits(lines):
    """Return {section: [(lineno, sample, text), ...]} for char/structure tells."""
    hits = {}

    def add(section, lineno, sample, text):
        hits.setdefault(section, []).append((lineno, sample, text))

    bold_lines = []
    for i, line in enumerate(lines, 1):
        for m in DASH_RE.finditer(line):
            if m.group() == "--" and FILENAME_LINE_RE.match(line.strip()):
                continue
            if is_range(line, m.start(), m.end()):
                continue
            add("§14 mondat-közi gondolatjel", i, repr(m.group()), line.strip())
        for m in CURLY_RE.finditer(line):
            add("§19 angol idézőjel (“…” a „…” helyett)", i, m.group(), line.strip())
        for m in EMOJI_RE.finditer(line):
            add("§18 emoji", i, m.group(), line.strip())
        if INLINE_HEADER_RE.search(line):
            add("§16 beágyazott fejlécű lista", i, "- **Header:**", line.strip())
        if BOLD_RE.search(line):
            bold_lines.append((i, line.strip()))
        hm = HEADING_RE.match(line)
        if hm:
            heading = hm.group(2)
            words = [w for w in re.findall(r"[A-Za-z][\w']*", heading)]
            capd = [w for w in words if w[0].isupper()]
            # Title Case = most non-small words capitalized AND at least one
            # small word that should have been lowercase is capitalized,
            # or 3+ capitalized words beyond the first.
            capd_small = [w for w in words[1:]
                          if w.lower() in SMALL_WORDS and w[0].isupper()]
            if len(words) >= 3 and (capd_small or len(capd) >= 3 and len(capd) == len(words)):
                add("§17 fejléc-nagybetűzés", i, heading, line.strip())

    # Boldface only counts as a tell when it clusters (mechanical heuristic:
    # 3+ bold spans across the document). A single bold phrase is fine.
    total_bold = sum(len(BOLD_RE.findall(l)) for l in lines)
    if total_bold >= 3:
        for i, text in bold_lines:
            add("§15 félkövér-özön", i, "**...**", text)

    return hits


def scan_text(text):
    """Run all three detectors on one document. Returns {section: [hits]}."""
    lines = mask_protected_regions(text).splitlines()
    hits = {}
    for d in (find_regex_hits(lines), find_phrase_hits(lines),
              find_template_hits(lines)):
        for section, items in d.items():
            hits.setdefault(section, []).extend(items)
    return hits


def report_hits(hits, header_label):
    """Print one document's hit report. Returns True if any hits."""
    if not hits:
        print(f"{header_label}Nem találtam jelet. "
              "(A jelentés-alapú mintákat ettől függetlenül kézzel kell végigjárni, "
              "lásd patterns.md.)")
        return False

    total = sum(len(v) for v in hits.values())
    print(f"{header_label}{total} jelölt találat, {len(hits)} mintában.")
    print("Ezek figyelemre szánt jelzések, nem ítéletek. Mindegyikről te döntesz "
          "(SKILL.md C lépés): MARAD az egyedülálló, megérdemelt sor; ÁTÍR a reflex "
          "vagy a készleten át ismétlődő alakzat. Az indokot jegyezd fel.\n")
    for section in sorted(hits, key=lambda s: int(re.match(r"§(\d+)", s).group(1))):
        items = hits[section]
        print(f"{section}  ({len(items)} találat)")
        seen = set()
        for lineno, sample, text in items:
            key = (lineno, sample)
            if key in seen:
                continue
            seen.add(key)
            quote = text if len(text) <= 100 else text[:97] + "..."
            print(f"  sor {lineno}: {sample}  | {quote}")
        print()
    return True


def report_cross_file(per_file_hits):
    """Surface template tells that repeat across sibling files.

    The loudest tell in a content set is the SAME reflex in every variant: an
    antithesis used once is a choice, used in all three platform variants it's a
    crutch. This pass exists because a per-file scan can call each variant
    'clean enough' while the repetition across them is glaring.
    """
    # Collect template-section hits by their label, tracking which files used each.
    by_label = {}
    for fname, hits in per_file_hits.items():
        labels_in_file = set()
        for section, items in hits.items():
            # A magyaritaskor a szakasznevek magyarra valtottak, ez a szuro viszont
            # angolul maradt -- igy a fajlok kozotti ismetlesvizsgalat nemán semmit
            # nem talalt. (Codex-atnezes L04.)
            if section not in ("§9 tagadó párhuzam", "§27 tekintély-fordulat"):
                continue
            for _lineno, label, _text in items:
                if (section, label) not in TEMPLATE_LABELS:
                    continue
                labels_in_file.add((section, "sablon-alakú ritmus"))
        for key in labels_in_file:
            by_label.setdefault(key, []).append(fname)

    repeated = {k: v for k, v in by_label.items() if len(v) >= 2}
    if not repeated:
        return False

    print("=" * 60)
    print("FÁJLOK KÖZÖTTI ISMÉTLÉS — ugyanaz a sablon-ritmus több fájlban.")
    print("Ez a legerősebb átírás-jelzés: egyszer használva döntés, ugyanaz a")
    print("lüktetés minden testvér-változatban reflex. Egy kivételével írd át.\n")
    for (section, label), files in sorted(repeated.items(), key=lambda kv: -len(kv[1])):
        print(f"{section} / {label}  — {len(files)} fájlban:")
        for f in files:
            print(f"    {f}")
        print()
    return True


def main(argv):
    paths = argv[1:]
    try:
        if not paths:
            # A `_utf8_kimenet()` a KIMENETET allitja at, a BEMENETET nem. Egy cp1252
            # szerint olvaso Python-folyamatban a magyar szoveg eltorzul, es a scanner
            # "nem talaltam jelet" eredmenyt ad -- vagyis NEMÁN tisztanak lat egy piszkos
            # szoveget. A nyers bajtokat olvassuk, es magunk dekodoljuk. (Codex-atnezes L11.)
            buffer = getattr(sys.stdin, "buffer", None)
            if buffer is not None:
                docs = {"<stdin>": buffer.read().decode("utf-8-sig", errors="replace")}
            else:
                docs = {"<stdin>": sys.stdin.read()}
        else:
            docs = {}
            for p in paths:
                with open(p, "r", encoding="utf-8-sig") as fh:
                    docs[p] = fh.read()
    except OSError as exc:
        sys.stderr.write(f"scan.py: cannot read input: {exc}\n")
        return 2

    multi = len(docs) > 1
    any_hits = False
    per_file_hits = {}
    for name, text in docs.items():
        hits = scan_text(text)
        per_file_hits[name] = hits
        label = f"[{name}] " if multi else ""
        if multi:
            print(f"===== {name} =====")
        if report_hits(hits, label):
            any_hits = True
        if multi:
            print()

    if multi:
        if report_cross_file(per_file_hits):
            any_hits = True

    return 1 if any_hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
