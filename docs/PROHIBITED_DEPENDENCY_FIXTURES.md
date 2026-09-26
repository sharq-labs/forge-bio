# Prohibited Dependency and Leakage Fixtures

**Status:** NORMATIVE PRE-CODE V1

These fixtures are deliberate failure cases. Verification must demonstrate that the architecture rejects or detects them.

## F-01 — Direct FutureEvent import

**Setup:** ranking module imports outcome repository or FutureEvent store.

**Expected:** dependency/import contract fails.

## F-02 — Future row sentinel

**Setup:** add a post-cutoff evidence record to a Past provider snapshot.

**Expected:** strict historical features/ranking are unchanged; temporal audit records REFUSE/UNKNOWN as appropriate.

## F-03 — Current ontology in historical normalization

**Setup:** historical feature builder silently uses a current ontology release whose watermark > T.

**Expected:** derived artifact is inadmissible.

## F-04 — Modern identity bridge in ranking

**Setup:** ranker imports evaluation-only modern identifier reconciliation.

**Expected:** import/dependency wall fails.

## F-05 — Modern L2G creates gene label

**Setup:** a 2011 locus is assigned to a gene solely by a 2026 knowledge-bearing L2G model.

**Expected:** strict gene-level outcome is not POSITIVE; assignment is AMBIGUOUS/contaminated unless separately qualified.

## F-06 — Old paper, new annotation

**Setup:** a 2008 paper is converted to a structured target claim by a 2026 knowledge-bearing annotator and stamped 2008.

**Expected:** representation watermark remains 2026/UNKNOWN; strict admission fails for T<2026.

## F-07 — Duplicate evidence through multiple databases

**Setup:** one experiment appears in three databases.

**Expected:** one IndependenceFamily, not three independent supports.

## F-08 — Participant-overlap replication

**Setup:** two genetic studies share material participants.

**Expected:** not counted as independent replication under a policy requiring independent cohorts.

## F-09 — UNKNOWN overlap treated as independent

**Setup:** cohort lineage is missing.

**Expected:** independence state remains UNKNOWN; strict independent-replication endpoint fails closed.

## F-10 — False novelty from incomplete Past source

**Setup:** primary Past source lacks a pre-T paper, but HistoricalNoveltyAudit finds it.

**Expected:** candidate becomes KNOWN_AT_T, not E1-NOVEL.

## F-11 — Zero-event disease deletion

**Setup:** evaluation code drops a disease after discovering it has no qualifying future event.

**Expected:** metric/benchmark verification fails unless the frozen estimand explicitly permits the exact transformation.

## F-12 — Outcome-aware endpoint tuning

**Setup:** sealed errors are inspected and endpoint quality threshold is changed.

**Expected:** lockbox generation is marked spent; result is exploratory or requires a new sealed generation.

## F-13 — Research-attention surrogate

**Setup:** biological ranker performance disappears when compared with attention momentum/discoverability control.

**Expected:** no biological discovery claim is earned.

## F-14 — Sealed adjudicator sees rank

**Setup:** borderline outcome classification is performed with candidate rank visible despite a blinded policy.

**Expected:** adjudication deviation is logged and confirmatory status may be invalidated.

## F-15 — Current "latest" provider

**Setup:** adapter resolves an unversioned current/latest endpoint during a historical run.

**Expected:** confirmatory execution refuses to start.

## F-16 — Hash before canonical serialization

**Setup:** unordered map/set serialization produces different artifact hashes for equivalent scientific content.

**Expected:** canonical-hash golden test fails.

## F-17 — Modern hard-coded biomedical constant

**Setup:** 2026 curated gene list is added to a generic-looking config.

**Expected:** watermark becomes 2026/UNKNOWN, not NON_KNOWLEDGE_BEARING.

## F-18 — Technology claim inflation

**Setup:** a modern algorithm uses only historical biomedical inputs and report text says "this exact system could have run in 2010".

**Expected:** claims linter/report review rejects the technology-contemporaneous statement unless separately established.


## F-19 — Suggestive pre-T signal mislabeled novel

**Setup:** candidate has preregistered suggestive pre-T genetics and later crosses the endpoint threshold.

**Expected:** E1-MATURATION, never E1-NOVEL-STRICT.

## F-20 — Related trait promoted to disease endpoint

**Setup:** future GWAS supports a biomarker, risk factor, or related trait rather than the benchmark disease.

**Expected:** OutcomePhenotypeMatchPolicy blocks the primary disease endpoint unless the frozen relation policy explicitly qualifies it.

## F-21 — Replication direction conflict

**Setup:** a later study maps to the same locus but the harmonized effect direction conflicts with the pre-T association.

**Expected:** replication verdict is DIRECTION_CONFLICT/INCONCLUSIVE, not REPLICATED.

## F-22 — Validation-set adaptive reuse

**Setup:** validation generation V1 is inspected, model/features are changed, then V1 is reported as untouched validation.

**Expected:** generation status becomes SPENT_FOR_MODEL_SELECTION and the untouched claim fails.

## F-23 — Moving Future Outcome snapshot

**Setup:** outcome provider changes from release R1 to R2 after MAP/ranking freeze.

**Expected:** evaluation refuses the silent substitution; R2 requires a new committed outcome artifact/generation.

## F-24 — Unblinded sealed adjudication

**Setup:** strongest L3 outcome adjudicator sees candidate rank/order during sealed label adjudication.

**Expected:** strongest confirmatory tier is automatically downgraded.

## F-25 — Cross-disease dependence hidden by ordinary bootstrap

**Setup:** apparent lift is concentrated in one related disease family sharing biology/cohorts.

**Expected:** disease-family/block sensitivity is reported; ordinary disease-level CI alone is insufficient for interpretation.
