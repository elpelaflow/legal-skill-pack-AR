#!/usr/bin/env python3
"""Sugerir bases de datos personales a partir del intake y señales del sistema."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DATABASE_RULES = [
    ("users_customers", "Usuarios / Clientes", ["auth", "billing"]),
    ("leads_marketing", "Leads / Marketing / CRM", ["marketing"]),
    ("support_tickets", "Soporte / Tickets / Conversaciones", ["support"]),
    ("hr_people", "Empleados / Candidatos / RRHH", ["hr"]),
    ("analytics_identifiable", "Analytics con identificabilidad", ["analytics"]),
    ("payments_fraud", "Pagos / Fraude / Riesgo", ["billing", "fraud"]),
    ("health_sensitive", "Salud / Datos Sensibles", ["health"]),
    ("surveillance_access", "Videovigilancia / Control de Accesos", ["surveillance"]),
    ("vendors_subprocessors", "Terceros con acceso operativo", ["vendors"]),
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_text(values: list[str]) -> str:
    return " ".join(str(value).lower() for value in values)


def default_subjects(code: str) -> list[str]:
    mapping = {
        "users_customers": ["usuarios", "clientes"],
        "leads_marketing": ["leads", "prospectos"],
        "support_tickets": ["usuarios", "clientes"],
        "hr_people": ["empleados", "candidatos"],
        "analytics_identifiable": ["usuarios", "visitantes"],
        "payments_fraud": ["clientes", "pagadores"],
        "health_sensitive": ["pacientes", "usuarios"],
        "surveillance_access": ["visitantes", "empleados", "proveedores"],
        "vendors_subprocessors": ["usuarios", "clientes", "empleados"],
    }
    return mapping.get(code, [])


def default_categories(code: str) -> list[str]:
    mapping = {
        "users_customers": ["identificación", "contacto", "cuenta", "uso del servicio"],
        "leads_marketing": ["contacto", "interés comercial", "origen de lead"],
        "support_tickets": ["contacto", "incidencias", "historial de soporte"],
        "hr_people": ["identificación", "laborales", "candidatura"],
        "analytics_identifiable": ["identificadores en línea", "IP", "eventos de uso"],
        "payments_fraud": ["facturación", "transacciones", "antifraude"],
        "health_sensitive": ["salud", "identificación", "prestación"],
        "surveillance_access": ["imágenes", "accesos", "identificación"],
        "vendors_subprocessors": ["metadatos operativos", "credenciales", "soporte"],
    }
    return mapping.get(code, [])


def infer_sensitive(code: str, intake: dict, joined_categories: str) -> bool:
    if code == "health_sensitive":
        return True
    if code == "hr_people" and any(word in joined_categories for word in ["salud", "biometr", "sindical", "penal"]):
        return True
    if code == "surveillance_access" and any(word in joined_categories for word in ["biometr"]):
        return True
    if code == "users_customers" and intake.get("sensitive_data", False) and any(word in joined_categories for word in ["salud", "biometr", "financier", "origen", "politic", "sindical"]):
        return True
    return False


def suggest(intake: dict, scan: dict) -> dict:
    groups = [str(item).lower() for item in intake.get("data_subject_groups", [])]
    categories = [str(item).lower() for item in intake.get("data_categories", [])]
    systems = [str(item).lower() for item in intake.get("systems", [])]
    vendors = [str(item) for item in intake.get("vendors", [])]
    hosting_locations = [str(item).lower() for item in intake.get("hosting_locations", [])]
    signals = scan.get("signals", {})
    joined_groups = normalize_text(groups)
    joined_categories = normalize_text(categories)
    joined_systems = normalize_text(systems)
    databases = []
    for code, title, areas in DATABASE_RULES:
        found = any(signals.get(area) for area in areas)
        if not found:
            if code == "hr_people" and any(word in " ".join(groups) for word in ["emple", "candidat", "rrhh"]):
                found = True
            if code == "users_customers" and any(word in " ".join(groups) for word in ["usuario", "cliente"]):
                found = True
            if code == "leads_marketing" and any(word in " ".join(groups) for word in ["lead", "prospect", "marketing"]):
                found = True
            if code == "payments_fraud" and any(word in (joined_systems + " " + joined_categories) for word in ["pago", "payment", "fraud", "riesgo", "transacci"]):
                found = True
            if code == "health_sensitive" and any(word in (joined_systems + " " + joined_categories + " " + joined_groups) for word in ["salud", "patient", "paciente", "medical"]):
                found = True
            if code == "surveillance_access" and any(word in (joined_systems + " " + joined_categories) for word in ["camara", "cámara", "video", "acceso", "badge"]):
                found = True
        if found:
            sensitive = infer_sensitive(code, intake, joined_categories)
            international = any(location != "argentina" for location in hosting_locations)
            databases.append(
                {
                    "code": code,
                    "name": title,
                    "purpose": "",
                    "data_subjects": default_subjects(code),
                    "data_categories": default_categories(code),
                    "sensitive_data": sensitive,
                    "third_parties": vendors[:6] if code in {"vendors_subprocessors", "analytics_identifiable", "payments_fraud", "support_tickets", "leads_marketing"} else [],
                    "international_transfer": international,
                    "retention_criteria": "",
                    "selected": True,
                    "risk_level": "alto" if sensitive or code in {"payments_fraud", "health_sensitive"} else ("medio" if international or code in {"analytics_identifiable", "surveillance_access", "vendors_subprocessors"} else "bajo"),
                }
            )
    return {
        "controller_name": intake.get("controller_name", ""),
        "vendor_summary": scan.get("vendor_summary", {}),
        "databases": databases,
        "confirmation_required": True,
        "user_confirmed": False,
    }


def write_markdown(path: Path, result: dict) -> None:
    lines = ["# Bases Detectadas", ""]
    for item in result.get("databases", []):
        lines.extend(
            [
                f"## {item['name']}",
                "",
                f"- Código: {item['code']}",
                f"- Finalidad: {item['purpose'] or 'Pendiente'}",
                f"- Titulares: {item['data_subjects'] or 'Pendiente'}",
                f"- Categorías de datos: {item['data_categories'] or 'Pendiente'}",
                f"- Datos sensibles: {'Sí' if item['sensitive_data'] else 'No'}",
                f"- Transferencia internacional: {'Sí' if item['international_transfer'] else 'No'}",
                f"- Terceros: {item['third_parties'] or 'Pendiente'}",
                f"- Riesgo: {item.get('risk_level', 'Pendiente')}",
                "",
            ]
        )
    if result.get("vendor_summary"):
        lines.extend(["## Vendors detectados en el escaneo", ""])
        for vendor, count in result["vendor_summary"].items():
            lines.append(f"- {vendor}: {count}")
        lines.append("")
    lines.extend(
        [
            "```text",
            "STOP_FOR_USER",
            "NEXT_ACTION: Confirme las bases detectadas y complete finalidad, datos, terceros y conservación.",
            "```",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True)
    parser.add_argument("--scan", required=True)
    parser.add_argument("--out-dir", default="RegistroDatosAAIP/Borradores")
    args = parser.parse_args()

    intake = load_json(Path(args.intake))
    scan = load_json(Path(args.scan))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    result = suggest(intake, scan)
    (out_dir / "BasesDetectadas.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(out_dir / "BasesDetectadas.md", result)
    print(f"OK bases detectadas: {out_dir / 'BasesDetectadas.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
