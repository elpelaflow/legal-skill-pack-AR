#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_skeleton(intake: dict, candidates: dict, prior_art: dict) -> dict:
    first = candidates.get("candidates", [{}])[0]
    return {
        "title": intake.get("invention_name", first.get("title", "Pendiente")),
        "technical_field": intake.get("technical_field", "Pendiente"),
        "technical_problem": first.get("technical_problem", "Pendiente"),
        "solution_summary": first.get("technical_solution", "Pendiente"),
        "technical_effect": first.get("technical_effect", "Pendiente"),
        "prior_art_note": f"Hay {len(prior_art.get('rows', []))} lineas de antecedente a revisar.",
    }


def write_markdown(path: Path, data: dict) -> None:
    lines = [
        "# Borrador de divulgacion tecnica",
        "",
        f"## Titulo",
        data["title"],
        "",
        "## Campo tecnico",
        data["technical_field"],
        "",
        "## Problema tecnico",
        data["technical_problem"],
        "",
        "## Resumen de la solucion",
        data["solution_summary"],
        "",
        "## Efecto tecnico",
        data["technical_effect"],
        "",
        "## Nota de antecedentes",
        data["prior_art_note"],
        "",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True)
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--prior-art", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    data = build_skeleton(load_json(Path(args.intake)), load_json(Path(args.candidates)), load_json(Path(args.prior_art)))
    (out_dir / "BorradorDivulgacionPatente.json").write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    write_markdown(out_dir / "BorradorDivulgacionPatente.md", data)


if __name__ == "__main__":
    main()
