import json
import unittest

from nebius_reasoner import (
    DEFAULT_MODEL,
    TokenFactoryError,
    explain_ranked_evaluations,
)


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


class NebiusReasonerTests(unittest.TestCase):
    def test_missing_key_fails_before_network(self):
        called = False

        def opener(*args, **kwargs):
            nonlocal called
            called = True
            raise AssertionError("network should not be called")

        with self.assertRaises(TokenFactoryError):
            explain_ranked_evaluations([], api_key="", opener=opener)
        self.assertFalse(called)

    def test_runtime_call_targets_token_factory_and_nemotron(self):
        captured = {}

        def opener(request, timeout):
            captured["url"] = request.full_url
            captured["authorization"] = request.get_header("Authorization")
            captured["timeout"] = timeout
            captured["body"] = json.loads(request.data.decode("utf-8"))
            return FakeResponse({
                "choices": [{"message": {"content": "Take the bounded next action."}}]
            })

        ranking = [{
            "title": "Blocked paid option",
            "eligible": False,
            "blockers": ["requires_new_cash"],
            "requires_human_decision": False,
            "score": 0,
            "reason": "Blocked: requires_new_cash",
        }]
        result = explain_ranked_evaluations(
            ranking,
            api_key="test-key",
            opener=opener,
            timeout_seconds=7,
        )

        self.assertEqual(result, "Take the bounded next action.")
        self.assertEqual(
            captured["url"],
            "https://api.tokenfactory.us-central1.nebius.com/v1/chat/completions",
        )
        self.assertEqual(captured["authorization"], "Bearer test-key")
        self.assertEqual(captured["timeout"], 7)
        self.assertEqual(captured["body"]["model"], DEFAULT_MODEL)
        self.assertIn("requires_new_cash", captured["body"]["messages"][1]["content"])

    def test_unexpected_response_shape_fails_closed(self):
        def opener(request, timeout):
            return FakeResponse({"unexpected": True})

        with self.assertRaises(TokenFactoryError):
            explain_ranked_evaluations([], api_key="test-key", opener=opener)


if __name__ == "__main__":
    unittest.main()
