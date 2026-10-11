#!/usr/bin/env python3
"""Fetch public node lists, normalize their encodings, and publish Shadowrocket links."""
from __future__ import annotations

import base64
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources.txt"
OUTPUT = ROOT / "subscribe.txt"
SCHEMES = (
    "vmess", "vless", "ss", "trojan", "hysteria", "hysteria2", "hy2",
    "tuic", "socks", "socks5", "http", "https", "wireguard", "snell",
    "shadowtls",
)
NODE_RE = re.compile(r"(?:" + "|".join(map(re.escape, SCHEMES)) + r")://[^\s\"'<>]+", re.I)


def maybe_decode(text: str) -> str:
    """Decode common whole-file Base64 subscriptions while leaving plain text intact."""
    compact = "".join(text.split())
    if not compact or len(compact) % 4 not in (0, 2, 3):
        return text
    try:
        raw = base64.b64decode(compact + "=" * (-len(compact) % 4), validate=True)
        decoded = raw.decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return text
    if "://" in decoded:
        return decoded
    return text


def fetch(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "sr-auto-subscription/1.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read(8_000_000).decode("utf-8", errors="replace")


def main() -> int:
    urls = [
        line.strip() for line in SOURCES.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    nodes: set[str] = set()
    errors: list[str] = []
    for url in urls:
        try:
            body = maybe_decode(fetch(url))
            nodes.update(match.rstrip(",;，；") for match in NODE_RE.findall(body))
        except Exception as exc:  # one dead feed should not prevent other feeds
            errors.append(f"{url}: {exc}")

    if not nodes:
        print("没有从订阅源解析到节点；为避免覆盖可用订阅，本次不生成空文件。", file=sys.stderr)
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    # Shadowrocket accepts Base64-encoded subscription content.
    payload = "\n".join(sorted(nodes)) + "\n"
    encoded = base64.b64encode(payload.encode("utf-8")).decode("ascii") + "\n"
    OUTPUT.write_text(encoded, encoding="ascii")
    print(f"已收集 {len(nodes)} 个唯一节点，写入 subscribe.txt")
    if errors:
        print(f"有 {len(errors)} 个订阅源暂时读取失败：", file=sys.stderr)
        for error in errors:
            print(error, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
