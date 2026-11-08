import unittest

from marketing_backend.contact_evidence import support_for_person, extract_official_people, role_priority, public_email_candidates


class ContactEvidenceTests(unittest.TestCase):
    def test_public_email_is_literal_unverified_and_retains_source(self):
        rows = [{"url": "https://news.example.org/people", "text": "Example Logistics: Morgan Lee can be reached at morgan@example.com."}]
        result = public_email_candidates("Morgan Lee", "Example Logistics", rows, "2026-11-05T00:00:00Z")
        self.assertEqual(result[0]["email"], "morgan@example.com")
        self.assertEqual(result[0]["source_url"], rows[0]["url"])
        self.assertEqual(result[0]["status"], "PUBLICLY_SOURCED_UNVERIFIED")
        self.assertIn(result[0]["email"], result[0]["evidence_quote"])

    def test_public_email_rejects_unsafe_stale_and_unrelated_excerpts(self):
        text = "Example Logistics: Morgan Lee previously used morgan@example.com"
        self.assertEqual(public_email_candidates("Morgan Lee", "Example Logistics", [{"url": "https://example.com", "text": text}], "2026-11-05"), [])
        text = "Example Logistics: Morgan Lee uses morgan@example.com"
        self.assertEqual(public_email_candidates("Morgan Lee", "Example Logistics", [{"url": "http://127.0.0.1/", "text": text}], "2026-11-05"), [])
        self.assertEqual(public_email_candidates("Taylor Doe", "Example Logistics", [{"url": "https://example.com", "text": text}], "2026-11-05"), [])
    def test_requires_person_role_and_company_in_same_safe_excerpt(self):
        rows = [{"url": "https://example.com/team", "text": "Morgan Lee is Operations Director at Example Logistics."}]
        self.assertEqual(len(support_for_person("Morgan Lee", "Operations Director", "Example Logistics", rows)), 1)
        self.assertEqual(support_for_person("Morgan Lee", "Fleet Manager", "Example Logistics", rows), [])
        self.assertEqual(support_for_person("Morgan Lee", "Operations Director", "Other Logistics", rows), [])
        unrelated = [{"url": "https://example.com/team", "text": "Example Logistics: Morgan Lee is Chief Executive. Taylor Doe is Operations Director."}]
        self.assertEqual(support_for_person("Morgan Lee", "Operations Director", "Example Logistics", unrelated), [])

    def test_stale_and_unsafe_evidence_is_not_supported(self):
        for url, text in [("https://example.com/team", "Former Operations Director Morgan Lee at Example Logistics"),
                          ("http://127.0.0.1/", "Morgan Lee is Operations Director at Example Logistics")]:
            self.assertEqual(support_for_person("Morgan Lee", "Operations Director", "Example Logistics", [{"url": url, "text": text}]), [])

    def test_independent_source_must_identify_the_accepted_domain(self):
        base = "Morgan Lee is Operations Director at Example Logistics"
        rows = [{"url": "https://news.example.org/people", "text": base + " (example.com)."}]
        self.assertTrue(support_for_person("Morgan Lee", "Operations Director", "Example Logistics", rows, website="https://example.com"))
        rows[0]["text"] = base
        self.assertFalse(support_for_person("Morgan Lee", "Operations Director", "Example Logistics", rows, website="https://example.com"))
        rows[0]["text"] += " (example.com)."
        self.assertFalse(support_for_person("Morgan Lee", "Operations Director", "Example Logistics", rows, website="https://example.com", profile_url=rows[0]["url"]))

    def test_extracts_adjacent_official_bullets_and_prefers_operations(self):
        rows = [{"url": "https://example.com/team", "text": "Example Logistics\nLEADERSHIP TEAM\n* MORGAN LEE\n* HEAD OF OPERATIONS\n* TAYLOR DOE\n* HEAD OF PEOPLE"}]
        people = extract_official_people(rows, "https://example.com", "Example Logistics")
        self.assertEqual([(p["name"], p["role"]) for p in people], [("MORGAN LEE", "HEAD OF OPERATIONS"), ("TAYLOR DOE", "HEAD OF PEOPLE")])
        self.assertTrue(people[0]["evidence"])
        self.assertGreater(role_priority(people[0]["role"]), role_priority(people[1]["role"]))
        rows[0]["url"] = "https://elsewhere.com/team"
        self.assertEqual(extract_official_people(rows, "https://example.com", "Example Logistics"), [])

    def test_stale_and_conflicting_page_roles_remain_unverified(self):
        rows = [{"url": "https://example.com/team", "text": "Example Logistics leadership\n* MORGAN LEE\n* HEAD OF OPERATIONS\nformerly in this role"},
                {"url": "https://example.com/people", "text": "Example Logistics leadership\n* MORGAN LEE\n* FLEET MANAGER"}]
        people = extract_official_people(rows, "https://example.com", "Example Logistics")
        self.assertEqual(len(people), 1)
        self.assertEqual(people[0]["evidence"], [])

    def test_different_people_with_same_singular_title_are_ambiguous(self):
        rows = [{"url": "https://example.com/team", "text": "Example Logistics leadership\n* MORGAN LEE\n* HEAD OF OPERATIONS\n* TAYLOR DOE\n* HEAD OF OPERATIONS"}]
        people = extract_official_people(rows, "https://example.com", "Example Logistics")
        self.assertEqual(len(people), 2)
        self.assertTrue(all(not p["evidence"] for p in people))


if __name__ == "__main__":
    unittest.main()
