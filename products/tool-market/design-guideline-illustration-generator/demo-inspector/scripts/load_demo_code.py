#!/usr/bin/env python3
"""Fetch Infra Design playground demo code by id or URL."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request


API_URL = "https://infrad.shopee.io/apis/faas/agent-code/read"


def extract_demo_id(source: str) -> str:
    parsed = urllib.parse.urlparse(source)
    query = urllib.parse.parse_qs(parsed.query)
    for key in ("id", "agent_code_id"):
        values = query.get(key)
        if values and values[0].strip().isdigit():
            return values[0].strip()

    for pattern in (r"(?:id|agent_code_id)=([0-9]+)", r"\b([0-9]+)\b"):
        matches = re.findall(pattern, source)
        unique_matches = sorted(set(matches))
        if len(unique_matches) == 1:
            return unique_matches[0]

    raise ValueError("Could not find a unique numeric demo id in the input.")


def fetch_demo(demo_id: str) -> dict:
    url = f"{API_URL}?{urllib.parse.urlencode({'id': demo_id})}"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "demo-inspector/1.0",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Request failed: {exc.reason}") from exc

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Response is not valid JSON: {raw[:200]}") from exc

    code = payload.get("code")
    if not isinstance(code, str) or not code.strip():
        raise RuntimeError("Response JSON does not contain a non-empty string field: code")

    return payload


def print_markdown(payload: dict, demo_id: str) -> None:
    print(f"Demo ID: {payload.get('id', demo_id)}")
    if payload.get("created_at"):
        print(f"Created at: {payload['created_at']}")
    if payload.get("updated_at"):
        print(f"Updated at: {payload['updated_at']}")
    print()
    print("```react")
    print(payload["code"])
    print("```")


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch Infra Design demo code by id or URL.")
    parser.add_argument("source", nargs="+", help="Demo id, playground URL, read URL, or text containing one id.")
    parser.add_argument(
        "--format",
        choices=("markdown", "code", "json"),
        default="json",
        help="Output format. Defaults to json for agent-side inspection.",
    )
    args = parser.parse_args()

    source = " ".join(args.source)

    try:
        demo_id = extract_demo_id(source)
        payload = fetch_demo(demo_id)
    except Exception as exc:  # noqa: BLE001 - command-line tool should surface concise errors.
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    elif args.format == "code":
        print(payload["code"])
    else:
        print_markdown(payload, demo_id)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
