---
name: landing-ceges-agy
description: "Felépíti és karbantartja a vállalkozás céges agyát: egy agy/ mappát sima md-fájlokkal (cég, márkahang, bizonyítékok, arculat, és ajánlatonként ajánlat, célcsoport, versenytársak), amiből a landing oldal szövegírója és építője dolgozik. Előbb a meglévő anyagokat olvassa és kutat (saját weboldal, versenytársak, a vásárlók hangja), aztán a választott landing oldal blokkjaiból kiszámolja, mi hiányzik, és csak arra kérdez rá. Használd elsőként, mielőtt landing oldalt írsz, és ha ezt írják: 'építsük fel a céges agyat', 'céges agy', 'készítsük el a cégprofilt', 'cégprofil', 'ismerd meg a cégemet', 'itt a weboldalam', 'landing oldalt akarok', 'új ajánlatom van', 'változott az ár', 'frissítsd a céges agyat', 'frissítsd a cégprofilt', vagy ha egy másik skill nem talál agy/ mappát."
---

# Landing céges agy

A céges agy a vállalkozásod „agya”: egy `agy/` mappa néhány sima szöveges (md) fájllal. Benne van, ki vagy, kinek és mit adsz el, milyen hangon beszélsz, hogyan nézel ki, és mivel tudod bizonyítani, amit állítasz. A landing oldal szövegírója és építője innen dolgozik, így nem kell minden oldalnál újra elmondanod ugyanazt.

Ez a skill felépíti az agyat, és később frissíti. Nem ír kész szöveget: azt a szövegíró teszi, ebből a mappából.

## A mappa

```
agy/
├── ceg/                         ← ami minden ajánlatodra igaz
│   ├── uzleti-profil.md         cég, szakértő, történet, pozicionálás, elérhetőség, jogi adatok
│   ├── markahang.md             tegezés vagy magázás, stílus, kerülendő szavak, 3 saját szövegminta
│   ├── bizonyitekok.md          vélemények, számok, logók, díjak, esettanulmányok: forrással
│   ├── arculat.md               színek, betűk, logó, fotók
│   └── design-rendszer/         ← később: a landing oldal építésekor ide kerül a design-rendszer
└── ajanlatok/
    └── <ajanlat>/               ← ajánlatonként egy mappa, csak ami ennél az ajánlatnál más
        ├── _attekintes.md       oldaltípus, recept, honnan jön a látogató és hova megy, kapcsolódó ajánlatok; hiánylista
        ├── ajanlat.md           mi ez, részek, mechanizmus, folyamat, jellemzők, esemény-adatok, ár, bónusz, garancia, limitek, a vásárlás feltételei, kifogások, amit nem ígérhetünk
        ├── celcsoport.md        kinek való, ki dönt és fizet, kinek nem, fájdalmak, vágyak, az ő szavaival
        └── versenytarsak.md     a versenytársak: mit ígérnek, mennyiért, mi a rés; a rossz alternatívák
forrasok/                        ← amit bedobsz, és amit a kutatás lement (nyersen)
oldalak/<oldal>/                 ← ide dolgozik a szövegíró: szoveg.md, később index.html
```

Az üres sablonok: `references/agy-sablon/`. A fájlok szerkezetén ne változtass, mert a szövegíró ezekre a címsorokra keres.

## Két szabály, amit mindig betartasz

1. **Egy tény egy helyen.** Ami minden ajánlatra igaz (a szakértő, a hang, a vélemények), az a `ceg/`-ben él. Az ajánlat-mappába csak az kerül, ami ennél az ajánlatnál más. Ha valami már megvan, hivatkozz rá, ne másold.
2. **Kitalálni tilos.**
   - Ami nem derült ki: `[[HIÁNYZIK: mi hiányzik]]`.
   - Vélemény és eredményszám csak a `bizonyitekok.md`-be kerülhet, és csak forrással. Ha a felhasználó azt kéri, „írj be pár jó véleményt”, mondd el, hogy ezt nem teheted, és kérd a valódiakat. A vélemény a `bizonyitekok.md`-ben él; ha a fájdalmat vagy a vágyat is jól mutatja, a `celcsoport.md` rövid részlettel hivatkozik rá.
   - A vásárló szavait szó szerint hagyd, ne fogalmazd át szebbre.
   - Az árnál mindig derüljön ki, hogy bruttó vagy nettó (alanyi adómentesnél: „végleges ár, ÁFA nélkül”).

