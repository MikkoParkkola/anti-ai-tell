# anti-ai-tell

A writing discipline, a linter, and a set of prompt blocks that keep prose from reading as AI-generated. Works as a Claude Code plugin, a standalone skill file, a Cursor rule, or a system-prompt block for any AI client.

## Why this exists

Readers have learned the cheap tells. Corpus studies put numbers on them: in 15.1 million PubMed abstracts, *delves* appeared at 28 times its expected frequency after ChatGPT arrived, *underscores* at 13.8 times, *showcasing* at 10.7 times (Kobak et al., Science Advances, 2025). In ICLR peer reviews, *meticulous* rose 34.7-fold (Liang et al., ICML 2024). People notice these words now, the same way they notice em-dashes and "it's not X, it's Y".

Scrubbing the word list is necessary and insufficient. Eve Fairbanks argued in The Atlantic (May 2026) that the deeper tell is the missing train of thought: prose nobody can argue with because no reasoning ever happened in it. Jason Koebler at 404 Media compressed the same idea into one line: the tell is that "problems with all these elements exist equally & at once."

So this repo works in three tiers:

| Tier | What | How |
|------|------|-----|
| 0 | Prevent AI-ese at generation time | prompt blocks in `adapters/` |
| 1 | Catch the 13 measured mechanical tells | `lint.py`, CI-gateable |
| 2 | The judgment pass: reasoning, friction, concreteness, commitment | checklist in `SKILL.md` |

## Install

**Claude Code (plugin):**

```sh
/plugin marketplace add MikkoParkkola/anti-ai-tell
/plugin install anti-ai-tell@anti-ai-tell
```

**Claude Code (bare skill):**

```sh
git clone https://github.com/MikkoParkkola/anti-ai-tell
cp -r anti-ai-tell/skills/anti-ai-tell ~/.claude/skills/
```

**Cursor:** copy `adapters/cursor-rules.mdc` into your project's `.cursor/rules/`.

**Any other client** (ChatGPT custom instructions, Gemini, local models): paste `adapters/SYSTEM_PROMPT.md` into the system prompt or custom-instruction field.

**Linter only:**

```sh
python3 skills/anti-ai-tell/lint.py DRAFT.md          # docs, READMEs
python3 skills/anti-ai-tell/lint.py DRAFT.txt --prose  # emails, posts
python3 skills/anti-ai-tell/lint.py DRAFT.md --json    # CI integration
```

No dependencies beyond Python 3.10.

## What the linter checks

Thirteen tells, each backed by a measurement or a primary source: em-dash overuse, negative parallelism, uniform sentence rhythm (coefficient of variation below 0.45 reads robotic), evenly paced paragraphs, throat-clearing openers, connective filler, closing bows, banned vocabulary (era-tagged in `data/vocabulary.json`), copulative avoidance ("serves as" where "is" belongs), rule-of-three compulsion, vague attribution, markdown artifacts in plain prose, and density clusters of AI-elevated common words.

Try it on the included samples:

```sh
python3 skills/anti-ai-tell/lint.py tests/sample-ai.txt --prose     # 12 findings
python3 skills/anti-ai-tell/lint.py tests/sample-human.txt --prose  # clean
```

A clean lint run means the cheap tells are gone. It does not mean the text reads human. That judgment lives in Tier 2, and no regex can make it for you.

## Maintenance

AI vocabulary drifts as models change: the *delve* era gave way to *showcasing*, then to *emphasizing*. `data/vocabulary.json` carries era tags and an update date. When a new corpus study lands, refresh the lists and bump the date. Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) page tracks the drift well and cites its sources.

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
