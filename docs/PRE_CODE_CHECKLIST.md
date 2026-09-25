# Pre-Code Readiness Checklist

**Status:** ACTIVE  
**Rule:** no production scientific implementation begins until all P0 items are closed.

## P0 — must close before core coding

- [x] Product scientific scope defined.
- [x] Past/Future scientific planes separated.
- [x] UNKNOWN is first-class and fail-closed.
- [x] Target defined as a hypothesis role, not a universal entity.
- [x] Evidence method separated from source channel.
- [x] CandidateUniverse separated from HistoricalKnowledgeView.
- [x] KnowledgeWatermark separated from implementation provenance.
- [x] AvailabilityAttestation defined.
- [x] Field-level provider qualification defined.
- [x] Historical disease sampling-frame rule defined.
- [x] Future-event independence requirement defined.
- [x] Canonical hashing/serialization policy defined.
- [x] Minimal contradiction primitive moved before first benchmark.
- [x] Nested temporal supervised-training policy defined.
- [x] Reconstruction Fidelity Study is a formal gate.
- [x] Coverage/UNKNOWN thresholds must be frozen in MAP.
- [ ] ADR-005 licensing posture decided by project owner.
- [ ] B-TGT-E1-v0 endpoint quality rule chosen after provider/outcome feasibility audit.
- [ ] Initial H candidate set and feasibility procedure accepted.
- [ ] Initial lockbox custodian/storage mechanism chosen.

## P1 — close before sealed confirmatory run

- [ ] ProviderCards complete for every Past source.
- [ ] Future outcome sources qualified independently.
- [ ] Disease sampling frame frozen from as-of-T criteria.
- [ ] Candidate universe policy frozen.
- [ ] Development/validation/sealed split frozen.
- [ ] Coverage thresholds frozen.
- [ ] Sample-size/event-yield feasibility completed on development sources.
- [ ] Primary K and success threshold chosen on development data only.
- [ ] Paired disease-level CI method frozen.
- [ ] MAP hash frozen.
- [ ] Lockbox credentials unavailable to ranking process/team path.
- [ ] Ranking artifact commitment mechanism tested.
- [ ] Reconstruction fidelity verdicts available for conditional providers.
- [ ] Identity gold-set error rate reported.
- [ ] Temporal metamorphic test suite passes.

## Sample-size / feasibility rule

Before freezing the sealed benchmark, use only development-visible information to estimate:
- number of diseases;
- candidate counts;
- event prevalence;
- censoring;
- expected CI width;
- sensitivity to K.

This is a feasibility analysis, not permission to inspect sealed outcomes.

If expected uncertainty is too wide to distinguish the model from the attention baseline, expand or redesign the benchmark before lockbox use.

## Lockbox custody rule

A Git hash alone is not custody.

SEALED_LOCKBOX requires:
- separate storage/schema or encrypted artifact;
- separate credentials from ranking runtime;
- append-only access event log;
- named custodian/process;
- MAP hash + ranking hash before opening;
- benchmark generation retirement after outcome-driven methodology changes.

## Go/no-go rule

GO FOR CORE CODE only when all P0 items are closed.

GO FOR SEALED CONFIRMATORY RUN only when all P1 items are closed.

A failed gate changes the plan; it is not bypassed to keep schedule.
