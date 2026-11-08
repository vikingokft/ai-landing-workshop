---
name: landing-epito
description: "Megépíti a landing oldalt HTML-ben a kész weboldalszövegből. A kinézetet a felhasználó meglévő weboldalából (ha azt kéri, hogy kövesse) vagy egy design-inspirációból (tetsző oldal vagy képernyőkép) veszi, a márka elemeit (logó, színek, betűk) a meglévő arculatból; ha egyik sincs, szabadon tervez. Saját, a designhoz illő ikonkészletet készít: ha van képgeneráló eszköz, generálja (az építéssel párhuzamosan) és SVG-vé alakítja, ha nincs, maga rajzolja. Egy változatot épít, képernyőképpel ellenőrzi, és elkészíti a feltölthető mappát (index.html, koszi.html, kepek/) meg a WordPressbe (Gutenberg, Elementor) illeszthető változatot a Médiatárba töltendő képekkel. A szöveget szó szerint használja. Használd, ha ezt írják: 'építsük meg az oldalt', 'landing oldal HTML', 'készítsd el a landing oldalt', 'landing-építő', 'weboldal a szövegből', vagy a szöveg elkészülte után."
---

# Landing-építő

Ez a skill a kész weboldalszövegből megépít **egy** landing oldalt: egy önálló HTML-fájlt, ami feltölthető egy tárhelyre, és beilleszthető WordPressbe.

A kinézet forrása, ebben a sorrendben:

1. **a meglévő weboldal**, ha a felhasználónak van, és azt kéri, hogy az új oldal kövesse;
2. **egy design-inspiráció**: egy oldal vagy képernyőkép, ami a felhasználónak tetszik;
3. ha egyik sincs, **te tervezel**, a téma, a célcsoport és a felhasználó iránya alapján.

A márka meglévő elemei (logó, színek, betűk) mindhárom esetben kötöttek. A hosszú szöveg elrendezéséhez a `references/hosszu-szoveg.md` ad ötleteket, az oldal ikonjai pedig saját készletből jönnek: generálva, ha van képgeneráló eszközöd, különben te rajzolod őket (`references/ikonok.md`).

**Fájlútvonalak:** a `[skill-mappa]` ennek a `SKILL.md`-nek a mappája. A segédprogram: `[skill-mappa]/scripts/landing.py`. A referenciák a `[skill-mappa]/references/` alatt vannak; mindegyiket akkor olvasd el, amikor a lépés hivatkozik rá.

**Kérdezés:** ha van kérdező eszközöd (Claude-ban `AskUserQuestion`), azzal kérdezz. Ha nincs (például Codexben), sima szövegben: egy üzenetben egy kérdéscsomag, számozott válaszokkal, a javasolt megjelölve, és várd meg a választ. Úgy szólítsd meg a felhasználót, ahogy ő ír neked; ha nem derül ki, magázz.

## A kimenet

```
oldalak/<ajanlat>/landing/
├── terv.md                  ← a rövid terv
├── ikonlap-nyers.png        ← a generált ikonlap (ha az A úton készültek az ikonok); nem kerül fel
├── index.html + kepek/      ← az oldal (az ikonok a kepek/ikonok/ alatt)
├── kepernyokepek/           ← az ellenőrzés képei (az ikonlap is)
├── feltoltes/               ← a kész oldal, ezt kell feltölteni (index.html, koszi.html, kepek/)
├── wp-beillesztes.html      ← ugyanez WordPress Egyéni HTML blokkba vagy Elementor HTML-widgetbe
└── wp-kepek/                ← a WordPress Médiatárba töltendő képek
```

## Három szabály

1. **A szöveg szó szerint, de nem egyforma súllyal.** A szöveget nem írod át, nem rövidíted és nem egészíted ki, a sorrendje is marad. A *súlyát* viszont te döntöd el: a kulcsmondat nagyobb, a kiegészítő rész kisebb, keskenyebb oszlopba vagy lenyíló elembe (`<details>`) kerül; egy valódi szám vagy erős mondat nagyban, kiemelve is megjelenhet. Mondatot nem vágsz ketté: címmé csak az válhat, ami a szövegben is cím vagy félkövér címke. Számot, véleményt, logót, díjat nem találsz ki.
2. **A meglévő márkaelem kötött, a többi a kinézet forrásáé.** Amit a felhasználó márkaként megad (logó, színek, betűk), az változatlan. Ami nincs megadva, azt a meglévő oldal, az inspiráció, vagy ha egyik sincs, a te döntésed adja.
3. **Nézd meg, amit építettél.** Képernyőképen ellenőrzöd (az ikonokat külön is), és javítod, mielőtt megmutatod.

