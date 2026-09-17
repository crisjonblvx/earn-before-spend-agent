import os
import unittest
from unittest.mock import patch

from nebius import DEFAULT_NEBIUS_MODEL, MAX_OUTPUT_TOKENS, NebiusConfig


class NebiusConfigTests(unittest.TestCase):
    def test_missing_key_blocks_without_fallback(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "no paid-provider fallback"):
                NebiusConfig.from_env()

    def test_default_is_nvidia_nemotron(self):
        with patch.dict(os.environ, {"NEBIUS_API_KEY": "test-key"}, clear=True):
            cfg = NebiusConfig.from_env()
        self.assertEqual(cfg.model_id, DEFAULT_NEBIUS_MODEL)
        self.assertEqual(cfg.strands_model_id, f"nebius/{DEFAULT_NEBIUS_MODEL}")

    def test_non_nvidia_model_is_rejected(self):
        with patch.dict(
            os.environ,
            {"NEBIUS_API_KEY": "test-key", "NEBIUS_MODEL_ID": "meta-llama/Llama-3.3-70B-Instruct"},
            clear=True,
        ):
            with self.assertRaisesRegex(RuntimeError, "NVIDIA open model"):
                NebiusConfig.from_env()

    def test_token_cap_rejects_uncapped_request(self):
        with patch.dict(
            os.environ,
            {"NEBIUS_API_KEY": "test-key", "NEBIUS_MAX_TOKENS": str(MAX_OUTPUT_TOKENS + 1)},
            clear=True,
        ):
            with self.assertRaisesRegex(RuntimeError, "between 1 and"):
                NebiusConfig.from_env()

    def test_public_summary_never_contains_key(self):
        cfg = NebiusConfig(api_key="super-secret")
        summary = cfg.public_summary()
        self.assertNotIn("super-secret", repr(summary))
        self.assertEqual(summary["api_key_present"], True)


if __name__ == "__main__":
    unittest.main()
