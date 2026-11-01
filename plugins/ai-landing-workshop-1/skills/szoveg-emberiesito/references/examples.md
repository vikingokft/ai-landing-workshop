# Emberiesítő példák

Ezek a példák a kimenet alakját kalibrálják. Referencia-anyag, nem forgatókönyv.

## Teljes, AI-nehéz példa

**Bemenet**

> Nagyszerű kérdés! Íme egy összefoglaló a témáról. Remélem, segítettem!
>
> Az AI-támogatott programozás a nagy nyelvi modellek átalakító potenciáljának maradandó bizonyítéka, és fordulópontot jelent a szoftverfejlesztés evolúciójában. A mai rohanó technológiai környezetben ezek a forradalmi eszközök — a kutatás és a gyakorlat metszéspontjában megbúvva — újraformálják, ahogyan a fejlesztők ötletelnek, iterálnak és szállítanak, rávilágítva kulcsfontosságú szerepükre a modern munkafolyamatokban.
>
> A lényeg világos: a folyamatok gyorsítása, az együttműködés fokozása és az összhang megteremtése. Nem csupán az automatikus kiegészítésről van szó, hanem a kreativitás felszabadításáról, biztosítva, hogy a szervezetek agilisak maradhassanak, miközben zökkenőmentes, intuitív és erőteljes élményt nyújtanak.
>
> Összességében a jövő fényes. Izgalmas idők várnak ránk ezen az úton. Szólj, ha bármelyik részt kifejtsem!

**Jó záró átírás**

> Az AI-programozó asszisztensek megváltoztatják, ahogyan a fejlesztők dolgoznak: gyorsabban jutnak el az ötlettől a kész kódig, és könnyebben dolgoznak együtt.
>
> Többet tudnak az automatikus kiegészítésnél. Ha a gépies részt átveszik, több idő marad a kreatív munkára, és a csapat rugalmasabb marad.

**Miért működik**

- Kiszedte a chatbot-keretet, a hype-ot, az üres zárást, a gondolatjeleket, a tölteléket és a hamis mélységet.
- Megtartotta a bemenet állításait (gyorsabb munka, jobb együttműködés, több tér a kreatív munkának, rugalmasabb csapat), és nem tett hozzá újat.
- Nem talált ki kutatást, embert, statisztikát, példát vagy korlátot. Ha a szöveg így vékony, az a bemenet hibája: jelezd, ne töltsd fel kitalált tartalommal.

**Amit konkrétan kiszedett:** `Nagyszerű kérdés!` (§22), `Íme egy` (§28), `Remélem, segítettem` (§20), `maradandó bizonyítéka` és `fordulópontot jelent` (§1), `a mai rohanó világban` és `forradalmi` (§7), `megbúvva` (§4), `rávilágítva` (§3), `kulcsfontosságú` (§7), `A lényeg világos` (§27), `gyorsítása, fokozása és megteremtése` (§10, mechanikus hármas), `Nem csupán X, hanem Y` (§9), `zökkenőmentes, intuitív és erőteljes` (§10 + §7), `Összességében a jövő fényes` (§25), `Szólj, ha` (§20).

## Az ítélet-lista alakja

```text
§22 „Nagyszerű kérdés!" -> ÁTÍR (talpnyalás, nem része a tartalomnak)
§1 „maradandó bizonyítéka" -> ÁTÍR (jelentőséget fúj fel, értelem nélkül)
§9 „Nem csupán X, hanem Y" -> ÁTÍR (sablon-szembeállítás, általános állítás)
§14 „eszközök — a kutatás" -> ÁTÍR (a záró szövegben nincs mondat-közi gondolatjel)
§27 „A lényeg világos" -> ÁTÍR (tekintély-fordulat, ami lassítja a gondolatot)
§3 „rávilágítva" -> ÁTÍR (lezáró igenév, hamis mélység)
```

## A fájl-munka jelentésének alakja

```text
Beállítás: cikk-részlet, márkahang az agy/ceg/markahang.md szerint, normál tisztítás, nincs testvér-készlet

Ítéletek:
- §7 „zökkenőmentes" -> ÁTÍR (AI-szókincs általános állításban)
- §19 angol idézőjel -> ÁTÍR (a “ nyitó angol; magyarban „ vagy egyszerű ")
- §9 „Nem X, hanem Y" -> MARAD (egyetlen előfordulás, viszi a gondolatot, a márkahang egyet engedélyez)
- §13 „elvégzésre kerül" -> ÁTÍR (szenvedő szerkezet, van cselekvő)

Ellenőrzés:
- scanner újrafuttatás: nincs kemény bukás
- ellenőrzőlista újrajárás: nincs feloldatlan jelentés-alapú jel
- tények, hivatkozások, fejlécek megőrizve

Végleges:
...
```

## Amit NEM szabad átírni — példa

**Bemenet** (valódi emberi próza, egyetlen jellel)

> Dórit 2017-ben ismertem meg egy vásárban. Akkor még papírzacskókat hajtogatott a pultnál, és azt mondta, ebből sose lesz megélhetés. Kulcsfontosságú volt az a beszélgetés: utána indította el a webshopot.

**Helyes ítélet**

```text
§7 „Kulcsfontosságú" -> MARAD (egyetlen jel egy konkrét, dátumozott, személyes bekezdésben; a szöveg nem sablonos)
```

Ha ezt átírnád, simább lenne, de nem jobb. **A csoportos megjelenés a jel, nem az egyedülálló szó.**
