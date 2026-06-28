# Visual AI tells — research catalog

The design counterpart to `anti-ai-tell`. Where the text skill catches prose that
reads as machine-written, this catalogs the **visual** tells that betray a design,
interface, image, logo, or document was AI-generated or shipped from AI defaults.

Compiled 2026-06-28 from ~90 sourced patterns across five research lanes (web/SaaS UI,
raster imagery, logos/branding, documents/decks, color-type-layout primitives). Every
pattern carries a real source. Severity uses the same scale as the text skill.

---

## The thesis (the visual analogue of "absence of a mind")

The text skill's load-bearing finding: surface scrubbing is necessary but insufficient;
the durable tell is the **absence of a mind at work** — no reasoning, no position, nothing
concrete.

The visual analogue is the **absence of design intent — regression to the training-data mean.**
AI design tools don't choose; they emit the statistical centre of design space and ship
defaults unchanged. Two consequences, which map exactly onto the text skill's two tiers:

- **Tier 1 — surface tells (swappable tokens).** Specific defaults: Tailwind `indigo-500`,
  Inter, glassmorphism, the gradient-blob logo, the orange-teal photo grade. Mechanical,
  recognizable, and — critically — **swapping them doesn't fix the problem.** Recolor the
  purple to green and the site still reads as AI, because the tells are downstream of a
  deeper cause.
- **Tier 2 — deep tells (absence of decisions).** No visual hierarchy, no point of view,
  structure that doesn't follow from content, defaults left untouched, polish with no
  purpose. This is the design equivalent of sycophancy + no-reasoning. No linter catches it.

A "vibe-coded" landing page that passes a token-swap still fails Tier 2 if every section is
the same width, every card the same radius, and nothing leads the eye. The missing
ingredient is *judgment*, and — as with prose — it cannot be post-processed in.

### Root causes (shared across all media)

1. **Mode collapse / centroid sampling.** Generative models pick the highest-probability
   output; the centre of the distribution is by definition the most generic thing.
2. **Default-token propagation.** One library default leaks into training data and becomes
   a global monoculture. The clearest case: Tailwind UI shipped `bg-indigo-500` as its
   example button; Adam Wathan (Tailwind founder) publicly apologized for "making every
   AI-generated interface on Earth turn indigo."
3. **Defaults shipped as finished work.** shadcn/ui, Gamma themes, resume-builder templates
   are *starting points*; AI (and rushed humans) ship them unchanged.
4. **No physical/semantic model.** Images: no light-transport or 3D model → impossible
   shadows, mangled hands, garbled text. Logos: no symbol model → letters as texture.
5. **Feedback loop.** AI output → next training set → more of the same. The monoculture
   compounds.

### Severity legend (same as the text skill)

- **Hard-tell** — instantly screams AI; one instance is often enough.
- **Strong-flag** — suspicious, especially in a cluster; a couple together = AI.
- **Density-watch** — fine once or deliberately; a pile-up in one artifact is the tell.

---

*(catalog sections follow: A. Web/App/SaaS UI · B. Color·Type·Layout primitives ·
C. Raster imagery · D. Logos·branding·illustration · E. Documents·decks · F. Resumes ·
plus overall Top tells and sources)*

---

## A. Web / app / SaaS UI

