# Semantic Invariants — B-TGT-E1 V0 / BIG 0F

**Status:** NORMATIVE — SPEC-CLOSED / IMPLEMENTATION-PENDING
**Decision record:** [ADR-022](adr/ADR-022-final-scientific-consistency-closure.md)

JSON Schema can check the shape of an artifact but not most of its meaning. This page lists the rules of meaning. Each invariant is also a **regression requirement**: the minimal pre-BIG 0F verification harness must implement one check per ID, with at least one passing fixture and one failing fixture, before BIG 0F starts.

**Enforcement column**

- `SCHEMA`: the JSON Schema in this repository already rejects violations.
- `HARNESS`: the rule is normative now, but only the future harness enforces it.

No invariant marked HARNESS may be described anywhere as machine-enforced until that check exists (INV-D2).

## INV-S — Status, sealing and time

| ID | Invariant | Enforcement |
|---|---|---|
| INV-S1 | Every sealable config has `status` ∈ {SEAL_CANDIDATE, SEALED} and `sealed_by_attestation_id`. `SEAL_CANDIDATE` ⇔ `sealed_by_attestation_id = null`. | SCHEMA (per config) |
| INV-S2 | `SEALED` requires two VERIFIED external-seal attestations over the **same** artifact digest: one PUBLIC_REGISTRY and one THIRD_PARTY_TIMESTAMP_SERVICE. A signed custodian attestation alone never seals. | HARNESS |
| INV-S3 | seal_time(artifact) = max(earliest Bitcoin block time in the verified OTS proof, public-registry registration time). Every "before" relation in the protocol uses seal_time and nothing else. A self-reported `sealed_at`, `created_at` or `frozen_at` never proves order. | HARNESS |
| INV-S4 | A registry record that is embargoed or otherwise not publicly retrievable gives no seal_time. | HARNESS |
| INV-S5 | No artifact contains `frozen_at` or uses FROZEN as a status value. In prose, "frozen" means SPEC-CLOSED. Any claim about **when** something was fixed requires SEALED (Freeze Statement §5). | SCHEMA (configs, estimand, MAP, endpoint rule) / HARNESS (docs grep) |
| INV-S6 | After S1, any change to a sealed artifact creates a new protocol version. The old registration is never overwritten. | HARNESS |
| INV-S7 | The seal bundle binds the digest of every artifact listed in the seal-bundle schema. A one-byte change to any component fails verification. | SCHEMA (required fields) / HARNESS (recompute) |
| INV-S8 | **Public-seal rule.** Every gating registration counts only if its upgraded OTS proof is attached to the public record and a public archive capture exists before the dependent step begins. Gating registrations are S1, S4, S6, BIG 0F results, the Stage B result, the BIG 1 verdict, the endpoint-quality rule, the MAP data-quality values, the MAP, the ranking commitment, the CDR, the §3a refit registration, the confirmatory seal bundle and label sets. Each has **exactly one** registration per generation. After the dependent step, the registration can be neither voided nor re-presented. A later defect means REDESIGN before the MAP seal (α is spent unless the REDESIGN is one of the qualifying mechanical results) and spends α after it. A withheld proof therefore never buys an option. The verifier recomputes the §3a refits deterministically from the committed code and key_c. | HARNESS |

## INV-E — Estimand and metric

| ID | Invariant | Enforcement |
|---|---|---|
| INV-E1 | The primary subtype is `E1-NOVEL-STRICT` and the primary metric is `EVENT_RANK_PERCENTILE_V1` in every V0 estimand, MAP and confirmatory or prospective attempt. | SCHEMA (estimand; MAP V0 conditional; attempt) |
| INV-E2 | The ranking universe U_d excludes every candidate with ScreenSignal ≠ NONE. ScreenSignal is computed from the ranker-visible snapshot only, identically for both arms, before outcomes are opened. | HARNESS |
| INV-E3 | Ranks use mid-rank ties. Any other tie rule makes the run INVALID. | SCHEMA (nuisance run) / HARNESS |
| INV-E4 | The competitor set C_p excludes the genes of other post-T event families of the same disease, identically in both arms. It depends only on the committed outcome ledger. \|C_p\| = 0 → INVALID. | HARNESS |
| INV-E5 | Family credit is the mean over assigned genes, never the best-ranked gene. A gene assigned to several families counts once. | HARNESS |
| INV-E6 | The confirmatory statistic is the equal-weight mean over event-bearing diseases. Zero-event diseases are reported and are excluded from Δ̄. | HARNESS |
| INV-E7 | The 0.05 effect appears only as a planning effect. No gate or success rule compares Δ̄ against 0.05. | HARNESS (docs grep) |
| INV-E8 | V0 has one confirmatory cutoff (T\*, H\*). No pooling across cutoffs. | SCHEMA (estimand) |
| INV-E9 | Recall@K and other companion metrics never replace the primary metric in V0. | SCHEMA (attempt `primary_metric` for CONFIRMATORY/PROSPECTIVE) / HARNESS |
| INV-E10 | Every confirmatory result carries the placebo-guard record (K = 19) and the leave-one-disease-out record. Success is impossible unless both BLOCKING analyses pass. | HARNESS |
| INV-E11 | The sensitivity list in Freeze Statement §3a is closed. A LABEL analysis never changes the decision; no unlisted analysis can grant or veto success. | HARNESS (docs grep + evaluator) |

