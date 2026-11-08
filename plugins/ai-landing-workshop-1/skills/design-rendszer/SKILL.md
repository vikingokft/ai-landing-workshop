---
name: design-rendszer
description: "Rendszerbe foglalja a vállalkozás vizuális alapjait a céges agyból: színek szerepekkel, Google-betűpár ő és ű betűvel, betűméret-skála, sormagasság, árnyékok, gomb- és űrlapstílus. Bemenet a logó, a fő szín, a betű és opcionálisan egy-három tetsző oldal vagy kép (URL vagy képernyőkép); ami hiányzik, arra javasolt opciókkal kérdez, a többit számolt skálákkal állítja össze; két jelöltet mutat egy stílusmintán, és a választottat az agy/ceg/design-rendszer/ mappába menti. Ebből dolgozik minden, ami később készül: landing oldal, weboldal, prezentáció, közösségimédia-kép. Logót nem tervez (ha nincs, egyszerű szöveges logót készít a névből), de a logóból színes, sötét és fehér változatot készít. Nem épít oldalt. Nem kötelező lépés: a landing-építő design-rendszer nélkül is dolgozik. Használd, ha a felhasználó kifejezetten design-rendszert kér, vagy ha ezt írják: 'design-rendszer', 'készítsük el a design-rendszert', 'arculat', 'nincs arculatom', 'milyen színeket használjak', 'betűtípus', 'stílusminta'."
---

# Design-rendszer

A design-rendszer az, ahogyan a vállalkozásod kinéz: a színek és hogy melyik mire való, a betűk, a méretek, a térközök, a gombok és az űrlapok formája. Egyszer készül el, és minden, amit később építesz (landing oldal, weboldal, prezentáció, kép), ebből dolgozik, így mind ugyanúgy néz ki.

Ez a skill **rendszerbe foglal**: összegyűjti a felhasználó vizuális alapjait (logó, fő szín, betű, és ha hoz, egy-három oldal vagy kép, aminek tetszik a kinézete), és ezekből a céges agyba (`agy/`) elkészíti a design-rendszert. Az ízlés a felhasználóé, a rendszerezés a skillé: ahol nincs bemenet, ott javasol, de a javaslatot mindig jelöli. Két jelöltet mutat, és a választottat elmenti. **Logót nem tervez:** ha van logó, beépíti, és elkészíti a színes, a sötét és a fehér változatát; ha nincs, a névből a címsorbetűvel egyszerű szöveges logót készít. **nem épít oldalt vagy anyagot**, és nem dönt az elrendezésről: azt az dönti el, ami a design-rendszert használja (például a **landing-építő**, a szövegből és a referencia-oldalakból, amiket a felhasználó hoz).

**Fájlútvonalak:** a `[skill-mappa]` ennek a `SKILL.md`-nek a mappája. A segédprogram: `[skill-mappa]/scripts/design.py`, a sablon: `[skill-mappa]/references/tokens-sablon.css`.

**Kérdezés:** ha van kérdező eszközöd (Claude-ban `AskUserQuestion`), azzal kérdezz. Ha nincs (például Codexben), sima szövegben: egy üzenetben egy kérdéscsomag, számozott válaszokkal, a javasolt megjelölve, és várd meg a választ. Úgy szólítsd meg a felhasználót, ahogy ő ír neked; ha nem derül ki, magázz.

## A kimenet

```
agy/ceg/design-rendszer/
├── design-rendszer.md     ← emberi nyelven: mi mire való, és mit ne
├── tokens.css             ← ugyanez CSS-változókban; az építő skillek ebből dolgoznak
├── stilus-minta.html      ← arculati tábla (színek, logó, betűk, árnyékok, gombok, űrlap) és webdesign minta
├── logo/                  ← logo.svg (színes), logo-sotet.svg (világos háttérre), logo-feher.svg (sötét háttérre), favicon
└── jeloltek/              ← a jelöltek; a választás után is megmarad
    ├── 1-<irany>/tokens.css, logo/
    └── 2-<irany>/tokens.css, logo/
```

## Három szabály, amit mindig betartasz

