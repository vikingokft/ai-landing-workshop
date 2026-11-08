# Technikai szabályok

Az oldal egyetlen HTML-fájl, ami három helyen is működik: magában egy tárhelyen (FTP), egy WordPress Egyéni HTML blokkban és egy Elementor HTML-widgetben. Ezért kötött a szerkezete.

## A váz

```html
<!doctype html>
<html lang="hu">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><!-- a hero címe vagy az ajánlat neve, legfeljebb kb. 60 karakter --></title>
<meta name="description" content="<!-- 1-2 mondat a hero szövegéből, legfeljebb kb. 155 karakter; ha rövidíteni kell, rövidíts, és az átadásban említsd -->">
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:image" content="kepek/og.jpg"><!-- helyőrző: 1200×630 kép -->
<link rel="icon" href="kepek/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="<!-- a Google Fonts link a ténylegesen használt betűkkel és súlyokkal (design-rendszernél a tokens.css GOOGLE-FONTS sora) -->">
<style data-csak-onallo>body{margin:0}</style>
<style>
.lp{ /* a színek, betűk, méretek változói: a tokens.css :root blokkja, vagy saját --lp- változók */ }
.lp *, .lp *::before, .lp *::after{box-sizing:border-box}
.lp img, .lp svg{max-width:100%;height:auto;display:block}  /* a width/height attribútum mellett ez tartja meg a kép arányát */
/* ... minden szabály .lp-vel kezdődik ... */
</style>
<!-- MÉRŐKÓDOK: ide jön a Meta Pixel és a Google Tag; kódot ne találj ki -->
</head>
<body>
<div class="lp">
  <!-- az oldal teljes tartalma -->
</div>
</body>
</html>
```

## CSS

- **Minden szabály `.lp`-vel kezdődik**, a reset is (`.lp h1`, `.lp .hero`, `@media (...) { .lp ... }`). Így WordPressbe illesztve a téma nem zavar bele, és az oldal sem zavar bele a témába. `:root`, `html`, `body` és csupasz elemválasztó (`h1{...}`) nem lehet a fő `<style>`-ban. Az egyetlen kivétel a `<style data-csak-onallo>`, amit a WordPress-változat kihagy.
- **A változók a `.lp`-re kerülnek**, nem a `:root`-ra. Ha van design-rendszer, másold át a `tokens.css` változóit (a `--ds-` neveket változatlanul), és mindenhol `var(--ds-...)`-szal hivatkozz rájuk. Ha nincs, a palettát és a betűket (a meglévő márkaelemekből és az inspirációból) saját változókba teszed: `--lp-szin-fo`, `--lp-szin-sotet`, `--lp-szin-alap`, `--lp-betu-cim`, `--lp-betu-szoveg` és így tovább. Színt csak ezekből használsz; árnyalatot keverhetsz: `color-mix(in srgb, var(--lp-szin-fo) 12%, white)`. A méretekhez, térközökhöz, kerekítéshez is vezess be változókat.
- **Önálló fájl:** minden CSS a fájlban. Külső forrás csak a Google Fonts. Tailwindet, CSS-keretrendszert, ikonkönyvtárat ne tölts be.
- **Mobil először:** az alap CSS a telefonra szól, a szélesebb képernyőt `@media (min-width: ...)` adja. A betűméretekhez `clamp()`-et használhatsz (a tokenekben már így vannak).
- **Specificitás:** vigyázz, hogy a szakaszok általános szabályai (például `.lp section{padding:...}`) ne írják felül a különlegeseket. A szakaszonkénti térközt a szakasz saját osztályán add meg.
- **Fókusz:** `.lp a:focus-visible, .lp button:focus-visible, .lp input:focus-visible{outline:2px solid currentColor; outline-offset:3px}` (vagy a fő szín, ha elég a kontraszt).
- **Mozgás:** ha van, a `@media (prefers-reduced-motion: reduce)` alatt kapcsold ki.
- **Képernyőmagasság:** vh-alapú magasságot mindig korlátozz: `min-height:min(100vh, 900px)`. A képernyőkép magas ablakban készül, ahol a korlát nélküli `vh` óriási üres részt ad.

