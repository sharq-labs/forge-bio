# BIG 0F Selection Custody, Randomness Pinning and Exposure Accounting

**Status:** NORMATIVE — SPEC-CLOSED / IMPLEMENTATION-PENDING
**Closes:**

- 16-pair outcome exposure;
- beacon and frame grinding;
- the "directly inspected" loophole;
- the showcase side channel;
- a predictable audit sample;
- amendments made after outcomes were seen but before adjudication.

## 1. Roles

The **selection custodian** executes the outcome-discovery procedure and every step below that touches post-T information.

- The custodian is independent of the design, ranking and adjudication teams. Independence is attested with the `SELECTION_CUSTODIAN` role in `schemas/big0f-adjudicator-independence.v1.schema.json`.
- The custodian's full exposure is logged.
- The custodian may not hold a ranking or adjudication role in the confirmatory generation.
- The custodian may also be the lockbox custodian.

## 2. Sequence

| Step | Actor | Action | Public record |
|---|---|---|---|
| S1 | Design team | Protocol registration: the digests of every SEAL_CANDIDATE config and normative document, including the frame rule, outcome-discovery spec, thresholds, adjudication policy, nuisance manifest and power policy | OSF registration (public, **not embargoed**) plus OpenTimestamps (OTS) |
| S2 | Custodian | Run the outcome-discovery procedure **once** per (frame disease, T, H) and hold the raw universes. For each of the 16 (T, H) pairs, in the frozen order, compute the §3 predicates. | — |
| S3 | Custodian | The first passing pair is (T\*, H\*). If none passes → REDESIGN. | — |
| S4 | Custodian | Selection registration containing: the predicate table; aggregate counts; digests of the custody-held raw universes; the frame_cov(T\*) digest; the digests of the sampling code, the nuisance fitting code and the verification harness; and a **pre-declared drand round R** (§7) | OSF (public, not embargoed) with the upgraded OTS proof attached |
| S5 | Custodian | At time(R): fetch and verify the round, derive the sampling key, and order diseases. Apply expansion and cap to the **S2 raw universe** of (T\*, H\*); there is no new query (INV-O1). Events are **held**. | Beacon artifact |
| S6 | Custodian | Seal bundle over every artifact, including S4, S5 and the commitments SHA-256(s_rev) and SHA-256(s_ret) of the two review salts (§7) | OSF plus OTS |
| S7 | Custodian | After seal_time(S6) has been established and independently verified (ADR-022 §5), release only the selected diseases' events to the adjudicators. Record the release in the exposure ledger. | Release log (the evidence that adjudication began after the seal) |
| S8 | Custodian | After the complete first-review label set (event and non-event cases) has been registered, the custodian uses s_rev **privately** to form the second reviewer's batch: the drawn duplicate set plus any undrawn MANDATORY_SAME_CONCEPT cases, in one undifferentiated batch. s_rev is published only after the second-review labels are registered. | OSF plus OTS for both label-set digests; then s_rev is published |
| S9 | Custodian (only after a rule revision) | After the complete **post-revision** first-review label set has been registered, the custodian privately draws the retest set from all cases in s_ret order, stratified by disease. s_ret is published after the retest labels are registered. | OSF plus OTS for the label-set digests; then s_ret is published |

## 3. Frozen cutoff/horizon predicates

A pair (T, H) passes only if all five predicates are true. None of them uses a per-disease outcome that the study team can see.

| Predicate | Definition |
|---|---|
| P_prov(T) | Every CRITICAL field with `time_scope: AS_OF_T` in `config/big0f-required-field-registry.v1.json` has an obtainable release dated ≤ T. EVALUATION-scope fields are checked by P_obs and the provider audit, not here. |
| P_obs(T, H) | T + H + 12 months ≤ release date of the pinned discovery sources |
| P_cov(T) | In frame(T), the share of diseases with coverage ≥ MODERATE is ≥ the manifest value, **and** their count is ≥ the manifest minimum |
| P_anchor(T, H) | P_cov(T − H) holds. This guarantees at least one nested-training anchor with NOVEL-STRICT labels (MODEL_TRAINING_POLICY §2). |
| P_evt(T, H) | The mean raw candidate count per frame_cov(T) disease is ≥ the manifest value. Only families not tagged PRE_T_LOCUS are counted. |