Egy jól jelölt hiány többet ér egy hihető, de kitalált adatnál: a szövegíró így tudja, hogy azt a blokkot kihagyja, vagy rákérdez.

### A jelölések

| Mikor | Jelölés |
|---|---|
| Te következtetted ki (például a hangot a szövegeiből) | `(következtetés, erősítsd meg)` |
| Piaci kutatásból jön (fórum, komment, más cég véleményei), nem az ő ügyfelétől | `(piaci hang, forrás: …)` |
| A felhasználó állítja, de nincs mögötte dokumentum vagy mérés (követőszám, „1 200+ elégedett vásárló”, „4,9 a Google-on”) | `(saját állítás, nem ellenőrzött)` |
| Régi anyagból jön (korábbi oldal, régi poszt), és nem tudod, érvényes-e még | `(régi forrás, ÉÉÉÉ: érvényes még?)` |
| A felhasználó meséli el, mit mondott egy ügyfél, de nem szó szerint | `(elmesélt, nem szó szerinti)`: véleményként nem használható |
| A felhasználó kérte, hogy ne kerüljön az oldalra | `(kizárva, a felhasználó kérésére)` |

### Néhány helyzet, amire a szabályok nem adnak egyértelmű választ

- **A fő ígéret:** azt ígérje, amit az ajánlat biztosan ad (tudás, eszköz, élmény, egy lépés), ne a vásárlón múló eredményt. „Négy és fél óra után érted, mi történik a tésztában” jó; „másnap sikerül az első kenyered” nem, mert az a vásárlón múlik. Ha az eredményt mégis kimondaná, feltétellel tedd („ha otthon a sütési lap szerint haladsz”), és a feltétel nélküli változat menjen az „Amit nem ígérhetünk” alá.
- **Ellentmondó források** (a régi oldal 38 videót ír, a friss tematika 46-ot; egy dátum rossz napra esik): a frissebb forrás nyer, a régit jelöld, és ha számít, kérdezz rá.
- **Régi anyag túlzó állításai** („garantáltan 7 nap alatt”, „csak ma 50%”, „5000 tanuló”): ne vedd át tényként; jelöld régi forrásként, és kérdezd meg, érvényes-e. Ha a felhasználó a kizárt szám helyett újat ad („kb. 1 100-an vették meg”), az új szám használható, `(saját állítás, nem ellenőrzött)` jelöléssel; csak a régit zárd ki.
- **A felhasználó kockázatos állítást kér** (gyógyhatás egy kozmetikumnál, garantált bevétel, garantált fogyás, „NAV-ellenőrzésen garantáltan nincs bírság”): ne írd be. Tedd az `ajanlat.md` „Amit nem ígérhetünk” részébe, és röviden mondd el, miért (a kozmetikum, az étrend-kiegészítő, az egészség, a pénzügy és a szabályozott szakmák állításait jogszabály korlátozza). Mondd ki, hogy ez nem jogi tanács; ha bizonytalan, szakember döntse el. Amit mondhat helyette (például „érzékeny bőrre, illatanyag nélkül”), azt javasold.
- **Vevői üzenetek, kérdőív-export, Google-értékelések:** ezek valódi ügyfélmondatok, nem kell megkérdezni, hogy valódiak-e. Csak akkor kérdezz rá, ha a felhasználó jegyzetében forrás nélkül állnak „az ő szavaikkal” jelöléssel. Ha a forrásban van hozzájárulás-oszlop, kövesd, és ne kérdezd újra.
- **Hány vélemény kerül be:** az engedéllyel rendelkezők mind; a `nem tudjuk` hozzájárulásúakból legfeljebb öt, a legerősebbek (konkrét eredmény, a célcsoport saját szavai, az ajánlathoz tartozik). A többi a `forrasok/`-ban marad, onnan később előhozható.
- **Hozzájárulás:** `igen, teljes névvel` / `keresztnévvel` / `keresztnév és a vezetéknév kezdőbetűje` / `monogrammal` / `nem` / `nem tudjuk`. Ha a felhasználó egy szabályt ad mindre („keresztnévvel mehet”), azt minden véleményre írd be, de az átadásban jelezd, hogy ezt ő döntötte el, nem az ügyfél. Az `agy/` fájljaiban a nevet már a megengedett formában írd („Zoltán K.”); ha a hozzájárulás „nem” vagy „nem tudjuk”, monogrammal. A teljes név és a felhasználónév (például egy Instagram-név) csak a `forrasok/` mappában maradhat. „Nem” esetén a mondat csak a `celcsoport.md`-ben maradhat, **név nélkül**, `(belső, nem jelenhet meg)` jelöléssel; más fájlba (például az `ajanlat.md` előnyei vagy kifogásai közé) ne idézd, mert a szövegíró onnan az oldalra vinné.
- **Panasz, negatív vélemény** (összetört a doboz, „drágább, mint az előző”): nem vélemény az oldalra, de jó kifogás-jelölt az `ajanlat.md`-be.
- **Egészségügyi adat** (várandósság, betegség, gyógyszer, testsúly, terápiás panasz): ha az űrlap vagy a szolgáltatás ilyet kér, az adatkezelési tájékoztatónak ki kell térnie rá. Jelezd az `ajanlat.md` következő lépésénél, és javasold, hogy az űrlap csak a szükséges minimumot kérje (a részletek mehetnek a felmérésre vagy egy külön kérdőívbe). Mondd ki, hogy ez nem jogi tanács.
- **Ha a felhasználó azt kéri, hogy valamit ne nézz meg** (például a félkész weboldalát): ne nézd meg.

