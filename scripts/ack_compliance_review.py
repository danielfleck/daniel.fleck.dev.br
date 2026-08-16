#!/usr/bin/env python3
"""Registra conclusão de revisão completa de conformidade."""

from __future__ import annotations
import argparse
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "governance" / "compliance-status.json"

def add_months(d: date, months: int) -> date:
    month0 = d.month - 1 + months
    year = d.year + month0 // 12
    month = month0 % 12 + 1
    month_lengths = [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
                     31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return date(year, month, min(d.day, month_lengths[month - 1]))

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="AAAA-MM-DD; padrão: hoje")
    parser.add_argument("--months", type=int, default=3)
    args = parser.parse_args()

    review = date.fromisoformat(args.date) if args.date else date.today()
    data = json.loads(STATUS.read_text(encoding="utf-8"))
    data["last_full_review"] = review.isoformat()
    data["next_full_review"] = add_months(review, args.months).isoformat()
    STATUS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("Revisão registrada:", data["last_full_review"])
    print("Próxima revisão:", data["next_full_review"])
    print("Revise git diff antes do commit.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