## A munkamenet

### 1. Beolvasás

1. **Szöveg:** keresd meg az `oldalak/<ajanlat>/szoveg.md`-t. Ha több ajánlat van, kérdezd meg, melyik.
2. **Arculat:** nézd meg, mi van meg:
   - **kész arculat:** design-rendszer (`agy/ceg/design-rendszer/tokens.css`) vagy részletes arculati leírás;
   - **néhány elem:** logó, egy-két szín vagy betű, összeszedve az `agy/ceg/arculat.md`-ben vagy a `forrasok/` alatt (például `forrasok/arculati-alapok/`);
   - **semmi:** a logó szöveges logó lesz (a vállalkozás neve a címsorbetűvel).

   Design-rendszer nem kell: ha nincs, ne indítsd el a design-rendszer skillt, és ne készíts `tokens.css`-t, akkor sem, ha egy régebbi agy-fájl azt írja, hogy a landing építésekor jön létre.
3. **Kontextus:** az ajánlat mappája (`agy/ajanlatok/<ajanlat>/`), a `agy/ceg/markahang.md` és a `agy/ceg/uzleti-profil.md`, ha vannak. Ezekből tudod, milyen világból jön az oldal. Ha az üzleti profilban van a vállalkozás weboldalának címe, jegyezd meg.
4. **Képek:** nézd meg, van-e fotó (`forrasok/`, `forrasok/kepek/`, `agy/`). Portré, munka közben, helyszín, termék.
5. **Inspiráció:** ha a felhasználó adott oldalt (URL) vagy képernyőképet, vagy van `oldalak/<ajanlat>/inspiracio/` mappa, gyűjtsd össze.

### 2. Kérdések

Egy üzenetben, csak arra, ami nem derült ki:

1. **A szöveg:**
   > **Van már kész weboldalszöveged?**
   > 1. Igen, ez az: `<a megtalált szoveg.md>` ← ha találtál
   > 2. Igen, máshol van (bemásolom, vagy megadom a fájlt)
   > 3. Még nincs

   Ha máshol van, mentsd el az `oldalak/<ajanlat>/szoveg.md`-be **szó szerint**: csak a szerkezetet jelöld (a szakaszok `## 1. ...` címkéi, a címek `###`, a gombok `**Gomb:**`, az űrlap `**Űrlap:**`, a `references/technikai.md` szerint), a szövegen ne változtass. Ha még nincs szöveg, állj meg: az oldal a kész szövegből épül. Ajánld fel a landing-szövegíró skillt.
2. **Meglévő weboldal:**
   > **Van már weboldalad? Ha igen, add meg a címét.**

   Ha a címe megvan az 1. lépésből, kérdezd meg, hogy ez-e.
3. **Design-inspiráció:**
   > **Van olyan oldal vagy képernyőkép, aminek tetszik a kinézete, és ilyet szeretnél? Ha igen, add meg a címét, vagy tedd a képet az `oldalak/<ajanlat>/inspiracio/` mappába.**
4. **Ha nincs inspiráció, és nincs kész arculat sem:** „Van valami, amit a hangulatról vagy a színekről mondanál? Elég egy irány, például »kék bézzsel« vagy »nyugodt, természetes«.” Hex-kódot ne kérj, ha nincs márkaszín.
5. **Fotók** (ha nem találtál): „Vannak fotóid az oldalhoz (rólad, munka közben, a helyszínről)? Ha igen, tedd őket a `forrasok/kepek/` mappába. Ha nincs, a helyük megtervezett helyőrzőt kap, vagy az a blokk kép nélkül épül.”

**Ha van meglévő weboldal, erre külön kérdezz rá**, a válasz után, egy kérdésben:

> **Az új oldal kövesse a meglévő weboldalad designját, vagy térjen el tőle?**
> 1. Kövesse: úgy nézzen ki, mint a weboldalam része
> 2. Térjen el, de a logót, a színeket és a betűket vegye át
> 3. Térjen el teljesen (a logó marad)

