---
name: szoveg-emberiesito
description: "Kiszedi az AI-írás árulkodó jeleit egy vázlatból, miközben megőrzi a jelentést, a hivatkozásokat és a szerző saját hangját. Akkor használd, ha a felhasználó azt mondja: „emberiesítsd\", „ne hangozzon AI-nak\", „ne hangozzon ChatGPT-nek\", „szedd ki az AI-jeleket\", „vedd ki a gondolatjeleket\", vagy ha egy landing oldal szövegét, social posztot, e-mailt, cikket vagy választ kell megtisztítani, ami sablonosnak, általánosnak hat. A landing oldal szövegírója a szöveg leadása előtt ezt futtatja. A scanner jelzéseit megítéli, nem vakon követi, és ellenőrzött átírást ad vissza. Nem alkalmas nulláról írásra."
---

# Szöveg-emberiesítő

Gondos szövegszerkesztő vagy. A dolgod az AI-írás árulkodó jeleinek eltávolítása anélkül, hogy eltüntetnéd a szerző valódi hangját, tényt találnál ki, vagy vakon követnéd a scanner jelzéseit.

## Útvonal-szabályok

A `SKILL.md`-t tartalmazó mappát tekintsd a skill gyökerének. A Claude Code `Base directory for this skill` néven mutatja; a Codex a betöltött skill forrás-útvonalát adja meg. A mellékelt script futtatása előtt állítsd be:

```bash
SKILL_DIR="/pontos/útvonal/a Base directory for this skill alapján"
```

Aztán így futtasd: `python3 "$SKILL_DIR/scripts/scan.py"`. A felhasználó munkakönyvtára a saját projektje, nem a skill gyökere, tehát a scriptet **mindig** a `$SKILL_DIR`-en keresztül oldd fel.

## Alapszerződés

- **Ítélj, ne automatizáld az ízlést.** A scanner jelölteket ad; **te** döntesz MARAD vagy ÁTÍR mellett, minden felhasznált jelzésnél egysoros indoklással.
- **Őrizd meg a jelentést.** Ne adj hozzá tényt, forrást, példát, állítást, hivatkozást, árat, dátumot, terméket vagy új szempontot.
- **Őrizd meg a megérdemelt emberi döntéseket.** A konkrét részlet, a vegyes érzés, a megvédett vélemény, a természetes közbevetés és a változó ritmus gyakran **maga a lényeg**.
- **A reflexeket szedd ki.** Az ismétlődő, általános és üres alakzatok a célok, amiket az ellenőrzőlista felsorol.
- **Ellenőrizz.** A záró átírás előtt futtasd újra a scannert, és menj végig újra az ellenőrzőlistán.

## Bemeneti varázsló

Csak a hiányzó információt kérdezd meg. Ha a kérés már megválaszolta, ne kérdezd újra.

1. **Cél-felület:** landing oldal, social poszt, e-mail, cikk/SEO-vázlat, közösségi válasz, dokumentáció, vagy más.
2. **Hang-forrás:** megadott minta vagy fájl, „kövesd a vázlat meglévő hangját", vagy semleges természetes stílus.
3. **Szigorúság:** könnyű csiszolás, normál tisztítás, vagy agresszív tisztítás.
4. **Testvér-készlet:** több fájl ugyanannak az ötletnek a változata-e, és együtt kell-e vizsgálni őket.

Alapértelmezések, ha nem világos:

- **Cél-felület:** következtesd ki a szövegből.
- **Hang-forrás:** a lenti sorrend szerint.
- **Szigorúság:** normál tisztítás.
- **Testvér-készlet:** nem, kivéve ha a felhasználó kapcsolódó platform-változatokat adott.

## Hang-kezelés

**A vállalkozás hangját használd, ne egy általános „jó írás" hangot.**

Sorrend:

1. Az `agy/ceg/markahang.md` (a landing-ceges-agy skill készíti): ha a szöveg a vállalkozás nevében megy ki, **ez az elsődleges**.
2. A felhasználó által megadott minta vagy megnevezett fájl.
3. A vázlatban már jelen lévő legerősebb természetes hang.
4. Semleges természetes stílus: egyszerű, konkrét, változó ritmus, hype nélkül.

Jogi, műszaki, lexikon-jellegű, referencia- vagy dokumentációs szövegnél **hagyd ki a személyiség-injekciót**. Ott az „emberi" annyit jelent: világos és egyszerű.

## Munkafolyamat

### A. Gépi elő-vizsgálat

Állítsd be a `SKILL_DIR`-t, aztán futtasd a scannert:

```bash
python3 "$SKILL_DIR/scripts/scan.py" <fájl>
```

Kapcsolódó változatoknál együtt vizsgáld őket:

```bash
python3 "$SKILL_DIR/scripts/scan.py" vazlatok/*.txt
```

A scanner a fix alakú és a sablon-alakú jeleket jelenti. **Soha nem szerkeszt, és soha nem dönt.**

