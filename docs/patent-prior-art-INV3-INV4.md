# Prior-art claim-chart — INV-3 & INV-4 (MIK-6623)

> **Status: SOTA literature map complete; patent-database search PENDING.**
> Per MIK-3263 doctrine, no public novelty claim or filing recommendation may be
> made until the formal patent-DB audit (not just the academic-literature map
> below) is run. This document is the skeleton that audit fills in. It does NOT
> assert patentability.

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

## Claim-chart skeleton (to complete during the patent-DB audit)

For each independent claim, the audit fills: claim text -> nearest patent/app ->
element-by-element overlap -> novel element(s) -> verdict.

- INV-3 independent claim (method): "A method of constraining a generative model
  across two or more output modalities using a single persistent style record,
  wherein de-genericization is verified by measuring distance from an unanchored
  output centroid." → [patent-DB rows pending]
- INV-4 independent claim (method): "A method of detecting machine-generated
  content by measuring variance across a set of artifacts and withholding any
  per-artifact classification." → [patent-DB rows pending]

## Remaining steps (the actual gate)

1. Run `docs/portfolio/patent-prior-art-doctrine.md` keyword set against patent
   databases (Google Patents, USPTO, EPO) — NOT just arXiv.
2. Complete the claim-chart rows above with cited patent numbers.
3. Verdict per invention: novel / partially / blocked.
4. If novel: defensive-publication vs filing recommendation. Else: documented
   kill of the patent claim. Until then, **no public novelty assertion.**