## INV-T — Thresholds

| ID | Invariant | Enforcement |
|---|---|---|
| INV-T1 | Every gate that any document uses to decide GO/REDESIGN/NO_GO exists by ID in `config/big0f-thresholds.v2.json`. No document states a numeric gate value that is not in the manifest. | HARNESS (docs grep) |
| INV-T2 | For MIN_REQUIRED gates: looser ≤ GO bound ≤ stricter. For MAX_ALLOWED gates: stricter ≤ GO bound ≤ looser. | HARNESS (checked for v2 when it was written) |
| INV-T3 | The NO_GO bound is at or beyond the GO bound in the failing direction. | HARNESS |
| INV-T4 | A missing or non-finite gate value → INCONCLUSIVE. It is never treated as a pass. | SCHEMA (decision semantics const) / HARNESS |
| INV-T5 | Precedence NO_GO > REDESIGN > INCONCLUSIVE > GO. | SCHEMA (const) |
| INV-T5a | Every GO/REDESIGN/NO_GO/INCONCLUSIVE consequence is expressible from the gate bounds alone, with no condition hidden in `metric_definition` text. Examples: the power screen's NO_GO is its own gate, `POWER_POOL_OPTIMISTIC_FLOOR`, and the non-event duplicate review is its own gate, `NON_EVENT_DUPLICATE_REVIEW_COVERAGE_RATIO`. | HARNESS |
| INV-T6 | GO requires every non-exempt gate to pass at its **stricter** bound, and GO under all three bound sets. If the terminal decision differs across the base/stricter/looser sets, the decision is the higher-precedence of (BASE decision, REDESIGN). A base NO_GO therefore stays NO_GO, and every other case becomes REDESIGN. | SCHEMA (pilot result v2, GO branch) / HARNESS |
| INV-T7 | Every BIG 0F evaluation is registered (public OSF + OTS) with its `big0f-pilot-result-v2` digest. Between evaluations, only procedural completion is allowed: missing artifacts, an incomplete duplicate review or an incomplete non-event audit. No config, learner, definition, threshold or case set may change. After two INCONCLUSIVE evaluations, the next result cannot be INCONCLUSIVE: it resolves to REDESIGN. | SCHEMA (`prior_inconclusive_count` ≤ 2; third cannot be INCONCLUSIVE) / HARNESS |
| INV-T8 | The endpoint-quality rule may only be equal to or stricter than adjudication policy v2 (`BIG0F-ADJUDICATION-V2`), criterion by criterion. | HARNESS |

## INV-A — Adjudication and agreement

| ID | Invariant | Enforcement |
|---|---|---|
| INV-A1 | The agreement statistic is Gwet AC1 for every gated task. κ is reported, never gated. | SCHEMA (pilot result) |
| INV-A2 | Each gated task passes only if its AC1 point estimate and its lower one-sided 90% BCa bound both clear their manifest thresholds. | HARNESS |
| INV-A3 | The duplicate-review set (event and non-event) equals the s_rev-salted keyed-hash selection, stratified by disease and recomputed from the sealed key and the revealed salt. The retest set follows INV-A5. MANDATORY_SAME_CONCEPT reviews are excluded from AC1 and coverage. The salt's commitment is in the S6 bundle. It is used only after the first-review label set is registered, and published only after the second-review labels are registered (seal_time order). Any other set or order → INVALID. | SCHEMA (policy consts, curation audit fields) / HARNESS |
| INV-A4 | Both reviewers' labels are stored for every duplicate-reviewed case. | SCHEMA (curation audit) |
| INV-A5 | At most one rule revision. It must be clarification-only (no policy value changes) and applied to all cases. The complete post-revision label set is registered before the retest is drawn. The retest set, min(N, max(30, ⌈0.30·N⌉)) cases, is drawn from all cases in s_ret order, stratified by disease, and gates are evaluated on it. Each salt is published only after the labels it selects for are registered. | SCHEMA (pilot result, policy consts, curation audit) / HARNESS |
| INV-A6 | NARROWER, BROADER, SURROGATE, RISK_FACTOR, INTERMEDIATE_PHENOTYPE and RELATED phenotype relations never qualify a primary positive. | SCHEMA (adjudication policy) |

