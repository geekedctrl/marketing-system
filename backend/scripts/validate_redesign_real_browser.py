"""Synthetic real-service browser acceptance for the native dashboard redesign.

Uses only the disposable native-acceptance stack and its patched synthetic worker.
Creates a uniquely named test workspace; never resets the shared acceptance DB.
"""
import json
import os
import re
import subprocess
import time
import uuid
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright


def main():
    base = os.getenv("NATIVE_ACCEPTANCE_URL", "http://127.0.0.1:8105").rstrip("/")
    endpoint = urlsplit(base)
    if endpoint.scheme != "http" or endpoint.hostname not in {"127.0.0.1", "localhost"}:
        raise SystemExit("Only the local synthetic acceptance frontend is allowed")
    fixtures = Path(os.getenv("NATIVE_ACCEPTANCE_FIXTURES", "tmp/ui-acceptance-accounts.json"))
    data = json.loads(fixtures.read_text(encoding="utf-8"))
    if not all(a["email"].endswith("@example.test") for a in data["accounts"].values()):
        raise SystemExit("Synthetic acceptance accounts only")

    marker = uuid.uuid4().hex[:8]
    workspace_name = "Browser Acceptance " + marker
    company_marker = "Browser discovery acceptance " + marker
    errors = []

    with sync_playwright() as runtime:
        executable = os.getenv(
            "FRONTEND_BROWSER",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        )
        browser = runtime.chromium.launch(
            headless=True,
            executable_path=executable if Path(executable).exists() else None,
        )
        try:
            context = browser.new_context(viewport={"width": 1440, "height": 1000})
            page = context.new_page()
            page.set_default_timeout(45000)
            page.on("pageerror", lambda error: errors.append(str(error)))

            def sign_in(role, target=page):
                target.goto(base)
                target.get_by_label("Email", exact=True).fill(data["accounts"][role]["email"])
                target.get_by_label("Password", exact=True).fill(data["accounts"][role]["password"])
                target.get_by_role("button", name="Sign in", exact=True).click()
                target.get_by_role("heading", name="Overview", exact=True).wait_for()

            def get_json(target, wid, path):
                response = target.request.get(f"{base}/gateway/{wid}/{path}")
                if not response.ok:
                    raise AssertionError(f"GET {path} returned {response.status}")
                return response.json()

            sign_in("ADMIN")
            page.get_by_role("button", name="Create workspace", exact=True).click()
            page.get_by_label("Workspace name", exact=True).fill(workspace_name)
            page.get_by_label("Description (optional)", exact=True).fill(
                "Disposable synthetic real-service browser acceptance"
            )
            page.get_by_role("button", name="Continue", exact=True).click()
            page.get_by_role("button", name="Create workspace", exact=True).click()
            page.get_by_role("heading", name="Settings", exact=True).wait_for()
            page.get_by_role("heading", name="Product setup", exact=True).wait_for()
            wid = page.locator("#workspace").input_value()
            assert wid and wid not in data["workspaces"], "Expected a fresh synthetic workspace"

            # This disposable acceptance stack's worker handles Python-owned jobs;
            # newly-created workspaces default to N8N ownership. Route only this
            # uniquely-created synthetic workspace to the fixture worker. Fail
            # closed unless both the loopback URL and exact disposable DB container
            # are in use; this does not alter application defaults or other tenants.
            fixture_db = os.getenv(
                "NATIVE_ACCEPTANCE_DB_CONTAINER", "ui-redesign-acceptance2-native-db-1"
            )
            if (
                base != "http://127.0.0.1:8105"
                or fixture_db != "ui-redesign-acceptance2-native-db-1"
                or not re.fullmatch(r"[0-9a-f-]{36}", wid)
            ):
                raise SystemExit("Refusing fixture ownership update outside the disposable acceptance2 stack")
            sql = (
                "UPDATE executor_ownership SET owner='PYTHON',state='ACTIVE',version=version+1 "
                f"WHERE workspace_id='{wid}'::uuid AND capability IN "
                "('SETUP','DISCOVERY','PREPARATION') AND owner='N8N'; "
                "INSERT INTO memberships(workspace_id,user_id,role) "
                f"SELECT '{wid}'::uuid,id,'REVIEWER' FROM users "
                "WHERE email='reviewer@example.test' ON CONFLICT(workspace_id,user_id) "
                "DO UPDATE SET role='REVIEWER'; "
                "INSERT INTO organization_memberships(organization_id,user_id,role) "
                f"SELECT w.organization_id,u.id,'MEMBER' FROM workspaces w CROSS JOIN users u "
                f"WHERE w.id='{wid}'::uuid AND u.email='reviewer@example.test' "
                "ON CONFLICT(organization_id,user_id) DO UPDATE SET role='MEMBER';"
            )
            routed = subprocess.run(
                ["docker", "exec", fixture_db, "psql", "-v", "ON_ERROR_STOP=1",
                 "-U", "native_acceptance", "-d", "marketing_native_acceptance", "-c", sql],
                capture_output=True, text=True, check=True,
            )
            if "UPDATE 3" not in routed.stdout or routed.stdout.count("INSERT 0 1") != 2:
                raise AssertionError("Expected three ownership rows plus reviewer workspace and organization memberships")

            page.get_by_label("Describe the real product", exact=True).fill(
                f"{company_marker}: commercial transport scheduling and delivery operations."
            )
            page.get_by_label("Target customers (optional)", exact=True).fill(
                "Transport companies with documented fleet operations"
            )
            page.get_by_label("Country code", exact=True).fill("MY")
            page.get_by_label("Language", exact=True).fill("English")
            page.get_by_label("Brand voice", exact=True).fill("Professional and concise")
            page.get_by_label("Maximum companies per batch", exact=True).fill("1")
            page.get_by_role("button", name="Continue", exact=True).click()
            page.get_by_role("button", name="Add offering", exact=True).click()
            page.get_by_label("Stable catalog code", exact=True).fill("OPS")
            page.get_by_label("Offering name", exact=True).fill("Fleet scheduling")
            page.get_by_label("Documented capabilities", exact=True).fill(
                "Commercial fleet scheduling and delivery operations support."
            )
            page.get_by_role("button", name="Continue", exact=True).click()
            page.get_by_role("button", name="Save offerings & activate", exact=True).click()
            page.get_by_role("heading", name="Jobs & history", exact=True).wait_for()

            deadline = time.monotonic() + 90
            while time.monotonic() < deadline:
                jobs = get_json(page, wid, "jobs")
                setup = next((j for j in jobs if j.get("kind") == "SETUP"), None)
                if setup and setup.get("status") in {"COMPLETED", "FAILED"}:
                    break
                time.sleep(0.5)
            assert setup and setup["status"] == "COMPLETED", "Synthetic setup worker did not complete"

            page.get_by_role("link", name="Discovery", exact=True).click()
            page.get_by_role("button", name="Find leads", exact=True).click()
            deadline = time.monotonic() + 90
            candidate = None
            while time.monotonic() < deadline:
                listing = get_json(page, wid, "candidates?status=READY_FOR_REVIEW")
                candidate = next(
                    (c for c in listing.get("items", []) if marker in c.get("domain", "")),
                    None,
                )
                if candidate:
                    break
                time.sleep(0.5)
            assert candidate, "Synthetic discovery worker did not persist the marked candidate"
            before_page = get_json(page, wid, "leads/page?limit=100")
            before = before_page.get("items", [])
            assert all(c["id"] != candidate.get("accepted_lead_id") for c in before)
            assert all(candidate["domain"] not in c.get("website", "") for c in before), (
                "Candidate became a lead before explicit human acceptance"
            )
            page.get_by_role("heading", name=candidate["company_name"], exact=True).wait_for()
            candidate_card = page.get_by_role(
                "heading", name=candidate["company_name"], exact=True
            ).locator("xpath=ancestor::article")
            candidate_card.get_by_text("Review details & evidence", exact=False).click()
            with page.expect_response(
                lambda response: response.url.endswith(f"/candidates/{candidate['id']}/accept")
            ) as accepted:
                page.get_by_role("button", name="Accept & start research", exact=True).click()
            assert accepted.value.status == 200, f"Candidate accept returned {accepted.value.status}"
            accepted_body = accepted.value.json()
            lead_id = accepted_body["lead_id"]
            detail = get_json(page, wid, f"candidates/{candidate['id']}")
            assert detail["status"] == "ACCEPTED" and detail["accepted_lead_id"] == lead_id

            deadline = time.monotonic() + 120
            latest = None
            while time.monotonic() < deadline:
                current = get_json(page, wid, "leads/page?limit=100")
                latest = next((x for x in current.get("items", []) if x["id"] == lead_id), None)
                prep = (latest or {}).get("current_preparation") or {}
                if prep.get("status") in {"PENDING_APPROVAL", "NEEDS_REVIEW", "FAILED"}:
                    break
                time.sleep(1)
            assert latest, "Accepted lead did not appear in real BFF lead listing"
            assert (latest.get("current_preparation") or {}).get("status") == "PENDING_APPROVAL", (
                f"Preparation did not reach human review: {(latest.get('current_preparation') or {}).get('status')}"
            )
            page.get_by_role("link", name="Approvals", exact=True).click()
            page.get_by_text(candidate["company_name"], exact=True).wait_for()

            # A reviewer can inspect the pending draft; this journey deliberately does not approve or send.
            reviewer_context = browser.new_context(viewport={"width": 1440, "height": 1000})
            reviewer = reviewer_context.new_page()
            reviewer.set_default_timeout(45000)
            reviewer_errors = []
            reviewer.on("pageerror", lambda error: reviewer_errors.append(str(error)))
            sign_in("REVIEWER", reviewer)
            with reviewer.expect_response(
                lambda response: response.url.endswith("/session/workspace")
                and response.request.method == "POST"
            ) as switched:
                reviewer.locator("#workspace").select_option(wid)
            assert switched.value.status == 200, (
                f"Reviewer workspace switch returned {switched.value.status}"
            )
            reviewer.get_by_role("heading", name="Overview", exact=True).wait_for()
            reviewer.get_by_role("link", name="Approvals", exact=True).click()
            prep_id = (latest.get("current_preparation") or {}).get("id")
            approval = next(
                (a for a in get_json(reviewer, wid, "approvals")
                 if a.get("status") == "PENDING"
                 and a.get("run_id") == prep_id),
                None,
            )
            assert approval, "Reviewer did not receive the pending draft"
            try:
                reviewer.get_by_role("heading", name="Draft review", exact=True).wait_for()
                reviewer.get_by_role("heading", name=candidate["company_name"], exact=True).wait_for()
            except Exception as error:
                body = reviewer.locator("body").inner_text(timeout=5000)
                raise AssertionError(
                    "Reviewer draft did not render after API returned the matching approval; "
                    f"url={reviewer.url!r}, body={body!r}, pageerrors={reviewer_errors!r}"
                ) from error
            draft_value = approval.get("snapshot", {}).get("draft", {})
            for field in ("subject", "body"):
                expected = draft_value.get(field)
                if expected:
                    reviewer.get_by_text(expected, exact=True).wait_for()

            # Nonmember workspace isolation is enforced by the real dashboard BFF/API boundary.
            outsider_context = browser.new_context(viewport={"width": 1440, "height": 1000})
            outsider = outsider_context.new_page()
            sign_in("OUTSIDER", outsider)
            denied = outsider.request.get(f"{base}/gateway/{wid}/leads/page?limit=25")
            if denied.status == 409:
                # The BFF denies cross-workspace requests before calling the API.
                # Require its exact non-data error payload to prove this is the
                # active-session workspace mismatch guard, not an ambiguous conflict.
                assert denied.json() == {
                    "detail": "Workspace changed. Refresh this page."
                }, f"Unexpected 409 body: {denied.text()}"
            else:
                assert denied.status in {403, 404}, (
                    f"Outsider workspace read unexpectedly returned {denied.status}"
                )
                assert "items" not in denied.json(), "Denied response disclosed lead data"
            assert not errors, errors
            print(
                "PASS synthetic real-service browser journey: fresh workspace setup, actual discovery worker, "
                "candidate hidden from leads until explicit accept, accepted lead researched through PENDING_APPROVAL, "
                "reviewer can inspect, outsider denied; no approval or message sent"
            )
            print(f"workspace={wid} candidate={candidate['company_name']} lead={lead_id} marker={marker}")
        finally:
            browser.close()


if __name__ == "__main__":
    main()
