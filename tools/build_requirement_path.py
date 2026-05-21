#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_list(values):
    return [str(value).strip().lower() for value in values or [] if str(value).strip()]


def build_requirement_path(intake: dict, signals: dict) -> dict:
    declared = normalize_list(intake.get("additional_requirements", []))
    exports_numeric = float(intake.get("exports_share_numeric", 0) or 0)
    activities = {item["activity"] for item in signals.get("activities", [])}

    scores = {
        "calidad": 2 if "calidad" in declared else 0,
        "capacitacion": 2 if "capacitacion" in declared else 0,
        "i+d": 2 if "i+d" in declared or "id" in declared else 0,
        "exportaciones": 2 if "exportaciones" in declared else 0,
    }

    if exports_numeric > 0:
        scores["exportaciones"] += 2
    if "ia_datos" in activities or "cloud_automatizacion" in activities:
        scores["i+d"] += 1
    if intake.get("training_hours") or intake.get("training_plan"):
        scores["capacitacion"] += 1
    if intake.get("quality_certification"):
        scores["calidad"] += 2

    ordered = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    primary = ordered[0][0] if ordered and ordered[0][1] > 0 else "pendiente"
    secondary = [name for name, score in ordered[1:] if score > 0]

    gaps = {
        "calidad": [
            "Falta documentar certificacion vigente o sistema formalizado de calidad."
        ],
        "capacitacion": [
            "Falta plan anual, horas y constancias asociadas a la nomina promovida."
        ],
        "i+d": [
            "Falta separar investigacion/desarrollo tecnico de mantenimiento ordinario."
        ],
        "exportaciones": [
            "Falta respaldo de ventas al exterior y segregacion de ingresos promovidos."
        ],
    }

    recommended_gaps = gaps.get(primary, ["Definir carril principal y evidencia asociada."])
    complementary_gaps = {name: gaps[name] for name in secondary}

    return {
        "declared_requirements": declared,
        "scores": scores,
        "primary_path": primary,
        "secondary_paths": secondary,
        "primary_gaps": recommended_gaps,
        "secondary_gaps": complementary_gaps,
    }


def write_markdown(data: dict, out_path: Path) -> None:
    lines = [
        "# Carril de requisitos LEC",
        "",
        f"- Carril principal sugerido: {data['primary_path']}",
        "",
        "## Puntajes",
        "",
    ]
    for name, score in sorted(data["scores"].items(), key=lambda item: item[1], reverse=True):
        lines.append(f"- {name}: {score}")

    lines.extend(["", "## Carriles complementarios", ""])
    for name in data["secondary_paths"] or ["sin_carriles_complementarios"]:
        lines.append(f"- {name}")

    lines.extend(["", "## Vacios del carril principal", ""])
    for item in data["primary_gaps"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Vacios complementarios", ""])
    if data["secondary_gaps"]:
        for name, gaps in data["secondary_gaps"].items():
            lines.append(f"### {name}")
            for gap in gaps:
                lines.append(f"- {gap}")
            lines.append("")
    else:
        lines.append("- No se detectaron vacios complementarios.")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--signals", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    data = build_requirement_path(
        load_json(Path(args.input)),
        load_json(Path(args.signals)),
    )
    (out_dir / "CarrilRequisitosLEC.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    write_markdown(data, out_dir / "CarrilRequisitosLEC.md")


if __name__ == "__main__":
    main()
