# Saját ikonok

Egy egységes, az oldalhoz készült ikonkészlet sokat ad egy hosszú landing oldalnak: lazítja a listákat és a lépéseket, és az oldal saját arcát erősíti. Egy általános ikonkönyvtár ikonjai ezt nem tudják, mert bármelyik oldalon ugyanazok.

Két út van. **Ha van képgeneráló eszközöd, az A út a javasolt**, mert gazdagabb, karakteresebb ikonokat ad; ha nincs, a B út.

## Mikor kell ikon, és milyen

Csak ahol segít: lista- és tételjelek, lépések, „mit kapsz” tételek, előnyök, elérhetőség, figyelmeztetés („előbb szólj”), a kinek szól / kinek nem címkéje. Nem minden tétel kap ikont.

- Az ikon a mellette álló szöveg **konkrét** tárgyát mutassa, a szakma világából: egy edzőnél kettlebell, stopper, edzőcipő; egy könyvelőnél bizonylat, naptár, mappa. Ne általános jelet (pipa, csillag, villám), ha van konkrétabb.
- Egy oldalon egy stílus. A stílust a design adja, erre nem kell rákérdezni: vékony, elegáns betűkhöz vonalas; lágy, kerek formákhoz lapos, lekerekített; személyes, meleg hangulathoz kézzel rajzolt; határozott, tömör designhoz kitöltött.
- Az ikon díszítés: `aria-hidden="true"` (képnél `alt=""`), a jelentése mindig a mellette álló szövegben van. Emoji ikon helyett nem lehet.

## A út: generált ikonkészlet (párhuzamosan az építéssel)

### 1. A lista és a prompt (a tervben)

Írd fel a tervbe az ikonokat (legfeljebb 8 egy lapon; ha több kell, két lap), mindegyiket egy rövid angol tárgyleírással (a képmodell angolul pontosabb), és válassz stílust. Stílus-előtagok kiindulásnak (a színek helyére a paletta hexkódjai):

| Stílus | Előtag |
|---|---|
| Lapos | Modern flat vector icon set, friendly rounded geometric shapes, bold simple solid shapes, no gradients, no outlines, no 3D. Limited palette only: {fő szín}, {világos szín}, {sötét szín}. |
| Vonalas + színfolt | Minimal monoline line-art icon set: uniform medium-weight {sötét szín} strokes with rounded caps, plus a flat {fő szín} colour blob slightly offset behind each drawing. Clean, editorial. |
| Kézzel rajzolt | Hand-drawn doodle icon set drawn with a thick felt-tip marker in {sötét szín}: loose, slightly wobbly lines, simple flat colour fills in {fő szín} and {világos szín} that slightly miss the outlines. |
| Kitöltött, határozott | Bold solid glyph icon set in {fő szín} with small {sötét szín} details, chunky shapes, consistent corner radius, no outlines, no gradients. |

A prompt többi része mindig ez (a listát és a kulcsszínt cseréld):

> Eight separate icons arranged in a clean 4 by 2 grid with generous equal spacing (each icon well inside its own cell, never touching another), each icon a single object, same size and same visual weight, all in exactly the same style: 1) …, 2) …, … 8) …. The background must be one perfectly flat, uniform pure chroma-key green #00FF00 everywhere, with no shadows, no gradient, no texture and no green used anywhere inside the icons. Absolutely no text, no letters, no numbers, no labels, no logo, no frame.

- **Kulcsszín:** alapból zöld (`#00FF00`). Ha a márka színei között zöld van, legyen bíbor (`#FF00FF`), és a feldolgozásnál add meg `--kulcs FF00FF`.
- **Sötét háttér:** a sötét vonalú ikon sötét szakaszon eltűnik. Ha ikon kerül sötét szakaszra, ott világos körbe tedd, vagy kérj egy második lapot világos vonallal.
- Árnyalatos, 3D-s stílus nem jó ide: a vektorizálás a lapos, kevés színű ikonokat tudja jól.

### 2. Generálás a háttérben

Mentsd a lapot ide: `oldalak/<ajanlat>/landing/ikonlap-nyers.png` (fekvő, 1536×1024). Ne a `kepek/` alá: az a feltöltési mappába kerül, a nyers lap pedig nem kell oda.

