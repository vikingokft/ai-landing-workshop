# AI Landing Workshop: skillek

Ezek a skillek a Vikingo AI Landing Workshop eszközei. Segítségükkel az AI a saját vállalkozásod anyagaiból írja meg és építi fel a landing oldaladat, nem általános sablonszöveget ad.

## Melyik plugin kell?

| Plugin | Mikor | Mi van benne |
|---|---|---|
| `ai-landing-workshop-1` (verzió: 0.2.1) | az 1. alkalomra | céges agy, szövegíró, emberiesítő |

A 2. alkalom skilljei külön pluginban érkeznek, a 2. alkalom előtt.

## Mi van benne

| Skill | Mire jó |
|---|---|
| `landing-ceges-agy` | Felépíti a céges agyat: egy `agy/` mappát a cégedről, az ajánlatodról, a célcsoportodról és a hangodról. Ezzel kezdj. |
| `landing-szovegiro` | A céges agyból megírja a landing oldal szövegét, blokkról blokkra. |
| `szoveg-emberiesito` | Kiszedi a szövegből az AI-írás árulkodó jeleit. A szövegíró magától lefuttatja, de bármilyen szövegen használhatod. |

## Telepítés

Válaszd azt, amelyik programot használod. A lenti parancsok az 1. pluginra szólnak.

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

## Használat

Elég, ha leírod, mit szeretnél, például: *„Építsük fel a céges agyat, itt a weboldalam: …”*. Az AI magától betölti a megfelelő skillt. Ha te akarod kiválasztani, írj be egy `/` jelet, és keresd meg a listában.

Dolgozz egy saját mappában (például `landing-oldalam/`), mert a skillek oda írják az `agy/` mappát és a szöveget.

## Frissítés

Ha javítunk a skilleken, így kapod meg:

- **Claude:** a GitHubról telepített plugin magától frissül (vagy: **Check for updates**). Ha zip-fájlt töltöttél fel, töltsd le és töltsd fel újra az újat.
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
