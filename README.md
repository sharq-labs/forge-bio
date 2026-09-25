# Forge Bio

Forge Bio is a **computational therapeutic hypothesis discovery and historical validation platform**.

It is designed to answer a narrow scientific question:

> Given only biomedical information that was genuinely available at time **T**, can a computational system prioritize disease mechanisms, therapeutic targets, and later existing-drug hypotheses that subsequently receive predefined independent validation?

The project is **benchmark-first**, not AI-first. Historical validity, provenance, evidence semantics, uncertainty, identity, and reproducibility are first-class requirements. Machine learning is introduced only after simple baselines and a leakage-resistant benchmark exist.

## What Forge Bio is

Forge Bio is a research platform for:

- temporally controlled biomedical evidence
- therapeutic hypothesis generation and ranking
- disease → mechanism → target prioritization
- later disease → existing active-moiety / drug repurposing prioritization
- explicit supporting evidence, counter-evidence, and gaps
- uncertainty and applicability reporting
- historical retrospective validation
- sealed benchmark evaluation
- prospective shadow validation

## What Forge Bio is not

Forge Bio is not:

- a patient diagnosis system
- a treatment recommender
- a dosing system
- a clinical decision-support system
- a system that claims computational predictions are proven therapies
- a pharmaceutical synthesis or manufacturing workflow
- an LLM whose output is treated as scientific truth

The platform produces **research hypotheses for further scientific investigation**.

## Scientific operating modes

Forge Bio distinguishes three modes:

1. **Strict historical benchmark** — every model-visible artifact must be defensibly admissible by cutoff T.
2. **Historical-input / modern-prior experiment** — historical explicit inputs may be combined with modern pretrained representations, but the run is labelled contaminated/non-historical and cannot support a strict retrospective claim.
3. **Current hypothesis discovery** — current evidence and current models are allowed for present-day research prioritization, with no historical claim.

## Core architectural rule

A ranker does not receive unrestricted storage plus a cutoff parameter.

It receives a frozen, read-only:

```text
HistoricalKnowledgeView(cutoff=T)
```

The Past/Historical Knowledge Zone and the Future Outcome/Oracle Zone are logically and preferably physically separated. The ranking artifact is frozen and hashed before future labels are available to evaluation.

## Scientific north star

The key question is not whether a model beats random.

It is whether it shows reproducible lift over what the research field was already paying attention to at T.

Important comparators therefore include:

- random ranking
- historical publication/research-attention ranking
- evidence-volume ranking
- target/drug popularity
- graph-degree/popularity controls
- deterministic evidence-quality ranking

## Initial benchmark sequence

Forge Bio will use two sibling benchmark families:

- **B-TGT — Target Discovery:** Disease → therapeutic target / intervention direction.
- **B-REP — Repurposing:** Disease → existing active moiety / drug.

B-TGT establishes whether the platform contains genuine biological prioritization signal. B-REP tests whether that signal translates into useful therapeutic prioritization.

## Authoritative project documents

- [Architecture V1](docs/ARCHITECTURE_V1.md)
- [Scientific Contract](docs/SCIENTIFIC_CONTRACT.md)
- [Scientific Master Plan](docs/SCIENTIFIC_MASTER_PLAN.md)

These documents are authoritative until superseded by an explicit ADR or a versioned replacement.

## Status

Current phase: **BIG 0 — Scientific Contract & Threat Model**

No production scientific model should be implemented before the project contracts, temporal rules, evidence semantics, and benchmark governance are frozen.
