import unittest
import hashlib
import json
from types import SimpleNamespace
from unittest.mock import patch

import httpx

from marketing_backend.providers import Providers
from marketing_backend.research import ProviderFailure
from marketing_backend.domain_corroboration import valid_saved_evidence


class ParallelSearchTests(unittest.TestCase):
    def setUp(self):
        self.provider = Providers(SimpleNamespace(checkpoint={}), lambda value: None)
        self.env = patch.dict("os.environ", {
            "PARALLEL_API_KEY": "synthetic",
            "PARALLEL_SEARCH_USD_PER_REQUEST": "0.001",
        })
        self.env.start()
        self.addCleanup(self.env.stop)

    def test_search_normalizes_and_caches(self):
        response = httpx.Response(200, json={"results": [{
            "url": "https://example.com/", "title": "Example", "excerpts": ["Evidence"]
        }]})
        with patch.object(self.provider, "reserve", return_value=1) as reserve, \
             patch.object(self.provider, "record") as record, \
             patch("marketing_backend.providers.httpx.post", return_value=response) as post:
            rows = self.provider.search("discovery", "transport", count=20, country="MY")
            self.assertEqual(rows[0]["text"], "Evidence")
            self.assertEqual(post.call_args.kwargs["json"]["advanced_settings"]["max_results"], 10)
            self.assertIn("MY", post.call_args.kwargs["json"]["objective"])
            self.assertEqual(post.call_args.kwargs["json"]["search_queries"], [post.call_args.kwargs["json"]["objective"]])
            self.assertEqual(self.provider.search("discovery", "transport"), rows)
            reserve.assert_called_once_with("PARALLEL", "discovery", 1000)
            record.assert_called_once_with(1, "SUCCESS")
            post.assert_called_once()

    def test_unsafe_result_is_rejected(self):
        response = httpx.Response(200, json={"results": [{"url": "http://127.0.0.1/"}]})
        with patch.object(self.provider, "reserve", return_value=1), \
             patch.object(self.provider, "record") as record, \
             patch("marketing_backend.providers.httpx.post", return_value=response):
            with self.assertRaises(ProviderFailure):
                self.provider.search("discovery", "transport")
            record.assert_called_once_with(1, "INVALID_OUTPUT")

    def test_identity_requires_citations_and_reserves_cost(self):
        response = httpx.Response(200, json={"status": "completed", "output": [{
            "type": "message", "content": [{"type": "output_text", "text":
                '{"company_name":"Example","official_website":"https://example.com/","assessment":"SUPPORTED","reason":"Found"}',
                "annotations": []}]}]})
        with patch.dict("os.environ", {"PARALLEL_RESPONSE_USD_PER_REQUEST": "0.01"}), \
             patch.object(self.provider, "reserve", return_value=1) as reserve, \
             patch.object(self.provider, "record"), \
             patch("marketing_backend.providers.httpx.post", return_value=response):
            result = self.provider.parallel_resolve_identity("identity", "Example", "https://example.com/")
            self.assertEqual(result["assessment"], "UNCERTAIN")
            reserve.assert_called_once_with("PARALLEL", "identity", 10000)

    def test_identity_keeps_safe_citations_and_bounds_long_text(self):
        response = httpx.Response(200, json={"status": "completed", "output": [{"type": "message", "content": [{
            "type": "output_text", "text": json.dumps({"company_name": "Example", "official_website": "https://example.com/", "assessment": "SUPPORTED", "reason": "x" * 2000}),
            "annotations": [{"type": "url_citation", "url": "http://127.0.0.1/"}, {"type": "url_citation", "url": "https://example.com/about"}]}]}]})
        with patch.dict("os.environ", {"PARALLEL_RESPONSE_USD_PER_REQUEST": "0.01"}), patch.object(self.provider, "reserve", return_value=1), patch.object(self.provider, "record"), patch("marketing_backend.providers.httpx.post", return_value=response):
            result = self.provider.parallel_resolve_identity("identity", "Example", "https://example.com/")
            self.assertEqual(result["sources"], ["https://example.com/about"])
            self.assertEqual(len(result["reason"]), 1500)

    def test_proposal_integrity_and_conflict(self):
        proposal = {"company_name": "Example", "official_website": "https://example.com/",
                    "assessment": "SUPPORTED", "reason": "A cited proposal", "sources": ["https://example.com/about"]}
        candidate = {"company_name": "Example", "website": "https://example.com/",
                     "source_url": "https://example.com/about", "evidence_quote": "Example operates trucks",
                     "identity_proposal": proposal, "verification_state": "PROPOSED"}
        payload = {key: candidate[key] for key in ("company_name", "website", "evidence_quote", "identity_proposal")}
        candidate["identity_digest"] = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()
        self.assertTrue(valid_saved_evidence(candidate))
        proposal["assessment"] = "CONFLICTING"
        self.assertFalse(valid_saved_evidence(candidate))

    def test_parallel_model_uses_responses_and_checkpoints(self):
        response = httpx.Response(200, json={"status": "completed", "output": [{"type": "message", "content": [{"type": "output_text", "text": '{"ok": true}'}]}]})
        with patch.dict("os.environ", {"PARALLEL_RESPONSE_USD_PER_REQUEST": "0.01"}), \
             patch.object(self.provider, "reserve", return_value=1), \
             patch.object(self.provider, "record"), \
             patch("marketing_backend.providers.httpx.post", return_value=response) as post:
            self.assertEqual(self.provider.model("research", "Return JSON", {"fact": "synthetic"}), {"ok": True})
            self.assertEqual(self.provider.model("research", "Return JSON", {}), {"ok": True})
            self.assertEqual(post.call_count, 1)
            self.assertEqual(post.call_args.kwargs["json"]["model"], "parallel")
            self.assertEqual(post.call_args.kwargs["json"]["text"]["format"]["name"], "company_research")
