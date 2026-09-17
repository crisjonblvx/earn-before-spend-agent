"""Offline tests for the Nebius/Nemotron adapter."""
from __future__ import annotations

import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from core import Opportunity, Pathway
from nebius_agent import NEBIUS_MODEL, build_user_prompt, run_nebius


def opportunity(*, title: str, new_cash: float = 0, payout_probability: float = 0.2) -> Opportunity:
    return Opportunity(
        title=title,
        pathway=Pathway.COMPETITION,
        payout_usd=1000,
        new_cash_required_usd=new_cash,
        cj_minutes_required=10,
        deadline_hours=48,
        payout_probability=payout_probability,
        legitimacy_score=95,
        fit_score=95,
        rights_clear=True,
        eligibility_clear=True,
        payout_verifiable=True,
        terms_require_human_acceptance=True,
        source_url="https://example.com",
    )


class FakeCompletions:
    def __init__(self) -> None:
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="Use the qualified path; human terms gate remains."))]
        )


class FakeClient:
    def __init__(self) -> None:
        self.completions = FakeCompletions()
        self.chat = SimpleNamespace(completions=self.completions)


class NebiusAdapterTests(unittest.TestCase):
    def test_prompt_preserves_deterministic_blocker(self) -> None:
        prompt = build_user_prompt([
            opportunity(title="Blocked paid entry", new_cash=25),
            opportunity(title="Qualified no-fee path"),
        ])
        self.assertIn('"eligible": false', prompt)
        self.assertIn("requires_new_cash", prompt)
        self.assertIn('"eligible": true', prompt)

    def test_live_call_uses_nemotron_model_and_guarded_context(self) -> None:
        client = FakeClient()
        text = run_nebius([opportunity(title="Qualified no-fee path")], client=client)
        self.assertIn("human terms gate", text)
        self.assertEqual(client.completions.kwargs["model"], NEBIUS_MODEL)
        self.assertIn("authoritative deterministic evaluation", client.completions.kwargs["messages"][1]["content"])

    def test_missing_api_key_fails_before_any_provider_call(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "NEBIUS_API_KEY"):
                run_nebius([opportunity(title="Qualified no-fee path")])


if __name__ == "__main__":
    unittest.main()
