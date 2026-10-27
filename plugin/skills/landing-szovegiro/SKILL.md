---
name: landing-szovegiro
description: "Megírja a landing oldal szövegét a vállalkozás céges agyából (agy/ mappa), az L1 · Alapoldal recept 15 blokkjának sorrendjében. Blokkonként szabadon ír, mint egy szövegíró: a blokk célja és a kontextus ad irányt, előre megszabott szöveghelyek és hosszak nincsenek. A végén a szöveg-emberiesítővel átnézeti, és egy szoveg.md-t ad, amiből a landing-építő dolgozik. Előfeltétel: a landing-ceges-agy skill már felépítette az agy/ mappát. Használd, ha ezt írják: 'írd meg a landing oldal szövegét', 'landing szöveg', 'írd meg az oldalt', 'szövegírás', 'jöhet a szöveg', vagy ha a céges agy elkészült, és a következő lépés a szöveg."
---

# Landing szövegíró

A céges agyból (`agy/`) megírja egy landing oldal szövegét, az **L1 · Alapoldal** recept 15 blokkjának sorrendjében. A blokkok a `references/blokklista.md`-ben vannak: mindegyiknél ott áll, mi a dolga, melyik mentális kapcsolót nyomja meg, és honnan jön hozzá az anyag.

**A szöveg az első, a forma utána.** Blokkonként úgy írsz, ahogy a gondolat kívánja: annyi mondattal, bekezdéssel, felsorolással, amennyi kell. Hogy ebből milyen designelemek lesznek (kártyák, ikonsorok, oszlopok), azt az építés dönti el, nem te.

Nem épít HTML-t (az a landing-építő dolga), nem változtat a blokkok sorrendjén, és nem talál ki tényt.

## 1. Ellenőrzés

1. Keresd meg az `agy/` mappát. Ha nincs, állj meg, és mondd, hogy előbb a **landing-ceges-agy** skill építse fel.
2. Melyik ajánlatra készül az oldal? Ha az `agy/ajanlatok/` alatt egy mappa van, az. Ha több, kérdezz rá egy mondatban.
3. Olvasd be: az ajánlat `_attekintes.md`-jét, `ajanlat.md`, `celcsoport.md`, `versenytarsak.md`, és a `ceg/` mind a négy fájlját.
4. **A mindig kötelező mag** nélkül nem írsz: a márka és a szakértő neve, a megszólítás, a fő ígéret, a következő lépés (mit tesz a látogató), és eseménynél az időpont. Ha valami hiányzik, sorold fel, és ajánld, hogy a landing-ceges-agy pótolja.

## 2. Írás

Olvasd el a `references/szabalyok.md`-t, a `references/blokklista.md`-t és a `references/cimsorok.md`-t, és nézd meg a `markahang.md` szövegmintáit. Aztán írd meg a szöveget blokkonként, sorrendben.

- **Előbb gondold végig az egészet.** Mi az az egy gondolat, amit az oldal elad, és hogyan vezeti végig rajta az olvasót a 15 blokk? A blokkok egy gondolatmenet részei, nem különálló dobozok: egymásra épülnek, és nem ismétlik egymást.
- **Minden blokknál** a blokklista „dolga” és „kapcsoló” sora az irány, a „fogás” egy ötlet, amit használhatsz. Az „anyag” sor mondja meg, melyik fájlban keresd a tényeket.
- **Címsorok:** a blokk szövege után írd meg őket, a `cimsorok.md` szerint: blokkonként a minta, felvezető csak ritkán, rövid címkeként, a Hero és a CTA címsorához 4-6 jelöltből választva, a végén az ellenőrző kérdésekkel.
- **Elhagyható (✱) blokk:** ha nincs hozzá valódi anyag (vélemény, eset, logó), a blokk egyetlen sora: `Kimarad: nincs anyag (…).`
- **Ha egy blokknak nincs saját tartalma,** mert minden, amit mondana, egy másik blokkban már elhangzott (egyszerű szolgáltatásnál gyakori), ne ismételd más szavakkal. Két út közül választhatsz:
  - **kihagyod**, és a blokk egyetlen sora: `Kimarad: nincs saját tartalma (…).` Ezt a nem ✱-os blokkokra is megteheted;
  - **kutatsz hozzá** (a témában, a versenytársak oldalain, a vásárlók kérdéseiben), és amit találsz, forrással beírod az `agy/` megfelelő fájljába, `(piaci hang)` vagy `(következtetés, erősítsd meg)` jelöléssel, aztán abból írod meg a blokkot.
  Az átadásban mondd el, melyiket választottad, és miért.
- **Ha egy tény hiányzik,** de a blokk enélkül is megírható, írd meg nélküle, és a hiányt sorold fel az átadásban. Ha nélküle nem írható meg, a helyére `[KITÖLTENDŐ: mi hiányzik]` kerül.

**A kimenet:** `oldalak/<ajanlat>/szoveg.md` (az `<ajanlat>` az ajánlat mappájának neve; ha ott már van ilyen fájl, a régit nevezd át `szoveg-elozo-ÉÉÉÉ-HH-NN.md`-re). A formája:

```markdown
---
cim: <az oldal címe>
recept: L1 · Alapoldal
ajanlat: <az ajánlat mappájának neve>
---

# <az oldal címe>

## 1. Hero

### <a blokk címsora>

<a blokk szövege, szabadon: bekezdések, felsorolás, gombszöveg, ahogy a gondolat kívánja>

## 2. Problémák és következményeik

…
```

Néhány szokás kötött, mert ezek segítik az építést:

