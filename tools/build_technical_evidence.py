#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def build_evidence(signals: dict) -> dict:
    activities = []
    for item in signals.get("activities", []):
        strength = item["strength"]
        proof_level = "fuerte" if strength == "alta" else "media" if strength == "media" else "debil"
        activities.append({
            "activity": item["activity"],
            "summary": item["description"],
            "proof_level": proof_level,
            "evidence": item.get("evidence", []),
            "gaps": [] if proof_level == "fuerte" else ["Agregar mas soporte documental o funcional."],
        })

    return {
        "project_root": signals.get("project_root"),
        "activities": activities,
        "risks": signals.get("risks", []),
    }


def write_markdown(data: dict, out_path: Path) -> None:
    lines = [
        "# Evidencia tecnica LEC",
        "",
        f"- Proyecto: `{data.get('project_root', 'Pendiente')}`",
        "",
    ]

    for item in data["activities"]:
        lines.append(f"## {item['activity']}")
        lines.append(f"- Resumen: {item['summary']}")
        lines.append(f"- Nivel probatorio: {item['proof_level']}")
        for evidence in item["evidence"]:
            lines.append(f"- Evidencia: {evidence}")
        for gap in item["gaps"]:
            lines.append(f"- Vacio: {gap}")
        lines.append("")

    lines.append("## Riesgos")
    lines.append("")
    for risk in data["risks"] or ["sin_riesgos_detectados"]:
        lines.append(f"- {risk}")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--signals", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    signals = json.loads(Path(args.signals).read_text(encoding="utf-8"))

    data = build_evidence(signals)
    (out_dir / "EvidenciaTecnicaLEC.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    write_markdown(data, out_dir / "EvidenciaTecnicaLEC.md")


if __name__ == "__main__":
    main()
