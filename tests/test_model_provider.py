import os
import sys
import types
import unittest
from unittest.mock import patch

import model_provider


class FakeOpenAIModel:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


def fake_strands_modules():
    strands = types.ModuleType("strands")
    models = types.ModuleType("strands.models")
    openai = types.ModuleType("strands.models.openai")
    openai.OpenAIModel = FakeOpenAIModel
    return {
        "strands": strands,
        "strands.models": models,
        "strands.models.openai": openai,
    }


class ModelProviderTests(unittest.TestCase):
    def test_no_provider_returns_none(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertIsNone(model_provider.configured_model())

    def test_unknown_provider_fails_closed(self):
        with patch.dict(os.environ, {"MODEL_PROVIDER": "unknown"}, clear=True):
            with self.assertRaisesRegex(ValueError, "Unsupported MODEL_PROVIDER"):
                model_provider.configured_model()

    def test_nebius_requires_environment_key(self):
        with patch.dict(os.environ, {"MODEL_PROVIDER": "nebius"}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "requires NEBIUS_API_KEY"):
                model_provider.configured_model()

    def test_nebius_uses_expected_defaults_without_network(self):
        env = {
            "MODEL_PROVIDER": "nebius",
            "NEBIUS_API_KEY": "test-only-not-a-real-secret",
        }
        with patch.dict(os.environ, env, clear=True), patch.dict(sys.modules, fake_strands_modules()):
            model = model_provider.configured_model()

        self.assertEqual(
            model.kwargs["model_id"],
            "nvidia/nemotron-3-super-120b-a12b",
        )
        self.assertEqual(
            model.kwargs["client_args"]["base_url"],
            "https://api.tokenfactory.us-central1.nebius.com/v1/",
        )
        self.assertEqual(model.kwargs["params"]["max_tokens"], 1200)
        self.assertEqual(model.kwargs["params"]["temperature"], 0.2)

    def test_nebius_allows_explicit_cost_control_overrides(self):
        env = {
            "MODEL_PROVIDER": "nebius",
            "NEBIUS_API_KEY": "test-only-not-a-real-secret",
            "NEBIUS_MODEL_ID": "nvidia/nemotron-3-super-120b-a12b",
            "NEBIUS_BASE_URL": "https://example.invalid/v1/",
            "MODEL_MAX_TOKENS": "350",
            "MODEL_TEMPERATURE": "0",
        }
        with patch.dict(os.environ, env, clear=True), patch.dict(sys.modules, fake_strands_modules()):
            model = model_provider.configured_model()

        self.assertEqual(model.kwargs["client_args"]["base_url"], "https://example.invalid/v1/")
        self.assertEqual(model.kwargs["params"]["max_tokens"], 350)
        self.assertEqual(model.kwargs["params"]["temperature"], 0.0)


if __name__ == "__main__":
    unittest.main()
