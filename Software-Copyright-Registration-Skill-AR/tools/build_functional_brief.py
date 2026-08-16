#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_brief(intake: dict, scan: dict) -> dict:
    dirs = sorted(scan.get("top_directories", {}).keys())[:8]
    return {
        "work_name": intake.get("work_name", "Pendiente"),
        "category": intake.get("category", "Pendiente"),
        "summary": f"Software de categoria {intake.get('category', 'Pendiente')} con estructura relevada en {', '.join(dirs) or 'directorios no identificados'}.",
        "modules": dirs,
    }


def write_markdown(path: Path, data: dict) -> None:
    lines = [
        "# Descripcion funcional",
        "",
        f"- Obra: {data['work_name']}",
        f"- Categoria: {data['category']}",
        "",
        data["summary"],
        "",
        "## Modulos o areas visibles",
        "",
    ]
    for item in data["modules"] or ["Pendiente"]:
        lines.append(f"- {item}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True)
    parser.add_argument("--scan", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    data = build_brief(load_json(Path(args.intake)), load_json(Path(args.scan)))
    (out_dir / "DescripcionFuncionalDNDA.json").write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    write_markdown(out_dir / "DescripcionFuncionalDNDA.md", data)


if __name__ == "__main__":
    main()
