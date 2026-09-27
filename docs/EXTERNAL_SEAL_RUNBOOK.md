# External Seal Runbook — BIG 0F

**Status:** SPEC-CLOSED / IMPLEMENTATION-PENDING. The procedure is identified; it has not yet been tested end to end (§7). Amended by [ADR-022](adr/ADR-022-final-scientific-consistency-closure.md) D13.  
**Purpose:** create independent evidence that the BIG 0F protocol, selection and randomness commitments existed before adjudication

**seal_time.** The single authoritative timestamp of any artifact is:

seal_time = max(earliest Bitcoin block time in its verified OTS proof, public registry registration time)

Every "before" relation below uses seal_time (INV-S3).

## 1. Seal strategy

Use a **dual seal**:

1. **Content commitment timestamp** — OpenTimestamps proof over the canonical manifest digest.
2. **Research registration** — an OSF Registration containing or referencing the protocol or manifest. For the BIG 0F commitments (S1, S4, S6), the registration must be **public and not embargoed** (INV-S4).

Neither Git commit time nor a project-controlled repository alone satisfies the strongest external-seal requirement.

## 2. Canonical seal bundle

Create a canonical JSON manifest. The normative field list is `schemas/seal-bundle-manifest.v1.schema.json` (bundle version `big0f-seal-bundle-v3`). It binds the Freeze Statement, the semantic invariants, every v2 config, the frame rule, outcome discovery, the required-field registry, the power policy, the custody artifacts and the verification harness. The list below is the historical v2 subset, kept for reference only:

```text
seal_bundle_version
protocol_version
protocol_sha256
disease_frame_sha256
frame_seal_attestation_sha256
randomness_beacon_id
randomness_beacon_sha256
derived_sampling_key_commitment_sha256
candidate_cutoff_order
candidate_horizon_order
sampling_algorithm_version
threshold_manifest_sha256
adjudication_policy_sha256
nuisance_feature_manifest_sha256
decision_engine_sha256
pilot_result_schema_sha256
sampling_code_sha256
threshold_manifest_schema_sha256
adjudication_policy_schema_sha256
nuisance_manifest_schema_sha256
power_analysis_schema_sha256
selection_provenance_schema_sha256
nuisance_run_schema_sha256
provider_audit_schema_sha256
adjudicator_independence_schema_sha256
provenance_verifier_sha256
external_authority_verifier_sha256
power_engine_sha256
created_at
created_by_role
```

Do not rely on filenames alone.

The externally attested manifest digest is the root commitment. Verification must compare against that independently stored/registered digest; recomputing a fresh digest from the manifest under test is not sufficient.

The study team does **not** choose a random seed.

The evaluator independently fetches the sealed DRAND round and requires the returned round/randomness to equal the beacon artifact. Unsupported beacon providers fail closed in V0 until a code-backed verifier exists for them.

Randomness follows [BIG_0F_SELECTION_CUSTODY.md](BIG_0F_SELECTION_CUSTODY.md) §7:

- **Chain.** Only drand quicknet is accepted (chain hash `52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971`).
- **Round.** R is **pre-declared** in the public S4 selection registration, about 7 days after submission. The upgraded OTS proof is attached to the public S4 record before time(R) − 24 h, and S4 can no longer be voided after that point.
- **Timing.** seal_time(S4) ≤ time(R) − 24 h is required.
- **Key.** Sampling key = SHA-256("forge-bio/big0f/sampling/v1" ‖ frame_cov(T\*) digest ‖ R ‖ randomness).

The team never picks "the first round after" an event, so neither the round nor the chain can be ground.

*Superseded (ADR-022 D13):* "first verified round published after the frame seal".

## 3. Canonicalization

Before hashing:

- UTF-8;
- deterministic JSON key ordering;
- normalized Unicode;
- explicit null representation;
- no timestamps generated during canonicalization;
- no unordered sets;
- manifest JSON strings are NFC-normalized;
- component files are hashed as **exact raw bytes**; line-ending changes therefore change their digests.

Compute SHA-256 for:
- every component;
- the canonical manifest;
- the complete bundle archive if one is used.

## 4. OpenTimestamps seal

Create an OpenTimestamps proof for the canonical manifest or its exact serialized file.

Record in ExternalSealAttestation:

```text
authority_type = THIRD_PARTY_TIMESTAMP_SERVICE
attestation_method = THIRD_PARTY_TIMESTAMP
artifact_digest = <manifest sha256>
verification_evidence_ref = <proof artifact id/path>
verification_status = VERIFIED only after proof verification
```

The timestamp proof is stored separately from the source repository and must be independently verifiable.

For a claim-valid BIG 0F evaluation, the future external-authority verifier must recreate the exact committed artifact bytes and verify the supplied OpenTimestamps proof through an independent protocol-compatible verification path. Missing proof, failed verification, or absence of a verified timestamp success result fails closed. A study-authored `verification_status = VERIFIED` field is not accepted as proof.

## 5. OSF registration seal

Submit the protocol/manifest as an OSF Registration before first case adjudication.