## A munkamenet

**Ahogy a felhasználóval beszélsz:** úgy szólítsd meg, ahogy ő ír neked. Ha magázva ír, vagy azt kéri, hogy az oldal magázódjon, magázd te is; ha tegez, tegezd. Ha nem derül ki, magázz. Ez a te üzeneteidre vonatkozik; az oldal megszólítása a `markahang.md`-be kerül, és a kettő lehet más.

### 0. Hol dolgozunk?

Nézd meg, van-e már `agy/` mappa a munkamappában. Ha van, olvasd be, és csak frissíts. Ha nincs, hozd létre a `references/agy-sablon/` alapján. Az `ajanlatok/_sablon/` mappát ne másold az `agy/`-ba: abból az ajánlat saját mappája lesz (lásd lent).

### 1. Egy nyitó üzenet: az ajánlat és a források

Ha a felhasználó még nem mondta el, egyetlen üzenetben kérdezz rá mindenre, amivel el tudsz indulni:

> Melyik ajánlatodhoz készül az oldal, és mit tegyen rajta a látogató (letöltsön valamit, jelentkezzen egy eseményre, vásároljon, időpontot foglaljon)? Van weboldalad vagy meglévő anyagod erről az ajánlatról és a cégedről (korábbi oldal, hírlevél, poszt, vélemények, prezentáció, jegyzet)? Küldd el a címet vagy a fájlokat, és abból indulok. Ha tudsz 1-3 versenytársat (név vagy weboldal), azt is írd meg, mert azokat kutatom le. Ha nincs semmi, kérdésekkel haladunk.

A minta tegező; ha a felhasználó magáz, magázva kérdezz. Ha az első üzenete ezek egy részét már tartalmazza, csak a hiányzót kérdezd meg, vagy kezdj el dolgozni.

