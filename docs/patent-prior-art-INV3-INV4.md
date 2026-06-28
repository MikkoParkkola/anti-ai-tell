# Prior-art claim-chart — INV-3 & INV-4 (MIK-6623)

> **Status: patent-database search COMPLETE (Google Patents, 2026-06-28). Verdicts
> below.** Per MIK-3263 doctrine, the verdicts are the audit output; an actual
> filing still needs counsel to chart the full granted claims of the two driving
> references. No public novelty assertion is made.

## Candidate inventions

- **INV-3 — cross-media persistent style anchor.** One `fingerprint.json` whose
  purpose is to de-genericize generated output across modalities (UI, raster,
  logo, docs, prose), with success measured as increased distance from the
  unanchored model centroid.
- **INV-4 — population-variance AI-sameness detection.** Scoring a *set* of
  artifacts for variance collapse as the detection signal, by construction never
  emitting a per-artifact "is AI" verdict (Sadasivan-safe).

## Closest published art (academic literature map — verified arXiv IDs)

| Area | Closest work | What it establishes | Gap vs our claim |
|---|---|---|---|
| Diversity loss from alignment | Kirk et al. ICLR'24 (2310.06452); Padmakumar & He (2309.05196); Zhang "Verbalized Sampling" (2510.01171) | RLHF reduces output diversity; "typicality bias" collapses to modal output | Establishes the *phenomenon* (our diagnosis, NOT novel) |
| Model collapse / variance loss | Shumailov, Nature 2024 (2305.17493); Alemohammad ICLR'24 (2307.01850); Dohmatob ICML'24 (2402.07043) | Recursive training shrinks tails/variance first | Diagnosis only; no detection or cure method |
| Algorithmic monoculture | Kleinberg & Raghavan PNAS (2101.05853); Bommasani NeurIPS'22 (2211.13972) | Shared models -> outcome homogenization | Social-welfare framing, not a detector or style tool |
| Detector impossibility | Sadasivan TMLR (2303.11156); Liang Cell Patterns (2304.02819) | Per-sample detection capped by TV-distance; false-flags humans | We *cite* this as why per-artifact fails — the bound, not our claim |
| Population/variance detection | Liang ICML'24 (2403.07183); Zhang MMD-MP (2402.16041); Basani DivEye (2509.18880) | Corpus prevalence estimation; per-doc variance | **Closest to INV-4.** None frames detection itself as a set-level variance signature |
| Style / steering vectors | ActAdd (2308.10248); CAA (2312.06681); RepE (2310.01405); Style Vectors EACL'24 (2402.01618); Persona Vectors (2507.21509) | Inference-time style/persona control | **Closest to INV-3.** All single-modality; diversity is a side-effect, never the objective; no cross-media anchor |

## Honest novelty partition (from the SOTA map; subject to patent-DB confirmation)

- **(a) Diagnosis "sameness = variance deficit": NOT NOVEL.** Mode collapse +
  homogenization re-described. Cite, do not claim.
- **(b) INV-4 detection inversion: OPEN WHITE SPACE in the literature.** No
  academic work frames detection as "this batch is AI because cross-artifact
  variance collapsed." Nearest (2403.07183) is prevalence estimation. Defensible
  *if* patent-DB search is also clear.
- **(c) INV-3 cross-media single anchor: NO ACADEMIC PRIOR ART found.** Style/
  persona vectors are single-modality and treat diversity as a side-effect. The
  cross-media de-genericizing anchor measured by inter-artifact distance appears
  unclaimed in the literature.

## Claim-chart (patent-DB search complete — Google Patents, 2026-06-28)

### INV-3 — VERDICT: PARTIALLY NOVEL

Closest patents:
- **US20240394945A1** *Digital Content Creation* (app, 2024) — DRIVER. A single
  persistent style vector, derived from average distance between a creator's style
  embeddings, stored in memory, fed into a generative model to de-genericize output.
- **US20250157093A1** *Visual Object Consistency in Image Generation* (app, 2025) —
  average Euclidean distance between cluster members and centroid as a cohesion metric.
- **US20240160902A1** *Similarity-based generative AI output filtering* (app, 2024).
- **US20250225802A1** *Attributing image generative models using latent fingerprints*
  (app, 2025) — but for attribution/watermarking, not style control.
- **US20230230198A1** Adobe text-informed style vector (app, 2023) — single-modality.

Element overlap: single persistent style record (ANTICIPATED, US20240394945A1);
derived from embedding distance (ANTICIPATED, same); de-genericization intent
(PARTLY, same). MISSING from all art: (a) one style record binding **two or more
output modalities** (UI/text/image/document) — all close art is single-modality;
(b) de-genericization **verified as distance from an unanchored-output centroid**
as an explicit quality gate.

**File narrow if at all:** the inventive combination is cross-modal single-record +
centroid-distance verification. Do NOT claim "persistent style vector constrains a
generative model" broadly — US20240394945A1 reads on it almost verbatim.

### INV-4 — VERDICT: BLOCKED (effectively)

Closest patents:
- **US8180717B2** *Estimating a distribution of message content categories* (Harvard,
  King/Hopkins/Lu, granted 2012, in force to ~2031) — DRIVER. Estimates a population
  category distribution "without individually classifying elements in the set." That
  is INV-4's headline novelty, granted, almost verbatim.
- **US9189538B2** (same family, 2015). **US8954577B2** Google population composition
  via EM (2015). **US20080133174A1** population-proportion estimator (2008).
- **US11853708B1** AI-text detection (2023) — but per-document, the opposite.

Element overlap: operate on a set (ANTICIPATED); population-level statistic
(ANTICIPATED); **deliberately withhold per-artifact classification** (ANTICIPATED
EXPLICITLY by US8180717B2 claim language); "variance" vs "distribution" (thin,
likely obvious). MISSING: only the application domain ("the artifacts are
machine-generated content").

**Documented kill of the patent claim as framed.** Pointing a known
population-proportion-without-individual-classification method at LLM output is a
textbook 35 USC 103 obviousness problem. Renaming "distribution" to "variance" does
not save it. The product feature stays (it is genuinely useful and Sadasivan-safe);
the *patent* on it is blocked unless a specific non-obvious mechanism is found (e.g.
a variance statistic tied to a generator's sampling-temperature signature, or a
calibration provably non-invertible to a per-item score).

### Filing recommendation (AAT.PA.3)

- **INV-3:** narrow filing CANDIDATE — claim cross-modal single-record + centroid
  verification only. Counsel to chart US20240394945A1 full granted claims first.
- **INV-4:** DO NOT FILE as framed (blocked by US8180717B2). Keep as a shipped
  product feature, not a patent.

### Caveat

Search was Google Patents only; the two driving references were confirmed in full
text, the rest characterized from abstract/spec snippets. Before any filing, pull
the full granted claims of US20240394945A1 and US8180717B2 and have counsel chart
them. Until then, no public novelty assertion.
