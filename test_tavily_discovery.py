from __future__ import annotations

import io
import json
import os
import tempfile
import unittest
from unittest.mock import patch

from tavily_discovery import TavilyConfig, TavilyDiscoveryError, discover_opportunities
from tavily_probe import write_probe


class FakeResponse:
    def __init__(self, payload: dict):
        self._raw = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return self._raw


class TavilyDiscoveryTests(unittest.TestCase):
    def test_env_gate_requires_explicit_human_enable(self):
        with patch.dict(os.environ, {"TAVILY_API_KEY": "tvly-test"}, clear=True):
            with self.assertRaises(TavilyDiscoveryError):
                TavilyConfig.from_env()

    def test_env_gate_requires_key(self):
        with patch.dict(os.environ, {"ALLOW_LIVE_TAVILY": "1"}, clear=True):
            with self.assertRaises(TavilyDiscoveryError):
                TavilyConfig.from_env()

    def test_search_is_bounded_and_normalized(self):
        seen = {}

        def opener(request, timeout):
            seen["request"] = request
            seen["timeout"] = timeout
            return FakeResponse(
                {
                    "results": [
                        {
                            "title": "Example grant",
                            "url": "https://example.com/grant",
                            "content": "No-fee grant details.",
                            "score": 0.91,
                        },
                        {
                            "title": "Example bounty",
                            "url": "https://example.com/bounty",
                            "content": "Fixed-scope bounty.",
                            "score": 0.82,
                        },
                    ]
                }
            )

        config = TavilyConfig(api_key="tvly-secret")
        rows = discover_opportunities("zero-cost earning opportunities", config=config, opener=opener, max_results=2)
        self.assertEqual(2, len(rows))
        self.assertEqual("unverified_evidence_only", rows[0]["qualification_status"])
        self.assertEqual("https://example.com/grant", rows[0]["url"])

        request = seen["request"]
        self.assertEqual("Bearer tvly-secret", request.headers["Authorization"])
        payload = json.loads(request.data.decode("utf-8"))
        self.assertEqual("basic", payload["search_depth"])
        self.assertEqual(2, payload["max_results"])
        self.assertFalse(payload["include_answer"])
        self.assertFalse(payload["include_raw_content"])
        self.assertFalse(payload["include_images"])

    def test_probe_writer_does_not_need_credentials(self):
        payload = {
            "live_call_observed": True,
            "provider": "Tavily Search API",
            "results": [],
            "truth_boundary": "test",
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = write_probe(payload, os.path.join(tmp, "evidence.json"))
            saved = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual("Tavily Search API", saved["provider"])
            self.assertNotIn("api_key", json.dumps(saved).lower())

    def test_rejects_unbounded_result_count(self):
        config = TavilyConfig(api_key="tvly-secret")
        with self.assertRaises(TavilyDiscoveryError):
            discover_opportunities("x", config=config, opener=lambda *a, **k: None, max_results=6)


if __name__ == "__main__":
    unittest.main()
