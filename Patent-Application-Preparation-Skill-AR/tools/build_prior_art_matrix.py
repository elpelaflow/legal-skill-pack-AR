#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_matrix(candidates: dict) -> dict:
    rows = []
    for item in candidates.get("candidates", []):
        rows.append({
            "candidate": item["title"],
            "search_terms": [item["title"], item["technical_problem"]],
            "checkpoints": [
                "validar novedad",
                "validar actividad inventiva",
                "buscar antecedente tecnico cercano",
            ],
        })
    return {"rows": rows}


def write_markdown(path: Path, data: dict) -> None:
    lines = ["# Matriz de antecedentes", ""]
    for row in data["rows"] or [{"candidate": "Pendiente", "search_terms": [], "checkpoints": []}]:
        lines.append(f"## {row['candidate']}")
        lines.append(f"- Terminos: {', '.join(row['search_terms']) or 'Pendiente'}")
        for cp in row["checkpoints"]:
            lines.append(f"- {cp}")
        lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    data = build_matrix(load_json(Path(args.candidates)))
    (out_dir / "MatrizAntecedentes.json").write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    write_markdown(out_dir / "MatrizAntecedentes.md", data)


if __name__ == "__main__":
    main()
