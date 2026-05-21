#!/usr/bin/env python3
"""Sugerir clases Niza probables para un caso marcario argentino."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CLASS_RULES = [
    {
        "class_number": 9,
        "label": "Software descargable y productos tecnológicos",
        "keywords": [
            "app",
            "aplicacion",
            "aplicación",
            "software descargable",
            "descargable",
            "mobile app",
            "hardware",
            "dispositivo",
            "iot",
        ],
        "reason": "Corresponde cuando la marca identifica software descargable, apps o productos tecnológicos.",
        "caution": "No usar por reflejo si el servicio real es solo SaaS o desarrollo a medida.",
    },
    {
        "class_number": 35,
        "label": "Publicidad, retail, marketplace y gestión comercial",
        "keywords": [
            "marketplace",
            "ecommerce",
            "e-commerce",
            "tienda",
            "venta",
            "retail",
            "publicidad",
            "marketing",
            "agencia",
            "comercio electronico",
            "comercio electrónico",
        ],
        "reason": "Suele aplicar a intermediación comercial, publicidad, marketing y servicios de venta.",
        "caution": "No reemplaza clases del producto principal; suele ser complementaria.",
    },
    {
        "class_number": 36,
        "label": "Servicios financieros y fintech",
        "keywords": [
            "fintech",
            "pagos",
            "billetera",
            "wallet",
            "credito",
            "crédito",
            "inversion",
            "inversión",
            "seguros",
            "prestamo",
            "préstamo",
        ],
        "reason": "Corresponde a pagos, billeteras, servicios financieros y seguros.",
        "caution": "Distinguir entre software financiero para terceros y servicio financiero prestado directamente.",
    },
    {
        "class_number": 38,
        "label": "Telecomunicaciones y transmisión",
        "keywords": [
            "mensajeria",
            "mensajería",
            "chat",
            "comunicacion",
            "comunicación",
            "telecom",
            "streaming",
            "videollamada",
            "llamadas",
        ],
        "reason": "Aplica cuando el núcleo del servicio es transmitir comunicaciones o habilitar conexión.",
        "caution": "No usar si la plataforma solo opera sobre infraestructura de terceros sin prestar telecomunicaciones.",
    },
    {
        "class_number": 41,
        "label": "Educación, capacitación y contenidos",
        "keywords": [
            "curso",
            "cursos",
            "educacion",
            "educación",
            "capacitacion",
            "capacitación",
            "academia",
            "tutorial",
            "contenido educativo",
            "training",
        ],
        "reason": "Aplica a formación, enseñanza, cursos, talleres y publicaciones no descargables.",
        "caution": "Si el valor principal es el software, puede convivir con clase 42 o 9.",
    },
    {
        "class_number": 42,
        "label": "SaaS, PaaS, desarrollo de software y servicios tecnológicos",
        "keywords": [
            "saas",
            "paas",
            "software as a service",
            "plataforma",
            "api",
            "hosting",
            "cloud",
            "nube",
            "ia",
            "inteligencia artificial",
            "desarrollo de software",
            "servicio tecnologico",
            "servicio tecnológico",
        ],
        "reason": "Es la clase más frecuente para servicios tecnológicos prestados en línea.",
        "caution": "No absorbe por sí sola retail, educación, finanzas o apps descargables.",
    },
    {
        "class_number": 43,
        "label": "Gastronomía y hospitalidad",
        "keywords": [
            "restaurante",
            "bar",
            "cafeteria",
            "cafetería",
            "hotel",
            "alojamiento",
            "delivery de comida",
        ],
        "reason": "Aplica a servicios de restauración, bebidas y hospedaje.",
        "caution": "Si la marca es de plataforma que conecta terceros, podría además convivir con clase 35 o 42.",
    },
    {
        "class_number": 44,
        "label": "Salud, medicina y bienestar",
        "keywords": [
            "salud",
            "medico",
            "médico",
            "medicina",
            "telemedicina",
            "clinica",
            "clínica",
            "bienestar",
            "nutricion",
            "nutrición",
        ],
        "reason": "Aplica a servicios médicos, de salud y bienestar.",
        "caution": "Separar claramente el servicio sanitario del software que lo soporta.",
    },
    {
        "class_number": 45,
        "label": "Servicios jurídicos, seguridad y redes sociales",
        "keywords": [
            "legal",
            "juridico",
            "jurídico",
            "compliance",
            "seguridad",
            "identidad",
            "red social",
            "social network",
        ],
        "reason": "Puede corresponder a servicios jurídicos, seguridad o redes sociales en línea.",
        "caution": "Es una clase que suele requerir revisión fina por el alcance del servicio real.",
    },
]


def normalize_text(value: str) -> str:
    value = value.lower()
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def score_rule(haystack: str, keywords: list[str]) -> tuple[int, list[str]]:
    hits: list[str] = []
    score = 0
    for keyword in keywords:
        if " " in keyword:
            matched = keyword in haystack
        else:
            matched = re.search(rf"\b{re.escape(keyword)}\b", haystack) is not None
        if matched:
            hits.append(keyword)
            score += 3 if " " in keyword else 2
    return score, hits


def gather_text(data: dict) -> str:
    values: list[str] = []
    for key in ("brand_name", "brand_type", "business_summary", "priority_details", "notes"):
        val = data.get(key)
        if isinstance(val, str):
            values.append(val)
    for key in ("current_offering", "channels"):
        val = data.get(key)
        if isinstance(val, list):
            values.extend(str(item) for item in val)
    return normalize_text(" ".join(values))


def suggest(data: dict) -> dict:
    haystack = gather_text(data)
    candidates = []
    for rule in CLASS_RULES:
        score, hits = score_rule(haystack, [normalize_text(k) for k in rule["keywords"]])
        if score <= 0:
            continue
        candidates.append(
            {
                "class_number": rule["class_number"],
                "label": rule["label"],
                "score": score,
                "matched_terms": hits,
                "reason": rule["reason"],
                "caution": rule["caution"],
            }
        )
    candidates.sort(key=lambda item: (-item["score"], item["class_number"]))
    return {
        "brand_name": data.get("brand_name", ""),
        "business_summary": data.get("business_summary", ""),
        "candidates": candidates,
        "selection_required": True,
        "user_confirmed": False,
    }


def write_markdown(path: Path, result: dict) -> None:
    lines = [
        "# Clases Niza Sugeridas",
        "",
        f"- Marca: {result.get('brand_name', '')}",
        "",
    ]
    candidates = result.get("candidates", [])
    if not candidates:
        lines.extend(
            [
                "No se detectaron clases claras automáticamente.",
                "",
                "Se requiere análisis manual.",
                "",
            ]
        )
    for item in candidates:
        lines.extend(
            [
                f"## Clase {item['class_number']} - {item['label']}",
                "",
                f"- Puntaje: {item['score']}",
                f"- Términos detectados: {', '.join(item['matched_terms']) if item['matched_terms'] else 'Ninguno'}",
                f"- Motivo: {item['reason']}",
                f"- Cautela: {item['caution']}",
                "",
            ]
        )
    lines.extend(
        [
            "```text",
            "STOP_FOR_USER",
            "NEXT_ACTION: Confirme la clase o clases seleccionadas antes de redactar productos y servicios.",
            "```",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-dir", default="MarcaINPI/Borradores")
    args = parser.parse_args()

    data = load_json(Path(args.input))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    result = suggest(data)
    (out_dir / "ClasesSugeridas.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_markdown(out_dir / "ClasesSugeridas.md", result)
    print(f"OK clases sugeridas: {out_dir / 'ClasesSugeridas.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
