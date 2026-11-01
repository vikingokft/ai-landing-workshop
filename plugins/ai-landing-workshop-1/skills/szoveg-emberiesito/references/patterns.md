# Emberiesítő minta-katalógus

Harmincegy minta öt csoportban, plusz észlelési útmutató. A `SKILL.md` B lépése ezen megy végig.

## Tartalom

- **Tartalmi minták** (1–6): felfújt jelentőség, hírérték-puffogás, felszínes elemzés, reklámnyelv, ködös hivatkozás, sablon-fejezetek
- **Nyelvi és nyelvtani minták** (7–13): AI-szókincs, nominalizáció, tagadó párhuzam, mechanikus hármas, szinonima-körözés, hamis sávok, szenvedő szerkezet
- **Stílus-minták** (14–19): gondolatjel, félkövér-özön, beágyazott fejlécek, fejléc-nagybetűzés, emoji, idézőjel
- **Kommunikációs minták** (20–22): chatbot-maradványok, tudás-korlát kifogások, talpnyalás
- **Töltelék és puhítás** (23–31): töltelékfordulatok, halmozott puhítás, üres pozitív zárás, kötőjeles párok, tekintély-fordulatok, útjelzők, töredék-fejlécek, diff-hez tapadó írás, AI-nyitány

## Észlelési ellenőrzőlista

Ezen menj végig a strukturált észlelési körben (`SKILL.md` B lépés), és újra az ellenőrzésnél (E lépés) — **kategóriánként egyszerre**, a valódi szöveg ellen, ne emlékezetből. Minden mintánál jegyezz fel egy `§N — „idézet"`-et, vagy írd: `nincs`.

**A találat feljegyzése nem törlési parancs.** A csoportosan jelentkező jelek átírandók; az egyedülálló jel valódi emberi prózában megőrzendő (lásd lent az Észlelési útmutatót). Tiszta szövegnél a `nincs` a **várt** válasz — ne gyártsd a találatokat, hogy legyen mit beírni.

**Kereséssel megtalálható jelek** — a `scripts/scan.py` (A lépés) ezeket gépiesen megtalálja; mindegyiket erősítsd meg és oldd fel.

- §7 AI-szókincs — kulcsfontosságú, elengedhetetlen, forradalmi, felbecsülhetetlen, merüljünk el, íme?
- §13 `-ásra/-ésre kerül` — „elvégzésre kerül", „kialakításra kerül"?
- §14 mondat-közi gondolatjel — bármilyen `—` vagy `–` mondat közben?
- §15 félkövér-özön — félkövér kifejezések csoportosan, mechanikus hangsúlyként?
- §16 beágyazott fejlécek — `**Fejléc:** …` alakú listaelemek?
- §17 fejléc-nagybetűzés — minden szó nagybetűvel a címben?
- §18 emoji — fejlécet vagy listaelemet díszít?
- §19 idézőjel — **angol** `“…”` a magyar `„…”` helyett? (Az ASCII `"…"` **rendben van** — a magyar billentyűzeten a `„` AltGr-kombináció, tehát az egyenes idézőjel a normális emberi alak. A `„…”` is rendben. Csak az angol nyitó `“` a jel: az se nem billentyűzet, se nem magyar tipográfia.)
- §20 chatbot-maradvány — „Remélem, segítettem", „Szólj, ha…", „Íme egy…"?
- §22 talpnyalás — „Nagyszerű kérdés!", „Teljesen igazad van!"?
- §23 töltelék — „annak érdekében, hogy", „azon okból kifolyólag", „fontos megjegyezni"?
- §24 halmozott puhítás — „talán esetleg elképzelhető, hogy"?
- §27 tekintély-fordulat — „a valódi kérdés az", „a lényeg az", „ami igazán számít"?
- §28 útjelző — „merüljünk el", „íme, amit tudni kell", „minden további nélkül"?
- §31 AI-nyitány — „A mai világban…", „Képzeld el, ahogy…", „Te is unod, hogy…?", „Lépésről lépésre végigvezetlek"?

