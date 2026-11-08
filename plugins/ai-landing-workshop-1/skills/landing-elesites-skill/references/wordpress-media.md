# WordPress-képek: feltöltés egyben, dátummappa találgatása nélkül

A felhasználó a `media-upload/` képeit változatlan fájlnevekkel egyszerre a médiatárba húzza, majd bemásolja a választott HTML-modul kódját. A képek címét a kód a WordPresstől kapja. Ez nem automatikus képfeltöltés; a feltöltés felhasználói lépés. A működés feltétele a megfelelő JavaScript-beillesztés és a nyilvános médiatár-REST-végpont elérhetősége.

## Fájlnevek és manifest

Az optimalizált képekből készíts egyedi, kisbetűs ASCII neveket: `lp-<csomagazonosító>-<képtartalom-hash>-<szerep>.webp` vagy más elfogadott képformátum. Például `lp-8ac310fe-b16de391ac42-hero.webp`. A csomagazonosítót exportáláskor hozd létre, ne látogatásonként. A hash az átadott kép bájtjait azonosítsa; a szerep legyen értelmes, például `hero`, `portre`, `edzes-anya-baba`. Az azonos képet ne kelljen többször feltölteni, az új képtartalom kapjon új nevet. Ne legyen név végén `-scaled`, `-rotated` vagy felbontásnak tűnő számpár.

A manifest tartalmazza a közös `batch` előtagot, a feltöltendő `files` fájlnévlistát és a források megfeleltetését, hogy a HTML/CSS minden képhasználata helyesen átvezethető legyen. Példa:

```json
{
  "batch": "lp-8ac310fe",
  "files": ["lp-8ac310fe-b16de391ac42-hero.webp"],
  "sourceMap": {"kepek/hero.jpg": "lp-8ac310fe-b16de391ac42-hero.webp"}
}
```

A feltöltési mappába csak a képek kerüljenek, ne a manifest, CSS, JS, font vagy útmutató. A neveket ne kelljen a felhasználónak kézzel kitalálnia vagy a HTML-ben javítania. A médiatári cím átírása nem egyenlő a fájl átnevezésével; a keresés fájlazonosítóra épüljön, ne a módosítható képcímre vagy slugra.

## A mellékelt képkereső beillesztése

A [../scripts/wp-media-resolver.js](../scripts/wp-media-resolver.js) tartalmát a kiadott kódba építsd, ne a skill helyi fájlútvonalára hivatkozz. Elementor esetén a widget `<script>` részébe, Gutenberg esetén a JavaScript-mezőbe kerül. Inicializáláskor az adott landing saját gyökerét és a manifestet add át. A hívás akkor történjen, amikor a gyökér már létezik; szükség esetén `DOMContentLoaded` után. Ismételt inicializálás ugyanarra a gyökérre nem indít új lekérdezést.

Példa a generált HTML megfelelő részére:

```html
<div id="lp-pelda" class="lp-root">
  <img data-lp-media="lp-8ac310fe-b16de391ac42-hero.webp"
       width="1200" height="800" alt="A projekt szerinti valós képleírás"
       fetchpriority="high">
  <p data-lp-media-status role="status" hidden></p>
</div>
```

A helper kódja után, a tényleges gyökér- és manifestértékekkel:

```js
LandingDeliveryMediaV1.resolve(document.getElementById('lp-pelda'), {
  batch: 'lp-8ac310fe',
  files: ['lp-8ac310fe-b16de391ac42-hero.webp']
}).then(report => {
  if (report.issues.length) console.warn('Landing-képek:', report.issues);
}).catch(error => console.warn('Landing-képbetöltés:', error.message));
```

A példát a projekt adataival helyettesítsd; a részletben ne maradjanak mintafájlnevek. A képméretek tartsák fenn a helyet betöltés előtt, a hero ne várjon más animációra. Ha a forrás nélküli képekhez átmeneti megjelenítést adsz, csak a képet érintse, a teljes landing tartalmát ne rejtse el. A státuszüzenet alapból rejtett, valódi hiba esetén látható. Technikainak ható diagnosztika a konzolba kerüljön.

### Többi képhasználat

