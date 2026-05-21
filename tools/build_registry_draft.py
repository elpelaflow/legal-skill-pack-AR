#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_company_size(size: str) -> str:
    value = (size or "").strip().lower()
    mapping = {
        "micro": "micro",
        "pequena": "pequena",
        "pequeña": "pequena",
        "small": "pequena",
        "mediana": "mediana",
        "medium": "mediana",
        "grande": "grande",
        "large": "grande",
    }
    return mapping.get(value, "pendiente")


def build_draft(intake: dict, signals: dict, evidence: dict, requirements: dict) -> dict:
    promoted = [item["activity"] for item in evidence.get("activities", [])]
    company_size = normalize_company_size(intake.get("company_size", ""))
    return {
        "company_name": intake.get("company_name", "Pendiente"),
        "cuit": intake.get("cuit", "Pendiente"),
        "company_size": company_size,
        "main_activity": intake.get("main_activity", "Pendiente"),
        "project_name": intake.get("project_name", "Pendiente"),
        "promoted_activities": promoted,
        "technical_summary": [
            item["summary"] for item in evidence.get("activities", [])[:3]
        ],
        "billing_share_promoted": intake.get("billing_share_promoted", "Pendiente"),
        "exports_share": intake.get("exports_share", "Pendiente"),
        "promoted_headcount": intake.get("promoted_headcount", "Pendiente"),
        "additional_requirements": intake.get("additional_requirements", []),
        "primary_requirement_path": requirements.get("primary_path", "pendiente"),
        "secondary_requirement_paths": requirements.get("secondary_paths", []),
        "requirement_gaps": requirements.get("primary_gaps", []),
        "risks": sorted(set(signals.get("risks", []) + intake.get("risks", []))),
        "formal_notes": [
            "Borrador orientado a Formulario 1278 + TAD.",
            "Requiere validacion societaria, fiscal y contable antes de presentacion.",
        ],
    }


def write_markdown(data: dict, out_path: Path) -> None:
    lines = [
        "# Solicitud LEC",
        "",
        "## Identificacion",
        "",
        f"- Razon social: {data['company_name']}",
        f"- CUIT: {data['cuit']}",
        f"- Tamano empresa: {data['company_size']}",
        f"- Actividad principal: {data['main_activity']}",
        f"- Proyecto / unidad de negocio: {data['project_name']}",
        "",
        "## Actividades promovidas sugeridas",
        "",
    ]

    for activity in data["promoted_activities"] or ["Pendiente"]:
        lines.append(f"- {activity}")

    lines.extend(["", "## Resumen tecnico", ""])
    for item in data["technical_summary"] or ["Pendiente"]:
        lines.append(f"- {item}")

    lines.extend([
        "",
        "## Variables economicas",
        "",
        f"- Facturacion promovida estimada: {data['billing_share_promoted']}",
        f"- Exportaciones estimadas: {data['exports_share']}",
        f"- Nomina afectada: {data['promoted_headcount']}",
        "",
        "## Requisitos adicionales invocados",
        "",
    ])
    for item in data["additional_requirements"] or ["Pendiente"]:
        lines.append(f"- {item}")

    lines.extend([
        "",
        "## Carril sugerido",
        "",
        f"- Principal: {data['primary_requirement_path']}",
    ])
    for item in data["secondary_requirement_paths"] or ["Sin complementarios"]:
        lines.append(f"- Complementario: {item}")

    lines.extend(["", "## Vacios del carril sugerido", ""])
    for item in data["requirement_gaps"] or ["Sin vacios detectados"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Riesgos y faltantes", ""])
    for risk in data["risks"] or ["sin_riesgos_detectados"]:
        lines.append(f"- {risk}")

    lines.extend(["", "## Notas formales", ""])
    for note in data["formal_notes"]:
        lines.append(f"- {note}")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True)
    parser.add_argument("--signals", required=True)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--requirements", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    draft = build_draft(
        load_json(Path(args.intake)),
        load_json(Path(args.signals)),
        load_json(Path(args.evidence)),
        load_json(Path(args.requirements)),
    )
    (out_dir / "SolicitudLEC.json").write_text(
        json.dumps(draft, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    write_markdown(draft, out_dir / "SolicitudLEC.md")


if __name__ == "__main__":
    main()
