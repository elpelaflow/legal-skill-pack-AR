#!/usr/bin/env python3
"""Generar matriz de riesgo para smart contracts en Argentina."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build(data: dict) -> dict:
    assets = [str(item).lower() for item in data.get("assets_involved", [])]
    deps = [str(item).lower() for item in data.get("external_dependencies", [])]
    purpose = str(data.get("business_purpose", "")).lower()
    action = str(data.get("automated_action", "")).lower()
    joined = " ".join(assets + deps + [purpose, action])
    risk_flags = []
    if any(word in joined for word in ["pago", "payment", "token", "cripto", "stablecoin"]):
        risk_flags.append("pagos_o_criptoactivos")
    if any(word in joined for word in ["dato", "personal", "cliente", "dataset"]):
        risk_flags.append("datos_personales")
    if any(word in joined for word in ["consumidor", "usuario final", "retail"]):
        risk_flags.append("consumo")
    if any(word in joined for word in ["oraculo", "oráculo", "validacion humana", "validación humana", "api externa"]):
        risk_flags.append("dependencia_externa")
    if any(word in joined for word in ["tokenizacion", "tokenización", "activo real", "royalty", "revenue split", "escrow", "vesting"]):
        risk_flags.append("estructura_contractual_sensible")
    if len(risk_flags) >= 3:
        level = "alto"
    elif len(risk_flags) >= 1:
        level = "medio"
    else:
        level = "bajo"
    if "datos_personales" in risk_flags and "pagos_o_criptoactivos" in risk_flags:
        level = "alto"
    pattern = "general"
    if "escrow" in joined or "hito" in joined:
        pattern = "escrow"
    elif "vesting" in joined:
        pattern = "vesting"
    elif "revenue split" in joined or "royalty" in joined:
        pattern = "revenue_split"
    return {
        "project_name": data.get("project_name", ""),
        "risk_flags": risk_flags,
        "risk_level": level,
        "execution_pattern": pattern,
        "irreversibility_concern": True,
        "confirmation_required": True,
        "user_confirmed": False,
    }


def write_md(path: Path, result: dict) -> None:
    lines = [
        "# Matriz de Riesgo",
        "",
        f"- Proyecto: {result.get('project_name') or 'Pendiente'}",
        f"- Riesgos detectados: {result.get('risk_flags') or 'Ninguno detectado automáticamente'}",
        f"- Nivel de riesgo: {result.get('risk_level') or 'Pendiente'}",
        f"- Patrón detectado: {result.get('execution_pattern') or 'Pendiente'}",
        f"- Preocupación por irreversibilidad: {'Sí' if result.get('irreversibility_concern') else 'No'}",
        "",
        "```text",
        "STOP_FOR_USER",
        "NEXT_ACTION: Confirme riesgos regulatorios y de ejecución antes de consolidar la especificación.",
        "```",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-dir", default="SmartContractSpecAR/Borradores")
    args = parser.parse_args()
    data = load_json(Path(args.input))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    result = build(data)
    (out_dir / "MatrizRiesgo.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_md(out_dir / "MatrizRiesgo.md", result)
    print(f"OK riesgo: {out_dir / 'MatrizRiesgo.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
