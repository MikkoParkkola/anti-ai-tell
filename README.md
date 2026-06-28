# anti-ai-tell

Make AI-assisted work read like a person made it — in prose and in design. This repo gives you:

1. **Prompt rules** for your AI client that stop AI-ese before it gets written: banned vocabulary, sentence-rhythm requirements, no em-dashes, concrete over abstract, take a position.
2. **A prose linter** (`lint.py`, zero dependencies, Python 3.10+) that flags measured AI tells in any draft, with a `--json` CI mode.
3. **A visual linter** (`visual_lint.py`) that flags the design defaults AI reaches for: indigo-500, Inter, gradient-clipped headlines, glassmorphism, untouched shadcn cards, emoji section headers, raster logos. Reads CSS, Tailwind, React/Vue/Svelte, Markdown, and SVG.
4. **A style fingerprint** (`fingerprint.py`): one small file that holds your chosen accent, font, voice, and density, then feeds both generation and the linters' allow-list. Genericness is a variance deficit — the cure is a chosen point of view, not a longer blocklist.
5. **A judgment checklist** for the tells no regex can catch: missing reasoning, sycophancy, symmetric hedging, nothing concrete anywhere.

Every banned word is backed by a published measurement, and a single generator keeps all eleven client formats in sync. The Claude Code plugin wires three hooks: lint on every write, inject the fingerprint at session start, and ask you for a style anchor when a design task has none.

## What it actually does

Run the linter on a draft and you get findings like these (from the included AI-slop fixture):

```
FAIL sample-ai.txt: 12 Tier-1 tell(s):
  - S8 hard-ban vocabulary (measured AI markers — replace): delve×1, tapestry×1, meticulous×1
  - S3 uniform rhythm: sentence-length CV=0.26 (<0.45 = robotic). Mix short punches with long builds.
  - S2 negative parallelism L1: It's not just about working harder, but about working smarter.
  - S11 vague attribution L1: 'Studies show' — name the source.
  - S9 copulative avoidance (prefer plain is/are/has): 'serves as a'×1
```

The prompt rules prevent most of that at generation time. The linter catches what slips through. The checklist covers what neither can: whether the text shows a mind at work.

## Visual and design tells

Prose is one medium. AI-generated interfaces, slides, logos, and documents converge on the same look for the same reason prose does: the model emits the centre of its training data. The visual linter catches the lintable defaults; the fingerprint supplies the point of view a linter can't invent.

```sh
python3 skills/anti-ai-tell/visual_lint.py client/src        # a whole UI directory
python3 skills/anti-ai-tell/visual_lint.py styles.css --json # one file, CI mode
```

Pointed at a real climate dashboard's hand-written stylesheet, it flagged exactly the marks you'd expect:

```
FAIL index.css: 4 visual tell(s):
  - V-CSS-3 gradient-clipped headline text — most-copied AI flourish  (×2)
  - V-CSS-4 Inter as the typeface — the AI-default font
  - V-CSS-6 glassmorphism blur — applied indiscriminately by AI       (×2)
  - V-CSS-8 blanket large radius
```

Build or refine the fingerprint with derive-then-confirm — read what your existing work already implies, then ask only about the gaps:

```sh
python3 skills/anti-ai-tell/fingerprint.py derive site.css   # extract font, accent, radius
python3 skills/anti-ai-tell/fingerprint.py gaps              # what to ask the user
```

A clean visual lint is the floor. The Tier-2 question the linter can't answer: is there a hierarchy, a point of view, a rough edge? Uniformity is itself the tell.

## Batch sameness, not per-item guessing

`variance_floor.py` scores a *set* of artifacts for variance collapse — the population signal that a batch came off one model. It refuses to judge a single artifact, because per-sample detection is provably unreliable (Sadasivan et al., 2303.11156). Use it on a folder of outputs, never on one.

## Why bother

Readers have learned the tells. In 15.1 million PubMed abstracts, *delves* appeared at 28 times its expected frequency after ChatGPT arrived, *underscores* at 13.8 times (Kobak et al., Science Advances, 2025). In ICLR peer reviews, *meticulous* rose 34.7-fold (Liang et al., ICML 2024). Hiring managers, editors, and customers now discount prose that smells like this; some readers stop at the first em-dash.

Scrubbing words is necessary and insufficient. Eve Fairbanks argued in The Atlantic (May 2026) that the deeper tell is the missing train of thought: prose nobody can argue with because no reasoning happened in it. That layer needs judgment, so this repo ships a checklist for it instead of pretending a script can do it.

## Install

### Fastest: one prompt to your AI agent

Paste this to Claude Code, Cursor, Codex CLI, or any agent with shell access. The same prompt installs and upgrades; re-running is always safe:

> Fetch https://raw.githubusercontent.com/MikkoParkkola/anti-ai-tell/master/INSTALL.md and follow it: detect which AI clients I use and install or upgrade the anti-ai-tell writing rules for each of them.

