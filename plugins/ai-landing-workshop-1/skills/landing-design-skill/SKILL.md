---
name: landing-design-skill
description: "Landing oldalak és bemutatkozó weboldalak készítése vagy áttervezése a projektmappa anyagai és a felhasználó vizuális referenciái alapján. Felméri a fájlokat, bekéri a hiányzó inspirációkat, asztali böngészőnézetben elemzi a referenciák vizuális rendszerét, majd megvalósítja és ellenőrzi az oldalt. Önálló referenciaelemzéshez is használható; nem általános alkalmazás- vagy dashboard-tervezési folyamat."
---

# Landing design

A projekt valós tartalmából és a ténylegesen megtekintett referenciákból készíts karakteres, használható oldalt. A munkamenet: felmérés → referenciaelemzés → kivitelezés → célzott ellenőrzés. Ne köss hozzá kötelező látványtervkört, stílusversenyt, keretrendszert, segédprogramot vagy másik design skillt. Ha a kérés csak elemzés, az elemzésnél állj meg.

## 1. Projektfelmérés és a hiányzó bemenetek

- Nézd át a releváns mappaszerkezetet, projektutasításokat, meglévő belépési pontokat és technikai alapokat. Ne olvasd végig a generált fájlokat, függőségeket vagy az ügyhöz nem tartozó bizalmas állományokat.
- Keresd meg a szövegeket, logókat, arculati anyagokat, képeket és betűfájlokat. A fontos képeket és a logót vizuálisan is nézd meg; a fájlnév nem bizonyítja, mire alkalmas egy kép. Mérd fel, mi használható herohoz, portréhoz, háttérhez vagy kisebb tartalmi képhez.
- Állapítsd meg a célközönséget, ajánlatot és fő cselekvést a briefből és fájlokból. Csak a munkát érdemben befolyásoló hiányokra kérdezz rá, az összetartozó kérdéseket együtt feltéve. Ne kérdezd újra azt, ami már meg van adva.
- Ha nincsenek megadott vizuális referenciák, kérj lehetőleg 1–3 URL-t vagy képernyőképet, és opcionálisan azt, mi tetszik bennük. Várd meg a választ, mielőtt referenciaalapúnak nevezett designt készítesz. Közben folytathatod a fájlok felmérését. Ha a felhasználó referencia nélkül kéri a folytatást, dolgozz a projekt arculatából, és nevezd meg ezt az alapot.
- Tartsd meg a meglévő technikai alapot. Üres projektben válassz a feladathoz arányos, egyszerű megoldást; csak akkor kérdezz technológiáról, ha a választásnak érdemi következménye van.

## 2. A referenciák tényleges megtekintése

A referenciaelemzéshez az **asztali nézet elegendő**. Nem kell minden inspirációt mobilon is megvizsgálni.

- Nyisd meg a megadott oldalt böngészőben. Nézd meg a hajtás feletti részt, görgess végig a fő szakaszokon és a láblécig; a különleges megoldásokat közelebbről is vizsgáld meg. Várd meg az érdemi betöltést, és különítsd el a betöltési hibát vagy takarást a tényleges designtól. Ne csak a heróból következtess az egész oldalra.
- A vizuális megfigyelést kiegészítheted DOM- és számítottstílus-adatokkal, például betűcsaláddal, mérettel vagy színnel. A puszta HTML-szöveg nem igazolja az oldal megjelenését. A képernyőkép a kompozíciót, a DOM az ellenőrizhető részleteket támasztja alá.
- Sikertelen megnyitás után próbálj egy ésszerű alternatívát, például másik elérhető böngészőeszközt vagy a kapott képernyőképet. Ne tölts időt ismétlődő próbálkozásokkal.
- Ha a referencia nem tekinthető meg, **azonnal jelezd, melyik URL nem elérhető és mit nem tudtál ellenőrizni**. Kérj képernyőképet vagy másik referenciát. A megtekinthető anyagokkal haladj tovább; ha semmi nem látható, a vizuális irányhoz várd meg a pótlást vagy a referencia nélküli folytatásra vonatkozó választ.
- Részleges hozzáférésnél pontosíts: például csak hero látható, képek hiányoznak, belépés szükséges. Ne nevezd teljes elemzésnek. Képernyőképből ne állíts biztos betűnevet, animációt vagy interakciót.

## 3. Részletes referenciaelemzés

