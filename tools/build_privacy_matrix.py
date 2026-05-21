#!/usr/bin/env python3
"""Generar matriz de privacidad para app/web."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build(data: dict) -> dict:
    trackers = data.get("cookies_or_trackers", [])
    permissions = data.get("mobile_permissions", [])
    categories = data.get("personal_data_categories", [])
    tracker_text = " ".join(str(item).lower() for item in trackers)
    permission_text = " ".join(str(item).lower() for item in permissions)
    category_text = " ".join(str(item).lower() for item in categories)
    has_ads_tracking = any(word in tracker_text for word in ["ads", "remarketing", "pixel", "retarget"])
    has_precise_geo = any(word in permission_text for word in ["geolocalizacion", "geolocalización", "location", "ubicacion", "ubicación"])
    has_biometric = any(word in (permission_text + " " + category_text) for word in ["biometr", "face id", "huella", "fingerprint"])
    return {
        "service_name": data.get("service_name", ""),
        "data_categories": categories,
        "trackers": trackers,
        "mobile_permissions": permissions,
        "third_parties": data.get("third_parties", []),
        "sensitive_data": bool(data.get("sensitive_data", False)),
        "minor_data": bool(data.get("minor_data", False)),
        "ads_tracking": has_ads_tracking,
        "precise_geolocation": has_precise_geo,
        "biometric_processing": has_biometric,
        "risk_level": "alto" if data.get("sensitive_data", False) or data.get("minor_data", False) or has_biometric else ("medio" if has_ads_tracking or has_precise_geo else "bajo"),
        "confirmation_required": True,
        "user_confirmed": False,
    }


def write_md(path: Path, result: dict) -> None:
    lines = [
        "# Matriz de Privacidad",
        "",
        f"- Servicio: {result.get('service_name') or 'Pendiente'}",
        f"- Datos: {result.get('data_categories') or 'Pendiente'}",
        f"- Trackers: {result.get('trackers') or 'Ninguno declarado'}",
        f"- Permisos móviles: {result.get('mobile_permissions') or 'Ninguno declarado'}",
        f"- Terceros: {result.get('third_parties') or 'Pendiente'}",
        f"- Datos sensibles: {'Sí' if result.get('sensitive_data') else 'No'}",
        f"- Datos de menores: {'Sí' if result.get('minor_data') else 'No'}",
        f"- Geolocalización precisa: {'Sí' if result.get('precise_geolocation') else 'No'}",
        f"- Biometría: {'Sí' if result.get('biometric_processing') else 'No'}",
        f"- Tracking publicitario: {'Sí' if result.get('ads_tracking') else 'No'}",
        f"- Riesgo: {result.get('risk_level') or 'Pendiente'}",
        "",
        "```text",
        "STOP_FOR_USER",
        "NEXT_ACTION: Confirme datos, trackers, permisos, terceros y sensibilidad antes del borrador de privacidad.",
        "```",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-dir", default="LegalesAppAR/Borradores")
    args = parser.parse_args()
    data = load_json(Path(args.input))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    result = build(data)
    (out_dir / "MatrizPrivacidad.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_md(out_dir / "MatrizPrivacidad.md", result)
    print(f"OK privacidad: {out_dir / 'MatrizPrivacidad.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
