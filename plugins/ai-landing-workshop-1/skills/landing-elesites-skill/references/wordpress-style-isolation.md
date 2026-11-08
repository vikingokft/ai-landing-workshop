# WordPress-stílusok: izolálás és ütközésvizsgálat

A WordPress-export CSS-korlátozása kétirányú: a landing ne változtassa meg a környező oldalt, és a sablon/Elementor szokásos globális szabályai ne írják felül a landing designját. Az Elementor- és Gutenberg-változatot külön ellenőrizd, a ténylegesen kiadott fájlokból.

## Közvetlen színek, megfelelő specifikusság

A befoglaló elem `color` értéke önmagában nem védi a címsorokat. Egy közvetlenül a címsort célzó sablonszabály megelőzi az örökölt színt, függetlenül a befoglaló szelektorának specifikusságától. A fontos színeket közvetlen, saját gyökérrel kezdődő elem- vagy komponensszabállyal add meg.

- A forrásdesignból vedd át az adott szerep és felület valódi színeit. Különítsd el a világos/sötét felületek címsorait, a hangsúlyokat, a szöveges és gombszerű hivatkozásokat, az elsődleges/másodlagos/letiltott gombokat és a mezőket. Ne állíts minden címsort vagy linket azonos színre.
- A címsorok (`h1`–`h6`), hivatkozások (`a` és állapotaik), gombok (`button`, gombszerű linkek, submit elemek), valamint címkék és űrlapmezők (`label`, `legend`, `input`, `textarea`, `select`) designkritikus színeit közvetlenül deklaráld. Szükség szerint a háttér-, szegély-, placeholder-, caret-, aláhúzás- és fókuszszínt is őrizd meg. Ugyanez érvényes más olyan szövegelemekre, amelyeket a célsablon közvetlenül stílusoz.
- A színeket a landingre névterezett, a saját gyökerén és felületein definiált CSS-változók is adhatják. Az elem közvetlen `color: var(...)` szabálya így a helyi felület megfelelő színét kapja. Ne támaszkodj kizárólag a gyökér színének öröklésére vagy az Elementor globális színváltozóira.
- A címsoron belüli `em`, `span` és más kiemelés saját szándékos színét tartsd meg, ne semlegesítsd általános `* { color: inherit }` vagy egységes fehér színnel. Az interakciós állapotokat (`:hover`, `:focus-visible`, `:active`, `:visited`, `:disabled`, szükség szerint érvénytelen mező) a forrásdesign szerint korlátozd és tartsd meg; ahol nincs szándékos eltérés, a normál állapot színét védd.
- Használd a tényleges landing-ID-t a szelektor elején, például `#SAJAT_GYOKER h1` vagy `#SAJAT_GYOKER .sotet-panel h2`. Ezek szemléltető helyőrzők, ne kerüljenek változtatás nélkül az exportba. A megoldás ne hivatkozzon konkrét Elementor kitre, témára vagy a WordPress-oldal más azonosítójára. Komponensváltozatok és állapotok kapjanak az általános saját szabálynál megfelelően erősebb szelektort.
- A gyökér-ID-t ne semlegesítsd `:where(#SAJAT_GYOKER)` használatával. Ne várj védelmet a specifikusságtól, ha az export normál szabályait a témához képest alacsonyabb kaszkádrétegbe teszed. A tényleges kaszkádot és a később betöltött host CSS-t is vizsgáld.
- Ne használj általános `!important` védőréteget, globális resetet vagy mindent felülíró `all: unset` megoldást. Ne kapcsold ki a téma/Elementor globális stílusait. Ha a tényleges környezet inline vagy `!important` szabálya miatt a normál, korlátozott CSS nem elegendő, nevezd meg a konkrét ütközést és a még szükséges célzott megoldást; ne ígérj minden lehetséges host-szabállyal szembeni védelmet.

Példa helyi színrendszerre (a neveket és értékeket a forrásdesignhoz igazítsd):

```css
#SAJAT_GYOKER { --lp-heading: #302a33; --lp-text: #302a33; --lp-accent: #98556e; }
#SAJAT_GYOKER .sotet-panel { --lp-heading: #fff7f9; --lp-text: #fff7f9; }
#SAJAT_GYOKER :is(h1,h2,h3,h4,h5,h6) { color: var(--lp-heading); }
#SAJAT_GYOKER h1 em { color: var(--lp-accent); }
```

Ez a részlet csak a címsorokat szemlélteti, nem teljes export-reset. A linkek, gombok, mezők és állapotaik a saját szerepüknek megfelelő, közvetlen szabályokat igényelnek.

## Aktív helyi előnézet

