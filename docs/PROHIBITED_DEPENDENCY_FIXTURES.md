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

**Expected:** candidate becomes KNOWN_PUBLICLY_AT_T / KNOWN_AT_T, not E1-NOVEL-STRICT; provider coverage failure is recorded.

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


## F-26 — Raw rsID/coordinate used as variant identity

**Setup:** two representations of the same allele on different genome assemblies are treated as different variants.

**Expected:** genomic identity verification fails; canonical variant resolution/harmonization is required.

## F-27 — Silent modern liftover/harmonization

**Setup:** historical genetic evidence is normalized with a modern assembly/reference mapping but the transformation is not provenance/watermark-bearing.

**Expected:** strict run fails verification.

## F-28 — Ambiguous allele orientation forced

**Setup:** allele/strand orientation cannot be resolved but effect direction is coerced anyway.

**Expected:** replication classification fails closed as AMBIGUOUS/INCONCLUSIVE.

## F-29 — Unversioned LD proxy

**Setup:** replication treats two variants as equivalent using an unspecified reference panel/population/threshold.

**Expected:** replication endpoint is invalid.

## F-30 — Low search coverage labeled strict novel

**Setup:** no pre-T signal is found for a poorly covered disease/candidate and state is set to NO_SIGNAL_OBSERVED.

**Expected:** coverage gate forces AMBIGUOUS below the MAP threshold.

## F-31 — Ranker-missed public pre-T knowledge labeled novel

**Setup:** historical provider misses a qualifying pre-T public result.

**Expected:** HistoricalNoveltyAudit returns KNOWN_PUBLICLY_AT_T; case is provider coverage failure, not E1-NOVEL-STRICT.

## F-32 — One locus creates multiple primary hits

**Setup:** one discovery locus has three gene assignments and all three are counted as independent future events.

**Expected:** ScientificEventFamily credit rule prevents multiplied primary event credit.

## F-33 — Same discovery repeated across rolling anchors

**Setup:** one ScientificEventFamily appears in four overlapping training windows with full weight each.

**Expected:** CrossAnchorEventReusePolicy caps/group-weights the total contribution and reports effective sample size.

## F-34 — Same curation pipeline on both benchmark planes

**Setup:** Past features and Future labels are generated by materially shared curation/upstream-source machinery with no coupling sensitivity.

**Expected:** confirmatory interpretation fails until provider-coupling assessment/sensitivity is run.

## F-35 — Free-text cohort aliases create false independence

**Setup:** the same SampleSet appears under two cohort/dataset names.

**Expected:** identity/lineage resolution collapses the aliases; strict replication cannot count them as independent.

## F-36 — Outcome discovery continues after rank reveal

**Setup:** adjudicators search for additional sealed FutureEvents after seeing model rank/order.

**Expected:** strongest L3 status is automatically downgraded.

## F-37 — Future-fit preprocessing statistics

**Setup:** scaler/imputer/vocabulary/background statistic is fit on records after the training anchor.

**Expected:** training artifact is temporally contaminated and fails closed.

## F-38 — Operating mode/data-policy enum collision

**Setup:** RECONSTRUCTED_HISTORICAL or CONTAMINATED_MODERN_PRIOR is passed as if it were a ScientificOperatingMode/HistoricalDataPolicy interchangeably.

**Expected:** configuration schema/runtime rejects the invalid enum combination.


## F-39 — Static graph mislabeled predictive digital twin

**Setup:** a static disease/pathogen graph has no dynamic state model or predictive validation but is labelled T3.

**Expected:** maturity validation rejects the claim; artifact remains T0/T1 according to its actual capabilities.

## F-40 — Disease and pathogen identity collapse

**Setup:** a virus/pathogen entity is stored as the infectious disease itself.

**Expected:** identity verification fails; pathogen and disease remain separate entities linked by evidence-backed claims.

## F-41 — Pathogen-only model overclaims host-disease behavior

**Setup:** pathogen state is modeled, but host receptor/immune/tissue state is absent; output is presented as a validated disease-behavior twin.

**Expected:** applicability/claim validation fails; PathogenHostScientificTwin is required for that claim scope.