| # | Pattern | Severity | Why it's a tell |
|---|---------|----------|-----------------|
| A1 | **Indigo/purple accent + violet→pink gradient** (`indigo-500`/`#6366f1`, `from-indigo-500 to-purple-600`) | Hard-tell | "The Purple Problem." Traces to Tailwind UI's default button color; baked into the corpus. Recoloring doesn't fix the genericness. |
| A2 | **Untouched shadcn/ui defaults** — neutral gray cards, 1px border, slight rounding, shipped as-is | Hard-tell | "The shadcn-ification of the internet" / "the modern Bootstrap." A starting point shipped as the finished product. |
| A3 | **The shadcn dashboard skeleton** — left sidebar + center data table + top-right button group + bottom-corner toast | Hard-tell | The literal default composition for "build me a dashboard." "You've seen this app. We've all seen this app." |
| A4 | **Three feature boxes with icons in a row** (Lucide icon + bold title + 2 lines muted) | Strong-flag | "The median of every Tailwind landing page in the training data. The AI isn't designing, it's averaging." |
| A5 | **Gradient-clipped text headline** (`bg-clip-text` purple→pink on hero H1) | Strong-flag | Most-copied "modern" flourish; r/webdev: "Why is the gradient text EVERYWHERE?!" |
| A6 | **Dark hero with aurora/radial glow** (`zinc-950` + soft purple-blue blob behind centered white text) | Strong-flag | Cloned Linear/Vercel "premium dark SaaS" look; instant déjà vu. |
| A7 | **Centered hero: headline + subhead + dual CTA** (filled purple primary + ghost secondary) | Strong-flag | The single most probable hero arrangement; the model's default absent constraints. |
| A8 | **Fixed landing-page section order** — hero → logo cloud → feature grid → testimonials → pricing → CTA band → footer | Strong-flag | Sameness is *structural*, not just stylistic; a recolored site still scans as generated. |
| A9 | **Functional gap behind the pretty shell** — forms with no validation/error/required states, CTAs wired to nothing, broken heading hierarchy | Strong-flag | Behavioral fingerprint: trained on static markup, not interaction flows. "Looks like a form, doesn't work like a form." |
| A10 | **Bento grid of mismatched-size cards** | Density-watch | The post-3-column "modern" upgrade everyone copied; distinctive once, generic in aggregate. |
| A11 | **"Trusted by" logo cloud of desaturated/placeholder logos** | Density-watch | A fixed template slot, often shipped with filler logos whether or not real customers exist. |
| A12 | **"Tailwind Blue" fallback** (`blue-500`/`600`) when not purple | Density-watch | Same defaulting behavior pointed at the second-most-common token; changes the hue, not the genericness. |

---

## B. Color · type · layout primitives (cross-cutting tokens)

These are the low-level design tokens that recur across web, docs, and apps. They are the
visual equivalent of the text skill's banned-vocabulary list.

| # | Pattern | Severity | Why it's a tell |
|---|---------|----------|-----------------|
| B1 | **Inter as universal body font** (+ Space Grotesk/Manrope headings, Playfair/Lora for "elegant") | Hard-tell | "You can spot a Claude-built app by its fonts." Statistical centre of the font distribution. Anthropic's own cookbook tells the model to avoid Inter. |
| B2 | **Permanent dark mode + neon glow** (`bg-black`/`zinc-950` + radial ambient glow) | Hard-tell | The single most common tell at **34% of audited pages**. "Modern" in a vague prompt resolves to dark+neon+glowy. |
| B3 | **"Everything is a card" + 3-column icon-card grid** | Hard-tell | The canonical AI shape; **22% of pages**. "Why does every AI site look like the same 3-column landing page with a purple gradient button?" |
| B4 | **Gradient background washes** (`radial-gradient(ellipse_at_center…)`, mesh gradients) | Strong-flag | Second-most-frequent tell at **27%**; default fill for empty hero space. |
| B5 | **Slate/zinc/neutral gray palette** (Tailwind default ramps, untouched) | Strong-flag | Sameness comes specifically from leaving the default color palette untouched. shadcn ships `baseColor: neutral`. |
| B6 | **Glassmorphism / frosted-glass cards** (`backdrop-filter: blur(12–24px)`, `bg-white/10`) | Strong-flag | A small set of visual rules applied indiscriminately; routinely fails WCAG AA body-text contrast (NN/g). |
| B7 | **Lucide / Heroicons / Phosphor ubiquity** | Strong-flag | The default open icon sets in the Tailwind/shadcn ecosystem; same ~20 glyphs (Zap, Shield, Rocket, Sparkles) everywhere. |
| B8 | **Uniform large border-radius** (`rounded-xl`/`2xl`, "20px minimum", squircles) | Density-watch | Prompt kits literally instruct a minimum radius everywhere; cards, buttons, inputs, images share one corner value. |
| B9 | **The `hover:scale-105` lift** (`hover:scale-105` + expanding shadow, identical easing) | Density-watch | Copy-paste micro-interaction baked into popular prompt templates; same scale value recurs verbatim. |
| B10 | **Emoji as feature icons** | Density-watch | Prompt recipes say "use emoji" for card icons; the zero-effort default when no icon set is wired. |
| B11 | **Centered `max-w-7xl mx-auto` container + uniform `py-28/40` padding** | Density-watch | Default Tailwind content shell; the page spine is identical app to app. |
| B12 | **8px spacing grid uniformity** (`p-4`, `gap-8`) | Density-watch | Near-universal token system; consistent but interchangeable — strips spacing personality. |
| B13 | **Uniform subtle drop-shadow scale** (`shadow-sm/md/lg` unchanged) | Density-watch | Identical elevation ramp across unrelated sites because nobody re-tokenizes it. |
| B14 | **"Alternative" fonts that are themselves a cliché** (Geist, Satoshi, Switzer, system-ui) | Density-watch | The escape hatch is on-distribution: "stop using Inter" lists converge on the same 5–7 substitutes. |
| B15 | **Neumorphism revival (soft-UI)** | Density-watch | Cyclical trend-trio (neumorphism/glassmorphism/neubrutalism) copied wholesale; unusable for interactive controls. |

