#!/usr/bin/env python3
"""Resume relatório DMARC agregado XML ou XML.GZ (RFC 9990).

Os relatórios devem ficar em diretório privado/ignorado pelo Git.
"""

from __future__ import annotations
import argparse
import gzip
import xml.etree.ElementTree as ET
from pathlib import Path

def local(tag: str) -> str:
    return tag.split("}", 1)[-1]

def child_text(element, path: list[str]) -> str:
    cur = element
    for name in path:
        found = next((c for c in cur if local(c.tag) == name), None)
        if found is None:
            return ""
        cur = found
    return (cur.text or "").strip()

def load(path: Path) -> bytes:
    data = path.read_bytes()
    if path.suffix.lower() == ".gz" or data[:2] == b"\x1f\x8b":
        return gzip.decompress(data)
    return data

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    args = parser.parse_args()

    root = ET.fromstring(load(args.report))

    org = child_text(root, ["report_metadata", "org_name"])
    report_id = child_text(root, ["report_metadata", "report_id"])
    domain = child_text(root, ["policy_published", "domain"])
    policy = child_text(root, ["policy_published", "p"])

    print("Organização:", org or "(não informado)")
    print("Report-ID:", report_id or "(não informado)")
    print("Domínio:", domain or "(não informado)")
    print("Política:", policy or "(não informado)")
    print()
    print("source_ip\tcount\tdisposition\tdkim\tspf\theader_from")

    total = 0
    for record in [e for e in root.iter() if local(e.tag) == "record"]:
        source_ip = child_text(record, ["row", "source_ip"])
        count = child_text(record, ["row", "count"])
        disposition = child_text(record, ["row", "policy_evaluated", "disposition"])
        dkim = child_text(record, ["row", "policy_evaluated", "dkim"])
        spf = child_text(record, ["row", "policy_evaluated", "spf"])
        header_from = child_text(record, ["identifiers", "header_from"])
        try:
            total += int(count or "0")
        except ValueError:
            pass
        print(f"{source_ip}\t{count}\t{disposition}\t{dkim}\t{spf}\t{header_from}")

    print("\nTotal de mensagens agregadas no relatório:", total)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
