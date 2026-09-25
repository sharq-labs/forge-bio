# ADR-005 — Licensing Posture

**Status:** OPEN — must be decided before provider implementation

## Decision required

Choose one:
1. academic/open research only;
2. commercial product later;
3. commercial from day one.

## Recommended default

Design for **commercial later** unless project ownership decides otherwise.

That means provider selection and redistribution architecture should avoid assuming that all research-access data can later be redistributed commercially.

## Consequences

- every source snapshot carries license metadata;
- restrictive providers may be excluded from core dependencies;
- provider qualification includes redistribution/derived-data constraints;
- a future commercial mode must not inherit incompatible data silently.

This ADR is engineering governance, not legal advice.