---

## C. Raster imagery (AI photos & illustration)

Caveat the sources stress: **no single tell is conclusive** — confidence comes from multiple
red flags stacking. And the classic tells (hands, faces) are fading fast in 2025+ models
(Nano Banana Pro, Flux), so the **Density-watch gestalt tells matter more going forward** than
any lone artifact.

| # | Pattern | Severity | Why it's a tell |
|---|---------|----------|-----------------|
| C1 | **Garbled text / nonsense signage** — gibberish on signs, packaging, labels | Hard-tell | Diffusion paints the *shape* of writing without a language model. Most reliable surviving tell. |
| C2 | **Mangled hands & fingers** — extra/fused digits, knuckles too far back | Hard-tell (when present); Density-watch (rare in 2025+) | No 3D constraint on finger count/joints; "plausible locally, wrong globally." The canonical tell — now fading. |
| C3 | **Plastic / waxy "airbrushed" skin** — porcelain-smooth, no pores, resin sheen | Strong-flag | Trained on retouched/filtered beauty imagery; "smooth skin" is the statistical default. An entire de-plasticizing tool industry exists to undo it. |
| C4 | **Uncanny "too-perfect" gloss (the Midjourney default look)** | Strong-flag | "When perfect becomes the tell" — anatomically correct but with a polish not found in real photos. The gestalt giveaway. |
| C5 | **Orange-and-teal color bias** — default complementary grade across unrelated images | Density-watch | Cinematic grading floods the training set; "orange and blue hell." Likely embedded in Midjourney's base model. The most-cited *color* tell. |
| C6 | **Impossible / conflicting shadows** — multiple directions under one sun | Strong-flag | No light-transport simulation; shadow texture stitched without a global light direction. A physics violation. |
| C7 | **Impossible reflections** — mirror/water/eye reflections that don't match the scene | Strong-flag | Accurate reflection needs 3D geometry; the model approximates "reflective-looking" texture instead. |
| C8 | **Lighting mismatch subject vs background** — foreground that doesn't belong to its background | Strong-flag | Subject and background composed as semi-independent regions; global illumination breaks at the seams. |
| C9 | **Smudgy patches / "patched-together" backgrounds** | Strong-flag | Where the model lacks a confident reconstruction it falls back to soft texture filler; locally plausible, globally incoherent. |
| C10 | **Over-multiplied background objects ("too many lamps")** | Strong-flag | Fills space by sampling plausible objects locally with no scene-level inventory; over-populates and duplicates. |
| C11 | **Melted / merging geometry — lines that don't join** | Strong-flag | Texture/patch-level generation enforces no long-range structural constraint; a railing won't stay one object. |
| C12 | **Misshapen irises, pupils, teeth, ears** (requires zoom) | Strong-flag | Small high-detail features sit below the resolution the model reasons about; rendered as approximate texture. |
| C13 | **Mangled faces in crowds / background people** | Strong-flag | Fidelity goes to the focal subject; off-center, small, or numerous faces degrade into garbled approximations. |
| C14 | **Hair as a "painted helmet" / flawless windswept hair** | Density-watch | Fine filaments are high-frequency near-random detail; averaged into a coherent painted shape. |
| C15 | **Hyperrealistic "over-detail" that means nothing** — busy crisp backgrounds with no purpose | Density-watch | Rewards locally rich texture but has no scene intent; maximizes detail density without semantic structure. |
| C16 | **Context / beauty mismatch** — magazine gloss in a crisis/candid/mundane scene | Strong-flag | Default pull toward idealized, well-lit output ignores situational realism. |
| C17 | **Compression / frequency-domain fingerprints** (tool-assisted, not eyeball) | Strong-flag | Generative pipelines leave spectral signatures distinct from camera sensor noise; detectable even when the image looks flawless. |

---

## D. Logos · branding · vector illustration

