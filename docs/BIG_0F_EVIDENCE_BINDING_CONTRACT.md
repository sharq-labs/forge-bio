# BIG 0F Evidence Binding Contract

**Status:** NORMATIVE PRE-CODE CONTRACT — SPEC-CLOSED / IMPLEMENTATION-PENDING (no verifier exists yet; see [SEMANTIC_INVARIANTS.md](SEMANTIC_INVARIANTS.md))

## Provider audit

A GO-capable provider audit must include all four mandatory source-family kinds:
1. primary publication/publication metadata (`PRIMARY_PUBLICATION_METADATA`);
2. historical GWAS/summary-statistic source (`GWAS_HISTORICAL`);
3. identity/ontology source (`IDENTITY_ONTOLOGY`);
4. historical gene-model/annotation source (`HISTORICAL_GENE_MODEL_ANNOTATION`).

Four arbitrary providers or four `OTHER` entries do not satisfy this requirement.

The provider audit scope is mechanically derived, not chosen: the selected pilot diseases in the bound selection provenance crossed with every field in `config/big0f-required-field-registry.v1.json` (scope rule `SELECTED_PILOT_DISEASES_CROSS_ALL_REGISTRY_FIELDS`; no subset, no optional fields). It is recorded with `schemas/big0f-provider-audit-scope.v2.schema.json`, binds the registry and selection-provenance digests, and is committed by digest before availability is inspected. The audit itself (`schemas/big0f-provider-audit.v2.schema.json`) binds the scope, registry and selection-provenance digests. Every source-family release and every required-field audit cell must carry an immutable provenance/evidence digest.

Required-field availability, coverage summaries, source-family counts, provider coupling, and ancestry coverage must be regenerable from the bound audit artifact.

## Applicability / ancestry

Each ancestry/population case record must identify its metadata source and provenance digest. The adequacy rule itself has a frozen ID and digest. Adequacy is a derived decision under that frozen rule, not a free scalar assertion.

## Symmetric event/non-event curation audit

The exact event case set, non-event case set, and duplicate-review selection are each committed by digest before burden summaries are accepted. The duplicate-review selection is the **salted** keyed-hash selection of adjudication policy v2, stratified by disease. It must be recomputable from the sealed key and the custodian review salt. The salt is committed in S6 and revealed only after the first-review label set is registered (INV-A3; custody §7; `schemas/big0f-curation-audit.v2.schema.json`).

Both event and non-event case records must store:
- minutes;
- historical-search status: RESOLVED / UNKNOWN / AMBIGUOUS / UNUSABLE;
- source-family IDs used;
- provenance digest;
- whether the case received duplicate review;
- duplicate-review outcome.

For non-events, duplicate review is no longer an optional narrative phrase. The target is:
```text
min(N_non_event, max(30, ceil(0.30 * N_non_event)))
```

The audit must report duplicate-review count/fraction, disagreement fraction, the preregistered agreement statistic (Gwet AC1, adjudication policy v2; κ is reported only), confusion-matrix digest, UNKNOWN fraction, and AMBIGUOUS fraction.

If the frozen duplicate-review minimum is not reached, the pilot is `INCONCLUSIVE` rather than silently waiving the requirement.

## Adjudicator independence

The second-adjudicator artifact must bind role-registry identity, independence evidence, conflicts, blinding commitments, assignment time, and digest. A bare reviewer ID is not sufficient.

The independent selection custodian carries the same kind of attestation (`schemas/big0f-adjudicator-independence.v1.schema.json`, role `SELECTION_CUSTODIAN`; [BIG_0F_SELECTION_CUSTODY.md](BIG_0F_SELECTION_CUSTODY.md) §1).

## Failure rule

Any GO-critical summary that cannot be regenerated from its underlying evidence artifact is `INCONCLUSIVE` and cannot support GO.

The reference list of artifacts the pilot result must bind by digest is `bound_artifacts` in `schemas/big0f-pilot-result.v2.schema.json`. Besides the audits above, it includes the protocol and seal bundle, threshold manifest v2, adjudication policy v2, nuisance manifest v2, power policy v2, outcome-discovery spec and run, recall audit, frame rule, required-field registry, selection registration and provenance, randomness beacon, nuisance run, power analysis, custodian independence attestation, exposure ledger and release log.