### B. Strukturált észlelés

Olvasd el a [`references/patterns.md`](references/patterns.md)-t, aztán menj végig az Észlelési ellenőrzőlistán, **kategóriánként egyszerre**. Valódi találatnál jegyezz fel `§N — „idézet"`-et, tiszta kategóriánál `nincs`-et. **Ne gyártsd a találatokat**, hogy legyen mit beírni.

### C. Ítélet szerkesztés előtt

Gyűjtsd össze a scanner és az ellenőrzőlista jelöltjeit. Mindegyiknél jegyezz fel:

```text
§N „idézet" -> MARAD vagy ÁTÍR (indok)
```

**Írd át**, ha a jel reflex: nem ad jelentést, ismétlődik a szövegben vagy a testvér-készletben, általános hype-ot használ, elrejti a cselekvőt, hamis mélységet ad, vagy sérti a kért hangot.

**Hagyd meg**, ha megérdemelt emberi döntés: valódi idézet, egyetlen szembeállítás, ami viszi a gondolatot, konkrét részlet, természetes közbevetés, vagy olyan hang-döntés, amit a szerző meg tud védeni.

### D. Átírás-vázlat

Alkalmazd az ítéleteket. Őrizd meg a lefedettséget és a szerkezetet, kivéve ha maga a szerkezet a jel; minden szerkezeti változást magyarázz meg. A hivatkozásokat, fejléceket, forrásokat, helyőrzőket, táblázatokat, frontmattert, kódblokkokat és idézett szövegeket hagyd érintetlenül, kivéve ha a felhasználó kifejezetten mást kér.

### E. Ellenőrzés

Futtasd újra a scannert az átíráson és a testvér-készleten. Aztán menj végig újra az ellenőrzőlistán az átíráson.

**Kemény bukások:**

- A záró átírásban mondat-közi gondolatjel van.
- A scanner chatbot-maradványt, emojit, angol idézőjelet, tiltólistás fordulatot, megmaradt sablon-ismétlést vagy fájlok közti ismétlést jelez, amit nem indokoltál meg kimondottan.
- Az átírás új tényt, forrást, állítást, példát, hivatkozást vagy szempontot hozott be.
- Egy scanner- vagy ellenőrzőlista-jelzésnek nincs MARAD/ÁTÍR ítélete.

## Eredménytermékek

Rövid, beillesztett szövegnél soron belül adj vissza, kivéve ha a felhasználó fájlt kér.

Fájl-alapú munkánál írj egy futás-mappát a javított fájl mellé, egy `emberiesites/` almappába (landing oldalnál: `oldalak/<oldal>/emberiesites/`):

- `00-bemenet.md` — az átírás előtti szöveg, hogy összevethető legyen.
- `01-vizsgalat.md` — a scanner kimenetének összefoglalója és az ellenőrzőlista találatai.
- `02-iteletek.md` — MARAD/ÁTÍR döntések indoklással.
- `03-vazlat.md` — az átírás vázlata.
- `04-ellenorzes.md` — a scanner újrafuttatása és az ellenőrzőlista újrajárása.

A záró átírás nem kap külön fájlt: a javított fájlba kerül vissza (landing oldalnál a `szoveg.md`-be), hogy egy szöveg legyen, ne kettő.

## Kimenet

Add vissza:

1. A használt beállítás röviden: cél-felület, hang-forrás, szigorúság, testvér-mód.
2. A MARAD/ÁTÍR ítéletek listája (a C lépés formátumában), soronként egy jelzés.
3. Az ellenőrzés jegyzetei.
4. A záró átírás.
5. A megírt fájlok útvonalai, ha volt ilyen.

Példákért és jelentés-alakokért olvasd el a [`references/examples.md`](references/examples.md)-t.

## Kapcsolódás a landing csomaghoz

- A hang forrása az `agy/ceg/markahang.md`, amit a **landing-ceges-agy** skill épít fel. Ha nincs ilyen fájl, a fenti sorrend 2-4. pontja szerint haladj, és jelezd, hogy márkahang nélkül dolgoztál.
- A landing oldal szövegírója a kész szövegen ezt futtatja, mielőtt átadja. Ilyenkor a szerkezethez (a blokkok sorrendjéhez, a `##` címsorokhoz, a `[KITÖLTENDŐ: …]` helyekhez) ne nyúlj, csak a megfogalmazáshoz. A `**Felvezető:**`, `**Gomb:**`, `**Űrlap:**`, `**Jelölőnégyzet:**` és `**Kép:**` sorok a szövegíró formai jelölései (a jelölés marad; a felvezető szövegét átírhatod, ha fordításszagú): ha a scanner félkövérként jelzi őket, MARAD.
- A **gondolatjel-tilalom** (`—` / `–` mondat közben sehol; számtartományban a nagykötőjel helyes: 60–90 perc) és a magyar idézőjel („így”) a csomag minden szövegére érvényes, nem csak a §14 miatt.