- Háttérképhez az elem kapjon `data-lp-background="fájlnév.webp"` attribútumot, és a saját CSS-ben `background-image: var(--lp-media-image)` szabályt. Ha több réteges háttér volt, a színátmenetek és egyéb rétegek maradjanak meg a CSS-ben. A helper csak a kép változóját tölti ki.
- Explicit, külön feltöltött reszponzív képekhez az `img` vagy `source` kapjon `data-lp-srcset='[{"file":"fájlnév.webp","descriptor":"800w"}]'` attribútumot. Minden hivatkozott fájl szerepeljen a manifestben és a feltöltési mappában. A régi helyi `srcset` ne írja felül a feloldott képcímeket.
- Ne maradjon kezeletlen `picture`-forrás, háttérkép, logó, maszkkép, CSS `image-set()` vagy JS által használt helyi képcím. A helper által közvetlenül nem kezelt használatot a feloldott URL-térképpel és saját gyökérre korlátozott kóddal vezesd át; ne szüntesd meg észrevétlenül a design rétegeit.

## Hogyan találja meg a képet?

A helper a WordPress oldal `<link rel="https://api.w.org/">` eleméből veszi a REST-gyökeret, vagy a manifestben előre megadott `restRoot` értéket használja. Kezeli az almappás WordPress és a `?rest_route=/` alakot is. Nem találgatja a domaint, a `wp-content` helyét vagy az aktuális év/hónap mappát.

Csak a csomagelőtagra keres a publikus `wp/v2/media` végponton, bejelentkezési adatok nélkül. A visszakapott `media_details.file`, `media_details.original_image` és `source_url` alapján választ, nem a keresés első találatát vagy a képcímet használja. A WordPress szokásos `-scaled`, `-rotated` és sorszámos fájlnév-változatait felismeri; a kapott valódi `source_url` lesz az elérés. Így a képek több hónapban, egyedi uploadmappában vagy médiakiszolgáló domainen is lehetnek.

A keresés legfeljebb öt, csak a csomagra szűrt találati oldalig és összesen tíz másodpercig tart. Hiányzó kép, több lehetséges csatolmány, tiltott API vagy átnevezés miatt elvesző azonosító esetén nincs önkényes választás és végtelen újrapróbálkozás. A többi egyértelműen azonosított kép megjelenhet, a hiba látható állapotot kap. A felhasználó ne nevezze át a feltöltési fájlokat, és ugyanazt a csomagot ne töltse fel többször; ismételt csatolmányoknál a helyes hozzárendelést ellenőrizni kell.

## Teljesítmény és korlátok

- Az automatikus feloldás egy extra adatlekérést jelent a képek előtt. Ha a képek már fel vannak töltve és a publikus WordPress-cím ismert, csomagoláskor kérdezd le a tényleges képcímeket, majd ezekkel generáld a kódot. A helper `urlMap` értéke az előre feloldott fájlnév → URL térkép lehet; teljes térképnél nem használ REST-kérést. A felhasználónak egyik módban sem kell képenként kódot szerkesztenie.
- A nyilvános REST-képelérés és a JavaScript futtatása nem minden telepítésen engedélyezett. A valódi ellenőrzés kijelentkezett látogatóként történjen. Ne tegyél adminjelszót, alkalmazásjelszót, nonce-ot vagy más hitelesítést a landing kódjába.
- Tiltott API vagy HTML-szűrés esetén mondd ki a korlátot. Támogatott, felhasználó által jóváhagyott móddal kérj tényleges képcímeket, és generáld újra a kész kódot; ne kérj képenkénti kézi keresés-cserét. A hónap szerinti rendezés kikapcsolását, az uploads mappa helyét vagy a REST-biztonsági beállításokat ne módosítsd automatikusan.
- A helper a fájlazonosítást ellenőrzi, nem bizonyítja egy átalakító bővítmény minden lehetséges viselkedését vagy a tényleges képfájl betöltését. Az éles képmegjelenés, a kivágás és a betöltési hibák a böngészős ellenőrzés részei.

## Hivatalos alapok

- [Médiatári év/hónap rendezés](https://wordpress.org/documentation/article/settings-media-screen/)
- [Médiatár REST API és source_url](https://developer.wordpress.org/rest-api/reference/media/)
- [REST API-gyökér felfedezése](https://developer.wordpress.org/rest-api/using-the-rest-api/discovery/)
- [REST fájlnév szerinti keresés](https://developer.wordpress.org/reference/classes/wp_rest_attachments_controller/prepare_items_query/)
- [WordPress egyedi fájlnevek](https://developer.wordpress.org/reference/functions/wp_unique_filename/)