## INV-P — Power

| ID | Invariant | Enforcement |
|---|---|---|
| INV-P1 | Stage A inputs come only from committed BIG 0F artifacts. No caller-supplied SD. | SCHEMA (power analysis) / HARNESS |
| INV-P2 | s_e,up = max(chi-square upper 95%, disease-cluster BCa upper 95%). | HARNESS |
| INV-P3 | The four scenarios and their roles are fixed: OPTIMISTIC = NO_GO boundary, PLANNING = GO boundary. | SCHEMA (power policy, power analysis) |
| INV-P4 | The simulation runs the frozen sign-flip test, not a z-approximation. The Normal approximation is reported only. | SCHEMA (method const) |
| INV-P5 | The confirmatory seal requires Stage B with ≥ 20 event-bearing DEVELOPMENT_EXPOSED diseases. External variance sources can only raise the planning SD. | SCHEMA (power analysis, variance registry) / HARNESS |
| INV-P6 | No BIG 0F biological-arm run exists. | HARNESS |
| INV-P7 | Stage A reserves N_DLVS = max(0, ⌈(20 − E_pilot)/p_eb,lower⌉) diseases. U is frozen by digest at the BIG 0F result registration. DLVS diseases are drawn by the custodian from U in `dlvs` key order, and this is the only permitted removal. The Stage B gate uses U_B = U − DLVS diseases, and any other exposure of a U disease spends the V0 allocation (INV-L9). | SCHEMA (power analysis, power policy) / HARNESS |

## INV-C — Custody, selection and randomness

| ID | Invariant | Enforcement |
|---|---|---|
| INV-C1 | The selection provenance lists exactly the 16 (T, H) pairs, unique and in lexicographic order (T ascending, then H ascending). | SCHEMA (selection provenance) |
| INV-C2 | (T\*, H\*) is the first pair whose five predicates all pass. If none passes → REDESIGN. | HARNESS |
| INV-C3 | Only the custodian computes predicates and holds per-event raw universes. The study team receives aggregates and digests only. | HARNESS (exposure ledger audit) |
| INV-C4 | The custodian holds no ranking or adjudication role in the confirmatory generation. | SCHEMA (adjudicator independence) / HARNESS |
| INV-C5 | At most one non-void S4 per protocol version. A new S4 is allowed only after the previous one was voided **before** time(R) − 24 h. A public archive capture taken before that point is authoritative, and an invalidation after it leads to REDESIGN with the S5 prefix exposed. | SCHEMA (beacon `s4_archive_ref`) / HARNESS |
| INV-C6 | The beacon is drand quicknet, chain hash `52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971`. R equals the round pre-declared in S4. | SCHEMA (beacon chain const) / HARNESS |
| INV-C7 | seal_time(S4) ≤ time(R) − 24 h, where time(R) = 1692803367 + 3·(R − 1). The upgraded OTS proof is attached to the public S4 record before time(R) − 24 h. The same rule applies to the confirmatory round R_c. | HARNESS |
| INV-C8 | The BLS signature of round R verifies against the pinned group key, checked independently by the custodian and the evaluator. | HARNESS |
| INV-C9 | Sampling key = SHA-256("forge-bio/big0f/sampling/v1" ‖ frame_cov(T\*) digest ‖ R ‖ randomness), with the byte encoding of custody §7. Every random choice uses HMAC-SHA256(key, domain ‖ id) with a domain from the closed list in custody §7; review selection also includes the salt. Confirmatory randomness uses key_c only. | SCHEMA (domain list) / HARNESS |
| INV-C10 | Expansion and cap operate on event families, following custody §8 exactly. | HARNESS |
| INV-C11 | Adjudicators receive events only after seal_time(S6) is established (release log). | HARNESS |
| INV-C12 | Exactly one non-void confirmatory draw registration (CDR) exists per program version. The CDR follows the MAP seal and the sealed rankings of every U_B disease, and it binds the MAP digest, the frozen U_B digest and the ranking commitment. key_c depends on the U_B digest and the ranking commitment, not on the MAP digest. The confirmatory sample, placebo and sign-flip seeds come only from key_c.<br>• The earliest **valid** CDR binds: its own seal is verified, and the MAP seal was verified at its registration. Any later CDR is void.<br>• Two non-void CDRs spend the allocation.<br>• All §3a refits (placebo, symmetric indicator) have their rank-output digests registered before the custodian releases any confirmatory outcome. | HARNESS |