1. **Kötött és szabad.** **Kötött** a logó, a kérdéskörben választott fő szín (alapból a logó színe) és minden, amit a felhasználó kifejezetten kér: ezeket nem cseréled „szebbre”. Egy meglévő szín világosabb vagy sötétebb árnyalata (háttérnek, keretnek, gombnak) még az ő színe; mondd el, melyik árnyalat honnan jön. Ha a fő szín nem éri el a kontrasztot, ne dobd el: tedd olyan szerepbe, ahol megfelel (például maradhat kiemelésnek, a gomb lehet a sötétebb árnyalata), és mondd el, miért. **Szabad** minden más: a betűk, a hangulat, a kiegészítő színek, a formák. Amit a régi anyagokból (árlista, szórólap, régi weboldal) olvasol ki, az **javaslat**, nem kötelező: egy régi nyomtatvány betűje és színei gyakran elavultak, és ha hűen átveszed, az új oldal is elavult lesz.
2. **Számolj, ne találj ki.** A semleges színeket (háttér, szegély, szövegek), a betűméreteket, a sormagasságot, az árnyékot, a mező- és a hibaszínt a `design.py skala` számolja a fő színből. Te a karakteren döntesz: betűpár, súly, nagybetűsítés, kerekítés, gombforma, a skála aránya. Ha egy számolt értéket átírsz, mondd el, miért.
3. **Mérj, ne becsülj.** A betűtípust és a kontrasztot a `design.py` ellenőrzi, nem a szemed vagy az emlékezeted. Amíg egy jelölt ellenőrzése nem zöld, nem mutatod meg.

## A munkamenet

### 1. Beolvasás

1. Keresd meg az `agy/ceg/` mappát (a céges agyat). Ha nincs, nem baj: nézd meg, milyen anyagai vannak a munkamappában (logó, weboldal címe, árlista, prezentáció), a hiányzót a 2. lépés kérdéseivel pótold, és a design-rendszert a munkamappa `design-rendszer/` mappájába írd. Ahol a lenti lépések az `agy/ceg/`-et említik, ott ezt a mappát érted. Ha van céges agy skill (például a landing-ceges-agy), egy mondatban ajánld, hogy azzal később teljesebb lesz.
2. Ha már van `agy/ceg/design-rendszer/tokens.css`, kérdezd meg: frissítjük (csak amit kér), vagy újat készítünk? Új esetén a régit nevezd át `design-rendszer-elozo-ÉÉÉÉ-HH-NN/`-ra.
3. Olvasd be: `arculat.md` (színek, betűk, logó, fotók, hangulat), `markahang.md` (a stílus és a hang), `uzleti-profil.md` (mivel foglalkozik, kinek, és a weboldala címe).
4. **Nézd meg a meglévő anyagokat** a `forrasok/` mappában: logófájl, árlista, prezentáció, szórólap, közösségimédia-képek. Keresd meg a logót (SVG vagy PNG), és olvasd ki, milyen színeket és milyen jellegű betűket használ már (talpas, talp nélküli, kézírásos). A logó kötött, a színek és a betűk a 2. lépés kérdéseinek opcióiba kerülnek, a többi csak kiindulópont (1. szabály). Ha a képeket meg tudod nézni, nézd meg őket. A pontos betűtípust egy képről általában nem lehet megállapítani: ilyenkor válassz hozzá hasonló Google Fontot, jelöld következtetésnek, és a kérdéskörben kérdezd meg, tudja-e a betű nevét. Ha van weboldala, és meg tudod nyitni, nézd meg a színeit és a betűit is.
5. **Vizuális referencia** (opcionális): ha a felhasználó adott egy-három oldalt (URL) vagy képet, aminek tetszik a kinézete, vagy van ilyen a `forrasok/` mappában (például `forrasok/referenciak/`), nézd meg. Ha URL, és meg tudod nyitni, olvasd ki a CSS-ből a betűtípusokat (`font-family`), a fő színeket, a kerekítést és az árnyékokat; ha kép, nézd meg. Ebből a **vizuális nyelvet** veszed át: a betűk karakterét (vagy magát a betűt, ha Google Font és tudja az ő, ű betűt), a színhangulatot (telített vagy visszafogott, meleg vagy hideg, mennyi a fehér), a formákat (kerekítés, gombforma, keret), az árnyékot és a levegősséget (ehhez igazítsd a `skala` arányát). Az elrendezést nem: az az építő skillé. A referencia márkáját ne másold: a logója és a saját márkaszíne nem lesz a felhasználóé, a fő szín a 2. lépésben dől el. Ha a referencia és a felhasználó egy kifejezett kérése ütközik, a kérése nyer.
6. Írd le magadnak egy bekezdésben: mi kötött (logó, fő szín, amit kifejezetten kért), mit veszel át a referenciából, mi következtetés (anyagból olvastad ki), és mi hiányzik.