| # | Pattern | Severity | Why it's a tell |
|---|---------|----------|-----------------|
| D1 | **Gradient-blob abstract mark** — an orb/petal/infinity-swoosh, two-stop gradient, left of the wordmark | Hard-tell | Models converge on the highest-probability "modern tech logo": the post-2018 gradient orb. Mirrors the crypto-boom homogenization. |
| D2 | **Mangled / jumbled lettering inside the mark** — gibberish, faux-Latin glyphs | Hard-tell | Image models paint letter-shaped texture without symbol meaning. The logo equivalent of six-fingered hands. |
| D3 | **Type rendered as line-art, not a real font** — uneven spacing, drifting stroke weight, no re-settable typeface | Hard-tell | AI "draws" type as artwork; the brand has no font to extend with. "There is no font assigned to these logos." |
| D4 | **Raster (JPG/PNG) output masquerading as a logo** — soft edges, baked-in background, pixel halos | Hard-tell | A real logo is vector; the raster artifact betrays the pipeline and fails at large/one-color print. |
| D5 | **Blue mark + geometric sans + "happy people collaborating"** — the full B2B-SaaS uniform | Hard-tell (as a system) | The densest "trustworthy software" cluster in the training data, reproduced as a whole brand kit. |
| D6 | **Rounded-geometric-sans wordmark** (Circular/Poppins/Inter-adjacent, often lowercase) | Strong-flag | The "sans-serif invasion" / "sea of sameness" — brands stripped of quirks toward the category's statistical centre. |
| D7 | **Over-detailed, won't-scale mark** — gradients, filigree, many colors, mud at favicon size | Strong-flag | Optimized for one attractive render, not for reduction/legibility a logo must survive. |
| D8 | **Broken symmetry where symmetry was intended** — compass rose / monogram subtly off | Strong-flag | Models approximate symmetry rather than constructing it on a grid; near-symmetric marks wobble. |
| D9 | **Hexagons, grids, "abstract illusion" geometry** — nodes-and-edges "platform/AI/blockchain" marks | Strong-flag | Crypto-era visual vocabulary re-emitted; signals "tech" generically rather than identifying anyone. |
| D10 | **"Too literal" icon mark** — a coffee brand whose logo is a coffee cup | Strong-flag | AI matches the prompt's nouns literally; no conceptual layer to find an oblique, ownable symbol. |
| D11 | **Fake-depth bevels, drop shadows, faux-3D sheen** on flat marks | Strong-flag | Image models paint photographic lighting onto shapes; destroys single-color usability. |
| D12 | **Corporate Memphis / "Alegria" flat people** (big noodly limbs, tiny heads) and its glossier AI successor | Strong-flag | Already the de-facto tech-illustration default → dominates training data; AI both reproduces and succeeds it. |
| D13 | **Over-uniform stock iconography** — identical stroke/radius/perspective, machine-stamped | Density-watch | Generators emit one homogeneous icon grammar; the absence of human variation is itself the signal. |
| D14 | **The "Crayola Bold / navy-and-taupe" palette** | Density-watch | Defaults to the most common un-curated palette; no reasoning about cultural meaning or tonal restraint. |
| D15 | **Indigo/violet gradient brand palette everywhere** | Density-watch | Gradient logos returned as the 2024–25 default; AI leans on the exact "AI product" indigo/violet range. |

---

## E. Documents · slides · decks (Gamma, Tome, Canva Magic, ChatGPT-formatted)

