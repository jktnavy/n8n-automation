#!/usr/bin/env python3

import base64
import json
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright
from datetime import datetime


BASE_DIR = Path("/home/heden/projects/n8n-automation")
TEMPLATE_DIR = BASE_DIR / "templates" / "invoice"
OUTPUT_DIR = BASE_DIR / "output" / "invoices"


BULAN_ID = [
    "",
    "Januari",
    "Februari",
    "Maret",
    "April",
    "Mei",
    "Juni",
    "Juli",
    "Agustus",
    "September",
    "Oktober",
    "November",
    "Desember",
]


def format_tanggal_indonesia(value):
    from datetime import datetime

    dt = datetime.strptime(value, "%Y-%m-%d")

    return f"{dt.day} {BULAN_ID[dt.month]} {dt.year}"

def format_periode_indonesia(start_date, end_date=None):
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")

    if not end_date:
        return format_tanggal_indonesia(start_date)

    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    if start_dt.year == end_dt.year and start_dt.month == end_dt.month:
        return f"{start_dt.day} s.d. {end_dt.day} {BULAN_ID[end_dt.month]} {end_dt.year}"

    if start_dt.year == end_dt.year:
        return f"{start_dt.day} {BULAN_ID[start_dt.month]} s.d. {end_dt.day} {BULAN_ID[end_dt.month]} {end_dt.year}"

    return f"{start_dt.day} {BULAN_ID[start_dt.month]} {start_dt.year} s.d. {end_dt.day} {BULAN_ID[end_dt.month]} {end_dt.year}"


def hitung_durasi_hari(start_date, end_date=None):
    if not end_date:
        return None

    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    return (end_dt - start_dt).days + 1

def terbilang_angka(n):
    n = int(n)

    angka = [
        "",
        "Satu",
        "Dua",
        "Tiga",
        "Empat",
        "Lima",
        "Enam",
        "Tujuh",
        "Delapan",
        "Sembilan",
        "Sepuluh",
        "Sebelas",
    ]

    if n < 12:
        return angka[n]

    if n < 20:
        return terbilang_angka(n - 10) + " Belas"

    if n < 100:
        return (
            terbilang_angka(n // 10)
            + " Puluh "
            + terbilang_angka(n % 10)
        ).strip()

    if n < 200:
        return ("Seratus " + terbilang_angka(n - 100)).strip()

    if n < 1000:
        return (
            terbilang_angka(n // 100)
            + " Ratus "
            + terbilang_angka(n % 100)
        ).strip()

    if n < 2000:
        return ("Seribu " + terbilang_angka(n - 1000)).strip()

    if n < 1_000_000:
        return (
            terbilang_angka(n // 1000)
            + " Ribu "
            + terbilang_angka(n % 1000)
        ).strip()

    if n < 1_000_000_000:
        return (
            terbilang_angka(n // 1_000_000)
            + " Juta "
            + terbilang_angka(n % 1_000_000)
        ).strip()

    if n < 1_000_000_000_000:
        return (
            terbilang_angka(n // 1_000_000_000)
            + " Miliar "
            + terbilang_angka(n % 1_000_000_000)
        ).strip()

    return str(n)

def rupiah(value):
    value = int(float(value))
    return f"{value:,}".replace(",", ".")

def gabung_kalimat(items):
    items = [str(i).strip() for i in (items or []) if str(i).strip()]
    if not items:
        return ""

    if len(items) == 1:
        return items[0]

    if len(items) == 2:
        return f"{items[0]} dan {items[1]}"

    return ", ".join(items[:-1]) + f", dan {items[-1]}"

def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: render_invoice.py '<base64-json>'")

    decoded = base64.b64decode(sys.argv[1]).decode("utf-8")
    data = json.loads(decoded)

    for item in data.get("items", []):
        item["unit_price_formatted"] = rupiah(item["unit_price"])
        item["subtotal_formatted"] = rupiah(item["subtotal"])

        if item.get("price_basis") == "per_day":
            item["price_basis_label"] = "per hari"
        else:
            item["price_basis_label"] = "per perjalanan"

    data["subtotal_formatted"] = rupiah(data["subtotal"])
    data["total_formatted"] = rupiah(data["total"])

    data["invoice_date_formatted"] = format_tanggal_indonesia(
        data["invoice_date"]
    )

    data["invoice_date_long"] = format_tanggal_indonesia(
        data["invoice_date"]
    )

    return_date = data.get("return_date")

    data["departure_date_formatted"] = format_tanggal_indonesia(
        data["departure_date"]
    )

    data["trip_period_formatted"] = format_periode_indonesia(
        data["departure_date"],
        return_date
    )

    durasi_hari = hitung_durasi_hari(
        data["departure_date"],
        return_date
    )

    data["durasi_hari"] = durasi_hari

    data["terbilang"] = (
        terbilang_angka(data["total"]).strip() + " Rupiah"
    )

    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=True,
    )

    template = env.get_template("invoice.html")

    data["logo_path"] = (TEMPLATE_DIR / "assets" / "logo.png").as_uri()
    data["stamp_path"] = (TEMPLATE_DIR / "assets" / "stamp.png").as_uri()
    data["signature_path"] = (TEMPLATE_DIR / "assets" / "signature.png").as_uri()

    data["included_sentence"] = gabung_kalimat(data.get("included", []))
    data["excluded_sentence"] = gabung_kalimat(data.get("excluded", []))

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