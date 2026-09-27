# Outcome-Discovery Specification v1

**Status:** NORMATIVE — machine-readable companion: `config/outcome-discovery.v1.json`
**Executed by:** the selection custodian ([BIG_0F_SELECTION_CUSTODY.md](BIG_0F_SELECTION_CUSTODY.md)), never by the ranking or design team.

This is the "frozen outcome-discovery procedure" referenced by [BIG_0F_PROTOCOL.md](BIG_0F_PROTOCOL.md). Every raw event universe comes from this procedure and nothing else. Those universes drive the cutoff/horizon feasibility check, the 12→15 expansion, the 150-family cap and adjudication.

## 1. Sources

| Role | Source | Pinning |
|---|---|---|
| Discovery index 1 | NHGRI-EBI GWAS Catalog, full associations file | Release fixed in the protocol registration. It must be dated at least 12 months after the latest candidate window end (2024-12-31). |
| Discovery index 2 | PubMed/MEDLINE, frozen query template (§3) | Executed once; the execution date and a digest of the returned PMID list are recorded |
| Adjudication evidence | Primary publications (full text and supplements), deposited summary statistics | Used to adjudicate, never to add events |

A catalog is a discovery index, not a label authority. A primary label is always adjudicated from the primary publication or its summary statistics ([BENCHMARK_V0_SPEC.md](BENCHMARK_V0_SPEC.md) §16).

## 2. Phenotype candidate scope

For each frame disease the frozen frame rule supplies a term set:

- the disease concept;
- its synonyms;
- its **narrower** descendants in the pinned ontology releases (EFO for the catalog, MeSH for PubMed).

Ancestors, risk factors, biomarkers and intermediate traits are **out of scope at discovery**, so they can never enter a raw universe. Adjudication later assigns the ADR-008 relation.

## 3. PubMed query template

```text
("<MeSH heading>"[MeSH Terms] OR "<entry term 1>"[tiab] OR …)
AND ("genome-wide"[tiab] OR "genome wide"[tiab] OR GWAS[tiab] OR "exome-wide"[tiab]
     OR "exome sequencing"[tiab] OR "whole-genome sequencing"[tiab] OR biobank[tiab])
AND ("<T+1>/01/01"[dp] : "<T+H>/12/31"[dp])
```

Returned records are screened for reported associations that meet §4. Screening is done by the custodian's curators with a frozen checklist. It is not done by adjudicators.

## 4. Candidate-event predicate

A candidate event is a reported association between a variant or locus and a term in the disease's scope that meets all of these:

- p ≤ 5×10⁻⁸ at any reported stage (discovery, replication or combined);
- any study design — the design class is adjudicated later;
- **first public availability** in (T, T+H].

First public availability is the earliest journal online date, or the earliest preprint posting that reports the same association. Catalog curation or "date added" dates are never used.

## 5. Grouping and pre-T locus tag

- **Grouping.** Events for the same disease whose lead variants lie within 500 kb of each other (GRCh38, harmonized per ADR-011) are single-linkage clustered into one GeneticDiscoveryEventFamily. A family's date is its earliest member's date.
- **Pre-T locus tag.** A family is tagged `PRE_T_LOCUS` when any lead variant lies within 500 kb of an association for the same disease (same term set, §2) that meets the §4 predicate (p ≤ 5×10⁻⁸) and whose first public availability is ≤ T. This uses the same pinned sources restricted to ≤ T. Tagged families can only be MATURATION or REPLICATION candidates. They are excluded from the raw count, from the cap and from NOVEL-STRICT adjudication.

## 6. Raw candidate count

The raw candidate count used by every feasibility and expansion rule is the number of event families **not** tagged `PRE_T_LOCUS`.

## 7. Completeness and stopping

- **One execution** per (disease, T, H) against the pinned releases. A re-query is a new procedure version and an exposure event.
- **Recall audit.** The custodian runs a broader screen, disease terms AND (association OR loci OR variant) over the same window, for ⌈0.25 × selected pilot diseases⌉ diseases (at least 3). The diseases are chosen in keyed-hash order, domain `recall-audit`.
- **Recall threshold.** Recall = families found by this procedure ÷ families found by either route. The threshold and its consequence are gate `OUTCOME_DISCOVERY_RECALL` in `config/big0f-thresholds.v2.json` (REDESIGN of the procedure). It is not restated here (INV-T1).
- **Closed world.** Families missed by the procedure are logged but **never added** to the pilot. Adding them after seeing them would be outcome-aware augmentation.

## 8. Outputs

| Output | Holder | Visible to study and ranking team |
|---|---|---|
| Per-event raw universe with provenance digests | Custodian | No (digest only) |
| Aggregate counts per frame and pair | Custodian | Yes |
| Selected diseases' events after sampling, expansion and cap | Custodian → adjudicators | Adjudicators only |

## 9. Confirmatory use

The confirmatory generation uses the custody-held **S2 raw universes** of the untouched diseases at (T\*, H\*). These come from the same single execution against the same pinned releases, with no re-pin and no re-query (INV-O1). They are committed by digest before any rank is revealed (ADR-010, ADR-013).