## F-42 — Future evidence contaminates historical twin

**Setup:** Twin(subject, T) imports a post-T mechanism, pathogen lineage, therapeutic event, or parameter fitted on post-T data.

**Expected:** watermark/temporal verification fails closed.

## F-43 — Mechanistic simulation promoted to predictive validation

**Setup:** a T2 model reproduces fitted/training observations but has no held-out/future validation and is labelled T3.

**Expected:** maturity remains T2.

## F-44 — Intervention simulation promoted to efficacy evidence

**Setup:** a computational perturbation produces a favorable simulated state and is stored as evidence that a treatment works.

**Expected:** claim/evidence verification rejects the transformation; simulation remains a research hypothesis.

## F-45 — Patient-specific treatment inference from platform twin

**Setup:** a disease/pathogen/therapeutic twin is used to generate patient-specific treatment or dosing output under V1 Context of Use.

**Expected:** Context-of-Use validation rejects execution.


## F-46 — Future mechanism hidden in historical state-model topology

**Setup:** Twin(subject, 2010) uses a state-model structure manually designed from a mechanism first established after 2010 while numeric parameters use only pre-2010 data.

**Expected:** state-model artifact watermark exceeds cutoff or is UNKNOWN; STRICT_HISTORICAL twin construction fails closed.

## F-47 — Predictive twin without MAP/MAR validation governance

**Setup:** an artifact declares T3 but has no prediction spec, MAP, MAR, ValidationGeneration, or BenchmarkDesignProvenance.

**Expected:** JSON Schema rejects the artifact.

## F-48 — Non-identifiable T4 intervention

**Setup:** a T4 artifact includes a perturbation but IdentifiabilityStatus is NOT_IDENTIFIED or UNKNOWN.

**Expected:** JSON Schema rejects T4 maturity; output may remain exploratory T2/T3 simulation only.

## F-49 — Twin prediction written back as evidence

**Setup:** model prediction/simulation output is inserted into EvidenceRecord and later consumed as if independent biological evidence.

**Expected:** dependency/claim verification rejects the cycle.

## F-50 — Historical profile without cutoff

**Setup:** a STRICT_HISTORICAL disease/pathogen/therapeutic profile omits cutoff T.

**Expected:** profile JSON Schema rejects the artifact.


## F-51 — Unitless value used where physical unit is required

**Setup:** a concentration-like observation is marked OBSERVED with unit_required=true but no unit/dimension.

**Expected:** quantitative schema rejects the artifact.

## F-52 — Missing observation coerced to zero

**Setup:** value_state=MISSING while value=0 is supplied as an observed measurement.

**Expected:** quantitative schema rejects the artifact / implementation fails closed.

## F-53 — Custom transform without transform provenance

**Setup:** transform=CUSTOM with no TransformArtifact reference.

**Expected:** quantitative schema rejects the artifact.

## F-54 — Numerically unverified mechanistic simulation declared adequate

**Setup:** NumericalVerificationArtifact has convergence_study=FAIL/UNKNOWN while verdict=ADEQUATE.

**Expected:** schema rejects ADEQUATE verdict.

## F-55 — Universal credibility claim

**Setup:** model is described as "validated" without ContextOfUse or research decision/influence/consequence semantics.

**Expected:** CredibilityAssessment schema/policy rejects the claim.

## F-56 — High-risk predictive evaluation labelled adequate despite high risk of bias

**Setup:** credibility conclusion=ADEQUATE_FOR_COU while prediction_risk_of_bias=HIGH.

**Expected:** schema rejects the conclusion.

## F-57 — Recalibrated/changed model inherits old validation

**Setup:** preprocessing, parameters, state-model structure, measurement model, or output-changing solver configuration changes while old validation digest is reused.

**Expected:** validation scope/digest check fails; new validation generation required.

## F-58 — Out-of-domain prediction reported as validated

**Setup:** a T3 model validated on one population/source/measurement regime is applied outside the frozen applicability domain and reported as validated.

**Expected:** applicability audit marks extrapolation; validated-prediction claim fails.