Minden elérhető referenciánál az alábbi vizuális rendszert keresd. Az elemzés legyen konkrét: a „modern, prémium, letisztult” önmagában nem ad kivitelezhető irányt. A domináns jegyeket és a szándékos hiányokat is rögzítsd. Nem szükséges minden értéket pixelpontosan lemérni.

| Terület | Mit vizsgálj? |
| --- | --- |
| Betűk és címsorok | Serif/sans/display jelleg, kontraszt és karakter, súlyok, kurzív, betűköz, sorköz, kis- és nagybetűk; H1/H2/törzs méretaránya, címsorok sortörése és sorhossza. Pontos betűnév csak ellenőrzött adatból. |
| Elrendezés és térköz | Tartalomszélesség, külső margók, oszloparányok, igazítások, üres tér, elemek közötti és szakaszok közötti távolság; szimmetria vagy tudatos aszimmetria. |
| Képek | Fotó vagy illusztráció, képi hangulat és tónus, képarány, kivágás, fókuszpont, méret és elhelyezés; téglalap, íves forma, kivágott alak, átfedés, kép és szöveg kapcsolata. |
| Színek és hátterek | Domináns, másodlagos és akcentusszínek szerepe; világos/sötét felületek váltása; színátmenetek iránya és erőssége; patternek, textúrák és díszítőelemek jelenléte, sűrűsége, feladata. |
| Gombok és navigáció | Elsődleges/másodlagos hierarchia, kitöltés vagy kontúr, méret, belső térköz, formák, felirat, nyíl/ikon, elhelyezés; látható hover és fókusz, fejléc felépítése. |
| Dobozok és részletek | Kártyák szerepe és gyakorisága, nyitott vagy dobozos elrendezés, szegély, elválasztó, árnyék iránya/lágysága, sarokkerekítés és ezek következetessége. |
| Ikonok | Vannak-e tartalmi/dekoratív ikonok; vonalas, tömör, duotone vagy illusztratív stílus; vonalvastagság, végződés, szín, méret, részletesség, háttérforma és gyakoriság. |
| Ritmus és figyelemvezetés | Mi az elsődleges fókusz; szöveges és képes, sűrű és levegős, nyitott és dobozos, világos és sötét szakaszok váltása; CTA-k helye, szakaszátmenetek és az oldalra jellemző emlékezetes megoldás. |
| Mozgás és működés | Csak ha látható: visszafogott vagy hangsúlyos animáció, sticky elemek, accordion, képi interakció. Válaszd külön a hasznos mintát a puszta díszítéstől. |

Az elemzés után foglald össze: **mit láttál → mit veszel át → az oldal melyik részén és hogyan alkalmazod → miből lesz felismerhető az eredményben**. Nevezd meg az irányadó referenciát, és azt, melyik további inspiráció ad csak egy részletet. Emelj ki általában 3–5 meghatározó, ténylegesen megvalósítandó vizuális megoldást, a tartalomhoz arányos számban: például a hero rétegzettségét, a háttérformák léptékét, a hangsúlyos színes felületeket vagy az ajánlat megkomponálását. A felsorolás a kivitelezést és a végső összevetést irányítsa; nem kell hozzá külön dokumentum, pontozás vagy új jóváhagyási kör.

## 4. Koherens irány és kivitelezés

- A felhasználó kifejezett döntései és kötöttségei az elsők. A referenciák vizuális bizonyítékot adnak, nem új terméktényeket. Az elemzés ne írja felül a megőrzésre kért arculatot vagy szöveget.
- **Őrizd meg az irányadó referencia vizuális intenzitását:** a kompozíció merészségét, a rétegzettséget, a tipográfiai léptéket, a színkontrasztot és a részletgazdagságot is fordítsd le a saját projektre. A kész oldal ezekben közelítse meg a referenciát; ne maradjon meg pusztán a színpaletta és a betűk jellege. Ne egyszerűsíts automatikusan egy látványos referenciát visszafogott változattá. Ha maga a referencia minimalista, ezt a karaktert tartsd meg. Az arculati kötöttségek és az olvashatóság továbbra is érvényesek.
- Több inspirációból egy összefüggő rendszert alkoss. Ne keverd automatikusan mindegyik betűjét, színét és gombját. Valódi ütközésnél kérdezd meg röviden, melyik tulajdonság fontosabb; egyébként válassz, indokold egy mondatban, és dolgozz tovább.
- Az irányt és a kiválasztott jellegzetességeket nevezd meg a kivitelezés előtt, az elemzés összegzéséhez kapcsolva. Ha nincs lényeges bizonytalanság, ne tegyél kötelező jóváhagyási kört a megvalósítás elé. Alapértelmezetten közvetlenül a működő oldalt készítsd; külön látványterv csak kérésre vagy valódi haszon esetén kell.
- A konkrét megoldásokat a saját tartalomra és képekre fordítsd le. Ne másolj márkanevet, logót, szöveget vagy nem átadott képet a referenciáról. Ne erőltesd annak kompozícióját egy alkalmatlan képre.
- Szöveghűségi kérésnél a publikálható szöveget szó szerint őrizd meg; a tipográfiai tördelés nem szövegátírás. A szerkesztői jelöléseket különítsd el, a kétértelmű kihagyásokról egyeztess. Ne találj ki véleményeket, eredményeket, árakat vagy működő integrációkat.

