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

**DiseaseScientificProfile** — versioned evidence-backed projection of disease identity, phenotypes, affected tissues/cells, molecular mechanisms, genetics, biomarkers, epidemiology, targets, therapeutic evidence, contradictions, gaps, and uncertainty.

**PathogenScientificProfile** — versioned evidence-backed projection of a pathogen's taxonomy, genome/proteome, strains/variants, host range, tropism, host interactions, lifecycle, immune interactions, resistance, associated disease, and therapeutic evidence.

**PathogenHostScientificProfile** — evidence-backed representation of interactions between a pathogen and host biological system, including receptors/factors, tissue/cell context, immunity, disease mechanisms, and target hypotheses.

**TherapeuticScientificProfile** — versioned evidence-backed representation of a therapeutic entity's identity, modality, targets, mechanism, indication/regulatory history, efficacy/safety evidence, PK/PD evidence, interactions, resistance, and uncertainty.

**ScientificDigitalTwin** — versioned research object built on scientific profiles and evidence state. It earns stronger twin maturity only through explicit dynamic/mechanistic/predictive capability and validation.

**DigitalTwinMaturityLevel** — T0_PROFILE_ONLY, T1_DYNAMIC_KNOWLEDGE_TWIN, T2_MECHANISTIC_TWIN, T3_VALIDATED_PREDICTIVE_TWIN, or T4_VALIDATED_INTERVENTION_SIMULATION_TWIN. T0 is not claimed as a digital twin.

**PathogenHostScientificTwin** — system-of-systems twin combining pathogen state and host biological context; preferred over a pathogen-only predictive twin when host response materially determines disease behavior.

**TwinState** — immutable, versioned state of a ScientificDigitalTwin at a time/cutoff with evidence snapshots, model/parameter artifacts, uncertainty, watermark, and digest.

**TwinValidationArtifact** — versioned verification/validation record supporting a twin maturity claim.

**TwinPerturbation / TwinSimulationResult** — formal research simulation input/output. Simulation output is a hypothesis and is not clinical evidence.

**GenomicVariant** — canonical allele identity against an explicit reference sequence with normalized location/reference/alternate state; an rsID or raw coordinate is only an external representation.

**GenomicLocus** — versioned genomic interval/credible-set concept tied to a genome assembly and locus-definition policy.

**GenomeAssembly / ReferenceSequence** — canonical reference context required to interpret genomic coordinates and alleles.

**VariantHarmonizationArtifact** — provenance-bearing normalization/liftover/strand/allele transformation between variant representations.

**LDRelation** — versioned relationship between variants with population/ancestry, reference panel/release, assembly, metric, value, derivation method, and provenance.

**Cohort / Dataset / Biobank / Consortium / SampleSet** — first-class study/population identities used to reason about sample lineage and independence.

## Time and historical validity

**Cutoff T** — the historical boundary used to determine what biomedical knowledge may be model-visible.

**First publicly available interval** — the earliest defensible interval during which information was publicly obtainable in the form relevant to the study.

**AvailabilityAttestation** — provenance-backed evidence supporting a public-availability interval.

**KnowledgeWatermark** — the latest biomedical knowledge a knowledge-bearing artifact could encode. It is not the code creation date.

**ScientificOperatingMode** — scientific claim-mode axis: STRICT_HISTORICAL, HISTORICAL_INPUT_MODERN_PRIOR, or CURRENT_DISCOVERY.

**STRICT_HISTORICAL** — ScientificOperatingMode in which every model-visible knowledge-bearing dependency is defensibly admissible by T.

**HistoricalDataPolicy** — independent source-state axis: ARCHIVED_ONLY or RECONSTRUCTED_ALLOWED.

**RECONSTRUCTED_ALLOWED** — HistoricalDataPolicy allowing reconstructed historical fields only when the frozen Reconstruction Fidelity gate and watermark rules pass.

**CONTAMINATED_MODERN_PRIOR** — classification of a historical-input run whose model-visible knowledge-bearing dependency has a later/unknown horizon; not a HistoricalDataPolicy value.

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

**HistoricalGeneticSearchCoverage** — provenance-bearing measure of how adequately pre-T genetic evidence could be searched/observed for a disease/candidate; E1-NOVEL-STRICT requires a frozen minimum grade.

**GeneticObservabilityAtT** — as-of-T assessment of whether the candidate/variant classes could realistically be genetically interrogated under the technology/source regime; used as a sensitivity, not a future-driven exclusion.

**KNOWN_TO_RANKER_AT_T** — qualifying pre-T knowledge present in the frozen model-visible historical view.

**KNOWN_PUBLICLY_AT_T** — qualifying pre-T knowledge established as publicly available even if the ranker's provider snapshot missed it.

**ScientificEventFamily** — canonical underlying scientific event grouping multiple manifestations such as preprint, publication, and database rows.

**GeneticDiscoveryEventFamily** — ScientificEventFamily specialized for genetic discovery, retaining disease, locus, studies, and gene assignments.

**ProviderLineage** — upstream-source/curation/ontology/identity-mapping lineage of a provider.

**InputOutcomeCouplingAssessment** — benchmark assessment of shared lineage between Past feature providers and Future outcome providers.

**CrossAnchorEventReusePolicy** — rule bounding repeated training credit from one ScientificEventFamily across overlapping temporal anchors.

**ValidationGeneration** — versioned validation case/outcome set with access count, maximum disclosure level, and ACTIVE / SPENT_FOR_MODEL_SELECTION / RETIRED state.

**ValidationDisclosureLevel** — information granularity exposed from validation: AGGREGATE_ONLY, SUBGROUP, PER_CASE, or FULL_LABEL.

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

**IndependenceFamily** — lineage grouping indicating observations that share an originating study, cohort, dataset, consortium, participant set, or experiment. It answers evidence dependence; it is not the same as ScientificEventFamily, which answers whether records are manifestations of the same underlying event.

**Independent replication** — evidence whose relevant lineage is sufficiently independent under the endpoint policy. Different database rows or publications do not automatically imply independence.

**Representation-time provenance** — provenance of when and how a structured annotation/assignment was created, separate from the date of the underlying primary observation.
