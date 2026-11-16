---
name: landing-elesites-skill
description: "Kész landing oldalak átadási csomagjainak elkészítése hagyományos FTP-tárhelyhez és WordPresshez. Statikus feltölthető fájlokat, Elementor HTML widgethez való kódot, WordPress Egyéni HTML blokkhoz való változatot és médiatárba behúzható, egyedileg elnevezett képmappát ad. A médiatár tényleges képcímeit év/hónap-mappák feltételezése nélkül kezeli. Meglévő design csomagolására és élesítés előkészítésére használd; nem új oldal tervezésére, és nem automatikus publikálásra."
---

# Landing élesítés

A kész, elfogadott landingből készíts használható átadási csomagokat. Tartsd meg a designt, a szöveget, a képeket, a reszponzivitást, az animációkat és az interakciókat; ne indíts új referenciaelemzést vagy áttervezést. A `landing-design-skill` skill futtatása nem előfeltétel, bármely kész landingből dolgozhatsz.

## 1. Forrás és célkörnyezet

Azonosítsd a végleges oldal forrását, a build módját, az összes hivatkozott assetet és a funkcionális függőségeket. A szerkeszthető forrást őrizd meg, az exportot külön mappába készítsd. A meglévő exportok frissíthetők, a felhasználó egyéb fájljait ne írd felül.

Csak a ténylegesen hiányzó adatokat kérdezd meg, együtt: melyik kész oldal a forrás; a WordPress-verzió/HTML-modul, ha a beillesztést befolyásolja; a publikus WordPress-cím, ha valós kompatibilitás-ellenőrzést vagy végleges képcímekkel generálást kérnek. A még nem ismert tárhely vagy WordPress-cím ne akadályozza a hordozható csomagok elkészítését, de a nem tesztelt kompatibilitást nevezd meg. A képekhez alapértelmezetten médiatári tömeges feltöltést használj, ne FTP-s képmappát és ne a teljes képkészlet base64-be ágyazását.

A részletekhez olvasd a [references/delivery.md](references/delivery.md) útmutatót. WordPress-exportnál kövesd a [references/wordpress-style-isolation.md](references/wordpress-style-isolation.md) szín- és stílusizolálási, valamint ütközéstesztelési útmutatóját. A médiatár-kezeléshez olvasd a [references/wordpress-media.md](references/wordpress-media.md) leírást, és használd a mellékelt képkeresőt a képcímek kitalálása helyett.

## 2. Két átadási mappa

```text
output/
  ftp/
    feltoltheto/             # index.html + minden futtatáshoz szükséges fájl
    TELEPITES.md
  wordpress/
    media-upload/            # csak a médiatárba behúzandó, elnevezett képek
    media-manifest.json      # fájlazonosítók és az eredeti képek megfeleltetése
    elementor/
      beillesztheto.html     # HTML + style + script egy widgethez
    gutenberg/
      html.html             # Egyéni HTML blokk HTML-mezője
      style.css             # a blokk CSS-mezője, ha támogatott
      script.js             # a blokk JavaScript-mezője, ha támogatott
    elonezet.html
    BEILLESZTES.md
```

- **FTP:** közvetlenül feltölthető statikus build, almappában is helyes assethivatkozásokkal. A látogatói működéshez ne kelljen Node.js vagy fejlesztői szerver. Ha szerveroldali képesség szükséges, azt külön jelezd; ne állítsd, hogy statikusan működik.
- **WordPress:** a közös designból adj külön Elementor- és Gutenberg-beillesztést, a fenti fájlokkal. A Gutenberg CSS/JS-mezők jogosultság- és verziófüggők; ha nem állnak rendelkezésre, nevezd meg a szükséges, támogatott kódbeillesztési lehetőséget. Ne állítsd, hogy egy szűrt HTML blokk önmagában minden kódot futtat. Az útmutatóban a felhasználónak a két WordPress-változat közül egyet kell választania, nem mindkettőt ugyanabba az oldalba illesztenie.
- A WordPress CSS-t és JS-t saját gyökérelemhez korlátozd, hogy a téma többi részét ne alakítsa át. Az önálló oldal `html`, `body` és `:root` szabályait a landing gyökerére fordítsd le. A címsorok, hivatkozások, gombok és űrlapelemek fontos színeit közvetlenül az elemekre célzó, megfelelő specifikusságú saját gyökérrel kezdődő szabályok állítsák be; a befoglaló színének öröklése nem elég. Őrizd meg a szakaszonkénti eltéréseket, kiemeléseket és interakciós állapotokat. Ne használj általános `!important` szabályt vagy a teljes WordPress-oldalt érintő resetet. Mindkét WordPress-változat ugyanazt a védett megjelenést és működést adja.
- A `media-upload/` fájljai kapjanak csomagazonosítót, tartalmi hash-t és értelmes szerepnevet. A felhasználó változatlan fájlnevekkel egyben tölthesse fel őket. A kód a WordPress által közölt valódi `source_url` értékeket használja, ne feltételezett `/uploads/ÉV/HÓ/` útvonalat. A részletek a médiatár-útmutatóban vannak.
- A HTML-hez tartozó fontokat és egyéb, médiatárba általában nem tölthető fájlokat külön kezeld. Ne legyenek a képek közé keverve, és ne maradjanak helyi fájlhivatkozások a bemásolandó kódban.