## A szöveg jelölései

A `szoveg.md` blokkjai (`## 1. Hero`, `## 2. ...`) a szakaszok. Bennük:

| Jelölés | Mi lesz belőle |
|---|---|
| `### Cím` | a szakasz címe (a hero-ban `<h1>`, máshol `<h2>`) |
| `**Felvezető:** ...` | rövid felvezető a cím fölött; csak ott van, ahol a szöveg adja |
| `**Gomb:** ...` | gomb, ami az űrlaphoz görget (`href="#jelentkezes"`); a felirata szó szerint ez |
| `**Űrlap:** Név, E-mail-cím` | a mezők, ebben a sorrendben |
| `**Jelölőnégyzet:** ...` | kötelező jelölőnégyzet az űrlap alján, a szövege szó szerint ez |
| `[KITÖLTENDŐ: ...]` | jól látható jelölés az oldalon (`<mark class="lp-kitoltendo">`), a márka színeiből, nem új színnel: `.lp .lp-kitoltendo{background:color-mix(in srgb,var(--lp-szin-fo) 15%,white);outline:1px dashed var(--lp-szin-fo);color:inherit}` (design-rendszernél a `--ds-` megfelelőkkel). Feltöltés előtt ki kell tölteni; az átadásban sorold fel |
| `Kimarad: ...` | ez a blokk nem kerül az oldalra |
| `(logó)` egy tétel végén | ide a szervezet logója kell, ha megvan (`forrasok/`, `forrasok/kepek/`); ha nincs, a név szövegként áll, a „(logó)” jelölés nélkül |
| Markdown-lista | lista vagy a választott kompozíció tételei |

**Súly és kiemelés:** a szöveg nem változik, de a súlya igen. A blokk kulcsmondata kaphat bevezető méretet (a törzsszövegnél érezhetően nagyobbat); a hosszú, kiegészítő rész keskeny oszlopba, két hasábba vagy `<details>` lenyílóba kerülhet. Egy valódi számot vagy mondatot nagyban, másodszor is megjeleníthetsz kiemelésként (kihúzott idézet, nagy szám): ilyenkor a kiemelt másolat kapjon `aria-hidden="true"`-t, hogy a felolvasó ne mondja el kétszer. Rövid díszítő címke vagy ábrafelirat (például „60–90 perc” egy képen, egy idővonal szakaszainak neve) csak a szövegben szereplő szavakból és számokból állhat, `aria-hidden`, és az átadásban sorold fel.

A szakaszok `##` címkéi (például „Problémák és következményeik”) belső nevek, nem kerülnek az oldalra.

## Ikonok

Az ikonok egy saját, egységes készletből jönnek, ami az oldal designjához és a téma világához illik: generált ikonok képként (`<img class="lp-ikon" src="kepek/ikonok/<nev>.svg" width="48" height="48" alt="">`), vagy rajzolt, beágyazott SVG-k (`<svg class="lp-ikon" ...>`); a részletek az `ikonok.md`-ben. A rajzolt SVG színe a környezet szövegszíne (`currentColor`), ezért CSS-ből színezed: `.lp .elonyok .lp-ikon{color:var(--lp-szin-fo)}`; a generált ikon színei a fájlban vannak. Emoji ikon helyett nem lehet. Az ikon díszítés (`aria-hidden="true"`), ezért a jelentése mindig a mellette álló szövegben legyen.

## Fejléc és lábléc

Egy oldal, egy cél: menü nincs. Fent csak a logó (`kepek/logo.svg`; ha nincs logó, szöveges logó: a vállalkozás neve a címsorbetűvel). Sötét háttérre fehér logó kell: ha nincs, és a logó SVG, készíts egy másolatot (`kepek/logo-feher.svg`), amiben minden szín fehér; ha nem SVG, sötét háttéren a név álljon szövegként, lent csak a vállalkozás neve, az adatkezelési tájékoztató linkje és az év. Ha a tájékoztató linkje nincs meg, `[KITÖLTENDŐ]` jelölés kerül a helyére.