## INV-X — Exposure

| ID | Invariant | Enforcement |
|---|---|---|
| INV-X1 | Any per-disease post-T information that reaches the study, design or ranking team, or any other audience that is not role-separated, by any route, makes that disease DEVELOPMENT_EXPOSED. | HARNESS |
| INV-X2 | Every disclosure is an exposure-ledger entry with an audience role and a disclosure level. | SCHEMA (ledger) / HARNESS |
| INV-X3 | Untouched pool U = frame_cov(T\*) − DEVELOPMENT_EXPOSED − any disease with exposure above AGGREGATE_ONLY to any audience other than SELECTION_CUSTODIAN, LOCKBOX_CUSTODIAN, OUTCOME_ADJUDICATOR or INDEPENDENT_REVIEWER. Role-separated access does not remove a disease from U. | SCHEMA (ledger audience scoping) / HARNESS |
| INV-X4 | Showcase cases come only from diseases that are already DEVELOPMENT_EXPOSED. | HARNESS |
| INV-X5 | Confirmatory NOVEL-STRICT families within 500 kb of any adjudicated event family of any DEVELOPMENT_EXPOSED disease at (T\*, H\*) are excluded from primary positives, in both arms. These exposed diseases are the pilot, the DLVS and any showcase. | HARNESS |
| INV-X6 | If any per-disease post-T information reached the design team before a protocol amendment, the revised pilot uses untouched diseases. | HARNESS |

## INV-O — Outcome discovery

| ID | Invariant | Enforcement |
|---|---|---|
| INV-O1 | Discovery is executed once per protocol version, by the custodian, with pinned source releases. | HARNESS |
| INV-O2 | The raw candidate count excludes families tagged PRE_T_LOCUS. | HARNESS |
| INV-O3 | Recall-audit recall ≥ the manifest bound; otherwise the recall gate fails. | HARNESS |
| INV-O4 | The event date is the earliest of journal-online date and preprint date. | HARNESS |

## INV-Q — Endpoint-quality applicability

| ID | Invariant | Enforcement |
|---|---|---|
| INV-Q1 | Every endpoint-quality rule has an applicability entry for all 13 dimensions. Each entry is APPLICABLE or NOT_APPLICABLE, and every NOT_APPLICABLE entry gives a reason. | SCHEMA |
| INV-Q2 | For E1-NOVEL-STRICT the matrix is fixed: REPLICATION is NOT_APPLICABLE, and the other 12 dimensions are APPLICABLE. A SEAL_CANDIDATE or SEALED rule has at least one criterion for each applicable dimension and none for REPLICATION. | SCHEMA |
| INV-Q3 | Every criterion is binding (`required: true`). A criterion may not be attached to a NOT_APPLICABLE dimension. | SCHEMA (binding) / HARNESS (attachment, other subtypes) |

## INV-L — Research-program ledger and α budget