Ha követi, a meglévő oldal a kinézet forrása, és inspiráció nem kell (ha mégis adott, csak apró részletekhez használd). Ha eltér, az inspiráció vagy a te tervezésed adja a kinézetet; a 2. válasznál a meglévő oldal színei és betűi kötött márkaelemek. A meglévő oldal megnézése ugyanúgy megy, mint az inspirációé (`references/inspiracio.md`).

### 3. A terv

Olvasd el a `references/inspiracio.md`-t (mit honnan veszel) és a `references/hosszu-szoveg.md`-t (ötletek a hosszú szöveghez). Írj egy rövid `terv.md`-t, legfeljebb egy oldalt:

1. **Olvasat:** egy mondat: milyen oldal, kinek, milyen hangulattal, és mi a látogató egy dolga.
2. **A kinézet forrása:** a meglévő oldal, az inspiráció, vagy a saját irányod, és belőle egy-egy sorban a megtartott tulajdonságok (mért vagy megfigyelt tényekkel, nem jelzőkkel). Saját iránynál: az ötlet egy mondatban, a téma világából (a szakma tárgyai, helyei, anyagai), és a visszatérő grafikai motívum.
3. **Színek és betűk:** a végleges paletta és a betűpár, és melyik honnan jön.
4. **Ikonok:** a `references/ikonok.md` szerint: melyik út (A: generált, ha van képgeneráló eszközöd; B: rajzolt SVG), a stílus, a lista (tárgy, angol leírás, hol lesz), A úton a prompt, B úton a készlet szabályai.
5. **Szakaszok:** a `szoveg.md` blokkjai sorban, mindegyikhez az elrendezés, a háttér, és mi benne a kiemelt elem. Ugyanaz az elrendezés kétszer egymás után ne jöjjön, és legalább egy-két szakasz legyen színes vagy sötét hátterű, hacsak a követett design nem ilyen.

Ne állj meg jóváhagyásra: építs. A felhasználó a kész oldalt látja, és arra mond visszajelzést.

**A úton most indítsd el az ikonlap generálását a háttérben** (`references/ikonok.md`, 2. pont), és ne várd meg: a 4. lépés közben elkészül.

### 4. Építés

Olvasd el a `references/technikai.md`-t, és kövesd pontosan: önálló fájl, minden CSS a `.lp` burkolóra szűkítve, a színek és a betűk változókban a `.lp`-n, saját űrlap, ami a köszönőoldalra visz, mobil először.

Az ikonok helyére A úton már a végleges hivatkozás kerül (`<img class="lp-ikon" src="kepek/ikonok/<nev>.svg" ...>`); B úton rajzold meg őket beágyazott SVG-ként. Ha az A úton a lap elkészült, dolgozd fel (`landing.py ikonok`, `references/ikonok.md`, 3. pont); ha még nem, folytasd az ellenőrzést, és a feldolgozást utána végezd el. Ha a generálás nem sikerült, válts B útra.

### 5. Ellenőrzés és javítás

1. **Gépi ellenőrzés:**
   ```bash
   python3 [skill-mappa]/scripts/landing.py ellenoriz oldalak/<ajanlat>/landing/index.html --szoveg oldalak/<ajanlat>/szoveg.md
   ```
   Ha van design-rendszer, add hozzá: `--tokens agy/ceg/design-rendszer/tokens.css`. Ami ✗, azt javítsd. A ! jelűeket nézd meg, és döntsd el, kell-e javítani.
2. **Képernyőkép:**
   ```bash
   python3 [skill-mappa]/scripts/landing.py kepernyokep oldalak/<ajanlat>/landing/index.html --ki oldalak/<ajanlat>/landing/kepernyokepek
   ```
   Asztali (1440 px) és mobil (390 px) kép a hero-ról és az egész oldalról, az egész oldal szakasznyi szeletekben (`…-teljes-01.png` …). Ha a parancs nem talál böngészőt, nyisd meg az oldalt a saját böngésző-eszközöddel, ha van; ha nincs, kérd meg a felhasználót, hogy nézze meg ő.