- **Codexben:** a beépített képgenerálással készítsd, és mentsd a fenti helyre.
- **Claude Code-ban és máshol:** ha a gépen van képgeneráló eszköz vagy skill, azzal, **a háttérben** (Claude Code-ban a parancs `run_in_background` módban), hogy közben építhess.
- Ha nincs képgeneráló eszköz, vagy a generálás hibát ad, ne várj: B út.

**Ne várd meg:** amíg a lap készül, építsd az oldalt (4. lépés). Az ikonok helyére már most a végleges hivatkozás kerül:

```html
<img class="lp-ikon" src="kepek/ikonok/kettlebell.svg" width="48" height="48" alt="">
```

### 3. Feldolgozás

Ha a lap elkészült, nézd meg: minden ikon a saját cellájában van, nincs rajta szöveg, a tárgy felismerhető, egy stílus? Ha egy ikon rossz, a teljes lapot generáld újra (egyszer); ha másodszorra is rossz, azt az egy ikont B úton rajzold meg. Aztán:

```bash
python3 [skill-mappa]/scripts/landing.py ikonok oldalak/<ajanlat>/landing/ikonlap-nyers.png \
  --nevek kettlebell,kerdoiv,stopper,... --ki oldalak/<ajanlat>/landing/kepek/ikonok --marka "#3D3C39,#98556E,#FFD9E8"
```

- A `--nevek` sorrendje a rácsé: balról jobbra, fentről le. A `--marka` a paletta színei: az ikonok színei ezekre igazodnak (ha elhagyod, a lapból olvassa ki őket, ilyenkor a `--szinek` a színek száma, a háttér nélkül).
- Ikononként átlátszó PNG-t ad, és ha telepítve van a `vtracer` (`python3 -m pip install vtracer`), színes SVG-t is. Ha SVG nem készült, az oldalon a `.png` fájlokra hivatkozz.

## B út: saját rajzolt SVG-ikonok

Az ikonokat te rajzolod, beágyazott SVG-ként. Előbb döntsd el és írd a tervbe a készlet szabályait, és utána minden ikont ezek szerint rajzolj:

- **Rács:** `viewBox="0 0 24 24"`, körben kb. 2 egység szabad hely.
- **Vonal:** egyetlen vonalvastagság az egész készletben, a betűkhöz illesztve (vékony betűhöz 1,25–1,5; határozotthoz 2–2,5), azonos `stroke-linecap` és `stroke-linejoin`.
- **Kitöltés:** vonalas, kitöltött vagy kétszínű (vonal és halvány kitöltés); egy oldalon egy fajta.
- **Szín:** `currentColor`, és ha kétszínű, a második réteg a paletta egy színe (`var(--lp-ikon-masodik)`), CSS-ből színezve.
- **Forma:** a design formanyelvéből; ha van grafikai motívum, az ikonokban is visszatérhet. Egyszerű legyen: legfeljebb 3–5 forma, 24 px-en is felismerhető.

```html
<svg class="lp-ikon" viewBox="0 0 24 24" width="28" height="28" aria-hidden="true" focusable="false"
     fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- path, circle, rect elemek -->
</svg>
```

Ha egy tárgyat sehogy nem sikerül felismerhetőre rajzolni, a skill tartalék ikonkészletéből (`landing.py ikon --lista`) vehetsz alapot, a készlet szabályaihoz igazítva.

## Ellenőrzés (mindkét útnál)

Az egész oldalas képernyőképen az ikonok kicsik, ezért külön is nézd meg őket:

```bash
python3 [skill-mappa]/scripts/landing.py ikonlap oldalak/<ajanlat>/landing/index.html -o oldalak/<ajanlat>/landing/kepernyokepek/ikonlap.html
python3 [skill-mappa]/scripts/landing.py kepernyokep oldalak/<ajanlat>/landing/kepernyokepek/ikonlap.html --ki oldalak/<ajanlat>/landing/kepernyokepek
```

Az ikonlap az oldal összes ikonját (`class="lp-ikon"`, beágyazott SVG vagy kép) egymás mellé teszi 24, 48 és 96 px-en. Nézd meg: egy készletnek látszanak? Mindegyik felismerhető kicsiben is? Van, ami kilóg a sorból, levágódik, vagy zöld szegélye maradt? Ami nem jó, azt javítsd.