| # | Pattern | Severity | Why it's a tell |
|---|---------|----------|-----------------|
| E1 | **Same-template "card sameness" across AI decks** — title + blurb + icon, repeated; different topics, identical skeleton | Hard-tell | Gamma's speed comes from a fixed card-based layout engine that reuses containers regardless of content. |
| E2 | **Emoji-as-section-header in documents** (✅ 🚀 💡 📌 🎯) | Hard-tell | ChatGPT's defining default; "showing up as a reason people cancel subscriptions." Users actively prompt it out "to clean tracks from obvious ChatGPT outputs." |
| E3 | **Markdown bleed** — literal `###`, `**bold**`, `\|table\|` pipes in a rendered Word/Docs/email | Hard-tell | Author pasted AI output verbatim; the syntax is a direct LLM artifact. Claude minimizes markdown, ChatGPT maximizes it. |
| E4 | **Default theme / auto-gradient background ("the Gamma purple")** | Strong-flag | Tools ship an opinionated default palette + auto-gradients; most users never override, so the default becomes a fingerprint. |
| E5 | **Uniform icon-left / text-right rows** — matching corner-radii + card shadows | Strong-flag | The generator stamps one row component repeatedly; designers must *re-introduce* variation to break it. |
| E6 | **Generic stock imagery + stock 3D/flat icons** (Pexels/Pixabay auto-pull) | Strong-flag | No brand specificity; the same imagery recurs across unrelated decks. |
| E7 | **Web-native look that breaks on PowerPoint export** — polished in the web viewer, mangled in .pptx | Strong-flag | Built for scrolling web cards, not slide geometry; "the exports break, enterprise IT rejects it on first review." |
| E8 | **Emoji-numbered lists** (1️⃣ 2️⃣ instead of 1. 2.) | Strong-flag | A specific ChatGPT reflex; no human types emoji digits for a numbered list. |
| E9 | **Bold-spam** — ~half the body bolded; a **Bold Label:** opening every bullet | Strong-flag | Default emphasis behavior bolds key terms with "no real logic" — a density no human editor chooses. |
| E10 | **Over-bulleting everything** — prose (letters, emails) flattened into lists | Strong-flag | ChatGPT defaults to bullets even when asked for narrative prose. |
| E11 | **"Agenda → 3 pillars → thank you" boilerplate structure** | Density-watch | Maps any prompt onto a stock storyboard; the structure is the template, not the argument. |
| E12 | **A table for everything** — sentences forced into 2/3-column comparison grids | Density-watch | Tables are part of the default markdown kit; on the standard "stop doing this" list. |

---

## F. Resumes & formatted application docs

The strongest signal here is **cross-applicant sameness** — the gestalt, not any single
feature — and it carries real cost: **49% of hiring managers reject AI-generated resumes**
(resume.io, survey of 3,000), peaking at 71% in Iowa. Managers prefer "poorly written but
authentic" over "perfectly polished AI."

| # | Pattern | Severity | Why it's a tell |
|---|---------|----------|-----------------|
| F1 | **Leftover chat scaffolding** — "You said:", "ChatGPT said:", "Here's your updated resume:", "[Company Name]" | Hard-tell | Unmistakable copy-paste residue; nothing else produces these strings. |
| F2 | **Identical boilerplate across many applicants** — ~40% of a 150-pool submitted the *exact same* answer | Hard-tell | A personal opinion can't be word-for-word identical across strangers. |
| F3 | **Cross-applicant sameness (the meta-tell)** — a stack that reads "like one person wrote all of them" | Strong-flag | Mass adoption of the same tools with the same defaults collapses variety; uniformity itself signals AI. |
| F4 | **Same five power verbs every bullet** — spearheaded/orchestrated/championed/pioneered/leveraged (+ adept, tech-savvy, cutting-edge) | Strong-flag | Recruiters report a sudden uniform spike post-ChatGPT "from candidates who weren't using those terms before." |
| F5 | **Em-dash overuse** — now a consciously recruiter-clocked fingerprint | Strong-flag | The text tell crossing into resumes; recruiters explicitly scan for it. |
| F6 | **Identical builder template + skill bars / rating dots** | Strong-flag | A small template set with decorative meters ATS can't parse; recognized on sight. |
| F7 | **Suspiciously clean round numbers + a "fits-anybody" summary** (improved efficiency 30%, cut costs 20%) | Density-watch | AI fabricates plausible-but-rounded metrics and writes the statistical average of a thousand similar resumes. |
| F8 | **Hidden/invisible keyword stuffing** — white-on-white text, near-zero font sizes | Hard-tell (when found) | Gaming ATS or diluting detectors; exposed by pasting into a plain-text editor. |

> **Detector caveat (load-bearing):** AI-text detectors are unreliable — ZeroGPT rated the
> Declaration of Independence 97.9% AI; GPTZero scored the Constitution ~92% machine. They
> over-flag non-native English and neurodivergent writers. **Human pattern-recognition, not a
> detector score, is what rejects these.** Don't build detection on detector tools.

---

## Overall: the 10 loudest tells (cross-medium)

