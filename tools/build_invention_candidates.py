#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_candidates(intake: dict, scan: dict) -> dict:
    candidates = []
    for signal, count in sorted(scan.get("signal_counts", {}).items(), key=lambda item: item[1], reverse=True)[:4]:
        candidates.append({
            "title": f"Candidato sobre {signal}",
            "technical_problem": intake.get("technical_problem", "Pendiente"),
            "technical_solution": f"Posible solucion tecnica apoyada en senales de {signal}.",
            "technical_effect": f"Mejora tecnica vinculada a {signal}.",
            "risk_note": "Verificar que no se trate de abstraccion no tecnica.",
        })
    return {"candidates": candidates}


def write_markdown(path: Path, data: dict) -> None:
    lines = ["# Candidatos de invencion", ""]
    for item in data["candidates"] or [{"title": "Pendiente", "technical_problem": "Pendiente", "technical_solution": "Pendiente", "technical_effect": "Pendiente", "risk_note": "Pendiente"}]:
        lines.append(f"## {item['title']}")
        lines.append(f"- Problema tecnico: {item['technical_problem']}")
        lines.append(f"- Solucion tecnica: {item['technical_solution']}")
        lines.append(f"- Efecto tecnico: {item['technical_effect']}")
        lines.append(f"- Riesgo: {item['risk_note']}")
        lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True)
    parser.add_argument("--scan", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    data = build_candidates(load_json(Path(args.intake)), load_json(Path(args.scan)))
    (out_dir / "CandidatosInvencion.json").write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    write_markdown(out_dir / "CandidatosInvencion.md", data)


if __name__ == "__main__":
    main()
