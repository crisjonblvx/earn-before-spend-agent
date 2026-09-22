import json
import unittest
from unittest.mock import patch

from core import Opportunity, Pathway
from nebius_runtime import (
    DEFAULT_MODEL,
    NebiusRuntimeError,
    _chat_completions_url,
    explain_ranked_results,
)


class _FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


def _opportunity(title="Clean bounty", cash=0, terms=False):
    return Opportunity(
        title=title,
        pathway=Pathway.BOUNTY,
        payout_usd=500,
        new_cash_required_usd=cash,
        cj_minutes_required=10,
        deadline_hours=48,
        payout_probability=0.5,
        legitimacy_score=90,
        fit_score=90,
        rights_clear=True,
        eligibility_clear=True,
        payout_verifiable=True,
        terms_require_human_acceptance=terms,
        source_url="https://example.com/opportunity",
    )


class NebiusRuntimeTests(unittest.TestCase):
    def test_requires_api_key(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(NebiusRuntimeError, "NEBIUS_API_KEY"):
                explain_ranked_results([_opportunity()])

    def test_builds_token_factory_request_and_preserves_gate(self):
        seen = {}

        def fake_urlopen(req, timeout):
            seen["url"] = req.full_url
            seen["headers"] = dict(req.header_items())
            seen["body"] = json.loads(req.data.decode("utf-8"))
            seen["timeout"] = timeout
            return _FakeResponse({"choices": [{"message": {"content": "Take the clean bounty next."}}]})

        with patch("nebius_runtime.request.urlopen", side_effect=fake_urlopen):
            result = explain_ranked_results(
                [_opportunity(), _opportunity(title="Paid entry", cash=10)],
                api_key="test-key",
                base_url="https://api.tokenfactory.nebius.com/v1/",
            )

        self.assertEqual(seen["url"], "https://api.tokenfactory.nebius.com/v1/chat/completions")
        self.assertEqual(seen["body"]["model"], DEFAULT_MODEL)
        self.assertIn("Bearer test-key", seen["headers"].values())
        self.assertTrue(result["evaluations"][0]["eligible"])
        blocked = next(item for item in result["evaluations"] if item["title"] == "Paid entry")
        self.assertFalse(blocked["eligible"])
        self.assertIn("requires_new_cash", blocked["blockers"])
        self.assertEqual(result["explanation"], "Take the clean bounty next.")

    def test_url_join(self):
        self.assertEqual(
            _chat_completions_url("https://api.tokenfactory.nebius.com/v1/"),
            "https://api.tokenfactory.nebius.com/v1/chat/completions",
        )


if __name__ == "__main__":
    unittest.main()
