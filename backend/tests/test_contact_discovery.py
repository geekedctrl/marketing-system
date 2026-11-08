import unittest
from types import SimpleNamespace
from unittest.mock import patch

from marketing_backend.stages import contacts
from marketing_backend.stage_contracts import validate_payload
from marketing_backend.research import ProviderFailure


class SyntheticProvider:
    def parallel_entity_search(self, operation, objective, *, count):
        return [{"name": "Morgan Lee", "url": "https://example.com/morgan", "description": "Title: Operations Director"},
                {"name": "Alex Doe", "url": "https://example.com/alex", "description": "Title: Fleet Manager"}]

    def search(self, operation, query):
        if "Morgan Lee" in query:
            return [{"url": "https://example.com/team", "title": "Team", "text": "Morgan Lee is Operations Director at Example Logistics."}]
        return [{"url": "https://example.com/old", "title": "Team", "text": "Former Fleet Manager Alex Doe at Example Logistics."}]

    def model(self, operation, instructions, data):
        return {"people": [{"index": 0, "role": "Operations Director"}, {"index": 1, "role": "Fleet Manager"}]}


class ContactDiscoveryTests(unittest.TestCase):
    def test_rate_limit_keeps_official_suggestions_and_stops_searching(self):
        provider = SyntheticProvider()
        calls = []
        def limited(operation, query):
            calls.append(operation)
            raise ProviderFailure("SEARCH_UNAVAILABLE", True)
        provider.search = limited
        job = SimpleNamespace(payload={"company_name": "Example Logistics", "website": "https://example.com/"})
        research = {"people": [], "pages": [{"source_url": "https://example.com/team", "text": "Example Logistics leadership\n* MORGAN LEE\n* HEAD OF OPERATIONS"}]}
        with patch("marketing_backend.stages.result", return_value=research):
            result = contacts(job, provider)
        self.assertEqual(len(calls), 1)
        self.assertEqual(result["unavailable_queries"], 1)
        self.assertEqual(result["stop_reason"], "CONTACT_SEARCH_UNAVAILABLE")
        self.assertTrue(any(s["name"] == "MORGAN LEE" for s in result["suggestions"]))
        self.assertIsNone(result["selected_contact"])

    def test_uncertain_transport_error_is_not_swallowed(self):
        provider = SyntheticProvider()
        def uncertain(operation, query):
            raise ProviderFailure("SEARCH_TRANSPORT_ERROR")
        provider.search = uncertain
        job = SimpleNamespace(payload={"company_name": "Example Logistics", "website": "https://example.com/"})
        with patch("marketing_backend.stages.result", return_value={"people": [], "pages": []}):
            with self.assertRaises(ProviderFailure) as error:
                contacts(job, provider)
        self.assertEqual(error.exception.code, "SEARCH_TRANSPORT_ERROR")

    def test_retry_searches_selected_official_person_for_email(self):
        provider = SyntheticProvider()
        provider.parallel_entity_search = lambda *args, **kwargs: []
        calls = []
        def search(operation, query):
            calls.append((operation, query))
            return [{"url": "https://news.example.org/post", "text": "Morgan Lee at Example Logistics: morgan@example.com"}]
        provider.search = search
        job = SimpleNamespace(payload={"company_name": "Example Logistics", "website": "https://example.com/"}, output_generation=2)
        research = {"people": [], "pages": [{"source_url": "https://example.com/team", "text": "Example Logistics leadership\n* MORGAN LEE\n* HEAD OF OPERATIONS"}]}
        prior = {"selected_contact": {"name": "MORGAN LEE"}}
        with patch("marketing_backend.stages.result", side_effect=lambda job, kind: research if kind == "RESEARCH" else prior):
            result = contacts(job, provider)
        self.assertEqual(len(calls), 1)
        self.assertIn('"MORGAN LEE" "Example Logistics" email', calls[0][1])
        self.assertIn("contact-selected-email-v1-g2-", calls[0][0])
        self.assertEqual(result["suggestions"][0]["email_candidates"][0]["email"], "morgan@example.com")
        self.assertIsNone(result["selected_contact"])

    def test_email_search_uses_stable_distinct_key_per_retry_generation(self):
        from marketing_backend.stages import discover_people
        calls = []
        provider = SyntheticProvider()
        provider.search = lambda operation, query: calls.append((operation, query)) or []
        job = SimpleNamespace(payload={"company_name": "Example Logistics", "website": "https://example.com/"}, output_generation=1)
        discover_people(job, provider)
        first = list(calls)
        calls.clear()
        discover_people(job, provider)
        self.assertEqual(first, calls)
        self.assertTrue(all("public business email" in query and "-v3-g1-" in key for key, query in calls))
        calls.clear()
        job.output_generation = 2
        discover_people(job, provider)
        self.assertNotEqual(first[0][0], calls[0][0])

    def test_public_email_is_saved_as_unverified_suggestion_not_selected(self):
        provider = SyntheticProvider()
        provider.search = lambda operation, query: [{"url": "https://example.com/team", "title": "Team", "text": "Morgan Lee is Operations Director at Example Logistics. Email morgan@example.com."}] if "Morgan Lee" in query else []
        job = SimpleNamespace(payload={"company_name": "Example Logistics", "website": "https://example.com/"})
        with patch("marketing_backend.stages.result", return_value={"people": []}):
            result = contacts(job, provider)
        candidate = result["suggestions"][0]["email_candidates"][0]
        self.assertEqual(candidate["email"], "morgan@example.com")
        self.assertEqual(candidate["status"], "PUBLICLY_SOURCED_UNVERIFIED")
        self.assertIsNone(result["selected_contact"])
        self.assertEqual(result["stop_reason"], "SUPPORTED_CONTACT_REQUIRED")
        validate_payload("contact.output", 3, result)

    def test_location_ranks_matching_company_ahead_of_namesake(self):
        provider = SyntheticProvider()
        provider.parallel_entity_search = lambda *args, **kwargs: [
            {"name": "Foreign Person", "url": "https://example.com/foreign", "description": "Indonesia logistics"},
            {"name": "Morgan Lee", "url": "https://example.com/morgan", "description": "Malaysia | Title: Operations Director"}]
        job = SimpleNamespace(payload={"company_name": "Example Logistics", "website": "https://example.com/", "context": {"preferences": {"country": "MY"}}})
        with patch("marketing_backend.stages.result", return_value={"people": []}):
            result = contacts(job, provider)
        self.assertEqual(result["suggestions"][0]["name"], "Morgan Lee")

    def test_empty_research_still_finds_suggestions_without_auto_selecting(self):
        job = SimpleNamespace(payload={"company_name": "Example Logistics", "website": "https://example.com/"})
        with patch("marketing_backend.stages.result", return_value={"people": []}):
            result = contacts(job, SyntheticProvider())
        self.assertIsNone(result["selected_contact"])
        self.assertEqual(result["stop_reason"], "SUPPORTED_CONTACT_REQUIRED")
        self.assertEqual([s["status"] for s in result["suggestions"]], ["SUPPORTED", "UNVERIFIED"])
        self.assertIsNone(result["suggestions"][1]["role"])
        self.assertNotIn("email", result["suggestions"][0])
        validate_payload("contact.output", 3, result)
        old = {key: value for key, value in result.items() if key != "suggestions"}
        self.assertEqual(validate_payload("contact.output", 1, old)["people"], [])
        self.assertEqual(validate_payload("contact.output", 2, old)["people"], [])

    def test_official_page_people_are_suggested_even_without_entity_match(self):
        provider = SyntheticProvider()
        job = SimpleNamespace(payload={"company_name": "Example Logistics", "website": "https://example.com/"})
        research = {"people": [], "pages": [{"source_url": "https://example.com/team", "text": "Example Logistics\nLEADERSHIP TEAM\n* AVERY NG\n* HEAD OF OPERATIONS\n* TAYLOR DOE\n* HEAD OF PEOPLE"}]}
        with patch("marketing_backend.stages.result", return_value=research):
            result = contacts(job, provider)
        self.assertEqual(result["suggestions"][0]["name"], "AVERY NG")
        self.assertEqual(result["suggestions"][0]["status"], "SUPPORTED")
        self.assertIsNone(result["selected_contact"])

    def test_ended_role_is_explicitly_flagged(self):
        provider = SyntheticProvider()
        provider.parallel_entity_search = lambda *args, **kwargs: [{"name": "Morgan Lee", "url": "https://example.com/morgan", "description": "Title: Operations Director | 2021-02-01 2024-02-01"}]
        provider.search = lambda *args, **kwargs: []
        job = SimpleNamespace(payload={"company_name": "Example Logistics", "website": "https://example.com/"})
        with patch("marketing_backend.stages.result", return_value={"people": []}):
            result = contacts(job, provider)
        self.assertEqual(result["suggestions"][0]["status"], "UNVERIFIED")
        self.assertIn("end dates", result["suggestions"][0]["uncertainty"])

    def test_conflicting_official_role_demotes_an_entity_match(self):
        provider = SyntheticProvider()
        job = SimpleNamespace(payload={"company_name": "Example Logistics", "website": "https://example.com/"})
        research = {"people": [], "pages": [{"source_url": "https://example.com/team", "text": "Example Logistics leadership\n* MORGAN LEE\n* HEAD OF OPERATIONS\n* MORGAN LEE\n* FLEET MANAGER"}]}
        with patch("marketing_backend.stages.result", return_value=research):
            result = contacts(job, provider)
        morgan = next(p for p in result["suggestions"] if p["name"].casefold() == "morgan lee")
        self.assertEqual(morgan["status"], "UNVERIFIED")


if __name__ == "__main__":
    unittest.main()
