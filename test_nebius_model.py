import json
import unittest
from unittest.mock import patch

from nebius_model import DEFAULT_MODEL, TokenFactoryConfig, TokenFactoryError, explain_ranking


class _FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


class NebiusModelTests(unittest.TestCase):
    def test_requires_explicit_api_key(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(TokenFactoryError):
                TokenFactoryConfig.from_env()

    def test_runtime_call_uses_nemotron_and_preserves_guardrail_prompt(self):
        captured = {}

        def opener(request, timeout):
            captured["request"] = request
            captured["timeout"] = timeout
            return _FakeResponse({
                "choices": [{"message": {"content": "Take the qualified fixed-scope path first."}}]
            })

        config = TokenFactoryConfig(api_key="test-key")
        text = explain_ranking(
            [{"title": "Fixed-scope code bounty", "qualified": True, "expected_value_usd": 70}],
            config=config,
            opener=opener,
        )

        self.assertEqual(text, "Take the qualified fixed-scope path first.")
        request = captured["request"]
        self.assertEqual(
            request.full_url,
            "https://api.tokenfactory.us-central1.nebius.com/v1/chat/completions",
        )
        self.assertEqual(request.get_header("Authorization"), "Bearer test-key")
        payload = json.loads(request.data.decode("utf-8"))
        self.assertEqual(payload["model"], DEFAULT_MODEL)
        self.assertIn("authoritative", payload["messages"][0]["content"])
        self.assertIn("Fixed-scope code bounty", payload["messages"][1]["content"])

    def test_rejects_unexpected_response_shape(self):
        def opener(request, timeout):
            return _FakeResponse({"unexpected": True})

        with self.assertRaises(TokenFactoryError):
            explain_ranking([], config=TokenFactoryConfig(api_key="test-key"), opener=opener)


if __name__ == "__main__":
    unittest.main()
