# AI Landing Workshop: skillek

Ezek a skillek a Vikingo AI Landing Workshop eszközei. Segítségükkel az AI a saját vállalkozásod anyagaiból írja meg és építi fel a landing oldaladat, nem általános sablonszöveget ad.

## Egy plugin, minden skill

Minden skill az `ai-landing-workshop-1` pluginban van (verzió: 0.3.0). Ha az 1. alkalom után már telepítetted, csak frissítsd (lásd lent a **Frissítés** részt), és megkapod a 2. alkalom skilljeit is.

## Mi van benne

| Skill | Mire jó |
|---|---|
| `landing-ceges-agy` | Felépíti a céges agyat: egy `agy/` mappát a cégedről, az ajánlatodról, a célcsoportodról és a hangodról. Ezzel kezdj. |
| `landing-szovegiro` | A céges agyból megírja a landing oldal szövegét, blokkról blokkra. |
| `szoveg-emberiesito` | Kiszedi a szövegből az AI-írás árulkodó jeleit. A szövegíró magától lefuttatja, de bármilyen szövegen használhatod. |
| `design-rendszer` (nem kötelező) | Ha szeretnéd, rendszerbe foglalja a vizuális alapjaidat (logó, fő szín, betű, és ha hozol, egy-három tetsző oldal vagy kép): színek szerepekkel, betűk, méretek, gomb- és űrlapstílus. Ami hiányzik, arra javaslatot ad. Logót nem tervez, de a logódból színes, sötét és fehér változatot készít; ha nincs logód, a nevedből egyszerű szöveges logót. |
| `landing-epito` | A kész weboldalszövegből megépíti a landing oldalt HTML-ben. A kinézetet a meglévő weboldaladból (ha azt kéred, hogy kövesse) vagy egy tetsző oldalból, képernyőképből veszi, a logót, a színeket és a betűket a meglévő arculatodból; ha egyik sincs, maga tervez. Saját, a designhoz illő ikonkészletet készít: ha az eszközödben van képgenerálás (például Codexben), generálja, és vektoros SVG-vé alakítja (ehhez a `vtracer` kell: `python3 -m pip install vtracer`; nélküle PNG lesz); ha nincs, maga rajzolja. Képernyőképpel ellenőrzi, és elkészíti a feltölthető mappát meg a WordPress-változatot. |
| `landing-design-skill` | Megtervezi vagy áttervezi az oldalt a mappád anyagaiból és a tetsző oldalakból, képernyőképekből: elemzi a referenciák vizuális rendszerét, aztán megépíti és ellenőrzi. |
| `landing-elesites-skill` | A kész oldalt élesítésre csomagolja: feltölthető fájlok FTP-tárhelyhez, kód Elementor HTML widgethez és WordPress Egyéni HTML blokkhoz, és egy képmappa a médiatárhoz. |

A sorrend: **céges agy → szöveg → átnézés → építés → élesítés.** A design-rendszer külön, ha szeretnél ilyet.

## Telepítés

Válaszd azt, amelyik programot használod.

### Claude (claude.ai vagy a Claude asztali app)

1. Nyisd meg: **Customize → Plugins** (https://claude.ai/customize/plugins).
2. **Add → Add marketplace**, és írd be: `vikingokft/ai-landing-workshop`
3. Keresd meg az **AI Landing Workshop 1** plugint, és kattints az **Add** gombra.

Ha nem akarsz GitHubot használni: töltsd le a zip-fájlt (https://github.com/vikingokft/ai-landing-workshop/releases/latest/download/ai-landing-workshop-1.zip), és ugyanitt válaszd az **Add → Upload plugin** lehetőséget.

A plugin a fiókodhoz mentődik, így a Cowork és a Claude Code is megkapja. A skillek egy része kis ellenőrző programot futtat. A böngészős chatben ehhez a kódfuttatásnak (Code execution) bekapcsolva kell lennie a beállításokban.

### Claude Code (terminál)

```bash
claude plugin marketplace add vikingokft/ai-landing-workshop
claude plugin install ai-landing-workshop-1@vikingo-ai-landing
```

### Codex

```bash
codex plugin marketplace add vikingokft/ai-landing-workshop
codex plugin add ai-landing-workshop-1@vikingo-ai-landing
```

Az alkalmazásban ugyanezt a **Plugins** menüből is megteheted.

### Ha Macen a git hiányzik

A Codex és a Claude Code a gitet használja a plugin letöltéséhez. Ha a gépeden még soha nem volt fejlesztői eszköz, a macOS feldob egy ablakot („A git parancshoz a parancssori fejlesztői eszközök telepítése szükséges”), a piactér hozzáadása pedig hibával áll le (`xcode-select: note: No developer tools were found`).

1. Az ablakban kattints a **Telepítés**, majd az **Elfogadom** gombra, és várd meg a végét (5-15 perc). Ha már bezártad, a Terminálban hozd elő újra:

```bash
xcode-select --install
```

2. Ellenőrizd, hogy működik. Ha egy verziószámot ír ki, rendben vagy:

```bash
git --version
```

3. Add hozzá újra a piacteret ugyanúgy, mint fent.

Ha a telepítő azt írja, hogy a szoftver nem érhető el, az Apple ID-ddal töltsd le kézzel a **Command Line Tools for Xcode** csomagot: https://developer.apple.com/download/all/

## Használat

Elég, ha leírod, mit szeretnél, például: *„Építsük fel a céges agyat, itt a weboldalam: …”*. Az AI magától betölti a megfelelő skillt. Ha te akarod kiválasztani, írj be egy `/` jelet, és keresd meg a listában.

Dolgozz egy saját mappában (például `landing-oldalam/`), mert a skillek oda írják az `agy/` mappát és a szöveget.

## Frissítés

Ha javítunk a skilleken, így kapod meg:

- **Claude:** **Customize → Plugins**, és az **AI Landing Workshop 1**-nél **Check for updates**. Magától nem mindig frissül, ezért ezt érdemes megnyomni. Ha zip-fájlt töltöttél fel, töltsd le és töltsd fel újra az újat.
- **Claude Code:**

```bash
claude plugin marketplace update vikingo-ai-landing
claude plugin update ai-landing-workshop-1@vikingo-ai-landing
```

- **Codex:**

```bash
codex plugin marketplace upgrade vikingo-ai-landing
codex plugin add ai-landing-workshop-1@vikingo-ai-landing
```

Utána indítsd újra a programot.
