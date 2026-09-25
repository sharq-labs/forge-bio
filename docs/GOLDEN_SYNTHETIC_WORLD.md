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

### F2 — E1-REPLICATION candidate
- disease D1
- gene G2
- independent cohort replicates association in 2012
- pre-T suggestive signal E-H2 exists
- subtype = E1-REPLICATION, not E1-NOVEL

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
8. E1-NOVEL and E1-REPLICATION remain distinguishable;
9. D2 is not silently removed because it has zero future events;
10. replacing a generic hashing implementation must not move a biomedical watermark;
11. converting an old paper with a 2026 knowledge-bearing annotation carries the 2026/UNKNOWN derivation watermark;
12. ranking/config digest is deterministic across repeated runs.

## 8. Expected role in implementation

The first implementation of kernel/temporal/identity/evidence/outcome/benchmark modules must be able to encode this world without special-case production logic.

It is intentionally tiny enough for golden tests and code review.
