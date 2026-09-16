import json
import unittest

from demo import sample_opportunities
from nebius_reasoner import (
    DEFAULT_MODEL,
    build_request_payload,
    call_token_factory,
    ranked_snapshot,
)


class FakeResponse:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps({
            "choices": [{"message": {"content": "Take the bounded action."}}]
        }).encode("utf-8")


class NebiusReasonerTests(unittest.TestCase):
    def test_snapshot_preserves_deterministic_gate(self):
        rows = ranked_snapshot(sample_opportunities())
        self.assertEqual(len(rows), 3)
        self.assertTrue(all("eligible" in row for row in rows))
        self.assertTrue(all("requires_human_decision" in row for row in rows))

    def test_payload_uses_nvidia_nemotron(self):
        payload = build_request_payload([{"eligible": True}])
        self.assertEqual(payload["model"], DEFAULT_MODEL)
        self.assertTrue(payload["model"].startswith("nvidia/nemotron"))
        self.assertIn("deterministic ranking", payload["messages"][1]["content"])

    def test_runtime_call_targets_token_factory_without_leaking_key(self):
        captured = {}

        def fake_open(request, timeout):
            captured["url"] = request.full_url
            captured["auth"] = request.headers["Authorization"]
            captured["body"] = json.loads(request.data.decode("utf-8"))
            captured["timeout"] = timeout
            return FakeResponse()

        text = call_token_factory(
            [{"eligible": True, "blockers": []}],
            api_key="unit-test-secret",
            opener=fake_open,
        )
        self.assertEqual(text, "Take the bounded action.")
        self.assertEqual(
            captured["url"],
            "https://api.tokenfactory.nebius.com/v1/chat/completions",
        )
        self.assertEqual(captured["auth"], "Bearer unit-test-secret")
        self.assertEqual(captured["body"]["model"], DEFAULT_MODEL)
        self.assertEqual(captured["timeout"], 45)

    def test_missing_key_fails_closed(self):
        import os
        old = os.environ.pop("NEBIUS_API_KEY", None)
        try:
            with self.assertRaisesRegex(RuntimeError, "NEBIUS_API_KEY"):
                call_token_factory([])
        finally:
            if old is not None:
                os.environ["NEBIUS_API_KEY"] = old


if __name__ == "__main__":
    unittest.main()