## Képek

- A változat mappájában `kepek/`: ide másold a logó fájljait (`logo.svg`, `logo-feher.svg`, `logo-sotet.svg`, `favicon.svg`, ha vannak) és a felhasznált fotókat (rövid, ékezet nélküli fájlnévvel). Az oldal relatív úttal hivatkozik rájuk (`kepek/portre.jpg`).
- Minden `<img>`-nek van `alt`, `width` és `height` attribútuma; a hero alatti képek `loading="lazy"`.
- Képoptimalizálás nem kell. Ha egy fotó a fájl adatai (EXIF) szerint el van forgatva, a `kepek/`-be helyes állású másolat kerüljön; az eredetihez ne nyúlj.
- **Megosztási kép (`og.jpg`):** ha van fotó, vágj ki belőle egy 1200×630-as képet (a portréból vagy a legjellemzőbb képből); ha nincs fotó, hagyd el az `og:image` sort.
- **Ha nincs fotó:** vagy kép nélkül építed a blokkot (ha így is erős), vagy a kép helye megtervezett helyőrző: a paletta színeiből kevert felület, a kép arányában, benne egy rövid, halvány leírással, mi kerül oda („Fotó: rólad munka közben, álló kép”). Szürke dobozt ne tegyél. Generált embert vagy kitalált terméket ne tegyél be.
- **Stockfotó:** magadtól ne tölts le. Ha a felhasználó kéri, javasolj képhelyenként egy-két keresőszót egy ingyenes stockoldalhoz (például Unsplash, Pexels); a választott képet ő tölti le a `forrasok/kepek/` mappába, és utána beépíted.

## Az űrlap

Saját HTML-űrlap a `**Űrlap:**` mezőivel és a `**Jelölőnégyzet:**` szövegével, egyszer az oldalon (a CTA szakaszban, `id="jelentkezes"`). Minden gomb ide görget.

```html
<form class="lp-urlap" id="jelentkezes-urlap" novalidate>
  <label for="lp-nev">Név</label>
  <input id="lp-nev" name="nev" type="text" autocomplete="name" required>
  <label for="lp-email">E-mail-cím</label>
  <input id="lp-email" name="email" type="email" autocomplete="email" required>
  <label class="lp-jelolo"><input type="checkbox" name="adatkezeles" required> Elolvastam és elfogadom az <a href="...">adatkezelési tájékoztatót</a>.</label>
  <button type="submit">Jelentkezem</button>
  <!-- AZ ŰRLAP MÉG NEM KÜLD ADATOT: az e-mailhez űrlapkezelő szolgáltatás vagy SMTP-beállítás kell. -->
</form>
<script>
document.getElementById('jelentkezes-urlap').addEventListener('submit', function (e) {
  e.preventDefault();
  if (!this.reportValidity()) return;
  window.location.href = 'koszi.html';
});
</script>
```

- A mezőtípusok a tartalomhoz illenek: `type="email"`, `type="tel"` (`autocomplete="tel"`), `autocomplete="name"`.
- Az adatok soha nem kerülnek az URL-be (ezért nem `method="get"`).
- A hibás mezőt egy jól látható hibaszín jelzi (design-rendszernél a `--ds-hiba`), és a böngésző saját üzenete mondja meg, mi a baj.
- A szkript az `.lp` burkolón belül, az űrlap után áll, hogy a WordPress-változatba is átkerüljön.

## A köszönőoldal (`koszi.html`)

Ugyanaz a váz, ugyanaz a `<style>` (ami nem kell belőle, kihagyható), ugyanaz a logó fent és a lábléc lent. Rövid: egy cím, két-három mondat arról, mi történik most, és egy link vissza a főoldalra (`index.html`). A `<head>`-be: `<meta name="robots" content="noindex">`.
