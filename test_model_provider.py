from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from model_provider import configured_model


class ModelProviderTests(unittest.TestCase):
    def test_default_keeps_sdk_provider(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertIsNone(configured_model())

    def test_nebius_requires_human_supplied_key(self):
        with patch.dict(os.environ, {"MODEL_PROVIDER": "nebius"}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "NEBIUS_API_KEY"):
                configured_model()

    def test_unknown_provider_is_blocked(self):
        with patch.dict(os.environ, {"MODEL_PROVIDER": "mystery"}, clear=True):
            with self.assertRaisesRegex(ValueError, "Unsupported MODEL_PROVIDER"):
                configured_model()


if __name__ == "__main__":
    unittest.main()
