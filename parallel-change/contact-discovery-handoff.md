# Parallel contact discovery: implementation and handoff

Last checked: 4 November 2026. This document describes the local implementation and its remaining work. Source code and executed tests take precedence over this handoff. Historical entries in `docs/ai/` may describe earlier states; the later entries supersede them.

## Current state and where the work lives

- The active implementation is in the isolated worktree `C:\Projects\marketing-contact-discovery`, branch `feature/parallel-contact-discovery`, based on commit `b7c6b8d25234da2bf962668f7fc18285bc83960e`.
- **The worktree is dirty and its changes are not committed, pushed, merged, or in the main codebase.** It contains the earlier Parallel preparation as well as the contact work and tests. The original checkout, `C:\Projects\marketing-system`, is on `checkpoint/parallel-ai-preparation` and already had substantial uncommitted changes before this contact work. Do not reset, overwrite, or blindly copy either checkout. Compare their diffs and preserve all user-owned changes.
- The current checkout's `parallel-change/` folder is where this handoff is saved. Existing plans in that folder are useful background but do not override the source or this newer status.
- Project rules remain in force: read `docs/ai/HANDOFF.md`, `docs/ai/PROJECT_STATE.md`, and `docs/ai/TASK_BOARD.md` before further work; preserve workspace isolation; use isolated branches and synthetic test data; and do not automatically send, publish, spend on providers, deploy, or merge. Human review/approval remains a separate decision. The lead owns `docs/ai/`.
- This is the native Python backend and worker flow. Do not infer that the legacy deployed executor has been replaced. The requested contact flow uses Parallel; n8n and xKiro are not part of the new contact-discovery path.

## What was implemented

### Parallel provider and cost controls

`backend/marketing_backend/providers.py` contains the Parallel search, Responses, company identity and entity-search adapters. Contact discovery calls Parallel's synchronous people Entity Search at `/v1beta/findall/entity-search`, using a bounded result count, and then performs a bounded set of Parallel Search calls for evidence. Entity Search supplies name, URL and description; it does not by itself establish a person's role or current employment.

Provider operations reserve estimated cost in the existing `ProviderUsage` ledger before a request. Parallel's configured monthly cap is constrained to at most USD 32, alongside the existing global and product-line limits. The entity-search adapter requires a configured reservation of at least USD 0.005 per request and caps its requested results at 100; the current contact flow requests 10 and investigates at most five. Prices are configuration inputs, not proof of a provider's actual account charge. The user explicitly said billing optimization/checking is not a current priority.

Durable checkpoints cache successful responses. Entity and evidence operations use distinct checkpoint names; evidence lookups use a hash of the candidate's name and URL rather than a mutable list position. Transport errors and provider 5xx responses are recorded as uncertain. `queue.fail`, lease-expiry recovery, and the job retry API prevent normal retry when a Parallel reservation is unresolved or a successful request has no corresponding checkpoint. The reservation remains counted until reconciled. See `providers.py`, `queue.py`, `api.py`, `test_parallel_entity_search.py`, `test_parallel_search.py`, and the budget/recovery tests in `test_native_pipeline.py` and `test_worker_pools.py`.

**Important limitation:** the broader Parallel/discovery changes were not fully reviewed; do not treat the existing safeguards as a completed security or release audit. The branch also contains earlier company-discovery changes outside the contact feature.

### Finding and ranking people

`backend/marketing_backend/stages.py` now runs company-wide people discovery even when the research brief has no named people. The Entity Search objective includes the accepted company's name, website and configured country. Candidate descriptions are ranked using website/location and operations, fleet, logistics, transport and seniority signals before the bounded evidence lookups. These are heuristics, not proof of identity. Country-name handling is currently explicit for Malaysia, Singapore and Indonesia and falls back to the configured country value elsewhere.

The worker also inspects already-saved research pages and Parallel Search excerpts. `backend/marketing_backend/contact_evidence.py` extracts adjacent name/role bullet pairs from an official company leadership, management, directors or executives page. This is deliberately a narrow deterministic pattern; it will not capture every possible page layout. It prefers operations/fleet/logistics decision-makers over general leadership and unrelated roles. It does not follow instructions found in source material or infer email addresses.

The final list is capped at five suggestions. Source-derived people can be included even when Entity Search did not return them. Duplicate entity/source suggestions are reconciled. Conflicting roles for the same person or multiple people with the same singular leadership title are treated as ambiguous, rather than silently choosing one. Dated historical role ranges are flagged for review; that date heuristic does not establish whether any other role is current.

### Evidence and uncertainty

