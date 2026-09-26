# ADR-005 — Licensing Posture

**Status:** Accepted — commercial-later engineering posture

## Decision

Forge Bio is designed for **commercial later**.

Repository source code and project documentation are licensed under **Apache License 2.0** unless a file explicitly states otherwise.

Provider data, downloaded artifacts, model weights, ontologies, mappings, and derived datasets do **not** inherit the repository license. Their source-specific rights and restrictions remain separately governed by SourceSnapshot license manifests.

## Provider rule

Provider selection and redistribution architecture must not assume that research-access data can be redistributed or used commercially.

Every SourceSnapshot records:
- license name/version;
- terms version/hash;
- attribution requirements;
- commercial-use status;
- redistribution constraints;
- derived-data constraints;
- share-alike/copyleft obligations where applicable;
- reviewer/status.

A provider may be:
- usable for internal research;
- prohibited from redistribution;
- prohibited from commercial use;
- excluded from the commercial-later core.

These states are independent of code licensing.

## Consequences

- the open repository may evolve toward commercial use without silently inheriting incompatible data rights;
- restrictive providers are isolated behind adapters/manifests;
- public releases exclude provider data unless redistribution rights are verified;
- future legal review may tighten provider eligibility without changing the scientific architecture.

This ADR defines engineering posture and is not legal advice.
