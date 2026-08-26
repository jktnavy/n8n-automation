#!/usr/bin/env python3

import base64
import json
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright


BASE_DIR = Path("/home/heden/projects/n8n-automation")
TEMPLATE_DIR = BASE_DIR / "templates" / "invoice"
OUTPUT_DIR = BASE_DIR / "output" / "invoices"


def rupiah(value):
    value = int(float(value))
    return f"{value:,}".replace(",", ".")


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: render_invoice.py '<base64-json>'")

    decoded = base64.b64decode(sys.argv[1]).decode("utf-8")
    data = json.loads(decoded)

    data["unit_price_formatted"] = rupiah(data["unit_price"])
    data["subtotal_formatted"] = rupiah(data["subtotal"])
    data["total_formatted"] = rupiah(data["total"])

    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=True,
    )

    template = env.get_template("invoice.html")
    html = template.render(**data)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    safe_number = data["invoice_number"].replace("/", "-")
    html_path = OUTPUT_DIR / f"{safe_number}.html"
    pdf_path = OUTPUT_DIR / f"{safe_number}.pdf"

    html_path.write_text(html, encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()
        page.goto(html_path.as_uri())

        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            margin={
                "top": "15mm",
                "bottom": "15mm",
                "left": "15mm",
                "right": "15mm",
            },
        )

        browser.close()

    print(
        json.dumps({
            "success": True,
            "pdf_path": str(pdf_path),
            "html_path": str(html_path),
        })
    )


if __name__ == "__main__":
    main()