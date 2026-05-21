#!/usr/bin/env python3
"""Consolidar borradores de Política de Privacidad y Términos y Condiciones."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_privacy(path: Path, intake: dict, privacy: dict) -> None:
    lines = [
        "# Política de Privacidad (Borrador)",
        "",
        f"Este documento describe cómo {intake.get('service_owner') or 'el titular del servicio'} trata datos personales en {intake.get('service_name') or 'el servicio'}.",
        "",
        "## Datos recolectados",
        "",
        f"- {privacy.get('data_categories') or 'Pendiente'}",
        "",
        "## Trackers y tecnologías similares",
        "",
        f"- {privacy.get('trackers') or 'Ninguno declarado'}",
        "",
        "## Permisos móviles",
        "",
        f"- {privacy.get('mobile_permissions') or 'Ninguno declarado'}",
        "",
        "## Terceros",
        "",
        f"- {privacy.get('third_parties') or 'Pendiente'}",
        "",
        "## Señales especiales",
        "",
        f"- Datos sensibles: {'Sí' if privacy.get('sensitive_data') else 'No'}",
        f"- Datos de menores: {'Sí' if privacy.get('minor_data') else 'No'}",
        f"- Geolocalización precisa: {'Sí' if privacy.get('precise_geolocation') else 'No'}",
        f"- Biometría: {'Sí' if privacy.get('biometric_processing') else 'No'}",
        f"- Tracking publicitario: {'Sí' if privacy.get('ads_tracking') else 'No'}",
        "",
        "## Derechos",
        "",
        "- Pendiente completar canal de ejercicio de derechos.",
        "",
        "```text",
        "STOP_FOR_USER",
        "NEXT_ACTION: Revise la política de privacidad y confirme antes de publicarla.",
        "```",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_terms(path: Path, intake: dict, terms: dict) -> None:
    lines = [
        "# Términos y Condiciones (Borrador)",
        "",
        f"Estos términos regulan el uso de {intake.get('service_name') or 'el servicio'}, operado por {intake.get('service_owner') or 'el titular'}.",
        "",
        "## Uso del servicio",
        "",
        "- Pendiente completar.",
        "",
        "## Cuentas",
        "",
        f"- {'El servicio prevé cuentas de usuario.' if terms.get('user_accounts') else 'No se informaron cuentas de usuario.'}",
        "",
        "## Pagos / Suscripciones",
        "",
        f"- {'El servicio incluye pagos o suscripciones.' if terms.get('payments') else 'No se informaron pagos.'}",
        "",
        "## Publicidad",
        "",
        f"- {'El servicio incluye monetización con anuncios.' if terms.get('ads') else 'No se informó monetización con anuncios.'}",
        "",
        "## Cláusulas reforzadas",
        "",
    ]
    if terms.get("clauses_required"):
        lines.extend(f"- {item}" for item in terms["clauses_required"])
    else:
        lines.append("- Pendiente")
    lines.extend([
        "",
        "## Ley y jurisdicción",
        "",
        "- Pendiente completar.",
        "",
        "```text",
        "STOP_FOR_USER",
        "NEXT_ACTION: Revise los términos y condiciones y confirme antes de publicarlos.",
        "```",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True)
    parser.add_argument("--service-map", required=True)
    parser.add_argument("--privacy", required=True)
    parser.add_argument("--terms", required=True)
    parser.add_argument("--out-dir", default="LegalesAppAR/Borradores")
    args = parser.parse_args()

    intake = load_json(Path(args.intake))
    _service_map = load_json(Path(args.service_map))
    privacy = load_json(Path(args.privacy))
    terms = load_json(Path(args.terms))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_privacy(out_dir / "PoliticaPrivacidad.md", intake, privacy)
    write_terms(out_dir / "TerminosYCondiciones.md", intake, terms)
    print(f"OK legales: {out_dir}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
