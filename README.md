# AI Landing Workshop: skillek

Ezek a skillek a Vikingo AI Landing Workshop eszközei. Segítségükkel az AI a saját vállalkozásod anyagaiból írja meg és építi fel a landing oldaladat, nem általános sablonszöveget ad.

Verzió: 0.1.0

## Mi van benne

| Skill | Mire jó |
|---|---|
| `landing-ceges-agy` | Felépíti a céges agyat: egy `agy/` mappát a cégedről, az ajánlatodról, a célcsoportodról és a hangodról. Ezzel kezdj. |
| `landing-szovegiro` | A céges agyból megírja a landing oldal szövegét, blokkról blokkra. |
| `szoveg-emberiesito` | Kiszedi a szövegből az AI-írás árulkodó jeleit. A szövegíró magától lefuttatja, de bármilyen szövegen használhatod. |
| `landing-epito` | A kész szövegből megépíti a HTML landing oldalt. (A 2. alkalomra érkezik.) |

A sorrend: **céges agy → szöveg → átnézés → építés.**

## Telepítés

Válaszd azt, amelyik programot használod.

### Claude (claude.ai vagy a Claude asztali app)

1. Nyisd meg: **Customize → Plugins** (https://claude.ai/customize/plugins).
2. **Add → Add marketplace**, és írd be: `vikingokft/ai-landing-workshop`
3. Keresd meg az **AI Landing Workshop** plugint, és kattints az **Add** gombra.

Ha nem akarsz GitHubot használni: töltsd le a zip-fájlt (https://github.com/vikingokft/ai-landing-workshop/releases/latest/download/ai-landing-workshop.zip), és ugyanitt válaszd az **Add → Upload plugin** lehetőséget.

A plugin a fiókodhoz mentődik, így a Cowork és a Claude Code is megkapja. A skillek egy része kis ellenőrző programot futtat. A böngészős chatben ehhez a kódfuttatásnak (Code execution) bekapcsolva kell lennie a beállításokban.

### Claude Code (terminál)

```bash
claude plugin marketplace add vikingokft/ai-landing-workshop
claude plugin install ai-landing-workshop@vikingo-ai-landing
```

### Codex

```bash
codex plugin marketplace add vikingokft/ai-landing-workshop
codex plugin add ai-landing-workshop@vikingo-ai-landing
```

Az alkalmazásban ugyanezt a **Plugins** menüből is megteheted.

## Használat

Elég, ha leírod, mit szeretnél, például: *„Építsük fel a céges agyat, itt a weboldalam: …”*. Az AI magától betölti a megfelelő skillt. Ha te akarod kiválasztani, írj be egy `/` jelet, és keresd meg a listában.

Dolgozz egy saját mappában (például `landing-oldalam/`), mert a skillek oda írják az `agy/` mappát és a szöveget.

## Frissítés

A 2. alkalom előtt új skill érkezik (a weboldal-építő), és ha javítunk a skilleken, azt is így kapod meg.

- **Claude:** a GitHubról telepített plugin magától frissül (vagy: **Check for updates**). Ha zip-fájlt töltöttél fel, töltsd le és töltsd fel újra az újat.
- **Claude Code:**

```bash
claude plugin marketplace update vikingo-ai-landing
claude plugin update ai-landing-workshop@vikingo-ai-landing
```

- **Codex:**

```bash
codex plugin marketplace upgrade vikingo-ai-landing
codex plugin add ai-landing-workshop@vikingo-ai-landing
```

Utána indítsd újra a programot.