A suggestion is `SUPPORTED` only when usable source text supports the name and role together and identifies the accepted company. The name and role must appear as a short explicit pairing, not merely somewhere on the same page. The accepted company's own website can support the association; an independent third-party excerpt must also explicitly identify the accepted website. A person's profile alone is not treated as proof of current employment. A source-backed match remains a suggestion for human review, and the UI says to confirm the role is current.

Other results remain `UNVERIFIED`; safe source links and bounded excerpts are retained where available. The matcher is intentionally conservative and may miss valid people or flag an entire source because it contains stale-language markers. It relies on excerpts rather than establishing publication freshness or continuously verifying employment. Human judgment remains necessary.

### Versioned artifacts, API and review UI

- New product-line contact artifacts use `contact.output` schema version 3, carrying suggestions, evidence, uncertainty and optional operator review. Version 1 and 2 artifacts remain readable. Existing older tasks keep their historical artifact shape; older-task public/job results can still carry the expanded suggestions. See `stage_contracts.py`, `worker_contracts.py`, `product_lines.py`, `contracts.py`, migration `019_discovery_candidate_v4.py`, and `human_artifacts.py`.
- The People view displays sourced suggestions, their support state and uncertainty. Supported suggestions can be selected for review without inventing an email. If no supported outreach channel exists, the run remains at `NEEDS_REVIEW` / `SUPPORTED_CONTACT_REQUIRED` rather than starting a draft.
- Unverified suggestions have **Review suggestion**. An ADMIN or OPERATOR can record **Keep for further review**, **Reject suggestion**, or **Leave unresolved**, with a required note. The item remains `UNVERIFIED`; recording a decision is not independent verification and does not select a primary contact, create a channel, start scoring, create approval, or send outreach.
- The review endpoint is `POST /workspaces/{wid}/preparation/{rid}/suggestions/{suggestion_index}/review`. It checks workspace/role, waiting state and context, and compares the submitted suggestion name and URL with the current entry to reject stale index submissions. The dashboard BFF allowlists the route for ADMIN/OPERATOR. Review actor, time, decision and note are saved in job history; versioned product-line runs additionally write a new immutable contact artifact. Older/unversioned work retains the history entry even when the old artifact schema cannot carry suggestions.
- Supported-contact selection and suggestion review do not approve or send outreach. Existing human-review and separate sending/approval controls remain in force.

## Pos Logistics local check

The local accepted lead is Pos Logistics, website `https://www.poslogistics.com.my/`. Its preparation run is `de95fb2b-41e1-4134-8b22-bcf675776ebf`; the CONTACT_SEARCH job is `492ceb9c-e10f-4600-8e15-87e2bd527d91`. These identifiers are for the isolated local database, not production.

The initial Entity Search returned some similarly named businesses in other countries. After adding website/country ranking, a live local retry returned five Malaysia/Pos Logistics Berhad-oriented suggestions and one source-supported Head of People. Inspection of the saved company leadership excerpt showed an operations lead whom Entity Search itself had not suggested. The later source-extraction change reprocessed the saved checkpoints without new provider calls and put **ABDUL RAHIM ALI — HEAD OF OPERATIONS** first, marked `SUPPORTED`, sourced to `https://www.poslogistics.com.my/board-of-directors`. The latest stricter name/role pairing check was also tested against that saved excerpt.

At the time this document was written the other four displayed suggestions were Kamarulariffin Chu Yusoff, Harald Raunio, Roskam Iryantie, and Luqman Hakim bin HJ A Rashid, all `UNVERIFIED`. Some descriptions contain past-role end dates. Their display is a lead for review, not a claim of current employment. The run and contact job remain `NEEDS_REVIEW` / `SUPPORTED_CONTACT_REQUIRED`; no person was selected, no email was guessed, and no outreach was sent. The operator-review action was tested synthetically, not exercised by making a real review decision for any of these people.

## Local runtime and configuration

The isolated Docker Compose project is named `parallel-local-test`. At the last check its native database, API, dashboard, research worker, discovery worker, scheduler and CONTACT_SEARCH worker were running and healthy. The local dashboard is `http://localhost:8081`; the native API is bound locally on port `18020`. These are local services, not a DEV or production deployment.

The API, dashboard and contact worker have been rebuilt from the isolated feature checkout. The worktree has an **ignored** `.env.local` containing local configuration copied from the running stack. It can contain credentials: do not print, share, or commit it. The original checkout's `.env.local` and other user-owned files were not replaced. Recreating the contact container from the isolated Compose configuration was checked against the existing local database. Dashboard sessions are process-local: rebuilding or recreating the dashboard clears sessions and requires users to sign in again.