- A kapott fájlokat és a felhasználó üzenetét másold a `forrasok/` mappába, és olvasd végig.
- Gyűjtsd ki, ami a sablon valamelyik mezőjébe illik.
- Nézd meg, a forrás tényleg a felhasználóé-e (lábléc, logó, szerző). Egy képzés, egy partner vagy egy sablonbolt anyaga tartalomnak jó, de a márkahangnak és az arculatnak nem: jelöld, honnan van.
- Ha a felhasználó megad versenytársakat (név vagy URL), jegyezd fel őket a kutatáshoz.

**Az oldaltípus és a recept.** Az ajánlat leírásából javasolj oldaltípust; a recept a workshopon mindig az **L1 · Alapoldal**, az oldaltípushoz igazítva (`references/receptek.md`, „Melyik receptet válaszd”). Írd be az ajánlat `_attekintes.md`-jébe, és az első kérdéskörben kérd a megerősítését. Nem kell külön üzenet róla. Ha a `receptek.md` kiegészítései közül valamelyik illik az ajánlatra (fizetős, helyszíni, ismétlődő esemény, fizikai termék), alkalmazd, és a végleges blokksort a kiegészítésekkel együtt írd be az `_attekintes.md` „Végleges blokksor” sorába: a hiánylistát erre számolod, és a szövegíró is ebből dolgozik.

- **A. Letölthető csali** (e-book, sablon, csekklista, videó, kvíz…)
- **B. Webinár, esemény** (egy alkalom, akár havonta ismétlődő; ingyenes vagy fizetős)
- **C. Kihívás** (több alkalom: kihívás, több alkalmas online program)
- **D. Értékesítési oldal** (online termék vagy fizikai termék)
- **E. Szolgáltatás** (konzultáció, ajánlatkérés, jelentkezés)

Az ajánlat-mappa a `references/agy-sablon/ajanlatok/_sablon/` másolata. A neve legyen rövid, ékezet nélküli, kötőjeles (például `agy/ajanlatok/alvas-webinar/`), a fájlokban pedig az `[Ajánlat neve]` helyére írd be az ajánlat nevét. Ha a felhasználó más ajánlatait is említi (a következő ajánlat, ajándékutalvány, céges változat), azok nem kerülnek ebbe a mappába: az `_attekintes.md` „Kapcsolódó ajánlatok” sorába írd őket egy-egy mondattal.

### 2. Kutatás

Három irány, a részletek a `references/kutatas.md`-ben. Azokat az eszközöket használd, amik elérhetők: webes keresés, weboldal megnyitása és olvasása. Ha valami nem olvasható be (bejelentkezés, JavaScript-falak), kérd meg a felhasználót, hogy másolja be a szöveget.

1. **A saját jelenlét:** a megadott weboldal fő oldalai (főoldal, rólam vagy rólunk, ajánlat- és szolgáltatásoldalak, vélemények, kapcsolat, impresszum, adatkezelés) és egy-két blogbejegyzés vagy poszt a hanghoz. Ebből jön az `uzleti-profil`, a `markahang` első változata és a `bizonyitekok` jelöltjei.
2. **Versenytársak:** a megadott versenytársak, vagy ha nincsenek, 3-5 keresés alapján, a téma és az oldaltípus szerint. Kiszeded: mit ígérnek, kinek, mennyiért, milyen szakaszokkal építik az oldalukat, mit nem mondanak. Ebből lesz a `versenytarsak.md`.
3. **A vásárlók hangja:** vélemények, kommentek, kérdések, fórumok a témában. Amit a célcsoport a saját szavaival mond a problémájáról és a vágyáról. Forrással, `(piaci hang)` jelöléssel kerül a `celcsoport.md`-be.

