# BIG 0F Evidence Binding Contract

**Status:** FROZEN PRE-CODE CONTRACT

## Provider audit

A GO-capable provider audit must include all four mandatory source-family kinds:
1. primary publication/publication metadata;
2. historical GWAS/summary-statistic source;
3. identity/ontology source;
4. historical gene-model/annotation source.

Four arbitrary providers or four `OTHER` entries do not satisfy this requirement.

The complete provider audit scope—diseases, mandatory source families, and required fields—is frozen by an audit-scope manifest digest before availability is inspected. Every source-family release and every required-field audit cell must carry an immutable provenance/evidence digest.

Required-field availability, coverage summaries, source-family counts, provider coupling, and ancestry coverage must be regenerable from the bound audit artifact.

## Applicability / ancestry

Each ancestry/population case record must identify its metadata source and provenance digest. The adequacy rule itself has a frozen ID and digest. Adequacy is a derived decision under that frozen rule, not a free scalar assertion.

## Symmetric event/non-event curation audit

The exact event case set, non-event case set, and duplicate-review selection are each committed by digest before burden summaries are accepted.

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

The audit must report duplicate-review count/fraction, disagreement fraction, the preregistered agreement statistic, confusion-matrix digest, UNKNOWN fraction, and AMBIGUOUS fraction.

If the frozen duplicate-review minimum is not reached, the pilot is `INCONCLUSIVE` rather than silently waiving the requirement.

## Adjudicator independence

The second-adjudicator artifact must bind role-registry identity, independence evidence, conflicts, blinding commitments, assignment time, and digest. A bare reviewer ID is not sufficient.

## Failure rule

Any GO-critical summary that cannot be regenerated from its underlying evidence artifact is `INCONCLUSIVE` and cannot support GO.
