# BIG 0F Operational Adjudication Definitions (policy `BIG0F-ADJUDICATION-V2`)

**Status:** NORMATIVE — machine-readable source: `config/big0f-adjudication-policy.v2.json`
**Rule:** These definitions are in force for the first adjudicated BIG 0F case. The post-BIG 0F endpoint-quality rule may be **equal or stricter**, never looser. A looser definition needs a new pilot on untouched cases.

## 1. Primary gene-assignment classes

| Class | Qualifies when | Rationale |
|---|---|---|
| HYPOTHESIS_FREE_CODING_OR_LOF | The lead variant — or a credible-set variant with PIP ≥ 0.5, or, when no fine-mapping is reported, a variant with r² ≥ 0.8 to the lead in the discovery ancestry — has a coding or splice consequence in exactly one gene. The association must have p ≤ 5×10⁻⁸, or a gene burden test must have p ≤ 2.5×10⁻⁶. | The coding link names the gene without author choice. 2.5×10⁻⁶ is exome-wide Bonferroni (0.05 / 20,000 genes). |
| HIGH_CONFIDENCE_FINE_MAPPING | The 95% credible set has ≤ 5 variants, and variants linked to **one** gene carry summed PIP ≥ 0.8. The link must be a coding or splice consequence, or a qualifying colocalization. | Fine-mapping identifies variants, not genes. Intronic position or nearest-gene placement is **not** a link, which closes the "fine-mapped then nearest gene" loophole. |
| PREREGISTERED_COLOCALIZATION | coloc-ABF with p1 = p2 = 1×10⁻⁴ and p12 = 5×10⁻⁶, a ±500 kb cis window, GTEx v8 (all tissues) or eQTLGen phase 1 cis-eQTL, PP.H4 ≥ 0.8, and exactly **one** gene at the locus reaching it. Run by the adjudication team; an author-reported colocalization counts only if it meets the same criteria. | p12 = 5×10⁻⁶ follows current coloc guidance; 1×10⁻⁵ over-calls. Requiring a unique gene prevents credit for multiple genes. |

A locus that meets no primary rule is `LOCUS_ONLY`. It earns locus-level sensitivity credit and never a gene-level primary positive.

The secondary classes are AUTHOR_NAMED, NEAREST_GENE, POSITIONAL_PROXIMITY_ONLY, GENERIC_DATABASE_GENE_FIELD, MODERN_L2G_ONLY, CURRENT_CURATED_TARGET_ONLY and TARGETED_CANDIDATE_GENE_CODING. OTHER_HIGH_SPECIFICITY_METHOD does not exist in V0.

## 2. Phenotype

- EXACT qualifies.
- SAME_CONCEPT_DIFFERENT_DEFINITION qualifies only when **both** reviewers assign it.
    - SAME_CONCEPT cases stay eligible for the salted duplicate draw. A drawn case's second review counts normally.
    - Every **undrawn** case that the first reviewer labels this way also gets a second review. It is mixed into the same second-reviewer batch with no indication of why (`review_phase: MANDATORY_SAME_CONCEPT`), and it is excluded from AC1 and from the coverage ratios.
    - Without a second review, the case fails closed.
- NARROWER never qualifies for the primary endpoint; it is sensitivity only, with no case-by-case exceptions.
- Every other relation does not qualify.
- UNRESOLVED fails closed.

## 3. Pre-T genetic state and novelty

| Parameter | Value | Rationale |
|---|---|---|
| QUALIFYING | p ≤ 5×10⁻⁸ | Genome-wide convention |
| SUGGESTIVE | p ≤ 1×10⁻⁵; or nominal p ≤ 0.05 in at least 2 independent pre-T candidate-gene studies | Suggestive-threshold convention. The candidate-gene clause is conservative for novelty; a sensitivity analysis without it is required. |
| Gene window for ScreenSignal | Gene body ± 500 kb, as-of-T gene model | Common locus-window convention. The same window is used for the universe screen ([NOVEL_STRICT_ELIGIBILITY_RULE.md](NOVEL_STRICT_ELIGIBILITY_RULE.md)). |
| Event novelty | Not novel if the post-T lead is within 500 kb **or** has r² ≥ 0.1 (1000 Genomes phase 3, matched ancestry) with a pre-T signal for the same disease | A deliberately permissive "same signal" test, so maturation cannot pass as novelty |
| Minimum coverage for NO_SIGNAL_OBSERVED | MODERATE (≥ 1 pre-T genome-wide study of the disease) | A sensitivity analysis restricted to HIGH is reported |

## 4. Agreement policy

| Element | Rule |
|---|---|
| Statistic | Gwet AC1 for every task, with Cohen κ, percent agreement and the full confusion matrix also reported. It is fixed now; no statistic is chosen after seeing prevalence. |
| Gated tasks | PRIMARY_ASSIGNMENT_ELIGIBILITY, PHENOTYPE_QUALIFICATION, NOVELTY_ELIGIBILITY, PRIMARY_POSITIVE_STATUS (each with 3 categories) |
| Reported tasks | Full assignment class, PreTGeneticState, event-family identity, sample overlap |
| Gate | The point estimate and the lower one-sided 90% bound (case bootstrap, BCa, 10,000 replicates, keyed seed) must each clear the manifest thresholds |
| Duplicate-review subset | min(N, max(30, ⌈0.30·N⌉)) cases, stratified by disease only (at least one case per non-empty stratum), in **salted** keyed-hash order: HMAC(key, `dup-review` ‖ s_rev ‖ case id), byte-encoded as in custody §7. The custodian review salt s_rev is committed in the S6 bundle. It is used privately by the custodian once the complete first-review label set is registered (public OSF + OTS), and published only after the second-review labels are registered. The first reviewer therefore cannot know which cases will be audited, and the second reviewer cannot tell drawn cases from mandatory ones ([BIG_0F_SELECTION_CUSTODY.md](BIG_0F_SELECTION_CUSTODY.md) §7). The same rule applies to the non-event duplicate subset. |
| Rule revision | At most one. It may only be a clarification that changes no value in adjudication policy v2 and is applied to **all** cases. Any other change is a protocol amendment (custody §9). After the revision, the first reviewer re-labels every case, and the complete post-revision label set is registered (public OSF + OTS). Only then does the custodian privately use a **second** salt s_ret, committed in S6, to draw the retest set: min(N, max(30, ⌈0.30·N⌉)) cases from **all** cases, stratified by disease, in s_ret order. The second reviewer reviews them under the revised rule, and s_ret is published after those labels are registered. Gates are evaluated on that retest set. The first reviewer therefore never knows which re-labelled cases will be checked. |
| Records | Both reviewers' categorical labels are stored for every duplicate-reviewed case |

## 5. Attention audits

| Audit | Statistic | Population |
|---|---|---|
| Attention vs assignment | Spearman ρ between the assigned gene's pre-T disease-specific attention percentile and an indicator of AUTHOR_NAMED or NEAREST_GENE assignment; Fisher-z 95% CI | All adjudicated post-T event families in the pilot. There is no separate matched sample. |
| Label-resolution bias | Spearman ρ between the nearest gene's attention percentile and an indicator that the locus resolves to any primary class; Fisher-z 95% CI | All post-T event families in the pilot |

Both audits trigger REDESIGN when the upper CI bound of |ρ| exceeds the GO bound in the manifest (MAX_ALLOWED: pass if ≤ the bound).