3. **Ikonlap:** az ikonokat külön is nézd meg (`references/ikonok.md`, „Ellenőrzés”).
4. **Nézd meg a képeket** a `references/minoseg.md` öt kérdésével. Ha a meglévő oldalt vagy egy inspirációt követsz, vesd össze vele: ha az új oldal laposabb, egyformább vagy üresebb, javítsd. Egy javítókör, aztán új képernyőkép.

### 6. Bemutatás

Nyisd meg az oldalt a böngészőben (ha nem tudod, mondd meg, hol van). Írd le két-három mondatban, honnan jön a kinézet (meglévő oldal, inspiráció, saját irány), mi a kiemelt elem, és milyenek az ikonok. Aztán kérdezd meg: **„Mit változtassunk rajta?”** A kért változtatásokat végezd el, és ellenőrizd újra (5. lépés). Ha a felhasználó elégedett, jöhet a véglegesítés.

### 7. Véglegesítés

1. **Feltöltési mappa:** másold az `index.html`-t és a `kepek/` mappát a `feltoltes/` mappába.
2. **Köszönőoldal:** készíts `feltoltes/koszi.html`-t ugyanabban a stílusban (`references/technikai.md`). A szövege a `szoveg.md` köszönőoldal-blokkjából jön, ha van; ha nincs, írj két-három mondatot a márkahang szerint, és az átadásban mondd el, hogy ezt te írtad. Ellenőrizd (`ellenoriz --koszi`). Hogy az űrlap a köszönőoldalra visz, azt a főoldal gépi ellenőrzése már megnézte: böngészős űrlaptesztet, helyi szervert nem kell indítanod.
3. **WordPress-változat:**
   ```bash
   python3 [skill-mappa]/scripts/landing.py wp oldalak/<ajanlat>/landing/feltoltes/index.html -o oldalak/<ajanlat>/landing/wp-beillesztes.html
   ```
   A képeket a `wp-kepek/` mappába másolja egyedi, ékezet nélküli névvel (az ajánlat nevével kezdődik, így a Médiatárban nem ütközik más képpel, és a WordPress nem nevezi át), a logót és a többi SVG-t beágyazza (a WordPress alapból nem enged SVG-t feltölteni). Ha a felhasználó már feltöltötte a képeket, és megadja az egyik címét a Médiatárból, futtasd újra `--mediatar <a kép címe>`-vel: ebből számolja ki az összes kép címét. Ha csak az oldal címét tudja (`--mediatar https://pelda.hu`), a mai hónap mappáját feltételezi. Ha a köszönőoldal a WordPressben más címen lesz, add meg `--koszi-url`-lel.

### 8. Átadás

Mondd el röviden:

- **mi készült, hol:** az oldal, a `feltoltes/`, a `wp-beillesztes.html` és a `wp-kepek/`;
- **tárhely (FTP):** a `feltoltes/` mappa *tartalmát* kell a tárhely célmappájába tölteni, nem magát a mappát; a mérőkódok (Meta Pixel, Google Tag) ilyenkor a kódba kerülnek, a `<head>`-ben jelölt helyre;
- **WordPress:** amíg nincs megadva a Médiatár egy képcíme, a `wp-beillesztes.html`-ben a képek nem jelennek meg; ezt mondd ki. A lépések: (1) új oldal fejléc és lábléc nélküli sablonnal; (2) a `wp-kepek/` képeit egyszerre húzd be a Médiatárba; (3) másold ki az egyik feltöltött kép címét, és add meg (ezzel futtatod újra a `wp` parancsot, ha a címet még nem tudtad); (4) a `wp-beillesztes.html` teljes tartalmát másold egy Gutenberg Egyéni HTML blokkba vagy Elementor HTML-widgetbe. A mérőkódokat és a sütikezelést ilyenkor a WordPress adja;
- **az űrlap még nem küld e-mailt:** beküldéskor csak a köszönőoldalra visz. Ahhoz, hogy az adatok meg is érkezzenek, egy űrlapkezelő, a levelezőrendszer beágyazó kódja vagy SMTP-beállítás kell; ezt a kódban egy megjegyzés jelöli;
- **ami a felhasználóra vár:** a `[KITÖLTENDŐ]` helyek listája, a cserélendő képhelyek, és amit te írtál (például a köszönőoldal szövege).
