# Golden Synthetic Biomedical World

**Status:** NORMATIVE PRE-CODE V1  
**Purpose:** Small deterministic fixture for temporal, identity, evidence, outcome, and benchmark tests.

## 1. Cutoff

```text
T = 2010-12-31
H = 5 years
```

## 2. Diseases

```text
D1 = Alpha disease
    known by T
    common-complex germline regime

D2 = Beta disease
    known by T
    common-complex germline regime
    has zero qualifying future E1 events within H

D3 = Gamma disease
    modern subtype created after T
    parent disease existed at T
```

D3 tests disease-representation leakage. The modern subtype is not model-visible at T unless a historical representation exists.

## 3. Genes and mappings

```text
G1 = Gene One
    historical ID HG:001
    modern ID MG:101
    exact historical mapping available by T

G2 = Gene Two
    historical ID HG:002
    modern rename after T
    evaluation bridge may reconcile identity

G3 = Gene Three
    one-to-many ambiguous historical alias
    must remain ambiguous

G4 = Gene Four
    first represented in provider after T
    not eligible for strict CandidateUniverse(T)
```

## 4. Historical evidence

### E-H1
- D1–G1 functional support
- publicly available: 2008-06-01
- admitted
- no pre-T qualifying human genetic support

### E-H2
- D1–G2 suggestive human genetic association
- publicly available: 2009
- year precision
- admitted at T
- does not meet strong replication endpoint

### E-H3
- D1–G3 pathway evidence
- nominal provider date 2009
- availability interval crosses T because source history is uncertain
- decision: UNKNOWN in strict mode

### E-H4 — future sentinel
- D1–G1 strong genetic evidence
- publicly available: 2012
- any appearance in historical features must fail tests

## 5. Future events

### F1 — E1-NOVEL candidate
- disease D1
- post-T locus discovered in 2012
- direct coding evidence establishes G1 in 2013
- no qualifying pre-T genetics after novelty audit
- gene-level positive may be accepted under assignment policy

### F2 — E1-MATURATION candidate
- disease D1
- gene G2
- pre-T suggestive signal E-H2 exists
- larger post-T study crosses the endpoint threshold in 2012
- this is E1-MATURATION, not E1-NOVEL-STRICT

### F2b — E1-REPLICATION candidate
- disease D1
- gene G2
- a separate post-T cohort reproduces the pre-existing association
- phenotype/locus/allele/direction handling is compatible
- cohort/sample independence passes
- subtype = E1-REPLICATION

### F3 — modern-assignment trap
- disease D1
- locus appears in 2011
- gene G3 assigned only by a knowledge-bearing 2026 L2G model
- strict gene-level label = AMBIGUOUS / not qualifying
- current learned assignment must not create a historical gene-level positive

### F4 — duplicate-source trap
- same originating cohort appears in two databases and two publications
- independence_family must collapse them to one evidence family

### F5 — overlap trap
- two studies share a participant-overlap group
- UNKNOWN/known material overlap prevents counting as independent replication under strict policy

### F6 — zero-event disease
- D2 has no qualifying E1 event in (T,T+H]
- D2 remains in the frozen disease sampling frame
- metric engine follows the frozen zero-event estimand policy rather than deleting D2 post hoc
- D2 contributes to all-frame review-budget accounting without being labelled biologically negative

### F7 — phenotype mismatch trap
- benchmark disease = D1
- future GWAS is for a related biomarker/risk-factor phenotype, not D1
- relation = RISK_FACTOR
- event does not qualify for the primary D1 endpoint

### F8 — replication direction-conflict trap
- same locus/compatible variant relation as a pre-T signal
- post-T effect direction is inconsistent after allele harmonization
- verdict = DIRECTION_CONFLICT, not REPLICATED

### F9 — moving outcome snapshot trap
- outcome provider release R1 is committed before evaluation
- release R2 later changes a mapping/adjudicated event
- R2 cannot silently replace R1 in the same benchmark generation

### F10 — spent validation generation
- validation generation V1 is inspected and methodology changes
- V1 status becomes SPENT_FOR_MODEL_SELECTION
- V1 is not described as untouched validation thereafter

## 6. Candidate universe at T

Expected eligible genes for D1/D2:

```text
G1
G2
G3 only if identity eligibility itself is resolved independently of E-H3
```

G4 is excluded because historical eligibility is not established by T.

Universe order and digest must be deterministic.

## 7. Required verification tests

1. adding/removing E-H4 cannot change historical ranking;
2. G4 cannot enter CandidateUniverse(T);
3. modern rename of G2 may reconcile outcome identity but cannot change historical features;
4. G3 ambiguous alias is not coerced to EXACT;
5. F3 cannot become strict gene-level POSITIVE through modern L2G alone;
6. duplicate F4 records count as one independence family;
7. F5 overlap is not independent replication;
8. E1-NOVEL-STRICT, E1-MATURATION, and E1-REPLICATION remain distinguishable;
9. suggestive pre-T genetics cannot qualify as E1-NOVEL-STRICT;
10. D2 is not silently removed because it has zero future events and appears in all-frame utility accounting;
11. F7 risk-factor phenotype cannot qualify as an exact disease endpoint;
12. F8 direction conflict cannot count as replication;
13. F9 provider release change cannot mutate the committed outcome snapshot in-place;
14. F10 validation reuse marks the generation spent;
15. replacing a generic hashing implementation must not move a biomedical watermark;
16. converting an old paper with a 2026 knowledge-bearing annotation carries the 2026/UNKNOWN derivation watermark;
17. ranking/config digest is deterministic across repeated runs.

## 8. Expected role in implementation

The first implementation of kernel/temporal/identity/evidence/outcome/benchmark modules must be able to encode this world without special-case production logic.

It is intentionally tiny enough for golden tests and code review.