**Részben gépi** — a scanner a gyakori alakot elkapja, a változatokat kézzel kell.

- §9 tagadó párhuzam — „Nem X, hanem Y", „Nem azért X. Hanem Y.", „Nem a … -vel van baj", „Nem X, csak Y". Kézzel is menj végig: egy megérdemelt szembeállítás maradhat, az ismételt reflex nem.

**Jelentés-alapú jelek** — ezeket a keresés nem látja, és ez a kör a legfontosabb.

- §1 jelentőség-felfújás — „mérföldkő", „fordulópontot jelent", „szélesebb trendeket tükröz"?
- §2 hírérték-puffogás — médiamegjelenés vagy követőszám bizonyítékként?
- §3 felszínes elemzés — lezáró `-va/-ve` fordulatok („rávilágítva", „tükrözve", „bemutatva")?
- §4 reklámnyelv — „lenyűgöző", „pezsgő", „kihagyhatatlan", brosúra-hangnem?
- §5 ködös hivatkozás — „szakértők szerint", „iparági jelentések", „megfigyelők szerint" forrás nélkül?
- §6 sablon-fejezetek — „Kihívások és jövőbeli lehetőségek" típusú szakasz?
- §8 létige-kerülés — „szolgál", „testesíti meg", „büszkélkedik" ott, ahol a „van" elég lenne?
- §10 mechanikus hármas — kivétel nélkül hármas felsorolás?
- §11 szinonima-körözés — ugyanaz a dolog minden bekezdésben más néven?
- §12 hamis sávok — „3–5 nap", ahol nincs mérés mögötte?
- §21 tudás-korlát kifogás — „a legutóbbi információim szerint", „bár a konkrét részletek korlátozottak"?
- §25 üres pozitív zárás — „Összességében ez izgalmas lehetőség"?
- §26 kötőjeles párok — „adat-vezérelt", „cél-orientált" halmozva?
- §29 töredék-fejlécek — fejléc, ami után egyetlen mondat áll?
- §30 diff-hez tapadó írás — a szöveg a változásról beszél, nem a dologról?

---

## TARTALMI MINTÁK

### 1. Felfújt jelentőség, örökség, szélesebb trendek

**A probléma:** a szöveg megmagyarázza, miért jelentős, amit épp elmondott, ahelyett hogy hagyná magától jelentősnek lenni.

**Előtte:**
> A rendelő 2017-ben nyílt meg, ami fordulópontot jelentett a helyi fogászati ellátásban, és a betegközpontú szemlélet szélesebb elterjedését tükrözi.

**Utána:**
> A rendelő 2017-ben nyílt meg.

### 2. Hírérték-puffogás

**A probléma:** a médiamegjelenés vagy a követőszám bizonyítékként szerepel a fontosságra.

**Előtte:**
> Munkáját több iparági kiadvány is bemutatta, és a közösségi médiában több ezer követője van.

**Utána:**
> Írt róla a [kiadvány neve].

A konkrétum (melyik kiadvány, hány követő) csak akkor kerül be, ha a forrásban ott van; ha nincs, a mondat kimarad. Az átírás nem hoz új tényt.

### 3. Felszínes elemzés lezáró határozói igenévvel

**Ez a minta újraírva.** Angolban a `-ing` végű lezárások adnak hamis mélységet („highlighting the importance of…"). Magyarban ennek a `-va/-ve` határozói igenév felel meg, és ugyanúgy üres.

**A probléma:** a mondat végére akasztott igenév úgy tesz, mintha elemzés lenne, de csak megismétli a mondatot.

**Előtte:**
> A rendelő négy szakorvost foglalkoztat, **rávilágítva** az átfogó ellátás iránti elkötelezettségre.

**Utána:**
> A rendelő négy szakorvost foglalkoztat.

**Amit keress:** `rávilágítva`, `tükrözve`, `bemutatva`, `hangsúlyozva`, `demonstrálva`, `illusztrálva` a mondat végén.

### 4. Reklámnyelv

**A probléma:** brosúra-hangnem tények helyett.

**Előtte:**
> A pezsgő Ráday utca szívében megbúvó, lenyűgöző rendelő kihagyhatatlan élményt kínál.

**Utána:**
> A rendelő a Ráday utcában van.

**Amit keress:** `megbúvó`, `pezsgő`, `lenyűgöző`, `kihagyhatatlan`, `varázslatos`, `felejthetetlen`.

### 5. Ködös hivatkozás és mosó-szavak

**A probléma:** állítás forrás nélkül, ami tekintélyt vesz fel kölcsönbe.

**Előtte:**
> Szakértők szerint ez a megközelítés hatékonyabb.

**Utána:** vagy nevezd meg a forrást, vagy hagyd ki az állítást.

**Amit keress:** `szakértők szerint`, `kutatások azt mutatják`, `iparági jelentések`, `sokak szerint`, `általánosan elfogadott`.

### 6. Sablon-fejezetek

**A probléma:** „Kihívások és jövőbeli lehetőségek" típusú szakasz, ami minden témára ráhúzható.

**Utána:** ha a szakasznak nincs konkrét tartalma, töröld. Ha van, adj neki valódi címet.

---

## NYELVI ÉS NYELVTANI MINTÁK

### 7. Túlhasznált AI-szókincs

**A probléma:** olyan szavak, amiket a gépi szöveg aránytalanul sokszor használ.

**A magyar lista:**

| Kerüld | Helyette |
|---|---|
| kulcsfontosságú | fontos, vagy mondd meg, miért |
| elengedhetetlen | kell, szükséges |
| forradalmi, felbecsülhetetlen | konkrét állítás |
| merüljünk el, íme | csak kezdd el |
| a mai rohanó világban | töröld |
| lehetőségek tárháza | konkrét felsorolás |
| holisztikus, szinergia | mondd el, mit jelent |
| kihívást jelent | nehéz, nem megy, akadályozza |
| a nap végén | végül, vagy töröld |
| izgalmas utazás | töröld |

**Tükörfordítások, amik magyarban idegenül hatnak:** `a nap végén` (at the end of the day), `merüljünk el` (let's dive in), `íme néhány` (here are a few), `emeld új szintre` (take it to the next level).

### 8. Létige-kerülés

**Ez a minta újraírva.** Angolban a `serves as / stands as / boasts` kerüli az `is`-t. Magyarban a jelen idejű létige eleve elmarad („a rendelő nagy"), tehát a kerülés máshogy jelentkezik: **igei körülírással**.

**A probléma:** egyszerű állítás helyett terjengős igei szerkezet.

**Előtte:**
> A rendelő négy szakorvos munkáját **fogja össze**, és a modern technológia **letéteményese**.

**Utána:**
> A rendelőben négy szakorvos dolgozik, modern eszközparkkal.

**Amit keress:** `letéteményese`, `megtestesíti`, `magában foglalja`, `büszkélkedik`, `képviseli`, `szolgál … -ként`.

### 9. Tagadó párhuzam és lezáró tagadás

**A probléma:** a „Nem X, hanem Y" szerkezet reflexszerű ismétlése. Egy jól elhelyezett szembeállítás erős; a harmadik már gépi.

**Előtte:**
> Nem a technológia a lényeg, hanem az ember.

**Utána:**
> Az ember a lényeg.

**A rejtett változatok is beleszámítanak:**
- kétmondatos: `Nem azért X. Hanem Y.`
- `Nem X, csak Y`
- `Nem a … -vel van baj`
- lezáró tagadás: `…, nem pedig fordítva.`

**Korlát:** teljes szövegben legfeljebb egyszer, vagy amit a `markahang.md` megenged.

**MAGYAR KALIBRÁCIÓ — ez a legfontosabb eltérés az angol eredetitől.**

Angolban az `it's not X, it's Y` retorikai reflex. **Magyarban a `nem … hanem` normál
nyelvtani szerkezet**, amit a helyreigazításra használunk:

> A raktár **nem** a lakásban van, **hanem** a Sorház utcában.

Ez tökéletesen természetes mondat, és **nem jel**. Ha minden `nem … hanem` párost jelölnénk,
a scanner zajossá válna, és sokkal több hamis pozitívot adna, mint az angol változat.

Ezért a scanner csak akkor jelöl, ha a szerkezet **elvont fogalmakat** állít szembe
(technológia, lényeg, kérdés, cél, siker, titok), nem konkrét helyet, időt, tárgyat vagy
személyt. Leteszteltem mindkét irányban: a fenti raktár-mondat átmegy, a
„Nem a technológia a lényeg, hanem az ember" fennakad.

Ha kézzel járod végig, ugyanezt a mércét használd: **konkrét szembeállítás marad, elvont
szembeállítás gyanús.**

### 10. Mechanikus hármas

**A probléma:** minden felsorolás pont három elemű.

**Előtte:**
> Gyors, egyszerű és hatékony.

**Utána:** kettő vagy négy elem, ha annyi van. A hármasság néha jó; a kivétel nélküli hármasság gépi.

### 11. Szinonima-körözés

**A probléma:** ugyanaz a dolog minden bekezdésben más néven, hogy ne legyen ismétlés.

**Előtte:** „a kezelés" → „az eljárás" → „a beavatkozás" → „a terápia", ugyanarra.

**Utána:** nevezd ugyanannak. Az ismétlés magyarban is rendben van, ha a dolog ugyanaz.

### 12. Hamis sávok

**A probléma:** számsáv, ami mögött nincs mérés.

**Előtte:**
> Az eredmény 3–5 héten belül látható.

**Utána:** ha van adat, írd le pontosan. Ha nincs, ne találj ki sávot.

### 13. Szenvedő szerkezet és hamis cselekvő

**A probléma:** a magyar hivatali nyelv legerősebb jele, és a gépi szöveg is előszeretettel használja.

**Előtte:**
> A kezelés elvégzésre kerül, majd a beteg tájékoztatásra kerül.

**Utána:**
> Elvégezzük a kezelést, aztán elmondjuk, mi történt.

**Amit keress:** `-ásra/-ésre kerül`, `megtörténik a …`, `sor kerül rá`, alany nélküli mondat.

Ide tartozik a **nominalizáció** is: „a döntés meghozatala során" helyett „amikor eldöntöd", és a **birtokos láncok**: „a bőr regenerációjának folyamatának támogatása".

---

## STÍLUS-MINTÁK

### 14. Mondat-közi gondolatjel

**A probléma:** a gondolatjel mondat közbeni közbevetésként angol szokás. Magyarban vessző, kettőspont, zárójel vagy két mondat.

**Előtte:**
> A kezelés — ami két órát vesz igénybe — érzéstelenítéssel történik.

**Utána:**
> A kezelés két órát vesz igénybe, és érzéstelenítéssel történik.

**Ne szemre ellenőrizd:** keress rá a `—` és a `–-` karakterre. Lista- és cím-elválasztóként rendben van; mondat közben nem.

### 15. Félkövér-özön

**A probléma:** félkövér kifejezések csoportban, mechanikus hangsúlyként.

**Utána:** bekezdésenként legfeljebb egy félkövér, és csak ha tényleg a legfontosabb.

### 16. Beágyazott fejlécű listák

**A probléma:** minden listaelem `**Fejléc:** magyarázat` alakú.

**Utána:** ha a fejlécek fontosak, legyen táblázat. Ha nem, legyen sima lista vagy folyó szöveg.

### 17. Fejléc-nagybetűzés

**Ez a minta magyarban másképp működik.** Angolban a Title Case a gépi jel. Magyarban a címekben **eleve nem nagybetűzünk** minden szót, tehát ha mégis megjelenik, az angol import.

**Előtte:**
> ## A Rendelő Bemutatása És A Kezelések

**Utána:**
> ## A rendelő és a kezelések

### 18. Emoji

**A probléma:** emoji díszíti a fejlécet vagy a listaelemeket.

**Utána:** vedd ki, kivéve ha a márkahang kifejezetten megengedi.

### 19. Idézőjel — csak az ANGOL alak a jel

Három alak van, és **csak az egyik** árulkodó:

| Alak | Mi ez | Jel? |
| --- | --- | --- |
| `"…"` ASCII | amit az ember gépel — a magyar billentyűzeten a `„` AltGr-kombináció | **nem** |
| `„…”` | helyes magyar tipográfia | **nem** — ezt jelezni azt büntetné, aki gondosan ír |
| `“…”` **angol** | se nem billentyűzet-alak, se nem magyar tipográfia | **igen** |

Az angol alak angolra állított Wordből, angol forrásból másolva, vagy angol tipográfiai
szokású gépi szövegből jön.

**A scanner csak a nyitó `“`-re kulcsol.** A záró `”` közös a két nyelvben — arra jelezni
minden helyes magyar idézetet megbuktatna.

**Előtte:**
> Azt mondta, “jó lesz”, de mások nem így látták.

**Utána:**
> Azt mondta, „jó lesz”, de mások nem így látták. *(vagy egyszerűen: "jó lesz")*

---

## KOMMUNIKÁCIÓS MINTÁK

### 20. Chatbot-maradványok

**A probléma:** a beszélgetés maradványai a kész szövegben.

**Amit keress:** `Remélem, segítettem`, `Szólj, ha kérdésed van`, `Íme egy …`, `Természetesen!`, `Az alábbiakban bemutatom`.

**Utána:** töröld. A szöveg a saját dolgáról szól, nem a beszélgetésről.

### 21. Tudás-korlát kifogások és hézag-tömés

**A probléma:** a szöveg a saját tudásának korlátairól beszél, vagy ködös mondattal tömi be a hézagot.

**Amit keress:** `a legutóbbi információim szerint`, `bár a konkrét részletek korlátozottak`, `nyilvánosan kevés adat áll rendelkezésre`, `visszafogottan kommunikál`.

**Utána:** vagy nézd meg és írd le a tényt, vagy jelöld `[megerősítendő]`-nek. Ne írj ködös mondatot a hézagra.

### 22. Talpnyalás

**A probléma:** dicsérő nyitás, ami nem visz előre.

**Amit keress:** `Nagyszerű kérdés!`, `Teljesen igazad van!`, `Kiváló észrevétel!`, `Szívesen segítek!`.

**Utána:** töröld, és kezdj a válasszal.

---

## TÖLTELÉK ÉS PUHÍTÁS

### 23. Töltelékfordulatok

| Kerüld | Helyette |
|---|---|
| annak érdekében, hogy | hogy |
| azon okból kifolyólag, hogy | mert |
| fontos megjegyezni, hogy | (töröld, és mondd ki) |
| azzal a céllal, hogy | hogy |
| a jelenlegi helyzetben | most |
| rendelkezésre áll | van |

### 24. Halmozott puhítás

**Előtte:**
> Ez talán esetleg elképzelhetően javíthat a helyzeten.

**Utána:**
> Ez javíthat a helyzeten.

Egy puhító szó elég. Három azt jelenti, hogy nem tudod, mit állítasz.

### 25. Üres pozitív zárás

**A probléma:** a szöveg egy általános, jó hangulatú mondattal zárul, ami semmit nem tesz hozzá.

**Előtte:**
> Összességében ez izgalmas lehetőséget kínál a fejlődésre.

**Utána:** töröld. Ha van valódi következtetés, azt írd le.

### 26. Kötőjeles párok

**Ez a minta magyarban gyengébb.** Angolban a `data-driven`, `cross-functional` típusú jelzők halmozása jel. Magyarban ezek tükörfordításként jelennek meg.

**Amit keress:** `adat-vezérelt`, `cél-orientált`, `ügyfél-központú`, `érték-alapú` — különösen ha egymás után több.

**Utána:** mondd el, mit jelent. „Adat-vezérelt döntés" helyett „a számok alapján döntünk".

### 27. Tekintély-fordulatok

**A probléma:** a szöveg bejelenti, hogy most jön a lényeg, ahelyett hogy elmondaná.

**Amit keress:** `a valódi kérdés az`, `a lényeg az`, `ami igazán számít`, `az igazi …`, `alapvetően`.

### 28. Útjelzők és bejelentések

**A probléma:** a szöveg elmondja, mit fog mondani.

**Amit keress:** `merüljünk el`, `íme, amit tudni kell`, `minden további nélkül`, `nézzük meg közelebbről`, `ebben a cikkben`.

**Utána:** töröld, és kezdd a dologgal.

### 29. Töredék-fejlécek

**A probléma:** fejléc, ami után egyetlen mondat áll. A fejléc szakaszt ígér, a szöveg nem ad.

**Utána:** vagy írd meg a szakaszt, vagy vedd ki a fejlécet, és fűzd össze a szöveget.

### 30. Diff-hez tapadó írás

**A probléma:** a szöveg a változásról beszél, nem a dologról. Ez főleg dokumentációnál jön elő.

**Előtte:**
> A korábbi verzióhoz képest most már négy szakorvos dolgozik itt.

**Utána:**
> Négy szakorvos dolgozik itt.

---

### 31. AI-nyitány

**A probléma:** a szöveg nem ott kezdődik, ahol a mondanivaló, hanem egy bemelegítő
fordulattal. Ezek **nem márka-döntések** — senkinek nem állnak jól, ezért itt a helyük,
nem a `markahang.md`-ben.

- ❌ „A mai világban egyre nehezebb…"
- ❌ „Képzeld el, ahogy…"
- ❌ „Te is unod, hogy…?"
- ❌ „Lépésről lépésre végigvezetlek…"

**Előtte:**
> A mai világban egyre nehezebb jó mézet találni.

**Utána:**
> Nehéz jó mézet találni.

Ha a forrásban van rá ok (például hogy a bolti méz nagy része keverék), azzal kezdd; ha nincs, ne találd ki.

---

## ÉSZLELÉSI ÚTMUTATÓ

### Amit NE jelölj (hamis pozitívok)

- **Egyetlen jel valódi emberi prózában.** Ha a szöveg egyébként konkrét, személyes és eleven, egy gondolatjel vagy egy „kulcsfontosságú" nem gépi jel. A **csoportos** megjelenés a jel.
- **Szó szerinti idézet.** Ha valakit idézünk, az ő szavait nem írjuk át. A keretező szöveget igen.
- **Szakszó a helyén.** A „holisztikus" egy gyógytornász szájából szakkifejezés lehet, nem buzzword.
- **Kódblokk, fájlnév, útvonal.** A `--flag`, a `foo--bar`, a fájlnevekben lévő kötőjel nem gondolatjel.
- **Táblázat- és lista-elválasztó.** A gondolatjel listajelölőként és cím-elválasztóként rendben van.
- **Márkahang-döntés.** Ha a `markahang.md` kifejezetten megenged valamit (például emojit a socialban), az nem jel.
- **Hármas felsorolás, ami tényleg három elemű.** Három szakorvos három szakorvos.

### Az emberi írás jelei — ezeket őrizd meg

- **Konkrét, ellenőrizhető részlet.** Név, dátum, összeg, helyszín, szám.
- **Egyenetlen mondathossz.** Az ember hosszú mondat után rövidet ír. A gép egyenletes.
- **Saját vélemény, kockázatvállalás.** „Szerintem ez hülyeség" — ilyet a gép nem ír magától.
- **Beszélt nyelvi fordulat.** Ha a szerző így beszél, hagyd benne.
- **Befejezetlen gondolat, ami később visszatér.** Emberi szerkezet.
- **Humor, irónia, önkritika.** Ha van, az érték.
- **A szerző szakmai szókincse.** Aki érti a szakmát, használja a szavait.

**A cél nem a semlegesítés.** Ha az átírás után a szöveg simább, de üresebb, rontottunk. A jelek eltávolítása után **több** hangnak kell maradnia, nem kevesebbnek.