A letöltött vagy kimásolt anyag a `forrasok/` mappába kerül, a forrás URL-jével és a dátummal. Ha az eszközöd csak kivonatot ad egy oldalról (nem a teljes szöveget), az is jó, de írd rá: `(kivonat)`. Szó szerint csak azt idézd, amit az eszköz szó szerint adott vissza; egy rövid idézet is elég, forrással. Írj kutatási naplót is (`forrasok/kutatas/kutatasi-naplo-ÉÉÉÉ-HH-NN.md`): mit kerestél, mit találtál, és mit nem. Ha egy keresés nem hozott használható eredményt (például általános kereséssel nem jön elő összevethető versenytárs-oldal), azt is írd le, ne erőltess gyenge találatot a fájlokba, hanem kérdezz rá.

### 3. Kitöltés és hiánytérkép

- Töltsd ki a fájlokat abból, amit az 1. és a 2. lépésben találtál.
- A **Gombszöveg ötlet** (`ajanlat.md`, A következő lépés) ne maradjon üres, ha van hangminta (`markahang.md`) és ismert a következő lépés: írj 1-2 javaslatot a felhasználó hangján, `(következtetés, erősítsd meg)` jelöléssel.
- Aztán nézd meg a választott recept blokkjait (`references/receptek.md`), és a `references/mezo-terkep.md` alapján számold ki, melyik blokkhoz mi hiányzik.
- **Az állapotok:**
  - **megvan:** a blokk minden mezőjéhez van adat, és a blokk soraiban nincs nyitott `[[HIÁNYZIK]]` (ha van, legfeljebb „részben”). A „saját állítás” is adat (jelölve). A „nem releváns” (például ingyenes ajánlatnál a garancia) is megvan.
  - **megerősítendő:** minden mezőhöz van adat, de legalább egy csak következtetés (a te következtetésed, vagy egy kutatott javaslat). A szövegíró dolgozhat belőle, a felhasználó nézze át. Az Előnyök (jellemzőből előny) és a Mechanizmus rése természeténél fogva következtetés: jelölve ezek is legfeljebb „megerősítendők”, nem „részben”.
  - **részben:** van adat, de egy mező hiányzik.
  - **hiányzik:** nincs adat.
  - **Lezárt hiány:** ha egy mezőre a felhasználó „nem tudom”-ot mondott, vagy ő döntötte el, hogy kimarad (például „a címet a visszaigazolásban küldjük”), a blokk állapota `részben (lezárva: …)`, a pontokkal az okkal. Így a szövegíró látja, hogy ez már nem kérdés, hanem a felhasználó teendője vagy döntése.
  - Az elmesélt mondat (a felhasználó mondja el, mit szoktak mondani az ügyfelei) a Problémák, a Vágyott eredmény és a Kifogáskezelés blokkhoz elég: ezeknél „megvan”. A Visszajelzésekhez nem elég.
  - A recept szakaszait számold. Ha ugyanaz a blokk ugyanazzal a tartalommal kétszer áll (például két CTA), egyszer; ha más a tartalma (az L1-ben a Hitelességnövelő elemek: esettanulmány és a Hitelességnövelő elemek: logósor), külön. Az L1 így 15 szakasz. A hiánylista táblájában a szakaszokat pontosan a recept neveivel írd (`references/receptek.md`), mert a szövegíró ugyanezekkel dolgozik. Az elhagyható (✱) blokkokat külön sorold fel: ha nincs hozzájuk anyag, kimaradnak, ez nem hiba.
- A recept blokkjai mellett nézd meg a **mindig kötelező magot** is (`references/mezo-terkep.md`): a nevek, a megszólítás, a fő ígéret, a következő lépés, a jogi minimum. Ez minden receptnél kell, akkor is, ha a recept nem tartalmaz Bemutatkozást.
- És nézd meg az **oldaltípus kötelező adatait** (ugyanott): ezek akkor is kellenek, ha a választott rövid receptben nincs hozzájuk blokk (például a letölthető csalinál, hogy mi van pontosan a PDF-ben, és az űrlap mezői). Ha hiányoznak, a hiánylistában külön sorban szerepeljenek.
- Az eredmény az ajánlat `_attekintes.md`-jébe kerül, ilyen formában:

> Az **L1 · Alapoldal** recept 15 szakaszából 8-hoz minden megvan, 3 megerősítendő (Előnyök, Mechanizmus, Kinek igen, kinek nem), 2 részben, 2-höz semmi. Hiányzik: **Hitelességnövelő elemek: esettanulmány** (nincs eset forrással), **Visszajelzések** (nincs vélemény forrással). A mindig kötelező magból hiányzik: az adatkezelési tájékoztató linkje.

### 4. Kikérdezés

Csak a hiányzó mezőkre kérdezz. A kérdések: `references/kerdesbank.md`. A kérdésbank körei témák szerint csoportosítanak; a kérdésköreidet a hiánylista szerint állítsd össze, bármelyik témából.

- Egy üzenetben egy kérdéskör, benne legfeljebb 6 kérdés. Egy félmondatos megerősítés („Az oldal is tegezzen?”) nem külön kérdés. Egy kérdés egy dologról szóljon; ha két dolog összetartozik (ár és ÁFA), az még egy kérdés. Ahol segít, adj példát, hogy lássa, milyen mélységű válasz kell. A példát az ő területéről vagy egy semleges területről írd, ne másold a kérdésbankból, és ne tartalmazzon kitalált adatot az ő cégéről.
- **A versenytársak listája:** a kérdések után egy sorban mutasd meg, kiket kutattál, és kérd, hogy a felhasználó húzza ki, aki nem az, vagy írjon helyettük másokat. Ez nem számít bele a hat kérdésbe, és ezért nem kell a kutatás közben megállnod.
- **Az első kör:** az oldaltípus megerősítése (ugyanabban a kérdésben: honnan jön a látogató, ha még nem tudod, mert ettől függ a recept hossza), aztán a mindig kötelező mag, az oldaltípus kötelező adatai és a recept kötelező blokkjaihoz hiányzó adatok, a legfontosabbal kezdve. Ezek előbb jönnek, mint a cég története.
- **A második kör:** ami még a kötelezőkből maradt, aztán az elhagyható (✱) blokkoké. **Az arculatról** (színek, logó, fotók helye) egyszer mindenképp kérdezz, ha még hiányzik: a szövegírónak nem kell, de a landing-építőnek igen, és később nehezebb visszakérdezni. Ha az első körben van rá hely (6-nál kevesebb kérdés), tedd oda; ha nincs, a második körbe; ha második kör nem lesz, az átadó üzenet végére, egyetlen kérdésként.
- Ha a kötelező hiányok nem férnek bele egy körbe, a legfontosabbakat kérdezd, a többi a következő körbe megy.
- Amit már tudsz, azt ne kérdezd meg újra, legfeljebb erősíttesd meg egy félmondattal. Mielőtt megírod a következő kört, olvasd át a korábbi válaszait, és minden tervezett kérdésnél nézd meg: felelt-e már rá (más szavakkal is)? Ha igen, töröld; ha részben, csak a hiányzó részt kérdezd (nem: „Ugyanaz a három szappan van a csomagban?”, hanem: „Ha a teafás elfogy, a csomag is elfogy?”). A mindig kötelező mag mezői (különösen a megszólítás) ne maradjanak következtetésként az átadásig: egy félmondattal erősíttesd meg őket valamelyik körben („A termékleírásaid tegeznek, az oldal is tegezzen?”).
- A „nem tudom” is jó válasz: abból hiányjelölés lesz, és haladtok tovább.
- Ha a felhasználó siet, az első kör után is leállhatsz: a hiánylista megmutatja, mi maradt.

Minden válasz után másold a választ a `forrasok/` mappába, frissítsd a fájlokat és a hiánylistát. Ha egy válasz új ellentmondást hoz (például a felhasználó egy terméket „2019 utáni Excelre” ígér, de a tematikában olyan függvény van, ami a 2019-esben nincs), jelöld, és vedd fel a következő körbe vagy az átadásba.

