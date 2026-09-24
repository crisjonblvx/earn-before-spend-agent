from __future__ import annotations

import unittest
from http.server import BaseHTTPRequestHandler
from pathlib import Path

from api.explain import handler as ExplainHandler
from api.healthz import handler as HealthHandler
from api.ranking import handler as RankingHandler


class VercelSurfaceTests(unittest.TestCase):
    def test_handlers_use_supported_python_function_shape(self) -> None:
        for handler in (RankingHandler, ExplainHandler, HealthHandler):
            self.assertTrue(issubclass(handler, BaseHTTPRequestHandler))

    def test_static_judge_page_targets_exact_api_routes(self) -> None:
        html = Path("index.html").read_text(encoding="utf-8")
        self.assertIn("fetch('/api/ranking')", html)
        self.assertIn("fetch('/api/explain'", html)
        self.assertIn("ALLOW_LIVE_NEBIUS=1", html)

    def test_vercel_config_keeps_api_runtime_bounded_to_project_code(self) -> None:
        config = Path("vercel.json").read_text(encoding="utf-8")
        self.assertIn('"api/**/*.py"', config)
        self.assertIn('"test_*.py"', config)


if __name__ == "__main__":
    unittest.main()
