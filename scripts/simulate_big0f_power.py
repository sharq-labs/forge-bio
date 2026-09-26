from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from pathlib import Path
from statistics import NormalDist


ENGINE_DOMAIN = "forge-bio-big0f-power-v1"
MIN_EFFECT = 0.05
ALPHA = 0.05
MIN_REPLICATES = 10000
MIN_POSITIVES = 30


def estimate_power(
    n_diseases: int,
    *,
    effect: float,
    disease_level_sd: float,
    alpha: float,
    replicates: int,
    seed: int,
) -> float:
    if n_diseases < 1:
        raise ValueError("n_diseases must be positive")
    if not math.isfinite(effect) or effect <= 0:
        raise ValueError("effect must be finite and positive")
    if not math.isfinite(disease_level_sd) or disease_level_sd <= 0:
        raise ValueError("disease_level_sd must be finite and positive")
    if alpha != ALPHA:
        raise ValueError("V0 alpha is frozen at 0.05")
    if replicates < MIN_REPLICATES:
        raise ValueError("at least 10,000 Monte Carlo replicates are required")

    zcrit = NormalDist().inv_cdf(1.0 - alpha)
    rng = random.Random(f"{ENGINE_DOMAIN}:{seed}:{n_diseases}:{effect}:{disease_level_sd}:{replicates}")
    threshold = zcrit * disease_level_sd / math.sqrt(n_diseases)

    successes = 0
    mean_sd = disease_level_sd / math.sqrt(n_diseases)
    for _ in range(replicates):
        simulated_mean = rng.gauss(effect, mean_sd)
        if simulated_mean > threshold:
            successes += 1
    return successes / replicates


def required_diseases(
    *,
    effect: float,
    disease_level_sd: float,
    target_power: float,
    alpha: float,
    replicates: int,
    seed: int,
    max_diseases: int = 500,
) -> tuple[int, float]:
    if not 0.80 <= target_power <= 0.99:
        raise ValueError("target_power must be in [0.80, 0.99]")
    for n in range(2, max_diseases + 1):
        p = estimate_power(
            n,
            effect=effect,
            disease_level_sd=disease_level_sd,
            alpha=alpha,
            replicates=replicates,
            seed=seed,
        )
        if p >= target_power:
            return n, p
    raise ValueError("target power not reached within max_diseases")


def canonical_digest(payload: dict) -> str:
    body = dict(payload)
    body.pop("digest", None)
    encoded = json.dumps(body, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def build_artifact(
    *,
    power_analysis_id: str,
    disease_level_sd: float,
    target_power: float,
    replicates: int,
    seed: int,
    input_provenance_ids: list[str],
    engine_sha256: str,
) -> dict:
    n, power = required_diseases(
        effect=MIN_EFFECT,
        disease_level_sd=disease_level_sd,
        target_power=target_power,
        alpha=ALPHA,
        replicates=replicates,
        seed=seed,
    )
    artifact = {
        "power_analysis_id": power_analysis_id,
        "schema_version": "big0f-power-analysis-v1",
        "method": "PAIRED_DISEASE_MONTE_CARLO_NORMAL_APPROX",
        "alpha": ALPHA,
        "target_power": target_power,
        "minimum_scientifically_meaningful_effect": MIN_EFFECT,
        "disease_level_sd": disease_level_sd,
        "simulation_replicates": replicates,
        "simulation_seed": seed,
        "estimated_power": power,
        "required_confirmatory_disease_count": n,
        "required_high_specificity_positive_count": MIN_POSITIVES,
        "input_provenance_ids": input_provenance_ids,
        "engine_sha256": engine_sha256,
    }
    artifact["digest"] = canonical_digest(artifact)
    return artifact


def verify_artifact(artifact: dict, *, engine_sha256: str) -> list[str]:
    errors: list[str] = []
    if artifact.get("engine_sha256") != engine_sha256:
        errors.append("power artifact engine_sha256 does not match current engine")
        return errors
    try:
        rebuilt = build_artifact(
            power_analysis_id=artifact["power_analysis_id"],
            disease_level_sd=artifact["disease_level_sd"],
            target_power=artifact["target_power"],
            replicates=artifact["simulation_replicates"],
            seed=artifact["simulation_seed"],
            input_provenance_ids=artifact["input_provenance_ids"],
            engine_sha256=engine_sha256,
        )
    except Exception as exc:
        return [f"cannot recompute power artifact: {exc}"]

    for key, expected in rebuilt.items():
        actual = artifact.get(key)
        if isinstance(expected, float):
            if not isinstance(actual, (int, float)) or not math.isfinite(float(actual)) or abs(float(actual) - expected) > 1e-12:
                errors.append(f"power artifact mismatch for {key}: {actual!r} != {expected!r}")
        elif actual != expected:
            errors.append(f"power artifact mismatch for {key}: {actual!r} != {expected!r}")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description="Compute/verify BIG 0F confirmatory power inputs")
    ap.add_argument("--id", default="BIG0F-POWER-V1")
    ap.add_argument("--disease-level-sd", type=float, required=True)
    ap.add_argument("--target-power", type=float, default=0.80)
    ap.add_argument("--replicates", type=int, default=20000)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--input-provenance-id", action="append", required=True)
    ap.add_argument("--engine-sha256", required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()

    if args.verify:
        artifact = json.loads(args.output.read_text(encoding="utf-8"), parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))
        errors = verify_artifact(artifact, engine_sha256=args.engine_sha256)
        if errors:
            for err in errors:
                print(err)
            return 1
        print("VALID")
        return 0

    artifact = build_artifact(
        power_analysis_id=args.id,
        disease_level_sd=args.disease_level_sd,
        target_power=args.target_power,
        replicates=args.replicates,
        seed=args.seed,
        input_provenance_ids=args.input_provenance_id,
        engine_sha256=args.engine_sha256,
    )
    args.output.write_text(json.dumps(artifact, sort_keys=True, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(artifact["digest"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
