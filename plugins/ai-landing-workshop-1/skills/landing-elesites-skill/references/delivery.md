# Átadás: FTP és WordPress

Ezt a részt a kész design csomagolásakor olvasd. Ugyanabból a végleges, ellenőrzött forrásból készíts két átadási mappát; az export ne indítson új designfolyamatot. Az itt megadott nevek alapértelmezések, a projekt meglévő struktúrájához igazíthatók. A csomagok készítése önmagában nem jelent éles feltöltést vagy publikálást.

## Közös elv

Őrizd meg a tartalmat, megjelenést, képeket, betűket, reszponzivitást, animációkat és működő interakciókat mindkét változatban. A célkörnyezet miatti szükséges eltérést nevezd meg. A szerkeszthető forrás maradjon meg; az átadási mappákba csak futtatáshoz és telepítéshez szükséges fájlok kerüljenek. Ne csomagolj titkokat, fejlesztői környezetet, függőségi mappát vagy a teljes munkamappát.

Az exporthoz szükséges hiányzó adatokat együtt kérdezd meg: WordPress-szerkesztő/HTML-modul, és szükség esetén a WordPress publikus címe. A képek alapértelmezett átadása a médiatárba behúzható képmappa. Ezek hiánya ne akadályozza a csomagok előkészítését. A nem eldöntött kompatibilitást jelöld; ismeretlen címet vagy működő integrációt ne találj ki.

## 1. FTP-re feltölthető önálló oldal

Javasolt struktúra:

```text
output/ftp/
  feltoltheto/
    index.html
    assets/                 # képek, fontok, CSS, JS, szükség szerint
  TELEPITES.md
```

- A `feltoltheto/` tartalma legyen a kész statikus oldal. A felhasználónak ezt kell a tárhely webes célmappájába másolnia; a mappaszerkezetet tartsa meg. Az `index.html` a választott webes célmappa gyökerébe kerüljön. A tárhely dokumentumgyökerét ne feltételezd biztosan `public_html`-nak.
- Normál statikus kiszolgálás mellett a látogatónak ne kelljen Node.js-t, fejlesztői szervert vagy buildfolyamatot futtatnia. Ha a projekt buildet igényel, az átadott mappa annak eredménye legyen. Ha szerveroldali működés szükséges, jelezd a tárhelyigényt; ne nevezz statikusan nem működő csomagot kész FTP-oldalnak.
- Használj a csomagon belül helyes, almappába telepítve is működő relatív assethivatkozásokat. Vizsgáld a CSS-beli URL-eket, fontokat, képeket, `srcset`/`picture` forrásokat, modulimportokat és dinamikusan betöltött fájlokat is. Ne maradjon `localhost`, `file://`, ideiglenes előnézeti URL vagy helyi abszolút fájlútvonal. A szándékos külső szolgáltatásokat különítsd el a hibás fejlesztői függőségektől.
- A képek, logók és szükséges betűfájlok legyenek a csomagban, a felhasználáshoz szükséges licencfájlokkal. Külső függőséget csak indokoltan tarts meg, és nevezd meg.
- A telepítési útmutató térjen ki a fájlok másolására, az elérési URL-re, az almappás telepítésre és a még szükséges beállításokra. Ne kérjen a működéshez helyi fejlesztői eszközt. Meglévő WordPress tárhelyén külön landing almappát javasolj; ne írd felül a WordPress fájljait.
- A statikus felület és az űrlapbeküldés külön képesség. Űrlaphoz valódi fogadó végpont, megfelelő adatkezelési tájékoztató és szükség esetén szerveroldali környezet kell. Hiányuk esetén a korábbi őszinte, nem küldhető állapot és a megadott kapcsolatfelvételi alternatíva maradjon meg. Ne állítsd, hogy az FTP-feltöltés önmagában e-mail-küldést biztosít.

## 2. WordPress HTML modulba illeszthető változat

Javasolt struktúra:

```text
output/wordpress/
  media-upload/             # a médiatárba egyszerre behúzható képek
  media-manifest.json
  elementor/beillesztheto.html
  gutenberg/html.html
  gutenberg/style.css
  gutenberg/script.js
  elonezet.html              # helyi ellenőrzési keret, nem a modulba való
  BEILLESZTES.md
```

Az Elementor `beillesztheto.html` és a Gutenberg `html.html` közvetlen HTML-részlet legyen, ne teljes dokumentum `doctype`, `html`, `head` és `body` elemekkel. Ne tartalmazzon PHP-t, fejlesztői importokat vagy buildet igénylő kódot. Az előnézet ugyanazt a részletet használja; ne legyen attól független második megvalósítás.

### Beillesztési környezet és izolálás

- A cél a megadott szerkesztő tényleges HTML modulja. Az Elementor HTML widget HTML-t, `<style>`-ba írt CSS-t és `<script>`-be írt JavaScriptet is fogadhat. Gutenberg vagy más szerkesztő esetén a megengedett elemek és a felhasználói jogosultságok alapján alakítsd az átadást; a Gutenberg-változathoz a CSS-t és a JS-t külön fájlban add, és pontosan nevezd meg, mi hová kerül. A jelenlegi, megfelelő jogosultsággal elérhető Egyéni HTML blokk külön HTML/CSS/JavaScript-mezőihez ez a célzott átadás; régebbi vagy korlátozott szerkesztőnél a támogatott eltérést dokumentáld.
- Egy egyedi gyökérelem alá rendezd a landinget. A CSS szelektorai és változói erre a gyökérre korlátozódjanak; a teljes oldal `html`, `body`, `:root`, általános `header`, `button`, `img`, `*` vagy más globális szabályait ne engedd a WordPress többi elemére hatni. Az eredeti oldal törzsre vonatkozó vizuális szabályait a landing gyökerén őrizd meg. A fontcsaládok és animációnevek is kapjanak egyedi névteret, ahol ütközhetnének.
- A címsorok, linkek, gombok és űrlapelemek színét a saját gyökérrel kezdődő, közvetlenül az adott elemekre célzó szabályokkal védd, megfelelő specifikussággal. A gyökéren örökölt fehér szövegszínt egy téma közvetlen címsorszíne felülírhatja. A helyi színváltozók, világos/sötét szakaszok, kiemelések és interakciós állapotok maradjanak meg; ne egységesíts mindent egy színre. Ne használj általános `!important`-ot, globális resetet vagy konkrét Elementor kit számához kötött javítást. A teljes eljárást a [wordpress-style-isolation.md](wordpress-style-isolation.md) írja le.
- A JavaScript a saját gyökérelemén belül keressen elemeket, ha a célmodul igényli, kezelje a később beszúrt tartalmat is, és ne kössön többször eseménykezelőt ismételt inicializáláskor. A horgonyok és azonosítók ne ütközzenek a környező oldallal. A menü, GYIK, űrlap és mozgások maradjanak működőképesek.
- Az útmutató jelezze, ha teljes szélességű/canvas oldalsablon, nulla konténerpadding vagy a téma fejlécének/láblécének elhagyása kell az önálló landinghez illő megjelenéshez. A dokumentumcím, metaleírás és favicon WordPress-oldali beállítás; ezeket ne teljes dokumentumként illeszd a HTML modulba, hanem add meg az útmutatóban. Ne változtasd meg automatikusan a WordPress téma globális beállításait.
- A WordPress, a jogosultságok, biztonsági beállítások és egyes modulok kiszűrhetik a CSS-t, JS-t, SVG-t, űrlapot vagy bizonyos URL-eket. Tényleges WordPress-ellenőrzés nélkül ne ígérj minden telepítésen garantált működést. Szűrés esetén dokumentált, támogatott beillesztési módot javasolj; ne rejts el tiltott kódot vagy gyengíts biztonsági beállítást a szűrés megkerülésére.

### Képek a WordPress médiatárából