**Mikor állsz meg a kérdezéssel:** ha a mindig kötelező mag és a recept kötelező (nem ✱) blokkjai megvannak, vagy amire nincs válasz, az „nem tudom” jelölést kapott. Ami nem kérdés, hanem a felhasználó dolga (megírni az adatkezelési tájékoztatót, levelezőrendszert választani, befejezni a PDF-et, véleményeket gyűjteni), azt ne kérdezd újra: az átadásba kerül, teendőként. Ha visszakérdez („nincs, kéne?”), válaszolj röviden, és vedd fel a teendők közé. Legfeljebb három kör; utána a maradék az átadásba kerül.

### 5. Átadás

Írj rövid összefoglalót a felhasználónak:
- melyik fájl kész, és hol maradt hiány;
- mi a forrásból jön, és mi következtetés vagy saját állítás, amit érdemes átnéznie;
- a választott recept blokkjai közül melyikhez van meg minden, és melyikhez nincs;
- **a teendői** számozva: amit neki kell pótolnia vagy eldöntenie, mielőtt az oldal élesbe megy (például: adatkezelési tájékoztató, valódi vélemények gyűjtése, egy döntés).

A teendőket írd be az ajánlat `_attekintes.md`-jének „Teendők az élesítés előtt” részébe is, hogy a csevegés után is megmaradjanak; ha az átadásban egyetlen eldöntendő kérdés maradt (például két forrás ellentmond egymásnak), az a teendők végére kerül, kérdésként, nem nyitsz miatta új kört.

Kérd meg, hogy nézze át a fájlokat, mielőtt a szövegíró dolgozni kezd: a rendszer csak abból tud jól dolgozni, ami le van írva. A következtetéseket ő erősíti meg vagy javítja.

## Frissítés később

Ha valami változik („új ajánlatom van”, „emeltem az árat”, „új időpont”, „új vélemények”):

1. Olvasd be az érintett fájlt. A többihez ne nyúlj.
2. Új ajánlathoz új almappa az `agy/ajanlatok/` alatt; a cég-szintet ne kérdezd újra.
3. A lejárt határidőt és a lezárt ajánlatot jelöld így: `(lezárva: ÉÉÉÉ-HH-NN)`.
4. Írd át a dátumot a fájl elején, és mondd el, mi változott.

## Ellenőrzés a leadás előtt

- [ ] Megvan az `agy/` mappa a sablon szerinti fájlokkal és címsorokkal?
- [ ] Minden ismeretlen adat `[[HIÁNYZIK: …]]` jelölést kapott, semmi sincs kitalálva?
- [ ] Minden véleménynek és számnak van forrása, és jelölve van, megjelenhet-e a név?
- [ ] A jelölések a helyükön vannak (következtetés, piaci hang, saját állítás, régi forrás, elmesélt, kizárva)?
- [ ] Az árnál kiderül, bruttó vagy nettó? Vásárlásnál megvan a fizetés, az elállás, és fizikai terméknél a szállítás?
- [ ] Az „Amit nem ígérhetünk” rész ki van töltve (vagy „nincs”)?
- [ ] Ki van számolva a hiánylista a választott recept blokkjaira és a mindig kötelező magra?
- [ ] Az átadásban ott a felhasználó teendőinek listája?
- [ ] A forrás-anyagok a `forrasok/` mappában vannak, URL-lel és dátummal?

## Kapcsolódó skillek

- **landing-szövegíró:** ebből az `agy/` mappából dolgozik, és a recept szakaszai szerint megírja a `szoveg.md`-t.
- **szöveg-emberiesítő:** a kész szöveget nézi át.
- **landing-építő:** a szövegből HTML oldalt épít; az `arculat.md`-t és a `design-rendszer/` mappát használja, és a design-rendszert is ide menti.