## 4. Exposure accounting

| Information | Who sees it | Exposure level | Consequence |
|---|---|---|---|
| Per-event raw universes for all 16 pairs | Custodian only | FULL_LABEL (custodian) | The custodian is barred from confirmatory ranking and adjudication roles |
| Frame-level aggregate counts and pass/fail | Everyone | AGGREGATE_ONLY | Frame diseases stay untouched |
| Events of the final sampled prefix | Adjudicators, then the study team | FULL_LABEL | Those diseases become DEVELOPMENT_EXPOSED |
| Diseases 13–15 when expansion is not triggered | Custodian only | — | Never released; they stay untouched |
| Showcase cases | Study team | FULL_LABEL | Only from diseases already DEVELOPMENT_EXPOSED, and each is logged |
| DLVS diseases (Stage B) | Adjudicators, then the study and ranking team | FULL_LABEL | DEVELOPMENT_EXPOSED; they leave U |

Every exposure is an entry in the BenchmarkExposureLedger, with an audience role and a disclosure level. Any per-disease post-T information that reaches the study, design or ranking team makes that disease DEVELOPMENT_EXPOSED, whatever the route.

## 5. Untouched pool

U = frame_cov(T\*) − DEVELOPMENT_EXPOSED diseases − diseases with any exposure above AGGREGATE_ONLY to **any audience that is not role-separated**, computed once and frozen by digest at the BIG 0F result registration. After that, the custodian's DLVS draw is the only permitted removal. Any other exposure of a U disease spends the V0 allocation and does not shrink U (Freeze Statement §4; INV-P7).

- The role-separated audiences are exactly SELECTION_CUSTODIAN, LOCKBOX_CUSTODIAN, OUTCOME_ADJUDICATOR (blinded) and INDEPENDENT_REVIEWER.
- Every other audience removes the disease from U: STUDY_TEAM, DESIGN_TEAM, RANKING_TEAM, PUBLIC and OTHER.
- The selection custodian's FULL_LABEL access to raw universes does not remove a disease from U. That access is role-separated: the custodian is barred from every confirmatory ranking and adjudication role (§1, INV-C4). Without this scoping U would be empty, because the custodian enumerates every frame disease.

U feeds the power screen ([BIG_0F_POWER_AND_VARIANCE_POLICY.md](BIG_0F_POWER_AND_VARIANCE_POLICY.md)).

## 6. Cross-disease locus exposure

A confirmatory NOVEL-STRICT event family whose locus lies within 500 kb of any adjudicated event family of **any DEVELOPMENT_EXPOSED disease at (T\*, H\*)** is **excluded from positives in the primary analysis**, because that discovery has been seen. Those exposed diseases are the BIG 0F pilot, the DLVS and any showcase.

- A REPORT analysis includes them (SENS-DEV-LOCUS).
- The exclusion depends only on development records, never on ranks.
- It applies to both arms.

## 7. Randomness pinning

