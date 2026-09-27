# Disease Frame Rule v1

**Status:** NORMATIVE — machine-readable source: `config/big0f-frame-rule.v1.json`
**Sealed:** in the protocol registration, **before** any cutoff/horizon predicate is computed.

The frame for cutoff T is a deterministic function of this rule and of pinned as-of-T releases. It contains no judgement per disease, which removes the "frame variants" grinding route.

## 1. Construction of frame(T)

1. **Vocabulary.** MeSH descriptors from the release in force on T (year(T) MeSH).
2. **Included trees.** C (Diseases) and F03 (Mental Disorders), **excluding**:
    - C01 (infections — pathogen genetics);
    - C04 (neoplasms — somatic regime);
    - C16 (congenital, hereditary and neonatal — Mendelian-dominated);
    - C21, C22, C25 and C26 (environmental, animal, chemically induced, injuries);
    - C23 (signs, symptoms and pathological conditions — not disease concepts).
3. **Common-complex filter.** ≥ 500 PubMed records dated ≤ T indexed with the descriptor itself (not exploded to descendants), **and** the descriptor is not under "Genetic Diseases, Inborn" in the year(T) tree.
4. **Multiple tree numbers.** A descriptor qualifies only if at least one of its tree numbers is in an included tree **and** none of its tree numbers is in an excluded tree.
5. **Disease family.** A frame disease's family is the top-level category of its first qualifying tree number (e.g. C10, C14, F03). This defines the clusters for the disease-family block bootstrap and SENS-FAMILY.
6. **Hierarchy resolution.** When a descriptor and one of its descendants both qualify, keep only the **most specific** qualifying descriptor. This prevents two frame diseases sharing the same events.
7. **Ordering.** Sort by descriptor UI and serialize canonically. The digest of that serialization is the frame digest.

## 2. Coverage-eligible frame

frame_cov(T) ⊆ frame(T) contains the diseases whose HistoricalGeneticSearchCoverage at T is ≥ MODERATE. Grades are defined in `config/big0f-adjudication-policy.v2.json` and computed from pinned sources restricted to first public availability ≤ T.

Pilot sampling and the untouched confirmatory pool are drawn only from frame_cov(T\*). E1-NOVEL-STRICT is undefined for diseases below MODERATE coverage.

## 3. What the rule deliberately does not do

- It does not use any post-T information, event counts or disease fame.
- It does not allow manual additions. Showcase cases are governed by [BIG_0F_SELECTION_CUSTODY.md](BIG_0F_SELECTION_CUSTODY.md) §4.
