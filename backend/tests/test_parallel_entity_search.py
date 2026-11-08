import unittest
from types import SimpleNamespace
from unittest.mock import patch

import httpx

from marketing_backend.providers import Providers
from marketing_backend.research import ProviderFailure


class ParallelEntitySearchTests(unittest.TestCase):
    def setUp(self):
        self.provider = Providers(SimpleNamespace(checkpoint={}), lambda value: None)
        env = patch.dict("os.environ", {"PARALLEL_API_KEY": "synthetic", "PARALLEL_ENTITY_SEARCH_USD_PER_REQUEST": "0.005"})
        env.start()
        self.addCleanup(env.stop)

    def test_reserves_and_checkpoints_suggestions(self):
        response = httpx.Response(200, json={"entity_set_id": "synthetic", "entities": [
            {"name": "Morgan Lee", "url": "https://example.com/morgan", "description": "Operations"},
            {"name": "Unsafe", "url": "http://127.0.0.1/", "description": ""},
        ]})
        with patch.object(self.provider, "reserve", return_value=1) as reserve, \
             patch.object(self.provider, "record") as record, \
             patch("marketing_backend.providers.httpx.post", return_value=response) as post:
            result = self.provider.parallel_entity_search("people", "Synthetic company")
            self.assertEqual(len(result), 1)
            self.assertEqual(self.provider.parallel_entity_search("people", "Synthetic company"), result)
            reserve.assert_called_once_with("PARALLEL", "people", 5000)
            record.assert_called_once_with(1, "SUCCESS")
            self.assertEqual(post.call_args.kwargs["json"]["entity_type"], "people")
            post.assert_called_once()

    def test_transport_failure_is_uncertain(self):
        with patch.object(self.provider, "reserve", return_value=1), \
             patch.object(self.provider, "record") as record, \
             patch("marketing_backend.providers.httpx.post", side_effect=httpx.ConnectError("synthetic")):
            with self.assertRaises(ProviderFailure):
                self.provider.parallel_entity_search("people", "Synthetic company")
            record.assert_called_once_with(1, "UNCERTAIN")

    def test_rejects_underpriced_configuration_before_reservation(self):
        with patch.dict("os.environ", {"PARALLEL_ENTITY_SEARCH_USD_PER_REQUEST": "0.001"}), \
             patch.object(self.provider, "reserve") as reserve:
            with self.assertRaises(ProviderFailure):
                self.provider.parallel_entity_search("people", "Synthetic company")
            reserve.assert_not_called()


if __name__ == "__main__":
    unittest.main()
