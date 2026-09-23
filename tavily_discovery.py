"""Fail-closed Tavily discovery adapter for Earn Before Spend.

Tavily is useful here because the product's first step is FIND: current earning
opportunities must come from live sources before deterministic qualification can
rank them. This module never searches unless a human has explicitly configured a
TAVILY_API_KEY and ALLOW_LIVE_TAVILY=1.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Callable

DEFAULT_SEARCH_URL = "https://api.tavily.com/search"


class TavilyDiscoveryError(RuntimeError):
    """Raised when Tavily configuration or response validation fails."""


@dataclass(frozen=True)
class TavilyConfig:
    api_key: str
    search_url: str = DEFAULT_SEARCH_URL
    timeout_seconds: float = 20.0

    @classmethod
    def from_env(cls) -> "TavilyConfig":
        if os.environ.get("ALLOW_LIVE_TAVILY") != "1":
            raise TavilyDiscoveryError(
                "Live Tavily discovery is disabled. Set ALLOW_LIVE_TAVILY=1 only after human approval."
            )
        api_key = os.environ.get("TAVILY_API_KEY", "").strip()
        if not api_key:
            raise TavilyDiscoveryError(
                "TAVILY_API_KEY is required for an intentional Tavily runtime call."
            )
        return cls(api_key=api_key)


def discover_opportunities(
    query: str,
    *,
    config: TavilyConfig | None = None,
    opener: Callable = urllib.request.urlopen,
    max_results: int = 5,
) -> list[dict[str, object]]:
    """Search current web sources and return a small normalized evidence set.

    Search results are evidence candidates only. They are never treated as
    qualified opportunities or earnings until deterministic checks verify rights,
    eligibility, payout, cash requirement, owner labor, and legitimacy.
    """
    if not query.strip():
        raise TavilyDiscoveryError("A non-empty discovery query is required.")
    if not 1 <= max_results <= 5:
        raise TavilyDiscoveryError("max_results must be between 1 and 5 for bounded discovery.")

    config = config or TavilyConfig.from_env()
    payload = {
        "query": query.strip(),
        "search_depth": "basic",
        "max_results": max_results,
        "include_answer": False,
        "include_raw_content": False,
        "include_images": False,
    }
    request = urllib.request.Request(
        config.search_url,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )

    try:
        with opener(request, timeout=config.timeout_seconds) as response:
            raw = response.read().decode("utf-8")
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise TavilyDiscoveryError(f"Tavily request failed: {exc}") from exc

    try:
        body = json.loads(raw)
        rows = body["results"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise TavilyDiscoveryError("Tavily returned an unexpected response shape.") from exc
    if not isinstance(rows, list):
        raise TavilyDiscoveryError("Tavily results must be a list.")

    normalized: list[dict[str, object]] = []
    for row in rows[:max_results]:
        if not isinstance(row, dict):
            continue
        title = row.get("title")
        url = row.get("url")
        content = row.get("content")
        if not isinstance(title, str) or not isinstance(url, str):
            continue
        normalized.append(
            {
                "title": title.strip(),
                "url": url.strip(),
                "content": content.strip() if isinstance(content, str) else "",
                "score": row.get("score"),
                "qualification_status": "unverified_evidence_only",
            }
        )
    return normalized