1. **Tailwind `indigo-500` purple + violet gradient** (web/UI, logos) — the single most-discussed tell, with a named origin (Wathan's apology).
2. **Untouched shadcn defaults — gray cards + the dashboard skeleton** (web/UI) — "the modern Bootstrap."
3. **Inter (+ Space Grotesk) everywhere** (typography) — "spot a Claude app by its fonts."
4. **"Everything is a card" 3-column icon grid** (web/UI, docs) — quantified at 22% of pages.
5. **Garbled text / nonsense signage** (raster, logos) — the most reliable image tell.
6. **Plastic/waxy skin + uncanny "too-perfect" gloss** (raster) — the AI sheen.
7. **Gradient-blob abstract logo + mangled lettering** (logos) — the orb and the six-fingered-hands-of-type.
8. **Emoji-as-section-header + markdown bleed** (documents) — ChatGPT's formatting signature.
9. **Cross-applicant resume sameness** (resumes) — drives 49% rejection.
10. **Permanent dark mode + glassmorphism + gradient washes** (web/UI) — the surface-effect cluster, 34% dark + 27% gradient.

---

## The Tier-2 design checklist (the part no linter catches)

The visual equivalent of the text skill's "show a mind at work." For any design/image/doc,
ask:

- **Hierarchy:** does one thing lead the eye, or is everything the same weight? (AI ships
  "no hierarchy beyond bigger-text-equals-header.")
- **Point of view:** is there a dominant color/idea, versus a timid evenly-distributed average?
- **Intent from content:** does the structure follow from *this* content, versus the
  template's structure stamped onto any content?
- **Untouched defaults:** are the radius/shadow/palette/font the library defaults, versus chosen?
- **Behavior, not just look:** do the forms validate, the CTAs go somewhere, the export hold?
- **A rough edge:** one deliberate asymmetry, an unexpected but right color, a custom mark —
  the visual contraction. Perfect uniformity *is* the tell.

If the answers are "no hierarchy / timid average / template structure / untouched defaults /
no behavior / perfectly uniform," it still reads as AI — even after every Tier-1 token is swapped.

---

## How this maps to a future skill

The text `anti-ai-tell` has Tier-1 (lint.py, mechanical) + Tier-2 (judgment checklist). A
visual version splits the same way:

- **Tier-1 lintable (some of these):** detectable in code/config — `indigo-500` in CSS, Inter
  in the font stack, untouched shadcn tokens, `bg-clip-text` gradient headlines, emoji in
  markdown headers, literal `###`/`**` in a .docx, `hover:scale-105`. A linter over a repo's
  CSS/Tailwind config plus a markdown/docx scanner could flag a real subset.
- **Tier-2 judgment (most of these):** hierarchy, intent, the raster gestalt tells, logo
  conceptual quality — these need a vision-model reviewer or a human, exactly as Tier-2 prose
  needs a mind.

Natural next artifacts: a `visual-vocabulary.json` (the B-section tokens, era-tagged like the
text vocab), a CSS/config linter, and a vision-model rubric for the Tier-2 gestalt.

---

## Sources (selected, by lane)

**Web/UI:** prg.sh "Why Your AI Keeps Building the Same Purple Gradient Website" (quotes
Anthropic's frontend cookbook verbatim) · dev.to/alanwest "Blame Tailwind's Indigo-500" ·
bhuwan-garbuja.com "why all websites look the same" · axe-web.com "Sea of Sameness" ·
r/webdev, r/Frontend, r/vibecoding threads.
**Color/type/layout:** developersdigest.tech "AI Design Slop: 16 Patterns" (the 34%/27%/22%
audit) · AIbase (Adam Wathan apology) · Kai Ni (Medium) · r/ClaudeAI "spot a Claude app by
its fonts" · NN/g glassmorphism · shadcn theming docs · Superfiles "Stop Using Inter."
**Raster:** GIJN "Guide to Detecting AI-Generated Content" (physics/geometry failures) ·
Kellogg/Northwestern · Flitto DataLab (orange-teal) · Leon Furze · ZDNET · Mashable · Forbes
· Watermarkly · OreateAI/andyhtu/WearView (plastic skin) · r/midjourney, r/AskUK.
**Logos/branding:** ebaqdesign "AI Startup Logos" · MWH Design · Corwin Design · The Business
Toolkit · VelvetShark · Creative Bloq "sea of sameness" · Typogram · Metabrand · Wikipedia
"Corporate Memphis" · r/GraphicDesigning, r/decadeology.
**Documents/decks/resumes:** getalai.com (Gamma card sameness) · Plus AI (Canva stock) ·
Presentations.ai (export breakage) · Unmarkdown · AI Productivity News · OpenAI community
bug threads · resume.io (49% study) · Hiration · Willo · Scale.jobs (named Intuit recruiter)
· r/Resume, r/ChatGPTPro, r/powerpoint, r/bestai2025.

*Method note: research run as 5 parallel agent lanes, each reading 8–12 sources end-to-end
via nab/brave. Soft citations (bento grid, logo cloud) flagged in-line as such rather than
overstated.*

