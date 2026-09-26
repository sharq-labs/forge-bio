# Lockbox and Benchmark Custody Policy

**Status:** NORMATIVE PRE-CODE V1

## 1. Chosen mechanism

SEALED_LOCKBOX is stored as an encrypted, immutable/versioned benchmark artifact in storage that is not accessible to the ranking runtime or ordinary developer credentials.

The repository stores only:
- lockbox ID;
- generation;
- cryptographic digest/commitment;
- schema/version metadata;
- access-policy reference.

Raw sealed outcomes and sealed disease identities are not committed to the ordinary source repository.

## 2. Roles

### Ranking Team

May access:
- historical providers/snapshots;
- development outcomes;
- validation outcomes under the MAP policy;
- BenchmarkSpec;
- HistoricalKnowledgeView;
- CandidateUniverse.

May not access:
- sealed outcome labels before ranking seal;
- lockbox decryption credentials;
- sealed outcome adjudication workspace.

Responsibilities:
- define/freeze algorithm and feature families;
- produce deterministic ranking artifact;
- seal ranking digest before lockbox evaluation.

### Outcome Adjudication Team

May access:
- future outcome sources;
- evaluation identity bridge;
- HistoricalNoveltyAudit sources;
- OutcomeGeneAssignmentPolicy evidence.

For strongest L3 SEALED_CONFIRMATORY work, **must be blinded to model rank/order for all sealed outcome adjudication**.

If sealed adjudication occurs with rank/order visible, the evaluation is automatically downgraded from the strongest confirmatory tier.

Responsibilities:
- construct/adjudicate FutureEvents;
- record ambiguity and lineage;
- never alter ranker features/configuration.

### Lockbox Custodian

Holds or controls the mechanism that releases sealed benchmark artifacts for evaluation.

May not change:
- MAP;
- candidate universe;
- endpoint rules;
- ranking artifact.

Responsibilities:
- verify frozen MAP digest;
- verify ranking artifact digest;
- log access/release;
- retire generation after outcome-driven methodology changes.

The project owner may temporarily fill the custodian role before a larger team exists, but the role and access event remain explicit.

## 3. Sealed disease identity policy

For the strongest retrospective confirmatory tier:
- sealed disease identities are hidden from the Ranking Team while methodology/feature families are being designed;
- identities may be revealed only after algorithm/configuration and evaluation protocol are frozen;
- if this separation is operationally impossible, the benchmark is explicitly downgraded and researcher-hindsight risk is reported.

Development/validation disease identities may remain visible.

## 4. Opening protocol

Before any sealed outcome release:

1. verify MAP status = FROZEN;
2. verify MAP digest;
3. verify benchmark generation;
4. verify CandidateUniverse digest;
5. verify validation-generation identity/status;
6. verify Future Outcome snapshot/ledger/adjudication/identity-bridge commitments;
7. verify ranking artifact digest;
8. verify benchmark exposure lifecycle is ACTIVE_CONFIRMATORY for strongest-tier claims;
9. verify required ExternalSealAttestation(s);
10. verify sealed adjudication blinding status;
11. record access actor/time/reason;
12. unlock only the evaluation-required artifact;
13. join the two immutable artifacts: sealed ranking + committed Future Outcome snapshot;
14. run evaluation without feeding sealed errors back into the frozen method;
15. append access/result event to custody and BenchmarkExposure ledgers.

## 5. Access log

Each access event records:

```text
access_event_id
lockbox_id
benchmark_generation
actor_role
actor_identity
timestamp
reason
map_digest
ranking_digest
artifact_scope
resulting_status
```

The log is append-only.

## 6. Validation-generation lifecycle

VALIDATION is not infinitely reusable.

Each validation generation records:
- case-set digest;
- outcome-snapshot digest;
- access count;
- maximum disclosure level: AGGREGATE_ONLY / SUBGROUP / PER_CASE / FULL_LABEL;
- ACTIVE / SPENT_FOR_MODEL_SELECTION / RETIRED status.

If validation results materially influence feature, model, endpoint, hyperparameter, threshold, disease, or candidate selection, the generation becomes SPENT_FOR_MODEL_SELECTION.

Spent validation results remain reportable but are not described as untouched evidence.

## 7. Sealed generation retirement and benchmark exhaustion

If individual sealed errors/outcomes are inspected and methodology changes in response:
- current generation becomes DEVELOPMENT_EXPOSED / SPENT_FOR_CONFIRMATORY_REUSE;
- results already obtained remain part of scientific history;
- a new independent sealed generation is required for another strongest-tier confirmatory claim.

Repeated exposure is tracked by a BenchmarkExposureLedger.

Generation lifecycle:

```text
ACTIVE_CONFIRMATORY
DEVELOPMENT_EXPOSED
EXHAUSTED
RETIRED
```

EXHAUSTED generations may be used for regression/development history but not a fresh strongest-tier confirmatory claim.

## 8. Future Outcome commitment

For strongest L3 work, outcome-event discovery and adjudication are completed and committed before model rank/order is revealed.

Before the ranking/outcome join, custody verifies immutable commitments for:
- future outcome source releases;
- Future Outcome snapshot digest;
- outcome-ledger digest;
- ScientificEventFamily ledger digest;
- adjudication-batch digest;
- evaluation identity-bridge digest;
- provider-lineage/input-outcome-coupling assessment digest;
- phenotype-match policy;
- gene-assignment policy;
- replication policy;
- genomic identity/harmonization/LD policy.

Searching for additional sealed outcome events after seeing rank/order automatically downgrades strongest L3 status.

A changed provider release, event-family ledger, adjudication batch, provider-coupling assessment, or evaluation bridge is a new evaluation generation.

## 9. Implementation verification deferred to P1

P0 chooses the custody mechanism and roles.

P1 must verify actual operational controls:
- storage isolation;
- encryption/credential separation;
- access logging;
- ranking-runtime denial;
- recovery procedure;
- branch/spec governance enforcement.


## 10. External sealing and prospective exposure

For strongest confirmatory/prospective work, required digests are externally attested through an independent custodian or timestamp/registration mechanism.

Internal repository hashes remain necessary but are not treated as sufficient evidence of study sequencing on their own.

Prospective PredictionExposureEvents record whether predictions were private, collaborator-shared, or public.

If a prediction could plausibly influence later research activity, resulting evidence is classified by exposure risk and is not automatically counted as clean independent prospective confirmation.

Normative policy: [BENCHMARK_LIFECYCLE_POLICY.md](BENCHMARK_LIFECYCLE_POLICY.md).
