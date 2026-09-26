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
random_seed_commitment_sha256
candidate_cutoff_order
candidate_horizon_order
sampling_algorithm_version
threshold_manifest_sha256
adjudication_policy_sha256
nuisance_feature_manifest_sha256
created_at
created_by_role
```

Do not rely on filenames alone.

The externally attested manifest digest is the root commitment. Verification must compare against that independently stored/registered digest; recomputing a fresh digest from the manifest under test is not sufficient.

The plaintext random seed may be held by the independent custodian. The public/time-stamped bundle may contain only its cryptographic commitment if revealing the seed would compromise blinding.

## 3. Canonicalization

Before hashing:

- UTF-8;
- deterministic JSON key ordering;
- normalized Unicode;
- explicit null representation;
- no timestamps generated during canonicalization;
- no unordered sets;
- line endings normalized.

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
3. generate a mock seed;
4. create the canonical manifest;
5. hash every component;
6. create timestamp proof;
7. verify timestamp proof independently;
8. create a test registration or documented registry dry run as allowed by the service;
9. reconstruct the bundle from stored artifacts;
10. validate the complete manifest against `schemas/seal-bundle-manifest.v1.schema.json`;
11. compare the canonical manifest SHA-256 against the **externally attested digest** (not a digest recomputed from a potentially modified manifest);
12. verify all component hashes;
13. verify that a one-byte component modification fails;
14. verify that any manifest-field mutation (protocol version, sampling algorithm, extra field, etc.) fails schema and/or attested-digest verification;
15. record an ExternalSealAttestation fixture.

Only after this dry run succeeds may the checklist item "seal mechanism identified and tested" be closed.

## 8. Seal timing

The following must occur **before first case adjudication**:

```text
protocol freeze
→ frame freeze
→ seed commitment
→ threshold manifest freeze
→ nuisance-family manifest freeze
→ canonical bundle digest
→ external timestamp/registration
→ verification
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