| ID | Invariant | Enforcement |
|---|---|---|
| INV-L1 | `ledger_sequence` is contiguous from 0. The genesis has `previous_ledger_digest = null`; every later state carries the digest of the state before it. | SCHEMA (genesis) / HARNESS (chain) |
| INV-L2 | No fork: at most one ledger state exists for each (program, sequence). Every state is anchored by a PUBLIC_REGISTRY attestation, and the published head is the only valid head. Two anchored states with the same sequence → the program is INVALID until resolved publicly. | SCHEMA (anchor fields) / HARNESS |
| INV-L3 | `attempt_id` is unique. `attempt_index` is contiguous from 1 within each tier. Attempts are append-only. | HARNESS |
| INV-L4 | A CONFIRMATORY or PROSPECTIVE attempt has a non-null `allocation_generation_id` and `allocated_alpha`. A DEVELOPMENT attempt has both null. | SCHEMA (attempt, ledger) |
| INV-L5 | `cumulative_confirmatory_alpha_spent` = Σ `allocated_alpha` over CONFIRMATORY and PROSPECTIVE attempts, and it is ≤ 0.05. | SCHEMA (≤ 0.05) / HARNESS (sum) |
| INV-L6 | Generation transitions are PLANNED → ACTIVE → SPENT, or PLANNED/ACTIVE → RETIRED. SPENT and RETIRED are terminal. | SCHEMA (allowed pairs) / HARNESS (terminality across entries) |
| INV-L7 | **Budget carryover.** A V1 redesign stays in the same research program and budget. α spent in V0 is never reset, and the two-generation cap covers V0 and V1 together. Renaming the benchmark, endpoint, frame or model does not reset the budget. | SCHEMA (`program_scope_lock`, `post_failure_policy` required) / HARNESS |
| INV-L8 | Development results never support a confirmatory claim. | SCHEMA (const) |
| INV-L9 | **One lifecycle, three views.** The three state vocabularies describe different aspects of one generation and must be consistent (table below). | HARNESS |

**INV-L9 consistency table**

| α allocation (budget, program ledger) | Exposure state (exposure ledger) | Validation-generation state (MAP, lockbox) | Meaning |
|---|---|---|---|
| PLANNED | ACTIVE_CONFIRMATORY | ACTIVE | Sealed, untouched, α reserved |
| ACTIVE | ACTIVE_CONFIRMATORY | ACTIVE | Confirmatory attempt registered and running |
| SPENT | EXHAUSTED | RETIRED | The confirmatory test was run; α is consumed whatever the result |
| RETIRED | RETIRED | RETIRED | A mechanical REDESIGN or NO_GO (BIG 0F decision, Stage B gate, BIG 1 fidelity), whose final result was registered under INV-S8 before the MAP seal. This is the **only** route by which α stays unspent and can pass to a new program version. |
| SPENT | RETIRED | RETIRED | Any withdrawal or abandonment not caused by such a registered result, at any time, without a test |
| SPENT | DEVELOPMENT_EXPOSED | SPENT_FOR_MODEL_SELECTION | Feedback reached a non-role-separated audience after the MAP seal, or a U disease was exposed after the BIG 0F result registration by any route other than the custodian's DLVS draw |

No other combination is valid. In particular, a generation that is DEVELOPMENT_EXPOSED or SPENT_FOR_MODEL_SELECTION can never be ACTIVE for α.

**INV-L10.** Once outcomes are unsealed for a confirmatory generation, its α allocation is SPENT, even if the run is later declared INVALID (Freeze Statement §4). A generation cannot be re-run. Enforcement: HARNESS.

**INV-L11.** For every CONFIRMATORY or PROSPECTIVE attempt, the MAP's `statistics.alpha`, the MAP's `statistics.success_threshold_numeric` and the attempt's `allocated_alpha` are all equal to the generation's allocation in the budget. The V0 confirmatory generation's allocation is 0.05. A second generation can be allocated α only from an allocation that was RETIRED unspent. That happens only through a mechanical REDESIGN or NO_GO result registered under INV-S8 before the MAP seal (INV-L9). Enforcement: SCHEMA (MAP V0 constants of 0.05) / HARNESS (cross-artifact equality).

## INV-D — Documentation

| ID | Invariant | Enforcement |
|---|---|---|
| INV-D1 | Where any document disagrees with [V0_FREEZE_STATEMENT.md](V0_FREEZE_STATEMENT.md), the Freeze Statement wins and the other document is a defect. | HARNESS (review) |
| INV-D2 | Closure labels come from a fixed vocabulary:<br>• `SPEC-CLOSED` — decided in normative text or schema<br>• `IMPLEMENTATION-PENDING` — needs harness or core code<br>• `EMPIRICAL-OPEN` — the value awaits a measurement under a frozen rule<br>• `OPERATIONAL-OPEN` — needs people or process, e.g. custodian recruitment<br>• `SUPERSEDED` — replaced, with a pointer<br>Legacy labels are allowed only through a legend that maps them onto this vocabulary. No document claims machine enforcement for a check that does not exist in code. | HARNESS (docs grep) |
| INV-D3 | No document or schema references a removed file. | HARNESS (link check) |
| INV-D4 | The simulations cited in ADR-022 §4 are reproduced as harness regression fixtures before BIG 0F. | HARNESS |