For BIG 0F registrations (S1, S4, S6), embargo is **not allowed**. They contain digests and aggregates only, so publishing them creates no per-disease outcome exposure. An embargoed record gives no seal_time (INV-S4).

Record:

```text
authority_type = PUBLIC_REGISTRY
attestation_method = PUBLIC_PREREGISTRATION
external_registry_or_custodian_ref = <registration identifier>
sealed_at = registration submission/approval timestamp under the registry record
verification_evidence_ref = <registration record reference>
```

For non-BIG 0F registrations that are embargoed for another reason, preserve the evidence needed later to show the original registration date and content identity. Such a record still gives no seal_time until it is public.

For BIG 0F claim-valid evaluation, the verification evidence reference must resolve through an approved HTTPS OSF host and the independently fetched registry evidence must contain the exact committed artifact digest. If the record is embargoed or otherwise inaccessible to the verifier at evaluation time, the external-verification gate remains closed rather than trusting a local assertion.

## 6. Independent custodian

The custodian must not be the ranking-method designer for strongest-tier use.

Custodian responsibilities:
- hold plaintext seed if blinded;
- verify component hashes;
- create/verify the timestamp proof;
- verify registry submission;
- release the committed seed/frame only according to the pilot protocol;
- record all access/release events.

## 7. End-to-end test before BIG 0F

Perform a dry run with synthetic/non-study content:

1. generate a mock protocol file;
2. generate a mock frame_cov and a mock S4 selection registration that pre-declares a real drand quicknet round R (about 7 days ahead, or a shorter test offset marked TEST);
3. publicly register and OTS-timestamp the mock S4; compute seal_time(S4) and check seal_time(S4) ≤ time(R) − 24 h;
4. at time(R), fetch round R from quicknet and verify its BLS signature against the pinned group key;
5. derive the sampling key through the frozen sampling contract, and check that a wrong round, chain or late seal_time fails;
6. create the canonical manifest;
7. hash every claim-bearing component, including the future evaluator/sampling implementations when they exist, plus pilot-result and policy schemas;
8. create timestamp proof;
9. verify timestamp proof independently;
10. create a test OSF/public-registry registration as allowed by the service;
11. reconstruct the bundle from stored artifacts;
12. validate the complete manifest against `schemas/seal-bundle-manifest.v1.schema.json`;
13. read the expected manifest digest from the independently stored attestation record — never from a caller-supplied command-line digest;
14. require both THIRD_PARTY_TIMESTAMP_SERVICE and PUBLIC_REGISTRY attestations over the same bundle digest;
15. verify all component hashes;
16. verify that a one-byte component modification fails;
17. once implementation exists, verify that evaluator/sampling/schema modification fails the committed identity check;
18. verify that any manifest-field mutation fails schema and/or attested-digest verification;
19. record both verified ExternalSealAttestation artifacts;
20. run the independent OpenTimestamps verification procedure against the exact committed bytes and proof;
21. fetch the OSF verification record independently and match the exact artifact digest;
22. fetch the pre-declared quicknet round R independently, verify its BLS signature, and match its randomness to the sealed beacon artifact;
23. verify that the release log's first release to adjudicators follows seal_time(S6);
24. verify, from the registry's own timestamps, that the upgraded OTS proof was part of the public S4 record before time(R) − 24 h, and that a public web-archive capture of S4 exists from before that time;
25. verify that each review salt (S8, S9) is published only after the label sets it selects for are registered, and that it matches its commitment in S6.

Only after this dry run succeeds may the checklist item "seal mechanism identified and tested" be closed.

## 8. Seal timing

The following must occur **before first case adjudication**:

```text
S1  protocol registration (public OSF + OTS): every SEAL_CANDIDATE config and normative document
→ S2/S3  custodian computes cutoff/horizon predicates; first passing pair (T*, H*)
→ S4  selection registration (public OSF + OTS) pre-declaring drand quicknet round R;
      seal_time(S4) ≤ time(R) − 24 h
→ S5  at time(R): verify round, derive key, order diseases, expansion/cap on the S2 universe (no re-query); events held
→ S6  canonical seal bundle (public OSF + OTS)
→ independent verification of seal_time(S6)
→ S7  custodian releases events to adjudicators (release log)
→ adjudication begins
→ S8  first-review label set registered → custodian privately forms the duplicate batch with s_rev → second-review labels registered → s_rev published
→ S9  (only after a rule revision) post-revision label set registered → custodian privately draws the retest with s_ret → retest labels registered → s_ret published
```

If adjudication starts first, the pilot is DEVELOPMENT-EXPOSED and the seal cannot retroactively repair the chronology.

## 9. Amendment rule

Any material post-seal change to:
- cutoff/horizon ordering;
- disease frame;
- seed/sampling algorithm;
- primary endpoint;
- assignment eligibility;
- GO/REDESIGN/NO-GO thresholds;
- nuisance families;
- adjudication policy

requires a new seal generation.

The old registration/timestamp remains part of the audit trail and is never overwritten.

## 10. Claim boundary

This runbook proves timing/integrity of commitments.

It does **not** prove:
- scientific validity;
- reviewer independence by itself;
- correct adjudication;
- absence of hidden side channels;
- prospective efficacy.

Those are separate gates.