From `C:\Projects\marketing-contact-discovery`, the targeted rebuild command is:

```powershell
docker compose --env-file .env.local -p parallel-local-test -f compose.backend.yml -f compose.worker-pools.yml up -d --no-deps --build backend-api dashboard-dev backend-contacts
```

Check that no relevant jobs are running before replacing workers or services. Avoid `down -v`, deleting databases/volumes, changing unrelated running stacks, or running the full Compose set without understanding the effects. The local configuration and database are not a portable release or migration procedure.

## Verification performed

- Synthetic contact tests cover no named research contacts, entity suggestions, source identity checks, role ranking, stale/ambiguous roles, unverified suggestions, source-link safety, absence of inferred email, artifact compatibility and the explicit review stop.
- Synthetic PostgreSQL/API tests cover cost reservation limits, uncertain request failure, blocked manual retries, lease-expiry recovery, workspace and role checks, supported-contact selection without an email, operator review and immutable product-line artifacts. A prior broad run reported 78 backend tests passing; after subsequent contact extraction, a 38-test pipeline/contact run passed and focused evidence and review tests were rerun after later changes. These numbers refer to separate runs, not a single final full-suite run.
- The latest operator-review change passed targeted synthetic PostgreSQL tests for permissions, stale selection and immutable history; 32 focused backend/contract tests passed in one run. Thirteen BFF checks and a headless browser acceptance passed, including reviewing a synthetic unverified suggestion and selecting a supported synthetic suggestion with no email. The browser journey uses a mocked upstream; it is not a full real-API browser acceptance for the new review action.
- The local real-provider Pos Logistics search and saved-evidence reprocessing are described above. They demonstrate this one case, not broad live-provider quality. The user asked not to spend time checking/optimizing billing. Historical local ledger estimates are reservations, not independently verified account charges.
- A full Orca review was **not completed**. `orca-review` planned the whole dirty worktree, which included earlier Parallel discovery/configuration changes outside the immediate contact work. It was submitted as partial and rejected with: `Unusable result, failing closed: review is partial`. This is **not a merge-readiness pass**. No full CI, PR, push, merge, or release is claimed.

## Pending work, in suggested order

1. **Complete a real review of the whole intended change.** Decide which earlier Parallel preparation changes belong with contact discovery. The current dirty worktree includes pre-existing user changes and contact work; establish a clean, reviewable diff without losing either. Run the repository's required local review and address findings. The last Orca result was partial, not passed.
2. **Complete integration deliberately.** Reconcile the isolated feature worktree with the intended source branch, inspect migration `019` and artifact/schema compatibility, run appropriate full backend, dashboard, browser, workspace-isolation and CI checks, and create any requested review artifact/PR. Respect the project rule against automatically merging or deploying. The original dirty checkout must not be overwritten as a shortcut.
3. **Expand evidence and extraction coverage.** The official-page extractor currently recognizes a specific adjacent-bullet layout and a bounded set of role/name patterns. Test more real public layouts, names, titles, dates, multiple executives, company-name collisions and long excerpts using synthetic fixtures. Verify that third-party evidence reliably ties a person and role to the correct accepted company; a search/profile match remains insufficient on its own. Add wider geography handling and assess ranking quality on more than one company.
4. **Exercise the complete operator flow against the real local API with synthetic data.** The browser test currently uses mocked API responses and the real API tests use synthetic PostgreSQL fixtures separately. Add an end-to-end native dashboard/BFF/API/database/worker journey for an unverified review, rejection, stale submission and no-email selection, including ADMIN/OPERATOR versus VIEWER and cross-workspace isolation. Confirm no draft or send is created as a side effect.
5. **Review operational behavior before regular use.** Test provider failures and uncertain-request reconciliation with the real restricted worker role and restarts, document an operator-safe reconciliation procedure, verify retry behavior after changes to a candidate list, and check that older artifacts and checkpoint generation work across upgrades. Verify retention/audit behavior when review decisions are changed, retried, or the result list is regenerated.
6. **Confirm product semantics.** The new operator action records a judgment on an unverified suggestion; it does not independently verify the person or turn them into the selected primary contact. Decide whether future UX needs a separate, explicit evidence-backed verification and selection flow, and how a usable supported channel is added. Preserve the no-email/no-automatic-send boundary.

The user explicitly deferred billing optimization, so do not make account billing analysis a blocker for the next contact-quality work unless they ask again. Any future live-provider request must still follow the project's existing human authorization and budget rules.