### A karakter az egész oldalon maradjon meg

A vizuális kidolgozottság terjedjen túl a herón. A fő tartalmi szakaszoknak — például az ajánlatnak, áraknak, folyamatnak, bemutatkozásnak és jelentkezésnek — adj a szerepükhöz illő kompozíciót, a meglévő tartalomból dolgozva. A hangsúlyos és nyugodt, képes és szöveges, sűrűbb és levegősebb részek váltakozása alkosson tudatos ritmust. Ne váljon minden szakasz ugyanazzá a címsor + szöveg + elválasztó vagy azonos oszlopos felsorolás mintává. Nem kell minden szakasznak új látványfogás: a kiválasztott formai nyelv visszatérése kapcsolja össze az eltérő kompozíciókat. Ezt a meglévő kivitelezési menetben oldd meg, külön szakaszonkénti tervezési körök nélkül.

**A hosszú szöveges részek is tervezési feladatok.** A célcsoportok, feltételek, kizárások és tájékoztató blokkok megjelenítését a tartalom jelentése és terjedelme alapján alakítsd ki. Használj felismerhető vizuális csoportokat, hangsúlyos címkezelést, megfelelő belső térközöket és az oldalhoz illő felületkezelést; ikonokat csak a referencia szerinti ikonhasználattal összhangban. Az eltérő hosszúságú tartalmakat ne kényszerítsd egyforma kártyákba vagy oszlopokba. A hosszabb rész kapjon több helyet, vagy önálló sorokat. A tömörséget a kompozícióval oldd, ne a szöveg zsugorításával vagy a megőrzendő szöveg rövidítésével. A fontos egészségügyi és részvételi feltételek maradjanak közvetlenül láthatók. Egy háttérszín és néhány elválasztó önmagában nem elegendő, ha a szakasz továbbra is töménynek és kidolgozatlannak hat. A tudatosan nyugodt pihenőszakasz maradhat egyszerű; ne adj minden bekezdéshez automatikusan dobozt vagy dekorációt.

### Tartalmi ikonok és dekoráció

**Ha az irányadó inspiráció érdemben használ tartalmi ikonokat**, készíts a projekthez **egyedi, AI által tervezett ikonkészletet**, a megfigyelt stílus nyelvén. Az átvett tulajdonság a vonalvezetés, vizuális súly, részletesség és színkezelés legyen, ne a referenciaikonok másolata. Az ikonok egységes méretráccsal, optikai mérettel, vonalvastagsággal és sarokkezeléssel készüljenek.

**Az egyszerű ikonokat tartalmi jelölésként használd:** felsorolások, előnylisták vagy folyamatlépések mellett, az adott pont jelentéséhez kapcsolódva. Ne nagyítsd fel és ne helyezd el őket önálló szakaszdíszként, címsorok fölött vagy üres helyek kitöltésére. Ha nincs egyértelmű kapcsolat a tartalommal, hagyd el az ikont; ne oszd szét ugyanazt a néhány motívumot pusztán változatosság kedvéért.

Egyszerű vonalas vagy geometrikus ikonokat saját SVG-ként rajzolj: ez éles és egységesen alakítható. Illusztratív vagy texturált ikonokhoz használj elérhető képgeneráló eszközt, ha az adott stílust ez szolgálja jobban. Az ehhez szükséges eszköz hiányát jelezd; ne állítsd egy letöltött készletről, hogy egyedi generálás. Ne használj emojit ikonpótlékként, és ne keverj eltérő ikonkészleteket.