## 3. Ellenőrzés és átadás

Csomagolás előtt nézd át a kész oldalon az **élesítés előtti alapokat** (a 2026-11-es workshop 20 beküldött oldalán ezek hiányoztak a legtöbbször): `<title>`, meta leírás, 1200×630-as megosztási kép (`og:image`; nélküle Facebookon és Messengerben üres doboz jelenik meg), favicon; képenként legfeljebb kb. 300 kB (WebP vagy JPEG, a megjelenési szélesség kétszeresére méretezve; a generált képek 2–5 MB-os PNG-k, ezeket mindig alakítsd át); egyetlen üres vagy `#` link se maradjon; a látható szövegben ne maradjon a készítőnek szóló mondat („élesítés előtt…”, „pótolandó”, `[KITÖLTENDŐ]`), ezek az átadásba kerülnek; magyar tipográfia („…”, mondat közben nincs gondolatjel). Ami hiányzik, azt pótold a csomagban (megosztási kép és favicon a meglévő képekből vagy a logóból), vagy nevezd meg az átadásban. Élesítés után kattints végig minden gombon, és ellenőrizd, hogy az oldal https-en fut.

A végleges exportot vizsgáld: az FTP-csomagot statikus kiszolgálással és almappás útvonalon; a tényleges Elementor- és Gutenberg-részletet külön, aktív ütköző sablon- és Elementor-jellegű CSS mellett, ugyanazon asztali méretben. Ehhez használd a [scripts/build-wp-style-preview.py](scripts/build-wp-style-preview.py) keretét és a stílusizolálási útmutató ellenőrzését. A keret a landing CSS-e után is közvetlen sötét címsorszínt ad. Böngészőben hasonlítsd a megjelenést és a fontos számított színeket az eredeti designhoz, a külső kontrollok stílusait pedig a landing nélküli alaphoz; vizsgáld a hover/fókusz és a használt űrlapállapotokat is. Ellenőrizd a képeket, fontokat, navigációt, GYIK-ot és a választott animációkat. Csomagolási hiba esetén a kapcsolódó exportokat együtt frissítsd, a designfolyamat újranyitása nélkül.

A képkeresőhöz [scripts/wp-media-resolver.js](scripts/wp-media-resolver.js) tartozik. Ha módosítod, futtasd a tesztjét:

```sh
node <skill-könyvtár>/scripts/test-wp-media-resolver.js
```

A teszt szimulált REST-válaszokat használ, nem igazol valós WordPress-kompatibilitást. Valódi WordPress-hozzáférés nélkül a helyi előnézetet ellenőrzöttnek, az éles mentést és médiatár-hozzáférést nem ellenőrzöttnek nevezd. A hiányzó képet, tiltott REST API-t vagy hiányzó űrlap-végpontot egyértelműen jelezd; ne legyen végtelen újrapróbálkozás, hibát elfedő sikerüzenet vagy önkényesen választott másik kép.

Az útmutatók magyarul, a konkrét csomagra szabva mondják meg, melyik mappát kell feltölteni, melyik fájlt hová kell bemásolni, és milyen beállítás maradt nyitva. Linkeld az FTP-mappát, a médiatári képmappát és a két WordPress-beillesztést. A csomagkészítés önmagában nem felhatalmazás éles feltöltésre, médiatári módosításra, beállításváltoztatásra vagy publikálásra.
