# Golden Synthetic Scientific Twin World

**Status:** NORMATIVE PRE-CODE V1  
**Purpose:** Deterministic fixture for scientific profile and digital-twin maturity/temporal tests.

## 1. Cutoff

```text
T = 2019-12-31
```

## 2. Synthetic entities

```text
D-INF = Delta infectious disease
P-VIR = Virus Phi
HOST  = Human host
TP-1  = Therapeutic Alpha
```

The pathogen and disease are distinct identities.

```text
P-VIR
    CAUSES / CONTRIBUTES_TO
D-INF
```

is represented through evidence-backed claims, not identity equivalence.

## 3. Historical profile state at T

### Disease profile

Before T:
- disease concept exists;
- phenotype set PH1/PH2 exists;
- tissue TIS1 is implicated;
- host pathway PW1 has moderate evidence;
- mechanism M2 is UNKNOWN.

### Pathogen profile

Before T:
- pathogen taxonomy exists;
- viral protein VP1 is known;
- host receptor HR1 interaction is supported;
- lineage L2 does not yet exist.

### Therapeutic profile

Before T:
- therapeutic TP-1 exists;
- target engagement with host factor HF1 is supported;
- no qualifying efficacy evidence for D-INF exists by T.

## 4. Future sentinels

After T:
- mechanism M2 gains strong evidence;
- viral lineage L2 emerges;
- TP-1 receives later investigation/efficacy evidence;
- a new host interaction HI2 is discovered.

These records must not alter any STRICT_HISTORICAL Twin(subject, T).

## 5. Maturity fixtures

### TW0 — Profile only

Contains:
- resolved entities;
- evidence-backed claims;
- contradictions/gaps;
- uncertainty;
- immutable profile snapshot.

Expected maturity:

```text
T0_PROFILE_ONLY
```

It must not be called a digital twin in a scientific claim.

### TW1 — Dynamic knowledge twin

Updates from versioned evidence snapshots:

```text
TwinState v1
→ admitted evidence update
→ TwinState v2
```

No predictive claim is made.

Expected maturity:

```text
T1_DYNAMIC_KNOWLEDGE_TWIN
```

### TW2 — Mechanistic twin

Adds an explicit state-transition model for a narrow pathogen–host mechanism with:
- named state variables;
- parameter provenance;
- assumptions;
- uncertainty;
- applicability domain.

Expected maturity:

```text
T2_MECHANISTIC_TWIN
```

No predictive maturity is earned merely because the model simulates.

### TW3 — Predictive twin

The TW2 model is frozen and evaluated against held-out/future observations.

Expected maturity only if:
- target/horizon were frozen;
- held-out/future evaluation passes;
- uncertainty is evaluated;
- applicability is reported.

Then:

```text
T3_VALIDATED_PREDICTIVE_TWIN
```

Otherwise it remains T2.

### TW4 — Intervention simulation twin

Requires T3-level validity for the relevant state/target plus a versioned computational perturbation and sensitivity/UQ analysis.

Output remains a research hypothesis.

Expected maturity:

```text
T4_VALIDATED_INTERVENTION_SIMULATION_TWIN
```

No clinical-treatment claim is implied.

## 6. Pathogen–host rule

For infectious disease:

```text
PathogenScientificTwin
+
HostContext
→ PathogenHostScientificTwin
```

A pathogen-only predictive model may not silently claim host-disease behavior when host biology is outside its represented state.

## 7. Required verification tests

1. P-VIR and D-INF never collapse into one identity.
2. future sentinel M2 cannot appear in Twin(D-INF, T).
3. future lineage L2 cannot appear in Twin(P-VIR, T).
4. future therapeutic outcome cannot alter TherapeuticTwin(T).
5. TW0 cannot serialize with maturity T1–T4 without required dynamic/model/validation fields.
6. TW1 cannot claim mechanistic or predictive validation.
7. TW2 cannot claim T3 merely because it reproduces training data.
8. T3 requires held-out/future validation artifacts.
9. T4 requires T3 validity plus perturbation sensitivity/uncertainty.
10. changing model parameters produces a new immutable TwinState/model artifact.
11. modern parameter fitting cannot contaminate STRICT_HISTORICAL Twin(subject, T).
12. pathogen-only state cannot be interpreted as a validated pathogen–host model.
13. simulation output is not stored as clinical evidence.