Alapértelmezetten a `media-upload/` képeit kell egyben a médiatárba húzni, átnevezés nélkül. A kódhoz a [wordpress-media.md](wordpress-media.md) útmutató szerint használj dátummappától független képkeresőt. A fájlnév és a csomagazonosító logikáját mindkét WordPress-változatban közösen tartsd. Ne használj automatikus FTP-s képhivatkozást vagy base64-képkészletet a felhasználó médiatári átadása helyett.

A fontokhoz lehetőleg a jogszerűen csomagolt, optimalizált fontfájlokat ágyazd a CSS-be, ha a célkörnyezet megengedi; máskülönben használj a felhasználóval egyeztetett publikus fontkiszolgálást. A betűcsaládot ne cseréld le észrevétlenül. Az SVG logó lehet saját névterű inline SVG, ha a célmodul fogadja; ha nem, készíts megfelelő felbontású, elfogadott formátumú logóexportot a médiatári csomagba. A WordPress által tiltott fájltípust ne próbáld más kiterjesztés mögé rejteni.

## 3. A csomagok ellenőrzése és átadása

- A végleges forrásból generáld a csomagokat. Későbbi javítás után az érintett exportokat is frissítsd; ne maradjon korábbi állapot a mappákban. A generálás módja legyen reprodukálható a projekt méretéhez illő paranccsal vagy meglévő buildfolyamattal, szükségtelen általános konverter készítése nélkül.
- A kiadott FTP-mappát szolgáld ki statikusan, almappás útvonalon is. Ellenőrizd az assethivatkozásokat és a fő interakciókat; az export ne függjön a projekt fejlesztői szerverétől.
- Az Elementor- és Gutenberg-export tényleges fájljaiból külön készíts helyi ütközéses előnézetet a [build-wp-style-preview.py](../scripts/build-wp-style-preview.py) segítségével. A keret a landing után betöltött, aktív sablon- és Elementor-jellegű szabályokat ad, közvetlen sötét címsor-, link-, gomb- és űrlapszínekkel. Az eredeti designhoz/FTP-változathoz hasonlíts, ne csak a két WordPress-exporthoz. A [stílusizolálási ellenőrzés](wordpress-style-isolation.md) szerint böngészőben ellenőrizd a megjelenést, a fontos számított színeket és interakciós állapotokat; a landing előtti és utáni kontrollok stílusait hasonlítsd a landing nélküli kontrolloldalhoz. Ellenőrizd a képeket, navigációt, GYIK-ot és a kiválasztott animációkat is, ugyanabban az asztali méretben, külön újratervezés nélkül. Az ütköző tesztstílusok és kontrollok ne kerüljenek a beilleszthető kódba.
- Ha nincs hozzáférés a valódi WordPresshez, az eredményt helyi beillesztési előnézetként jelöld; ez nem igazolja a WordPress mentés utáni szűrését és a téma teljes kompatibilitását. A médiatári képkeresést csak a feltöltés után, kijelentkezett látogatói helyzetben lehet élesen ellenőrizni; helyi válaszszimulációval ne állíts éles ellenőrzést.
- A két útmutató legyen a konkrét csomaghoz írt, rövid magyar lépéssor: mit töltsön fel/másoljon be, melyik mappából vagy fájlból, milyen beállítás szükséges, és mi maradt nyitva. A végső válaszban linkeld a két mappát, a médiatári képmappát és a szerkesztőnként bemásolandó fájlokat, jelezd a tesztek tényleges hatókörét. Igény esetén a feltölthető mappa ZIP-je is átadható.

## Hivatalos háttéranyag

A célkörnyezet konkrét korlátainál ellenőrizd az aktuális dokumentációt:

- [Elementor HTML widget](https://elementor.com/help/edit-html-elementor/)
- [WordPress Custom HTML](https://wordpress.org/documentation/article/custom-html/)
- [WordPress engedélyezett URL-protokollok](https://developer.wordpress.org/reference/functions/wp_allowed_protocols/)
- [WordPress médiatár REST API](https://developer.wordpress.org/rest-api/reference/media/)
- [WordPress média-beállítások](https://wordpress.org/documentation/article/settings-media-screen/)
