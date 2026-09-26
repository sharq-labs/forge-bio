# Forge Bio Glossary

**Status:** NORMATIVE PRE-CODE V1

This glossary defines terms that must not be used interchangeably.

## Scientific objects

**Entity** — an immutable internal scientific identity such as a disease concept, gene, protein, pathway, active moiety, publication, or study.

**Representation** — a versioned name, identifier, ontology record, mapping, annotation, or other description of an entity.

**Claim** — a structured proposition about scientific entities and context.

**EvidenceRecord** — a source-backed observation bearing on a claim.

**Hypothesis** — a research proposition to be prioritized or evaluated. A model score is not evidence.

**Target** — a disease/context-specific therapeutic role, not a universal entity type.

**CandidateUniverse** — the immutable set of entities/hypotheses eligible to be ranked for one benchmark under an as-of-T inclusion policy.

**HistoricalKnowledgeView** — the frozen, read-only capability containing only benchmark-approved model-visible scientific knowledge for cutoff T.

## Time and historical validity

**Cutoff T** — the historical boundary used to determine what biomedical knowledge may be model-visible.

**First publicly available interval** — the earliest defensible interval during which information was publicly obtainable in the form relevant to the study.

**AvailabilityAttestation** — provenance-backed evidence supporting a public-availability interval.

**KnowledgeWatermark** — the latest biomedical knowledge a knowledge-bearing artifact could encode. It is not the code creation date.

**STRICT_HISTORICAL** — operating mode in which every model-visible knowledge-bearing dependency is defensibly admissible by T.

**RECONSTRUCTED_HISTORICAL** — historical state reconstructed from later/current sources under an explicit reconstruction policy and fidelity assessment.

**CONTAMINATED_MODERN_PRIOR** — historical explicit inputs combined with a later or unknown-horizon knowledge-bearing representation/model.

**KNOWLEDGE_HISTORICAL** — biomedical knowledge visible to the method is admissible by T.

**TECHNOLOGY_CONTEMPORANEOUS** — the complete computational method could realistically have been implemented with technology available at T. This is a stronger and separate claim.

## Outcomes and labels

**FutureEvent** — a provenance-bearing event in the Future/Outcome plane from which endpoint-specific labels may be derived.

**Endpoint** — the predeclared future event definition used to evaluate a ranking.

**PreTGeneticState** — frozen historical assessment of whether the candidate has NO_SIGNAL_OBSERVED, SUGGESTIVE, QUALIFYING, or AMBIGUOUS pre-T human genetic evidence under the benchmark policy.

**E1-NOVEL-STRICT** — qualifying post-T human genetic support only when PreTGeneticState = NO_SIGNAL_OBSERVED and HistoricalNoveltyAudit = NOVEL_CONFIRMED.

**E1-MATURATION** — a pre-T suggestive genetic signal later crosses the qualifying endpoint threshold. It is not de novo discovery.

**E1-REPLICATION** — qualifying independent post-T replication of a pre-existing association under the GeneticReplicationPolicy.

**E1-CROSSMODAL** — a pre-T non-genetic ranking evaluated against later qualifying human genetic support.

**KNOWN_AT_T** — the endpoint or a declared stronger equivalent was already established by T.

**UNKNOWN** — available information does not establish the required state. UNKNOWN is not negative, safe, zero, or absent.

**RIGHT_CENSORED** — the full endpoint horizon cannot be observed.

**COMPETING_EVENT** — another event prevents interpretation of the primary endpoint under the benchmark policy.

**OutcomeGeneAssignmentPolicy** — governed policy for determining when locus/variant-level human genetic evidence may support a gene-level outcome.

**OutcomePhenotypeMatchPolicy** — governed policy for determining whether a future disease/trait phenotype is scientifically equivalent enough to the benchmark disease to count for the primary endpoint.

**GeneticReplicationPolicy** — governed policy for deciding whether a later genetic study is a genuine replication based on phenotype, locus/variant, allele harmonization, effect direction, population, cohort independence, overlap, and related comparability.

**HistoricalNoveltyAudit** — evaluation-side audit verifying the pre-T signal state and whether a purported strict-novel outcome had already been observed before T.

**ValidationGeneration** — versioned validation case/outcome set with access count and ACTIVE / SPENT_FOR_MODEL_SELECTION / RETIRED state.

**OutcomeSnapshotCommitment** — immutable commitment to the exact future-outcome releases, ledger, adjudication batch, and evaluation identity bridge used for evaluation.

## Bias and governance

**Research attention** — historical scientific interest/popularity, commonly approximated through publication or co-mention activity.

**Discoverability / observation propensity** — the probability that a candidate will receive a future observable endpoint because of study opportunity, statistical power, measurability, annotation, funding, or related non-biological factors.

**Ascertainment bias** — distortion caused by non-random observation/recording of outcomes.

**Researcher hindsight / design-time leakage** — future knowledge influencing benchmark design, feature choice, case selection, thresholds, or adjudication even when future databases are technically isolated.

**BenchmarkDesignProvenance** — record of designers, roles, future-outcome exposure, disease exposure, freeze points, and deviations for a benchmark generation.

**Lockbox** — future labels/cases held under access controls so ranking/model decisions are frozen before evaluation.

**Development / Validation / Sealed Lockbox** — benchmark access tiers. Once sealed individual errors influence methodology, that lockbox generation is spent for future confirmatory claims.

## Statistics

**Estimand** — the exact population-level quantity a study intends to estimate, including disease/candidate population, weighting, endpoint, horizon, and handling of zero-event cases.

**Primary metric** — the single preregistered headline statistic used for the primary claim.

**Multiplicity policy** — the preregistered rule governing interpretation of multiple endpoints, metrics, cutoffs, subgroups, and sensitivity analyses.

**Calibration** — agreement between predicted probabilities and observed frequency for a precisely defined endpoint/horizon. Ranking scores are not probabilities unless calibrated.

## Evidence independence

**IndependenceFamily** — lineage grouping indicating observations that share an originating study, cohort, dataset, consortium, participant set, or experiment.

**Independent replication** — evidence whose relevant lineage is sufficiently independent under the endpoint policy. Different database rows or publications do not automatically imply independence.

**Representation-time provenance** — provenance of when and how a structured annotation/assignment was created, separate from the date of the underlying primary observation.
