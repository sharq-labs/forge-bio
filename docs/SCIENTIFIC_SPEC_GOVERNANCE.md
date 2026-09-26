# Scientific Specification Governance

**Status:** NORMATIVE PRE-CODE V1

## 1. Authoritative branch policy

Scientific contracts, benchmark specifications, schemas, and ADRs must change through reviewed pull requests.

Direct unreviewed edits to the authoritative branch are prohibited once V1 is frozen.

Recommended repository enforcement:
- protect `main`;
- require pull request review;
- require status/verification checks once implementation exists;
- disallow force-push to protected scientific history;
- use CODEOWNERS or equivalent reviewers for `docs/`, benchmark, temporal, identity, and outcome modules.

## 2. Freeze lifecycle

```text
DRAFT
→ PRE-CODE CANDIDATE
→ FROZEN
→ SUPERSEDED / RETIRED
```

A frozen spec records:
- commit SHA;
- document version;
- content digest where used by runtime;
- effective benchmark generation;
- approving reviewers/ADR.

## 3. Semantic change rule

A change affecting any of the following requires a new version or ADR:
- endpoint meaning;
- label derivation;
- candidate-universe inclusion;
- temporal admission;
- identity mapping semantics;
- evidence category meaning;
- primary metric/estimand;
- baseline family;
- success threshold;
- lockbox policy.

Editorial typo fixes may retain semantic version only when meaning is unchanged.

## 4. Confirmatory benchmark rule

After MAP freeze:
- no in-place edits to the MAP;
- no silent benchmark-spec edits;
- no silent provider-release updates;
- no silent mapping expansion;
- no threshold tuning from sealed outcomes.

Required changes create a new benchmark/MAP generation.

## 5. Lockbox generation retirement

Once individual sealed outcomes/errors influence methodology, that generation is spent for future confirmatory claims.

It remains valid historical evidence of what happened; it is not deleted.

## 6. Merge authority

Before implementation, the project owner may approve scientific-doc PRs.

Before FROZEN V1 and before sealed confirmatory work, at least one reviewer independent of the change author must approve changes affecting endpoint, estimand, labels, identity semantics, temporal admission, or lockbox policy.

A pull request authored and merged by the same person with no independent review does not satisfy this requirement.

## 7. Current repository action

The policy decision is now fixed: **reviewed PRs + protected authoritative branch (or equivalent enforced review control) are required before FROZEN V1**.

Repository support files now include `.github/CODEOWNERS`.

Actual GitHub branch-protection/ruleset configuration remains an operational prerequisite and must be verified separately. **FROZEN V1 is prohibited while the authoritative branch is unprotected or reviewed-merge enforcement is off.**


## 8. Required scientific roles

Before sealed confirmatory work, responsibilities are separated conceptually into:
- **Ranking Team** — historical inputs, features, models, sealed ranking production;
- **Outcome Adjudication Team** — FutureEvent construction, novelty audit, gene assignment, blinded adjudication;
- **Lockbox Custodian** — custody/access control and release after MAP/ranking freeze.

One person may temporarily occupy more than one role in early development only when the conflict is documented and the claim tier is downgraded where necessary.

The normative custody details are in [LOCKBOX_POLICY.md](LOCKBOX_POLICY.md).


## 9. Machine-verifiable schemas

Normative Markdown schemas have executable JSON Schema companions under `/schemas`.

Frozen QoI/MAP/MAR artifacts must:
- validate against the pinned JSON Schema version;
- reject unknown fields in governed structures;
- contain no unresolved freeze placeholders;
- record schema version and digest.

Schema validation complements, but does not replace, scientific semantic review.