### 2. Egy kérdéskör

Egy üzenetben, legfeljebb négy kérdés. A **betűre** és a **fő színre** mindig kérdezz rá (kivéve, ha a felhasználó már kifejezetten megmondta), a többire csak akkor, ha nem derült ki. Minden kérdésnél legyen javasolt válasz, hogy a felhasználó egy számmal felelhessen. Az opciókba írd bele, amit az anyagokból kiolvastál (a logó színének hex kódját, a régi anyag színeit), hogy lássa, miből választ.

1. **Hangulat és referencia** (ha az `arculat.md`-ben nincs hangulat, és nem adott referenciát): „Milyen hatást keltsen az oldal, két-három szóban (például: nyugodt, meleg, szakmai)? Ha van egy-három oldal vagy kép, aminek tetszik a kinézete, küldd el a linkjét vagy a képernyőképét is: abból veszem át a stílust.” A referencia nem kötelező; ha nem küld, a szavaiból dolgozol.
2. **Címsorbetű:**
   > **Milyen betű legyen a címeken?**
   > 1. A logóhoz illő ← *javasolt* (rokon vagy tudatosan ellentétes betű, lásd lent)
   > 2. Az ajánlathoz illő: a márkahangból és a célcsoportból választok
   > 3. A referenciához illő: a küldött oldal vagy kép betűjéből (csak ha küldött referenciát)
   > 4. Valami egészen más: írd le, milyet (például klasszikus talpas, modern talp nélküli, karakteres, kézírásos)
   > 5. Van konkrét betűm: megadom a nevét

   Ha nincs logó, az 1. opció kimarad, és a javasolt a 3. (ha van referencia), különben a 2. Ha a felhasználó már megadta a betűt, ne kérdezd: erősítsd meg egy mondatban.
