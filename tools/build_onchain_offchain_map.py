#!/usr/bin/env python3
"""Generar mapa on-chain / off-chain."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build(data: dict) -> dict:
    return {
        "project_name": data.get("project_name", ""),
        "onchain": [],
        "offchain": [],
        "external_dependencies": data.get("external_dependencies", []),
        "confirmation_required": True,
        "user_confirmed": False,
    }


def write_md(path: Path, result: dict) -> None:
    lines = [
        "# Mapa On-chain / Off-chain",
        "",
        f"- Proyecto: {result.get('project_name') or 'Pendiente'}",
        f"- Dependencias externas: {result.get('external_dependencies') or 'Ninguna declarada'}",
        "",
        "## On-chain",
        "",
        "- Pendiente",
        "",
        "## Off-chain",
        "",
        "- Pendiente",
        "",
        "```text",
        "STOP_FOR_USER",
        "NEXT_ACTION: Confirme qué componentes deben quedar on-chain y cuáles off-chain.",
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
    (out_dir / "MapaOnchainOffchain.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_md(out_dir / "MapaOnchainOffchain.md", result)
    print(f"OK split: {out_dir / 'MapaOnchainOffchain.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
