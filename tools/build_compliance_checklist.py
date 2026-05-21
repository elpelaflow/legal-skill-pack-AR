#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_checklist(intake: dict, requirements: dict) -> dict:
    inscription_date = intake.get("expected_inscription_date") or "Pendiente"
    annual_due = "Pendiente"
    biennial_due = "Pendiente"

    if inscription_date != "Pendiente":
        try:
            base = datetime.strptime(inscription_date, "%Y-%m-%d")
            annual_due = base.replace(year=base.year + 1).strftime("%Y-%m-%d")
            biennial_due = base.replace(year=base.year + 2).strftime("%Y-%m-%d")
        except ValueError:
            pass

    items = [
        "Controlar continuidad de actividad promovida y su segregacion.",
        "Actualizar nomina afectada y altas/bajas relevantes.",
        "Documentar capacitacion, I+D, calidad o exportaciones que sostienen requisitos adicionales.",
        "Preparar presentacion anual con soporte verificable.",
        "Preparar revalidacion bienal desde la fecha de inscripcion.",
        "Verificar pago de tasa de verificacion y control.",
        "Conservar evidencia para auditorias e inspecciones.",
    ]
    primary_path = requirements.get("primary_path", "pendiente")
    path_task = {
        "calidad": "Actualizar certificaciones, procedimientos y evidencia de mejora continua.",
        "capacitacion": "Actualizar plan anual, horas, asistentes y constancias de capacitacion.",
        "i+d": "Actualizar backlog, experimentos, PoCs y resultados de investigacion/desarrollo.",
        "exportaciones": "Actualizar contratos, factura E, soporte operativo y segregacion de exportaciones.",
    }.get(primary_path, "Definir carril principal de requisito adicional.")
    items.insert(2, path_task)
    return {
        "expected_inscription_date": inscription_date,
        "annual_due": annual_due,
        "biennial_due": biennial_due,
        "primary_path": primary_path,
        "items": items,
    }


def write_markdown(data: dict, out_path: Path) -> None:
    lines = [
        "# Checklist de permanencia LEC",
        "",
        f"- Fecha base de inscripcion: {data['expected_inscription_date']}",
        f"- Vencimiento anual orientativo: {data['annual_due']}",
        f"- Revalidacion bienal orientativa: {data['biennial_due']}",
        f"- Carril principal a sostener: {data['primary_path']}",
        "",
        "## Tareas",
        "",
    ]
    for item in data["items"]:
        lines.append(f"- {item}")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True)
    parser.add_argument("--requirements", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    checklist = build_checklist(
        load_json(Path(args.intake)),
        load_json(Path(args.requirements)),
    )
    (out_dir / "ChecklistPermanenciaLEC.json").write_text(
        json.dumps(checklist, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    write_markdown(checklist, out_dir / "ChecklistPermanenciaLEC.md")


if __name__ == "__main__":
    main()