A [../assets/wp-preview-host.css](../assets/wp-preview-host.css) szándékosan ütköző, kizárólag teszteléshez való host-stílusokat tartalmaz. Közvetlenül sötétre állítja a címsorokat, és eltérő link-, gomb-, mező-, placeholder- és interakciós színeket használ. Kit-számtól és landing-ID-től független. Ezt ne másold a kiadott landing kódjába, és ne védd ki a tesztben a host-stílusok kikapcsolásával.

A meglévő, kész exportokból készíts előnézetet:

```sh
python3 <skill-könyvtár>/scripts/build-wp-style-preview.py \
  --elementor <elementor/beillesztheto.html> \
  --gutenberg-html <gutenberg/html.html> \
  --gutenberg-css <gutenberg/style.css> \
  --gutenberg-js <gutenberg/script.js> \
  --output-dir <külön-helyi-előnézeti-mappa>
```

A JS-opció elhagyható, ha az export nem tartalmaz JavaScriptet. Ha a helyi assetekhez kell, a `--base-url` a már kiszolgált HTTP(S) előnézeti mappára mutathat. A média-feloldást a meglévő helyi előnézetnek megfelelően kezeld; ez a segéd a stíluskörnyezetet biztosítja, nem WordPress REST-szerver.

A segéd három fájlt készít:

- `elementor-conflicts.html`: az Elementor HTML-részlet aktív host-stílusokkal.
- `gutenberg-conflicts.html`: a külön HTML/CSS/JS kimenet ugyanilyen környezetben.
- `baseline-conflicts.html`: csak a környező sablont helyettesítő kontrollok, landing nélkül.

A host CSS szándékosan a landing szabályai után töltődik be. A landing előtt és után is vannak környező címsor-, szöveg-, link-, gomb- és mezőkontrollok. Az eredeti exportokat a segéd nem módosítja. A tesztkörnyezetet ne add át éles beillesztőkódként.

## Egy összevont, kétirányú ellenőrzés

1. A forrásdesignból vagy az önálló FTP-változatból azonosíts reprezentatív elemeket és azok elvárt színeit: világos és sötét felületen címsor, címen belüli kiemelés, szöveges link, elsődleges/másodlagos gomb, címke, mező, placeholder és letiltott állapot. Az elvárt értékeket ne a potenciálisan hibás WordPress-exportból vezesd le.
2. Mindkét aktív előnézetben nézd meg a megjelenést és a böngésző `getComputedStyle` értékeit. A gyökér színe helyett magukat az elemeket, a szükséges pszeudoelemeket és a hover/billentyűzetfókusz állapotokat ellenőrizd. Az eltérő felületeken a szándékos színkülönbségek is maradjanak meg. A `:visited` szín teljes történetét a böngésző adatvédelmi okból nem feltétlenül adja vissza; a korlátozott deklarációt is ellenőrizd, ne állíts nem mért bizonyítékot.
3. A landing előtti és utáni kontrollok színei, hátterei, szegélyei és releváns állapotai egyezzenek a landing nélküli baseline megfelelő kontrolljaival. A baseline host-színei legyenek ténylegesen aktívak: egy kikapcsolt vagy nem illeszkedő host CSS nem érvényes ütközésteszt.
4. A javítás csak a landing saját szabályait érintse. A két kiadási változatot együtt frissítsd, majd a javított elemeket és a környező kontrollokat ellenőrizd újra. A forrásdesign és a téma globális beállításai maradjanak változatlanok.

A jelentés külön nevezze meg az Elementor- és Gutenberg-előnézet eredményét, az ellenőrzött állapotokat és az esetleges nyitott eltéréseket. Ez **helyi ütközésszimuláció**, nem valódi WordPress/Elementor mentés utáni teszt. Ha van hozzáférés a céloldalhoz és engedély az ellenőrzésre, a tényleges kit- és témaszabályokkal végzett külön vizsgálat eredményét önállóan jelezd.

A preview-segéd regressziós mintái (önálló tesztadatok, nem meglévő landingek):

```sh
python3 <skill-könyvtár>/scripts/test-wp-style-preview.py --output-dir <ideiglenes-QA-mappa>
```

Ez a segéd szerkezetét és a bemenetek megőrzését ellenőrzi, valamint böngészőben vizsgálható pozitív és hibás mintákat készít. A CSS-kaszkád helyességét a böngészős mérések igazolják; a Python-teszt önmagában nem.

## Háttér

- [CSS-specifikusság és közvetlen szabályok elsőbbsége az örökléssel szemben](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascade/Specificity)
- [Elementor globális témaelemek](https://elementor.com/help/site-settings/)