The agent clones the repo, detects your clients, installs the right adapter for each (replacing any previous version), and verifies the linter against the included fixtures.

### Claude Code plugin

```sh
/plugin marketplace add MikkoParkkola/anti-ai-tell
/plugin install anti-ai-tell@anti-ai-tell
```

### Claude Code bare skill

```sh
git clone https://github.com/MikkoParkkola/anti-ai-tell
cp -r anti-ai-tell/skills/anti-ai-tell ~/.claude/skills/
```

### Any other client, by hand

| Client | File | Install location |
|--------|------|------------------|
| Codex CLI, Jules, Amp, Devin (AGENTS.md standard) | `adapters/AGENTS.md` | project root `AGENTS.md` |
| Cursor | `adapters/cursor-rules.mdc` | `.cursor/rules/anti-ai-tell.mdc` |
| GitHub Copilot | `adapters/copilot-instructions.md` | `.github/copilot-instructions.md` |
| Cline / Roo Code | `adapters/clinerules.md` | project root `.clinerules` |
| Windsurf | `adapters/windsurf-rules.md` | `.windsurf/rules/anti-ai-tell.md` |
| Gemini CLI | `adapters/GEMINI.md` | project or `~/.gemini/GEMINI.md` |
| Aider | `adapters/CONVENTIONS.md` | `aider --read CONVENTIONS.md` |
| Zed | `adapters/zed-rules.md` | project root `.rules` |
| ChatGPT | `adapters/chatgpt-custom-instructions.txt` | Settings → Personalization (fits the field limit) |
| CLAUDE.md without plugin | `adapters/CLAUDE.md-snippet.md` | paste into CLAUDE.md |
| Anything else | `adapters/SYSTEM_PROMPT.md` | system prompt / custom instructions |

All adapters are generated from `data/vocabulary.json` by `build_adapters.py`, so the word lists cannot drift between clients. Edit the JSON, rerun the script, commit. CI fails if generated files drift from the generator.

### Linter only

```sh
python3 skills/anti-ai-tell/lint.py DRAFT.md          # docs, READMEs
python3 skills/anti-ai-tell/lint.py DRAFT.txt --prose  # emails, posts
python3 skills/anti-ai-tell/lint.py DRAFT.md --json    # CI integration
```

Try it on the included samples:

```sh
python3 skills/anti-ai-tell/lint.py tests/sample-ai.txt --prose     # 12 findings
python3 skills/anti-ai-tell/lint.py tests/sample-human.txt --prose  # clean
```

## The prose lint checks

Em-dash overuse, negative parallelism ("not just X, but Y"), uniform sentence rhythm (coefficient of variation below 0.45 reads robotic), evenly paced paragraphs, throat-clearing openers, connective filler, closing bows ("In conclusion"), banned vocabulary (era-tagged), copulative avoidance ("serves as" where "is" belongs), rule-of-three compulsion, vague attribution ("studies show"), markdown artifacts in plain prose, density clusters of AI-elevated common words, paragraphs with no concrete anchor (no number, no named thing), and terms your own fingerprint says to avoid. The `--json` mode also emits a single machine-likeness score from 0 to 100.

A clean lint run means the cheap tells are gone. It does not mean the text reads human. That judgment lives in the Tier-2 checklist in `skills/anti-ai-tell/SKILL.md`, and no regex can make it for you.

## Maintenance

AI vocabulary drifts as models change: the *delve* era gave way to *showcasing*, then to *emphasizing*. `data/vocabulary.json` carries era tags and an update date. When a new corpus study lands, refresh the lists, rerun `build_adapters.py`, and bump the date. Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) page tracks the drift well and cites its sources.

## Sources

- Eve Fairbanks, ["The Biggest Tell That Something Was Written by AI"](https://www.theatlantic.com/technology/2026/05/how-to-tell-ai-writing/687345/), The Atlantic, 2026-05-29
- Kobak et al., ["Delving into LLM-assisted writing in biomedical publications through excess vocabulary"](https://arxiv.org/abs/2406.07016), Science Advances 11(27), 2025
- Liang et al., ["Monitoring AI-Modified Content at Scale"](https://arxiv.org/abs/2403.07183), ICML 2024
- Hans et al., ["Spotting LLMs With Binoculars"](https://arxiv.org/abs/2401.12070), 2024
- Krishna et al., ["Paraphrasing evades detectors of AI-generated text"](https://arxiv.org/abs/2303.13408), NeurIPS 2023
- Muñoz-Ortiz et al., ["Contrasting Linguistic Patterns in Human and LLM-Generated News Text"](https://arxiv.org/abs/2308.09067), 2024
- Jason Koebler, ["Your AI Use Is Breaking My Brain"](https://www.404media.co/your-ai-use-is-breaking-my-brain/), 404 Media
- Victoria Turk, ["The Great Language Flattening"](https://www.theatlantic.com/technology/archive/2025/04/great-language-flattening/682627/), The Atlantic, 2025
- Wikipedia, [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

## License

MIT