**A dekoratív ikonok mellőzése mellett őrizd meg az irányadó referencia vizuális gazdagságát.** Már a tervezéskor határozd meg, mely szakaszok kapnak hangsúlyos vizuális kompozíciót, és milyen eszközök adják azok karakterét.

Használd a referenciában megfigyelt rétegzett képhasználatot, háttérformákat, patterneket, illusztrációkat, színátmeneteket vagy tipográfiai megoldásokat a saját tartalomhoz igazítva. Ne redukáld a referencia változatos megoldásait ismétlődő halvány háttérívekre és lekerekített dobozokra.

Nem kell minden szakaszt dekorálni. A hangsúlyos és nyugodt részek tudatos váltakozása adja az oldal ritmusát; az üres tér is ennek része legyen.

**Ha az irányadó inspiráció nem használ tartalmi ikonokat, ne hozz létre tartalmi ikonkészletet.** Ne alakíts minden bekezdést ikonos kártyává. Egy menüjel, navigációs nyíl vagy accordion-jel önmagában nem indokol ikonkészletet; ezek külön funkcionális elemek, a működéshez szükséges jelzések megmaradhatnak. A nem betöltött oldal alapján nem jelenthető ki, hogy nincs ikonhasználat. A meglévő záró ellenőrzésben vizsgáld az ikonok tartalmi kapcsolatát is, és az önálló szakaszdíszként használt egyszerű ikonokat távolítsd el vagy váltsd a referenciához illő dekorációra.

### Animációk és mikrointerakciók

**A mozgást is kezeld a vizuális rendszer részeként.** A referenciákban ténylegesen megfigyelt animációk karakterét és intenzitását ültesd át a saját oldalra. Ha a referencia mozgása nem vizsgálható, ezt ne állítsd megfigyelt tulajdonságnak; a briefhez illő, visszafogott mikrointerakciókat ettől még tervezhetsz.

A mozgás segítse a figyelemvezetést, érzékeltesse az elemek kapcsolatát, és adjon visszajelzést az interakciókra. Legyen összehangolt a sebessége és lefolyása. Használhatsz például összehangolt hero-belépést, finom gomb- és nyílreakciókat, enyhe képi reakciót rámutatáskor, folyamatos GYIK-nyitást vagy néhány kiemelt elem görgetéshez kapcsolódó megjelenését. Ezek lehetőségek, nem kötelező effektlista. Alapértelmezetten néhány gondosan kidolgozott mozdulatot válassz. Ne animálj automatikusan minden szakaszt ugyanazzal a belépőeffekttel, és ne használj folyamatos lebegést vagy erős parallaxot pusztán a látvány kedvéért.

A tartalom animáció nélkül is legyen elérhető. Tartsd tiszteletben a csökkentett mozgás beállítását; az animáció ne késleltesse az olvasást, ne okozzon elrendezésugrást, és ne rontsa a képkivágásokat. A meglévő asztali ellenőrzés során nézd meg a kiválasztott mozgásokat és interakciókat is; ehhez ne indíts külön animációtervezési vagy jóváhagyási kört.

## 5. Minőségi alapelvek és vizuális ellenőrzés

A vizuális intenzitást a brief és a referenciák határozzák meg. A következő minőségi elveket a választott irányhoz igazítva alkalmazd, külön tervezési folyamat vagy további skill futtatása nélkül.