- a blokk címsora `###` (a logósornak nem kell); ha ritkán felvezető is kell, az a címsor fölött áll: `**Felvezető:** …`;
- ha a blokk felsorol (problémák, lépések, kérdések), az Markdown-lista legyen;
- a gomb, az űrlap és a jelölőnégyzet így áll:

  ```markdown
  **Gomb:** Kérem a helyem
  **Űrlap:** Keresztnév, E-mail-cím
  **Jelölőnégyzet:** Elolvastam és elfogadom az adatkezelési tájékoztatót.
  ```

- a blokkok `##` címsora pontosan a blokklista neve, a `✱` jel nélkül.

Ha kész, futtasd az ellenőrzést (a skill gyökere az a mappa, amelyikben ez a `SKILL.md` van):

```bash
python3 "<a skill gyökere>/scripts/ellenoriz.py" oldalak/<ajanlat>/szoveg.md
```

## 3. Emberiesítés

Futtasd a **szöveg-emberiesítő** skillt a `szoveg.md`-n: cél-felület landing oldal, hang-forrás az `agy/ceg/markahang.md`, normál szigorúság, a futás-mappája az `oldalak/<ajanlat>/emberiesites/`. Mondd meg neki, hogy a véleményeket és a vásárló idézőjeles mondatait ne írja át, a `##` blokk-címsorokhoz, a `[KITÖLTENDŐ: …]` helyekhez és a `**Felvezető:**`, `**Gomb:**`, `**Űrlap:**`, `**Jelölőnégyzet:**` jelölésekhez ne nyúljon (a scanner ezeket félkövérként jelezheti: MARAD). A záró átírás a `szoveg.md`-be kerül vissza; külön végleges fájl nincs.

Ha a szöveg-emberiesítő nincs telepítve, olvasd végig a szöveget a `szabalyok.md` 9. pontja szerint, és írd át, ami fordításnak hangzik.

Utána futtasd újra az ellenőrzést.

## 4. Végső ellenőrzés

Olvasd végig a kész `szoveg.md`-t, és válaszolj igennel vagy nemmel:

1. A Hero után tudja az olvasó, mi ez, kinek szól, és mit kap?
2. A CTA szakasz a Hero ígéretét adja vissza?
3. Minden szám, név, vélemény, ár és határidő az `agy/`-ból jön, vagy `[KITÖLTENDŐ]` áll a helyén?
4. Semmi nem lépi át az „Amit nem ígérhetünk” határait?
5. A jellemzők mellett ott van, mit nyer vele az olvasó?
6. A címsorok mondanak valamit, nem csak a blokk nevét (kivéve a funkcionális blokkokat)?
7. Hangosan felolvasva úgy szól, mint a `markahang.md` mintái?

Ahol nem, javítsd. Ha a javításhoz adat kell, ami nincs az `agy/`-ban, az átadásba írd.

## 5. Átadás

Rövid összefoglaló a felhasználónak:

- hol a `szoveg.md`, és hogy ebből dolgozik a landing-építő;
- melyik blokk maradt ki, és miért; hol maradt `[KITÖLTENDŐ]`;
- **amit érdemes átnéznie:** a `(saját állítás)`, `(elmesélt)` vagy következtetett adatból írt részeket, a kihagyott kockázatos állításokat, és ha az `agy/` fájljai ellentmondtak egymásnak;
- az emberiesítő mérésének két-három sora.

Kérd meg, hogy olvassa végig a szöveget hangosan: ő ismeri a piacát, a vevőit és az ajánlatát, itt tud a legtöbbet hozzáadni.

## Ha új változatot kérnek

Alapból egy változatot írsz. Csak akkor írsz többet, ha kérik.

**Egy-két blokk új változatban:**
1. Olvasd be az `agy/`-at és a kész `szoveg.md`-t, hogy a többi blokkot ismerd, és ne ismételd őket.
2. Írd meg a kért blokkot 2-3 változatban, mindegyiket más irányból (például az egyik a problémából, a másik az eredményből indul; a címsor más-más típusból a `cimsorok.md` szerint).
3. A változatok az `oldalak/<ajanlat>/valtozatok/<blokk>-ÉÉÉÉ-HH-NN.md` fájlba kerülnek; a `szoveg.md`-hez ne nyúlj.
4. Emberiesítés csak az új szövegeken; a végső ellenőrzésből csak a blokkra vonatkozó kérdések (ha a Hero vagy a CTA változik, a 2. kérdés is).
5. Add át egymás mellett, változatonként egy mondattal, miben más. Ha a felhasználó választott, cseréld be a `szoveg.md`-be (előtte mentsd el a régit `szoveg-elozo-ÉÉÉÉ-HH-NN.md` néven), és futtasd az ellenőrző szkriptet.

**Az egész oldal új változatban:** kérdezd meg egy mondatban, miben legyen más (fő gondolat, hangnem, hossz, célcsoport). Ha nem mond semmit, válassz más fő gondolatot, mint az elsőnél. Futtasd a 2-5. lépést (az 1. kimaradhat, ha az agy nem változott); a kimenet `szoveg-b.md`, az első megmarad. Az átadásban két mondatban írd le, miben más a két változat.

## Kapcsolódó skillek

- **landing-ceges-agy:** felépíti az `agy/` mappát, amiből ez a skill dolgozik.
- **szoveg-emberiesito:** a 3. lépésben átnézi a szöveget.
- **landing-építő** (2. alkalom): a `szoveg.md`-ből és az `arculat.md`-ből épít HTML oldalt.
