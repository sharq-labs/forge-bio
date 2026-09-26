# External Seal Runbook — BIG 0F

**Status:** OPERATIONAL CANDIDATE — identified, not yet end-to-end tested  
**Purpose:** create independent evidence that the BIG 0F protocol/frame/seed commitment existed before adjudication

## 1. Seal strategy

Use a **dual seal**:

1. **Content commitment timestamp** — OpenTimestamps proof over the canonical manifest digest.
2. **Research registration** — OSF Registration containing or referencing the protocol/manifest, public or embargoed according to confidentiality needs.

Neither Git commit time nor a project-controlled repository alone satisfies the strongest external-seal requirement.

## 2. Canonical seal bundle

Create a canonical JSON manifest:

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

The disease frame is externally sealed first. The exact verified frame-seal attestation artifact is hashed into the root bundle. A verified public randomness-beacon round published after that frame seal is then bound to both the frame digest and the exact frame-seal attestation digest. The sampling key is derived deterministically from frame digest + beacon randomness. This makes pre-commitment seed grinding detectable/prohibited.

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

For a claim-valid BIG 0F evaluation, `scripts/verify_external_authorities.py` recreates the exact committed artifact bytes in a temporary verification workspace and executes the OpenTimestamps client against the supplied `.ots` proof. Missing client/proof, non-zero verification, or absence of a verified timestamp success result fails closed. A study-authored `verification_status = VERIFIED` field is not accepted as proof.

## 5. OSF registration seal

Submit the protocol/manifest as an OSF Registration before first case adjudication.

Use an embargo when revealing the protocol/frame would compromise the study or create avoidable research-attention exposure.

Record:

```text
authority_type = PUBLIC_REGISTRY
attestation_method = PUBLIC_PREREGISTRATION
external_registry_or_custodian_ref = <registration identifier>
sealed_at = registration submission/approval timestamp under the registry record
verification_evidence_ref = <registration record reference>
```

If embargoed, preserve evidence needed later to show the original registration date and content identity.

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
2. generate a mock frame;
3. externally seal the mock frame digest;
4. obtain/use a mock verified beacon artifact whose publication time is after the mock frame seal;
5. derive the sampling key through the frozen sampling code;
6. create the canonical manifest;
7. hash every component, including evaluator code, sampling code, pilot-result schema and policy schemas;
8. create timestamp proof;
9. verify timestamp proof independently;
10. create a test OSF/public-registry registration as allowed by the service;
11. reconstruct the bundle from stored artifacts;
12. validate the complete manifest against `schemas/seal-bundle-manifest.v1.schema.json`;
13. read the expected manifest digest from the independently stored attestation record — never from a caller-supplied command-line digest;
14. require both THIRD_PARTY_TIMESTAMP_SERVICE and PUBLIC_REGISTRY attestations over the same bundle digest;
15. verify all component hashes;
16. verify that a one-byte component modification fails;
17. verify that evaluator/sampling/schema modification fails;
18. verify that any manifest-field mutation fails schema and/or attested-digest verification;
19. record both verified ExternalSealAttestation artifacts;
20. run the code-backed OpenTimestamps verifier against the exact committed bytes and proof;
21. fetch the OSF verification record independently and match the exact artifact digest;
22. fetch the selected DRAND round independently and match its randomness to the sealed beacon artifact.

Only after this dry run succeeds may the checklist item "seal mechanism identified and tested" be closed.

## 8. Seal timing

The following must occur **before first case adjudication**:

```text
protocol + threshold + adjudication + nuisance freeze
→ disease frame freeze
→ external frame timestamp/registration
→ later public randomness-beacon round
→ deterministic sample-order derivation
→ canonical bundle including evaluator/sampling/schema digests
→ dual external timestamp + public registration of bundle digest
→ independent verification
→ adjudication begins
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
