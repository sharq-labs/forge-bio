# Context of Use Schema

**Status:** NORMATIVE PRE-CODE V1

## Required schema

```yaml
context_of_use_id: string
schema_version: string

intended_use: string
intended_users: [string]
decision_supported: string
model_influence: string

consequence_of_false_positive: string
consequence_of_false_negative: string

direct_patient_impact: none | indirect | prohibited
human_review_required: boolean

applicability_domain:
  disease_regimes: [string]
  evidence_regimes: [string]
  populations: [string]
  historical_eras: [string]
  excluded_domains: [string]

excluded_uses: [string]
required_claim_language: [string]
prohibited_claim_language: [string]
```

## V1 context

```yaml
context_of_use_id: research-prioritization-v1
schema_version: cou-v1
intended_use: retrospective benchmark development and computational research prioritization
intended_users:
  - computational biologists
  - bioinformatics researchers
  - drug-discovery researchers
decision_supported: which hypotheses deserve further scientific review/investigation
model_influence: low-to-moderate; humans control scientific follow-up
consequence_of_false_positive: wasted research effort and misleading scientific prioritization
consequence_of_false_negative: potentially useful hypothesis receives lower priority
direct_patient_impact: none
human_review_required: true
applicability_domain:
  disease_regimes:
    - benchmark-specific
  evidence_regimes:
    - provenance-bearing temporally governed biomedical evidence
  populations:
    - benchmark-evaluated populations only
  historical_eras:
    - provider-audit-qualified eras only
  excluded_domains:
    - direct clinical decision support
excluded_uses:
  - diagnosis
  - prescribing
  - dosing
  - patient-specific recommendations
  - clinical efficacy claims from rank alone
  - pharmaceutical synthesis/manufacturing instructions
required_claim_language:
  - endpoint-specific
  - uncertainty-aware
  - applicability-bounded
prohibited_claim_language:
  - cure
  - proven treatment
  - safe because ranked highly
  - clinically validated from computational rank alone
```