| Item | Frozen value |
|---|---|
| Network | drand **quicknet** |
| Chain hash | `52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971` |
| Scheme | `bls-unchained-g1-rfc9380`; period 3 s; genesis 1692803367 |
| Round time | time(R) = 1692803367 + 3·(R − 1) |
| Round choice | R is written into the S4 registration. The custodian should choose R about 7 days after submission, to leave time for the seal to complete. Only the validity rule below is binding. |
| Validity | seal_time(S4) ≤ time(R) − 24 h, where seal_time = max(earliest Bitcoin block time in the verified OTS proof, public OSF registration time) ([ADR-022](adr/ADR-022-final-scientific-consistency-closure.md) §5). The **upgraded OTS proof must be attached to the public S4 record** before time(R) − 24 h, so validity is publicly decided before R's randomness exists. |
| Void and invalid | If the validity rule fails **before** time(R) − 24 h, S4 is void. It is re-registered with a new R, and the void record stays public. Before time(R) − 24 h, the custodian and an independent verifier also capture the public S4 record and its proof in a public web archive. That capture is authoritative, so later unavailability of the registry record changes nothing. If S4 is nevertheless invalidated after time(R) − 24 h, the outcome is REDESIGN with the S5 prefix (the first 15 diseases in R-order) treated as DEVELOPMENT_EXPOSED. A withheld proof or a withdrawn record therefore buys nothing. |
| Verification | BLS signature against the pinned group public key, checked by the custodian with the reference drand client, and independently by the evaluator |
| Encoding | Strings are UTF-8. Digests are raw 32 bytes, R is an 8-byte big-endian unsigned integer, and randomness is raw 32 bytes. ‖ is byte concatenation. The HMAC message is UTF-8(domain) ‖ 0x00 ‖ [salt ‖ 0x00 ‖] UTF-8(item id). |
| Sampling key | SHA-256("forge-bio/big0f/sampling/v1" ‖ frame_cov(T\*) digest ‖ R ‖ randomness) |
| Disease order | Ascending HMAC-SHA256(key, disease UI) |
| Sub-sample keys | HMAC-SHA256(key, domain ‖ item id). The domains are `dup-review`, `retest`, `non-event`, `cap`, `agreement-ci`, `power-sd`, `power-sim`, `dlvs` and `recall-audit`. The list is closed (INV-C9). |
| Review salts | `dup-review` messages also contain s_rev, and retest messages (domain `retest`) contain s_ret. Both are 32-byte custodian secrets whose SHA-256 is committed in S6. Each salt is published only after the labels it selects for have been registered, at the end of S8 and S9 respectively. No reviewer can compute an audit set, or tell drawn cases from mandatory ones, while labelling. |
| Confirmatory randomness | The BIG 0F key is **never** reused. The confirmatory sequence runs in this order: MAP sealed → rankings of both arms for **every** U_B disease sealed → one **confirmatory draw registration** (CDR). The CDR binds the MAP digest, the frozen U_B digest (registered with the Stage B gate result) and the ranking commitment, which includes the refit code digests. It pre-declares a quicknet round R_c under the validity, archive and no-void rules above. The CDR is valid only if the MAP's public seal (INV-S8) verifies when the CDR is registered. Once a verified CDR exists, the program counts as past the MAP seal. At time(R_c), the placebo and symmetric-indicator refits run, and their rank-output digests are registered **before** the custodian releases any confirmatory outcome. key_c = SHA-256("forge-bio/confirmatory/v1" ‖ U_B digest ‖ ranking-commitment digest ‖ uint64be(R_c) ‖ randomness). The key does **not** depend on the MAP digest. Its domains are `confirmatory-draw`, `placebo` and `confirmatory-signflip`. |
| One draw per program version | Exactly one non-void CDR exists per program version. The earliest **valid** CDR binds: its own seal is verified, and the MAP seal was verified at its registration. Later ones are void (INV-C12). After the MAP seal, any withdrawal, abandonment or U_B exposure spends the allocation (INV-L9; Freeze Statement §4), so neither re-registering nor retiring can re-roll the draw. |

The chain values above were read from api.drand.sh on 2026-09-27. The custodian re-verifies them at S1 and records any discrepancy before registration.

## 8. Expansion and cap (event-family level)

- **Expansion.** Start with the first 12 diseases in order. Add diseases 13, 14 and 15 one at a time, only while the cumulative raw candidate family count is below the manifest minimum. Families tagged PRE_T_LOCUS are never counted.
- **Cap.** If there are more raw candidate families than the manifest maximum, first keep one family per disease that has at least one raw candidate family (lowest `cap` key). Fill the remaining slots in ascending `cap` key over families.
- **Unit.** Families are sampled, not raw records, so a locus reported many times is not over-sampled. PRE_T_LOCUS families are outside the cap and are not adjudicated as NOVEL-STRICT candidates.

## 9. Amendments

Any change to a sealed artifact after S1 requires a new protocol version. If any per-disease post-T information has reached the design team, the revised pilot must use untouched diseases, even if no case has been adjudicated.

The BIG 0F nuisance learner, adjudication definitions and thresholds are never changed after pilot labels exist. Between INCONCLUSIVE evaluations only procedural completion is allowed (INV-T7).