- **Ne számozd dekorációként az oldal szakaszait:** ne jelenjen meg `01 /`, `02 /` vagy hasonló sorszám a bemutatkozás, ajánlat, előnyök és más tartalmi részek mellett. A forrásdokumentum szerkesztői szakaszszámait se emeld át látogatói designként. A referenciában látott dekoratív számozást is hagyd el. Számozás valódi sorrendet közvetítő tartalomnál maradhat, például egy jelentkezési folyamat lépéseinél, illetve a felhasználó kifejezett kérésére. A végső vizuális ellenőrzésben az indokolatlan szakaszszámokat távolítsd el.
- A hierarchia, térköz és olvashatóság legyen tudatos. Ne helyettesítsd a referencia karakterét egy általános hero + egyforma kártyák sablonnal. Ugyanakkor a referenciában indokolt kártyát, színátmenetet, árnyékot vagy lekerekítést ne tiltsd meg általános ízléselv alapján.
- Használj a megfigyelt jelleghez illő, valóban elérhető betűtípust; figyelj a magyar ékezetekre és a hosszú valós címsorokra. A fontos arányokat őrizd meg, ne merev pixelszámokat.
- A törzsszöveg kontrasztja legalább 4,5:1, a nagy szövegé legalább 3:1 legyen. A halvány referencia-szöveget javítsd olvashatóra a vizuális karakter megtartásával. Működjön a billentyűzetfókusz és a csökkentett mozgás beállítása.
- A szükséges hover, fókusz, letiltott, küldési, siker- és hibaállapotok legyenek valósak. Hiányzó űrlap-végpontnál ne jelezz sikeres küldést; jelezd a még szükséges beállítást, és használd a megadott kapcsolati alternatívát, ha van.
- Optimalizáld a nagy képeket, tartsd meg a fókuszpontot, adj méreteket és értelmes alternatív szöveget; a hero főképe ne késleltetett betöltésű legyen. A dekoráció ne lassítsa és ne takarja a tartalmat.
- A kész oldalt **asztali böngészőnézetben** nézd végig. Ugyanebben az ellenőrzésben vizsgáld a referenciához való illeszkedést, a teljes szakaszritmust, tördelést, képkivágásokat, kontrasztot, túlcsordulást, navigációt és a fő cselekvést. Vesd össze a megvalósítást az elemzésben vállalt jellegzetességekkel: **Mi adja a referencia karakterét, és ez felismerhető-e a kész oldalon? Mely részek lettek indokolatlanul visszafogottabbak? Hol ismétlődik ugyanaz az elrendezés eltérő tartalmak ellenére?** A színek és betűk hasonlósága önmagában nem elég, ha a kompozíció, rétegzettség vagy hangsúlyok elvesztek. Az indokolt eltéréseket a brief, a tartalom vagy az olvashatóság magyarázza, ne az automatikus egyszerűsítés. A feltárt eltéréseket és hibákat egy célzott javítási menetben kezeld, majd a módosított részeket ellenőrizd újra. Ha a vállalt karakter és a működési feltételek teljesülnek, zárd le a munkát; új bizonyíték nélkül ne indíts újabb általános designkeresést.
- **Elkészítés után minden felhasznált képet a kész oldal tényleges asztali elrendezésében is ellenőrizz**, ne csak az eredeti képfájlt vagy a CSS-t. Nézd meg, hogy a képarány, kivágás és fókuszpont megfelelő-e: nincs-e véletlenül levágott fej vagy arc, zavaróan csonkolt végtag, takart termék vagy elvesző fontos részlet; marad-e elegendő tér a téma körül. Vizsgáld a háttérképeket, maszkokat, lekerekítéseket, valamint a képre helyezett szövegek és dobozok takarását is. A tudatos közeli kivágást különítsd el a hibás vágástól; ne tiltsd meg a kompozíciót szolgáló részletképeket. Hibánál igazítsd képenként az `object-position` / `background-position`, képarány, méret vagy `object-fit` beállítást; ha ezekkel nem oldható meg, válassz alkalmasabb képet vagy elrendezést. A javított képet újra nézd meg a kész oldalon. Ha a reszponzív elrendezés lényegesen más kivágást használ és emiatt hibagyanú van, célzottan azt a nézetet is ellenőrizd.
- **Szakaszonként is ellenőrizd a kidolgozottságot a fenti böngészős bejárás során.** Néhány látványos rész ne fedje el egy hosszú szöveges blokk hiányosságait. Keresd a tömény felsorolásokat, az aránytalanul kitöltött oszlopokat és a csak háttérszínnel elkülönített, egyébként megtervezetlen részeket. Ezeknél javítsd a csoportosítást, hierarchiát és kompozíciót a meglévő javítási menetben, az oldal vizuális nyelvét és a szöveghűséget megtartva. Különböztesd meg a szándékos visszafogottságot a kidolgozatlanságtól; nem minden egyszerű rész hibás.
- A megvalósítás legyen reszponzív, de külön mobilos referenciaelemzés vagy vizuális tesztkör alapértelmezetten nem kötelező. Mobiltesztet kérésre vagy konkrét hibagyanúnál végezz.
- Ha a kész oldal böngészős ellenőrzése nem lehetséges, ezt mondd ki; kódellenőrzést ne nevezz vizuális ellenőrzésnek. A végén add át a működő előnézetet vagy fájlokat, és röviden nevezd meg a megmaradt korlátokat. Az elemzés kedvéért ne vezess be új telepítést, publikálást vagy külső szolgáltatást.
