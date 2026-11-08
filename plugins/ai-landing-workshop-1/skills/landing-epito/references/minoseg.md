# Minőség

Három rész: az alsó határ, ami mindig kötelező; a rövid lista arról, mi árulja el, hogy egy oldalt AI generált; és az öt kérdés, amivel a képernyőképeket nézed.

## Az alsó határ (mindig)

- **Olvashatóság:** a törzsszöveg legalább 17 px, a sora legfeljebb kb. 70 karakter (`max-width: 65ch` körül); 16 px alatti szöveg csak apró címke és jogi szöveg lehet. A kontraszt legalább 4,5:1, a nagy címeké legalább 3:1.
- **Hierarchia:** egy H1 (a hero címe), alatta H2 a szakaszcímeknek, H3 a tételeknek. A cím fölött több hely legyen, mint alatta.
- **Mobil:** 390 px-en se legyen vízszintes görgetés; a gombok legalább 44 px magasak.
- **Fókusz és mozgás:** minden kattintható elemnek látható fókusza van (`:focus-visible`); a mozgás a `prefers-reduced-motion` mellett megáll.
- **Képek:** `alt`, `width` és `height` minden képen.
- **Igazság:** szám, vélemény, logó, díj, határidő csak a `szoveg.md`-ből jöhet.

## Ami az AI-t elárulja

Ha valamelyik szerepel, legyen rá erre az oldalra szóló okod.

- Minden szakasz ugyanaz a forma (például mindenhol középre zárt cím és három egyforma kártya, vagy mindenhol bal oldalt cím, jobb oldalt bekezdés).
- Kis, ritkított, nagybetűs felvezető minden cím fölött; egyetlen kiemelt szó a címben.
- Lila-kék színátmenet, színátmenetes szöveg, üvegeffekt, neonos ragyogás, emoji ikonként.
- **Üres hasáb:** a cím bal fent, a szöveg jobbra tolva, alatta a bal oldal üres. Ha két hasáb, mindkettő dolgozzon, különben legyen egy hasáb.
- **Árva elem:** egy rácsban az utolsó elem egyedül, más szélességben lóg. A rács igazodjon az elemek számához.
- **Kettévágott mondat:** egy bekezdés első fél mondata álcímként, a folytatása alatta.
- **01, 02, 03 számozás**, amikor a tartalom nem sorrend.
- A teljesen fehér, apró betűs, színfelület nélküli „minimalista” oldal, ha az inspiráció nem ilyen.
- Általános ikonok (pipa, csillag, villám) mindenhol, amikor a téma világából lehetne konkrétabb; vagy egymáshoz nem illő ikonok (más vonalvastagság, más stílus).

## Öt kérdés a képernyőképekhez

Úgy nézd, mintha egy másik csapat munkája lenne. Mindegyikre igen vagy nem, és ha nem, mi a javítás:

1. **Az első képernyő** (asztali és mobil): van rajta valami, ami megállítja a szemet: kép, nagy betű, színfelület?
2. **A forrás:** ha a meglévő oldalt vagy egy inspirációt követ, ráismerni rá? Ha nincs ilyen, van az oldalnak saját ötlete és motívuma, vagy bármelyik hasonló vállalkozásé lehetne?
3. **A ritmus:** ha a teljes oldalt bélyeg méretűre kicsinyíted, látszanak a váltakozó színek, méretek, képek, vagy egyforma csíkok sora?
4. **A hosszú szakaszok:** van, ami vezeti a szemet (vezetőmondat, kiemelés, kép, hasábok), vagy egyforma bekezdések falai?
5. **A kivitel:** a térközök, igazítások, betűméretek következetesek, mobilon is? Van levágott, kilógó, túl apró elem, üres hasáb, árva elem?

Ha kettőre vagy többre nem a válasz, javíts, aztán új képernyőkép. Pontszámot ne adj magadnak.