3. **Fő szín:**
   > **Mi legyen a fő szín?**
   > 1. A logó színe (#…) ← *javasolt*
   > 2. A meglévő anyagaid színe (#…, például az árlistáról)
   > 3. Új szín: írd le, milyet, vagy add meg a kódját
   >
   > Ha van szín, amit biztosan nem akarsz, azt is írd meg.

   Ha a felhasználó már megadta a fő színt, ne kérdezd: erősítsd meg egy mondatban. Ha nincs logó, az 1. opció kimarad; ha anyagból sem olvastál ki színt, kérdezd egyszerűen: „Van színed, amit szeretsz, vagy amit biztosan nem akarsz?”
4. **Világos vagy sötét** (csak ha a hangulatból nem következik): „Világos alapú legyen az oldal, vagy sötét?” Javasolt: világos.

A válaszok kötöttek: a választott fő szín és a megadott betű nem változik a jelöltek között. Ha a felhasználó a javasoltat választja, vagy rád bízza, a két jelölt a betűben eltérhet (például az egyik rokon, a másik ellentétes a logóval).

### 3. Két jelölt

Készíts **két** jelöltet (ha a felhasználó többet kér, legfeljebb hármat). Mindkettő megtartja a kötött elemeket, de a két jelölt legyen tényleg más, ne ugyanaz két árnyalatban. Jó felosztás: az **1. jelölt közelebb marad** a bemenetekhez (a referenciához, ha van, különben a meglévő anyagok hangulatához, korszerű méretekkel és formákkal), a **2. bátrabb**: más betűkarakter, más skálaarány, más gombforma. Ha a felhasználó a betűt és a színt is megadta, a jelöltek a formákban, az arányban és a módban térnek el. A `LEIRAS` sorba írd meg, miből jön (például: „a logó bordó színéből és a referenciaoldal kapszulagombjaiból”).

Jelöltenként:

1. **Mappa:** `agy/ceg/design-rendszer/jeloltek/<szám>-<irany>/` (az irány rövid, ékezet nélküli, kötőjeles, például `1-meleg-magazin`).
2. **Betűk:** egy címsorbetű és egy szövegbetű, mindkettő a Google Fontsból. Ellenőrizd:
   ```bash
   python3 [skill-mappa]/scripts/design.py fontok "Cím Font" "Szöveg Font"
   ```
   Ha valamelyik ✗, válassz másikat. Ha nincs internet (?), a felhasználó nézze meg a fonts.google.com oldalon a „Language: Hungarian” szűrővel, vagy válassz olyat, amiről biztosan tudod, hogy jó.
3. **Számolt alap:** futtasd a skálát a fő színből:
   ```bash
   python3 [skill-mappa]/scripts/design.py skala --szin "#A8435B" --mod vilagos --arany 1.333 --cim-betu talpatlan
   ```
   Az `--arany` a címek és a szöveg közti különbség: `1.25` visszafogott, `1.333` kiegyensúlyozott (javasolt), `1.414` merész. A `--cim-betu` a címsorbetű (`talpas` vagy `talpatlan`), ettől függ a sorköz és a betűköz. Sötét alapú oldalhoz `--mod sotet`. A két jelöltnél eltérhet az arány és a mód.
4. **tokens.css:** a `references/tokens-sablon.css` másolata, kitöltve. A ⚙ jelű sorokba a `skala` kimenete kerül. A változók nevét ne változtasd meg. A színek hex kódok, vagy hivatkozások egy másik változóra (`var(--ds-elsodleges)`): a gomb, a sáv és a mező színei maradjanak hivatkozások, ha csak lehet, így a paletta változását követik. A fejlécben az `IRANY`, a `LEIRAS`, a `NEV` (a vállalkozás neve, ahogy az `uzleti-profil.md`-ben áll; logó híján ez áll a minta fejlécében) és a `GOOGLE-FONTS` sor is legyen kitöltve. A `MOD` sor `vilagos` vagy `sotet` (világos vagy sötét alapú oldal). A GOOGLE-FONTS egy működő `css2` link: a címsorbetűnél a `--ds-cim-suly` értékével, a szövegbetűnél 400, 500 és 700 súllyal (a gomb felirata 700).
   - **A paletta nyolc szín** (elsődleges, másodlagos, sötét, szöveg, világos szöveg, szegély, világos, fehér). Az **elsődleges** a márka kiemelt színe: alcím, ikon, akcentus. Ha nincs külön második akcentus, a másodlagos legyen ugyanaz.
   - **A betűk karaktere:** a címnél a betűpár, a súly és a nagybetűsítés (`--ds-cim-nagybetu: uppercase`) adja a stílus nagy részét; ezeket tudatosan válaszd. Kerüld a megszokott „alapértelmezett” párosokat (Open Sans, Roboto, Lato, Montserrat, Poppins, vagy egy klasszikus Baskerville-szerű talpas), hacsak nem kötött: válassz karakteresebbet a Google Fontsból.
   - **Logóhoz illő betű:** ha a kérdéskörben a logóhoz illőt választotta (vagy rád bízta), a címsorbetűt a logóhoz válaszd; ha mást választott, az ő válasza dönt, és a logóhoz csak finomítasz (például súlyban), mert a fejlécben és a hero-ban egymás mellett állnak. Nézd meg a logót képként (az SVG-t böngészőben vagy PNG-vé alakítva); ha az SVG-ben `<text>` elem van, a `font-family` megmondja a betű nevét. Olvasd ki a felirat karakterét: talpas vagy talpatlan, geometrikus (kerek o, egyenletes vonalvastagság) vagy humanista (tollszerű, változó vastagság), vékony vagy vastag, keskeny vagy széles. Ha a logó betűje ismert és megvan a Google Fontsban, a címsorbetű lehet maga az a betű. Ha nem, két jó út van: **rokon** betű (ugyanaz a kategória, hasonló arány és vonalvastagság), vagy **tudatos ellentét** (például vékony, talpatlan logó mellé karakteres talpas cím). A „majdnem ugyanolyat” kerüld: két majdnem egyforma betű egymás mellett hibának látszik. A két jelölt választhat más utat (például az egyik rokon, a másik ellentétes), és a `LEIRAS` mondja meg, hogyan illeszkedik a betű a logóhoz. A szövegbetű maradhat semleges, jól olvasható.
   - **Árnyékok:** a `skala` rétegzett, puha árnyékot ad (az 1-es a kártyáé, a 2-es a kiemelésé). Nyers, grafikus stílushoz cseréld elmosás nélküli, eltolt árnyékra (`4px 4px 0px 0px <sötét szín>`); ha nem kell árnyék, nulla átlátszóságú.
   - **Gombok:** a felirat alapból csupa nagybetűs (`--ds-gomb-nagybetu: uppercase`, 14 px, kis betűközzel); kisbetűset csak akkor válassz, ha a stílus kifejezetten kéri (például kézírásos, játékos irány), és mondd el, miért. A menüpontok ugyanazt a betűt, méretet és nagybetűsítést kapják, mint a gomb. Az elsődleges gomb legyen a legjobban kiugró elem; a hover színe legyen jól láthatóan más (gyakran a sötét szín). A másodlagos gomb körvonalas. A kerekítés (`0` szögletes, `999px` kapszula), a belső térköz és a keret vastagsága a stílus része.
   - **A sötét záró sáv** (`--ds-sav-...`): a CTA szakasz. A gombjának a sötét sávon is el kell válnia; ha az elsődleges szín ott elvész, adj neki világos változatot (például a világos színt az elsődleges felirattal).
   - **Űrlap:** a mező kerete, a fókusz és a hiba színét a `skala` adja; a fókusz alapból a fő szín.
   - Kerüld az „AI-sablon” színeket: lila-kék színátmenet, neon, minden árnyalat egyforma telítettséggel.
5. **Kontraszt:**
   ```bash
   python3 [skill-mappa]/scripts/design.py kontraszt agy/ceg/design-rendszer/jeloltek/<mappa>
   ```
   Ami ✗, azt javítsd (sötétebb szöveg, más gombszöveg-szín, sötétebb gomb), és futtasd újra, amíg minden ✓.
6. **Logó és változatai** (jelöltenként, mert a sötét szín jelöltenként más lehet):
   - **Van logó, SVG-ben:** készítsd el a három változatot a jelölt `--ds-sotet` színével:
     ```bash
     python3 [skill-mappa]/scripts/design.py logo-valtozatok forrasok/<logó>.svg --ki agy/ceg/design-rendszer/jeloltek/<mappa>/logo --sotet "<--ds-sotet>"
     ```
     Ha a parancs azt írja, hogy egy részlet beolvadhat, nézd meg a stílusmintán, és ha fontos rész tűnt el, mondd el. Ha a felhasználónak már van saját sötét vagy fehér változata, azt használd a generált helyett.
   - **Van logó, de csak PNG:** a parancs csak átmásolja. Mondd el, hogy egyszínű változathoz SVG kell, és kérd el, ha van.
   - **Nincs logó:** készíts szöveges logót a névből (pontosan úgy, ahogy az `uzleti-profil.md`-ben áll), a jelölt címsorbetűjével és súlyával, a sötét színnel, aztán ebből a változatokat:
     ```bash
     python3 [skill-mappa]/scripts/design.py logo --szoveg "Kiss Blanka" --font "<cím font>" --suly <cím súly> --szin "<--ds-sotet>" --ki <mappa>/logo/szoveges.svg
     python3 [skill-mappa]/scripts/design.py logo-valtozatok <mappa>/logo/szoveges.svg --ki <mappa>/logo --sotet "<--ds-sotet>"
     ```
     A színes változat itt a sötét színű. A `logo` parancshoz kell a `fonttools`: ha hibát ír, telepítsd (`pip3 install fonttools`; ha nem tudod futtatni, kérd meg a felhasználót). Ha nem sikerül, hagyd ki: a minta fejlécében a név a betűvel szedve jelenik meg. A szöveges logó ideiglenes, ezt mondd is ki.
   - **Favicon:** ha van, másold `favicon.svg` (és `favicon.ico`) néven. Ha nincs, a kezdőbetűkből készíts: `logo --szoveg "KB" --font "<cím font>" --suly <cím súly> --szin "#FFFFFF" --keret kor --keret-szin "<--ds-elsodleges>" --meret 64 --ki <mappa>/logo/favicon.svg`.

### 4. Stílusminta és választás

```bash
python3 [skill-mappa]/scripts/design.py minta agy/ceg/design-rendszer/jeloltek/1-<irany> agy/ceg/design-rendszer/jeloltek/2-<irany> -o agy/ceg/design-rendszer/stilus-minta.html
```

A stílusminta jelöltenként egy **arculati táblát** mutat (színek a kontrasztméréssel, logó, ha van, betűtípusok H1-től a gombig, árnyékok, gombok normál és hover állapotban, űrlapmezők), alatta egy **webdesign mintát** (menü, hero, kártyák, idézet, sötét sáv, lábléc). A jelöltek között felül fülekkel lehet váltani. Nyisd meg a böngészőben (ha nem tudod, mondd meg a felhasználónak, hol van). Írd le két-három mondatban, miben más a két jelölt, és miből jön mindkettő. Aztán **állj meg**, és kérdezd meg:

> Melyik legyen? Vagy vegyünk át valamit a másikból (például a gombot vagy a betűt)?

Ha keverést kér, készíts egy harmadik jelöltet (`3-...`), ellenőrizd a kontrasztot, és mutasd meg újra.

### 5. Véglegesítés

A választás után:

1. Másold a nyertes jelölt `tokens.css`-ét és `logo/` mappáját (ha van) az `agy/ceg/design-rendszer/` gyökerébe. A `jeloltek/` mappa marad. Ha a mappában van a céges agy sablonjából jött `README.md` („Ez a mappa most üres”), írd át egy sorra: „A design-rendszer leírása: `design-rendszer.md`.”
2. Futtasd a mintát csak a véglegesre, ugyanabba a fájlba:
   ```bash
   python3 [skill-mappa]/scripts/design.py minta agy/ceg/design-rendszer -o agy/ceg/design-rendszer/stilus-minta.html
   ```
3. Írd meg a `design-rendszer.md`-t (lent a forma).
4. Az `arculat.md` üres (`[[HIÁNYZIK]]`) mezőibe írd be a választott színeket és betűket, mögé: `(a design-rendszerből, ÉÉÉÉ-HH-NN)`. A felhasználó saját adatát ne írd felül. A „Design-rendszer” szakaszba írd: „Kész: `design-rendszer/` (ÉÉÉÉ-HH-NN), a választott irány: <név>.”

A `design-rendszer.md` formája:

```markdown
# Design-rendszer

frissítve: ÉÉÉÉ-HH-NN · irány: <név>

<Egy bekezdés: milyen hatást kelt, és miből jön.>

## Honnan jön
| Elem | Forrás |
|---|---|
| Logó | a felhasználóé (`logo/…`) |
| Fő szín | a felhasználó választása / a logóból / javaslat |
| Betűk | a felhasználóé / a referenciából (<oldal>) / javaslat |
| Formák, árnyék | a referenciából / javaslat |
| Semleges színek, méretek, sormagasság | számolt (`design.py skala`) |

## Színek
| Szín | Kód | Mire |
|---|---|---|
| Elsődleges / kiemelt | #… | alcím, ikon, akcentus |
| … | | |

## Gombok
Elsődleges, másodlagos és a sötét sáv gombja: normál és hover színek, kerekítés, keret.

## Árnyékok
Árnyék 1 (kártya) és Árnyék 2 (kiemelés): egy mondatban, milyen hatású.

## Betűk
- **Címsor:** <font>, <súly>. **Szöveg:** <font>. Google Fonts link: <link>
- **Méretek:** a skála aránya, a H1 mobilon és asztalin, a törzsszöveg mérete, a sormagasságok.

## Űrlap
A mező kerete, a fókusz és a hiba színe.

## Formák
Kerekítés, gombforma, keret, árnyék: egy-egy mondatban.

## Logó
Melyik fájl hova való: `logo.svg` (színes, alapból), `logo-sotet.svg` (világos háttérre, egyszínű helyre), `logo-feher.svg` (sötét háttérre, a sötét sávban és fotón), `favicon.svg`. Ha a logó szöveges és ideiglenes, az is.

## Képek
Milyen fotók illenek hozzá (fény, színvilág, emberek vagy tárgyak), és milyenek nem.

## Amit ne
3-5 pont: például ne legyen több gombszín, a fő színt ne használd hosszú szövegre.
```

### 6. Átadás

Mondd el röviden:
- melyik irány lett, és hol vannak a fájlok;
- mi jött a felhasználótól (anyag, választás, referencia), és mi a te javaslatod;
- ha egy meglévő színt más szerepbe tettél, vagy egy számolt értéket átírtál, azt is;
- ha a logó szöveges (mert nem volt), egy mondatban: ez ideiglenes, egy tervezett logóra később lecserélhető, a változatokat akkor újra kell generálni;
- a következő lépést: a design-rendszert bármelyik építő használhatja. Landing oldalnál a **landing-építő** a `szoveg.md`-ből és ebből építi meg az oldalt; ehhez hozzon egy-három oldalt (link vagy képernyőkép), aminek tetszik az elrendezése vagy a hangulata.
