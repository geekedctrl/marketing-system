# LorrySystem AI Development Handoff

## Native frontend continuation — 11 October 2026

Latest: backend BE-01–06 fixes consumed from `rebuild/native-frontend-support`. Frontend profile/pagination/detail/lifecycle/revision adapters implemented and integer contact-search count fixed. Eight BFF groups and expanded synthetic browser checks pass. Both original and support-specific actual browser journeys passed against disposable native API/PostgreSQL/workers through localhost8095. The older connection-blocked statement below is superseded. See `docs/native-frontend-backend-support.md` and `docs/native-frontend.md`. Production session storage and BE-07–11 remain separate work; no release or real-provider activity.

Backend follow-up task brief: [backend-native-frontend-handoff.md](../backend-native-frontend-handoff.md). It prioritizes actual native integration, typed contracts/capabilities, detail/lists, revisions and catalog lifecycle, with ownership and acceptance requirements for the backend agent.

User authorized implementation of the native frontend plan on `geekedctrl/redesign-frontend`. Current task follows the native Python backend handoff, superseding the historical campaign next steps below. Independent entry point `dashboard/app/native.py`, native HTML/CSS/JS, copied frontend handoff/OpenAPI, and synthetic BFF/browser validation have been added. Read `docs/native-frontend.md` for run commands, behavior, limitations and verification. Do not execute the historical push/merge steps below as instructions for this task.

Backend checkpoint721a44f is in the separate `rebuild/python-backend` checkout. Only read-only source/reference inspection was performed there. Native container-internal `/health` succeeds; Windows localhost8020 refuses connections. Actual backend/worker/browser integration remains pending. Sessions are process-local for single-process local preview; shared production session storage is a release dependency. No provider calls, emails, deployment, push or merge performed.

## Last Updated
2026-10-10T10:28:00+08:00

## Project Goal
Evolve the existing product; Milestone B delivers mock campaign strategy from qualified evidence-backed prospects to saved proposals and human review.

## Repository State
Application https://github.com/geekedctrl/lorrysystem-marketing-system — codex/campaign-strategist, base9c0a3b0f03306d399ba9ee76ab14a8be37e7ed09. Initial knowledge checkpoint9540786. Implementation currently uncommitted and about to be checkpointed; run git status --short and git rev-parse HEAD.
Deployment https://github.com/geekedctrl/lorrysystem-deploy — main,cba785acbb4da43a135da4a6bc06d1bfb94cda40 inspected through API; no modifications.

## Current Milestone
B — mock Campaign Strategist; feature code and local verification complete, PR/remote CI pending.

## Current Task
B-04, lead, IN_PROGRESS: checkpoint and PR to develop.

## Completed Work
Three bounded audits, shared vendor-neutral docs, API/migration015 and dashboard review UX.13 offline tests,27 PostgreSQL checks,62 actual HTTP/dashboard checks,8 focused dashboard tests. Existing workspace183 checks, research, pipeline, quality, automation, n8n70, presentation8 and UX5 passed. See TEST_STATUS.md.

## Incomplete Work
Push implementation and open PR; remote CI results. Live providers, creative generation, global budget ledger, multichannel conversion, CRM and video are later milestones. Contact verification metadata and browser viewport visual QA remain limitations.

## Changed Files
api/app auth/router/model/schema/service registrations; api/scripts campaign suites and workspace RLS count; database/migrations/versions/015_campaign_proposals.py; dashboard/app routes, workspace roles, templates and portable import temp path; dashboard/scripts/validate_campaign_proposals.py; .github/workflows/ci.yml; README.md; docs/campaign-strategist.md; AGENTS.md and docs/ai.

## Architecture Decisions
DECISIONS.md ADR001–004. Proposal review is not outbound action approval. Mock provider constrained in DB. Unknown future asset cost is null; generation cost0 is known. Context/optimistic versions guard review and edits.

## Test Results
TEST_STATUS.md gives commands/environment/caveats. WindowsPython3.14 venv, PostgreSQL17 disposable container lorry-campaign-test-8882 at localhost55432/campaign_test, API8012/dashboard8092. No existing data volumes. Synthetic-only tests. No actual search/model/send.

## Blockers
No local implementation blocker. Git shared metadata requires sandbox escalation. Remote CI not executed yet. USD50 total monthly policy is not implemented; live paid adapters must wait for cost controls and authorization.

## Next Steps
1. Commit reviewed implementation, push codex/campaign-strategist and create PR targeting develop.
2. Record PR and remote CI result; stop task-owned local services/container after testing.
3. Review/merge only with user authorization; then plan milestone C mock asset lifecycle and budget reservations.

## Safety Notes
No merging, DEV/PROD deployment, real prospect contact, paid provider calls, account credentials or infrastructure changes authorized. Feature branch does not trigger DEV deployment. Free-form copy remains an unverified human-reviewed suggestion; social affiliation remains hypothesis. Migration downgrade drops proposal history, requiring backup/export.

## Handoff Readiness
PARTIAL — verified code local; remote checkpoint/PR pending.

## Native backend priority — 11 October 2026

The user explicitly superseded the campaign roadmap with an n8n-free backend/workers rebuild. Current branch is `rebuild/python-backend`; the earlier campaign milestone records below/above are historical context. New native product setup, discovery, bounded deeper research, professional contacts, scoring, matching, drafting and pending human approval are implemented locally in `backend/`. PostgreSQL owns stage transitions, leases, workspace boundaries, source snapshots, provider reservations and approvals. See `docs/native-preparation-workers.md` and `docs/native-worker-migration-plan.md`.

Acceptance: 30 PostgreSQL tests with synthetic providers, including six companies across two unrelated catalogs and the actual restricted worker DB role; running restricted-role HTTP API/worker smoke test also passes without provider calls. These results do not establish live provider quality. Native migrations are independent of the legacy application.

Next: dashboard integration, encrypted provider connections, authorized live calibration, separate sending parity and controlled data/account/approval migration with one-executor ownership and rollback. Existing deployed n8n remains active; no rebuild deployment, provider spend, outbound messages or automatic approval occurred. PRs target develop; production is separate. User-owned .gitignore and docker-compose.yml changes remain outside rebuild commits.

## Frontend handoff — 11 October 2026

User requested a shareable requirements and source-location brief for a separate frontend developer. See [frontend-native-backend-handoff.md](../frontend-native-backend-handoff.md) and [OpenAPI snapshot](../contracts/native-backend-openapi.json). The handoff maps native screen requirements, roles, request/result contracts, UI states, existing design references and missing backend support. OpenAPI was exported from the running native API; untyped responses still require the documented/source response map. Implementation checkpoint721a44f and the handoff are being published together as the next PR targeting develop; the foundation was already merged in PR #28. No frontend implementation or executor cutover occurred. The replacement backend remains an independent runtime, not the currently deployed executor.

## Native frontend backend support — 11 October 2026

Implemented BE-01–BE-06 locally on rebuild/native-frontend-support, based on merged PR #29. See ../native-frontend-backend-support.md for new typed contracts/auth capabilities, direct/paginated leads, immutable human revision and separate reviewer, soft catalog lifecycle/versioning, partial setup semantics and frontend adapter requirements. The now-removed compose.native-integration.yml was used for historical restricted API/DB/worker checks with the frontend owner's read-only native UI. Synthetic external providers only; worker-loop discovery scheduling gap fixed.

Verification: 37 PostgreSQL tests passed; actual API/BFF/worker two-product/contact/failure/retry/role/isolation checks passed; actual headless Edge product-form/preparation/review/approval and tablet/mobile checks passed; actual restricted API revision/lifecycle checks passed. Windows Docker forwarding remains defective, with a tested localhost-only gateway fallback at8095; frontend-to-API internal networking works. No frontend-owned files, deployed executor, paid providers or sending changed. New BFF allowlists/adapters and nonzero unavailable-search count rendering remain frontend-owner work. BE-07–11 and shared production sessions remain later milestones. New changes local, not pushed/deployed; PR base develop.


## Real DEV discovery diagnosis � 11 October 2026

User-authorized real discovery test completed against the deployed legacy DEV application through an SSH loopback forward. Shared n8n discovery was patched for visible HTML punctuation, explicit all-candidate evidence rejection and literal-node provider usage collection. A real Soon Lee Transport lead was accepted and rendered; research was queued automatically. All 73 n8n JavaScript tests pass. See ../dev-discovery-acceptance.md. Existing native rebuild remains a separate runtime; no app deployment, sending or cutover performed. Local follow-up branch fix/dev-discovery-evidence; native frontend support fd6c5a3 was previously pushed. PR base remains develop.

## DEV login recovery — 11 October 2026

Current work: fix/login-session-recovery, based on develop8c62de7 (user merged/deployed PR32). Stale login POSTs previously returned a bare403 and reloading repeated the invalid submission. Login now redirects303 to a fresh GET form; invalid/missing CSRF cannot reach the account API. A dedicated host-only marketing_dashboard_session cookie prevents generic-session conflicts; existing users sign in once. Initial browser mismatch cause remains unconfirmed. Public DEV GETs returned stable fresh tokens, no-store and Cloudflare DYNAMIC. See ../dashboard-login-recovery.md.

Local acceptance: ten synthetic HTTP session/login regressions, eight campaign dashboard, eight research presentation and five UX tests pass. CI includes the new login suite. User-owned .gitignore/docker-compose.yml edits are preserved. DEV deployment is authorized by the user's existing request; production and outbound sending remain outside scope. Remote CI/deployment acceptance is pending.

### DEV release acceptance — 11 October 2026, 13:23 UTC

DONE: login fix d740ed04080ae2cfb5e6900c4fe5beef7057adae deployed to DEV through successful deployment run38142917502 (https://github.com/geekedctrl/lorrysystem-deploy/actions/runs/38142917502). Both code CI runs passed: push38142704887 and PR38142725972. Public HTTPS verification passed for the dedicated cookie, invalid-token recovery to GET, actual admin sign-in/dashboard rendering and logout of the test-owned session. Cookie/password values were not logged; the temporary private verification script was deleted. Initial browser mismatch remains unconfirmed, but the reload trap is reproduced and corrected.

PR33 targets develop: https://github.com/geekedctrl/lorrysystem-marketing-system/pull/33. It remains open for the user's merge; deployment already contains the code fix. This completion record is a documentation-only follow-up. Production, accounts/passwords/keys, n8n and outbound sending were unchanged. User-owned local compose/gitignore hashes match their original values. Users should open https://dashboard-dev.obsidian.cam/login directly and sign in with the fresh form; the new cookie requires one sign-in.

## Recurring DEV session mismatch — 11 October 2026

User still sees /login?notice=session-expired on the repaired DEV runtime. Reproduced a concurrent session overwrite: hold a static response until after login and new-form generation; Starlette's unchanged-session Set-Cookie restores the old anonymous cookie and rejects the new token. Sequential verification had missed this. StableSessionMiddleware now suppresses only unchanged dashboard cookie writes, retaining signed mutation/expiry/logout behavior. Missing cookies have an actionable message; logs record only rejection reason categories. Whether this race caused the user's browser request is not yet confirmed.

Local acceptance:13 login/session HTTP tests (including a regression that failed before the fix, delayed static response, expiry, read-only cookie suppression and security gates),8 campaign dashboard,8 research and5 UX pass. See ../dashboard-login-recovery.md. Existing PR33 against develop will be updated; CI and DEV re-verification pending. User-owned local files preserved. Native frontend and production remain unchanged.

### Stable-session DEV acceptance — 11 October 2026

Code678c5d10ffb06f72458e280ca649d99feebe2a5a passed both complete CI runs38143665891 (push) and38143669343 (PR). DEV deployment38143843825 succeeded: https://github.com/geekedctrl/lorrysystem-deploy/actions/runs/38143843825. Public HTTPS checks passed: no cookie rewrite on unchanged login/static/health/dashboard, stale-token recovery, specific missing-cookie explanation, actual admin sign-in/session retention and test-session logout. All13 controlled HTTP tests also passed against the deployed image, including the delayed-response regression. The temporary private verifier was deleted.

The user has been asked to retry their affected browser. Exact browser-specific root cause remains unconfirmed until that result; the reproduced cookie-overwrite race is corrected and rejection logs now distinguish missing, invalid/expired and mismatched session state without logging sensitive values. PR33 remains open with base develop. No production, provider, outbound-send, account/password/key or user-owned compose/gitignore changes.

## DEV company discovery selection — 11 October 2026

Current branch fix/company-discovery-selection includes the unmerged PR33 session repair to preserve the running DEV baseline. Recent default-query jobs completed with zero companies despite healthy worker/provider activity. A bounded search probe confirmed directory/ranking starvation before a new official company homepage. Shared search now adds official-company wording and safe workspace-memory site exclusions; directories are removed before fetch budgeting and homepages rank first. All-fetch failures are explicit, and managed dashboard polling shows accepted results in All discoveries. Product setup targets observable customer business types. See ../company-discovery-selection.md.

Local acceptance:76 n8n tests,13 login/session checks,8 campaign dashboard and5 UX pass; discovery JS syntax passes. Refined search returns official operator sites. CI, live workflow publication, DEV app release and dashboard batch acceptance pending. User-owned gitignore/compose preserved; production and sending outside scope. New PR base develop; PR33 may be merged first to remove overlapping session changes.

### Exact discovery excerpts — 11 October 2026

Initial corrected default-query batches a1a4bdf0 and ca5f5ec8 reached official KGW/Hock Cheong pages but failed DISCOVERY_EVIDENCE_REJECTED. Diagnostic execution21159 confirmed that the model stitched nonadjacent Hock Cheong passages into one quote. Temporarily enabled child execution saving was restored to none immediately after collection. New extraction selects supplied source/excerpt IDs; the application resolves exact fetched text/URL, while name, identity, ICP, confidence and quotation gates remain. Invalid cross-page/unknown IDs cannot create a lead.79 n8n tests pass. Follow-up CI/publication and final live batch pending; initial search/UI release3066c2e already deployed in DEV through38145264438. PR34 is open against develop and includes PR33 session changes. No production changes or sending.


### Company discovery DEV acceptance — 11 October 2026

Code `8b9d162dfdcc6301404bbbe0060399703a9f213b` passed full push CI `38145984359` and PR CI `38145987247`. DEV deployment [38146226265](https://github.com/geekedctrl/lorrysystem-deploy/actions/runs/38146226265) succeeded. Discovery and setup child workflows were published through the DEV n8n API with existing named credentials and workspace/lease headers preserved; the dispatcher resumed. All three workflows are active with current published versions and execution saving set to `none`.

A normal public-HTTPS admin login and LorrySystem workspace switch submitted the unchanged dashboard default query with a target of one company. Discovery job `960988f3-ffcb-4835-80e3-4084f9b2d07c` completed with `COMPANIES_ACCEPTED`, one new candidate and one accepted lead: **Hock Cheong**, `hockcheong.com.my`, lead `53f3592e-b375-4f7b-bb49-5c46be4d78d2`. A separate normal HTTP session verified the company in `/leads`, its detail page and `/discovered-leads?status=ALL`. Both test sessions logged out. The batch used one search, two fetches and one model call (4,932 input / 137 output tokens); recorded monetary cost is unavailable.

Follow-up research automatically ran and stopped at `NEEDS_REVIEW` / `SUPPORTED_CONTACT_REQUIRED`; discovery succeeded, but outreach preparation is not claimed complete. No outreach was approved or sent. The task-created retained diagnostic execution `21159` and temporary credential-bearing verifiers/raw diagnostic payload were removed after verification. User-owned compose/gitignore contents remain intact. PR [34](https://github.com/geekedctrl/lorrysystem-marketing-system/pull/34) targets `develop` and includes unmerged PR33's session repair to preserve the DEV baseline. Production and native-worker rollout are unchanged.


### Discovery rebuild discussion — 11 October 2026

User correction: discovered companies must await explicit human acceptance; automatic acceptance is no longer the desired policy. Both deployed `api/app/routers/automation.py` candidate ingestion and native `backend/marketing_backend/pipeline.py` discovery finalization currently create official leads automatically and schedule research. Both require revision before claiming manual-review behavior. The preceding successful one-company DEV test proves that one batch worked, not that discovery is broadly reliable.

Discussed direction: native Python discovery workers collect website evidence and use the existing xKiro adapter for catalog/ICP assessment. Reuse the existing queue/workspace/provider infrastructure. Proposed flow: search → bounded company-site crawl/extraction → evidence-backed assessment → candidate inbox → explicit Accept/Reject → accepted lead and research → remaining preparation → human outreach approval. Ordinary HTTP fetching and structured extraction first, browser rendering as a controlled fallback. Candidate-level failures, retryable discovery memory and visible stage counts are proposed reliability work. Search-provider choice and implementation scope remain discussion items; this entry changes documentation only and does not disable running workflows or alter records.


## Native discovery with manual review — 11 October 2026

Implemented on rebuild/manual-discovery: Brave website finding, guarded Python company crawling, Trafilatura extraction, optional guarded Playwright rendering and per-company xKiro assessments with numbered evidence excerpts. Discovery persists review candidates only. Explicit human Accept creates the lead/research run atomically and idempotently; Reject preserves the decision; targeted Reassess and retryable memory cover unavailable companies. Workspace RLS, catalog staleness, concurrent domain duplicate checks and native-worker lead INSERT denial guard the transition. Native dashboard/BFF adds candidate review, evidence, filters/paging and stage counts. Legacy ingestion, contract/export and summaries now also require human acceptance in source. See ../native-lead-discovery.md and the refreshed OpenAPI.

Acceptance: 50 PostgreSQL/backend tests, including actual Chromium network isolation, empty JavaScript shells and malformed links; nine BFF groups and the synthetic browser; actual local browser/product form/BFF/restricted API/native worker manual acceptance; actual two-product native API/worker acceptance; legacy shared automation regression; 79 n8n checks; 13 login/session and five UX checks. Providers are synthetic. Local disposable projects discovery-review-test and discovery-legacy-test isolate fixtures. Live provider calibration/native DEV cutover and coordinated legacy n8n publication remain release work; no deployed executor changed and no outbound messages sent. Existing PR #33/#34 are now merged; latest develop `9e74818` adds separate frontend CSS. Preserve user-owned gitignore/compose; PR base develop.


Release checkpoint: implementation commit `bec7684`, integrated latest develop `9e74818` with merge `cf90bb9`; pushed branch `rebuild/manual-discovery`. Draft PR #36 targets develop: https://github.com/geekedctrl/lorrysystem-marketing-system/pull/36 . Keep draft until coordinated legacy guard/API publication or native cutover is ready; DEV has not been changed. GitHub CI is running. Local fixture projects `discovery-review-test` and `discovery-legacy-test`, their disposable volumes and the port 8098 gateway were removed after verification; pre-existing local stacks remain untouched. User-owned root compose/gitignore hashes remain unchanged and those edits are excluded.

## Native DEV rollout checkpoint - 12 October 2026

Implementation branch: geekedctrl/native-dev-cutover. Native API, worker, isolated PostgreSQL and single-process native dashboard are wired in Compose and CI alongside legacy DEV. Images build; a fresh disposable DB migrated; API/dashboard Docker health passed; dashboard-to-API networking returned HTTP 200. No provider calls, server changes, production changes, push, PR or data migration occurred. DietPi helper still builds/starts only legacy API/dashboard; add native migration, services and health checks before rollout. Three server DB passwords are required for Compose preflight. Compose include requires v2.20.3+. Keep n8n and legacy DEV until human-reviewed native acceptance and rollback gates pass. See docs/native-dev-cutover.md and docs/ai/TASK_BOARD.md.

## Local Parallel contact discovery — 4 November 2026

The isolated `feature/parallel-contact-discovery` worktree adds a bounded Parallel Entity Search and source searches for the CONTACT_SEARCH stage. Results are review suggestions, not verified employment; only an exact person, role and company excerpt on the accepted company's own domain is offered for selection. Unsupported results retain search excerpts for review. No email is inferred. Older contact artifacts remain readable; new product-line contact artifacts use version 3. The local Pos Logistics job completed with five unverified suggestions and remains at SUPPORTED_CONTACT_REQUIRED. One Entity Search and five searches succeeded (estimated $0.010); one model request was rejected (reservation $0.010; actual provider charge not confirmed). The role model step was removed after the rejection and saved search checkpoints were reused. No outreach was sent.

Local runtime note: the updated API and dashboard files were copied into the existing local containers; `parallel-local-contact-discovery` runs the updated contact worker image using the existing local worker configuration. These container changes are not a reproducible Compose release and will need the worktree changes integrated into the source checkout and images rebuilt. The original checkout's pre-existing edits remain untouched. Synthetic contact discovery/evidence/provider tests, the 25-test native pipeline, product-line tests, restricted worker-pool tests and JavaScript syntax check passed; live account billing was not verified.

## Contact pool follow-up — 4 November 2026

Matching now includes the accepted website and country, ranks entity results before source searches, and uses candidate-specific checkpoint keys. Independent sources may support a suggestion only when the excerpt explicitly identifies the accepted company website as well as the person, role and company; a profile alone is not employment proof. Evidence remains for human review. Uncertain Parallel calls block both automatic and manual retries, including older failed jobs with unresolved usage records. Version 1/2 contact payloads remain readable; version 3 carries suggestions.

The local API, dashboard and CONTACT_SEARCH pool were rebuilt with Compose from this isolated checkout under project `parallel-local-test`, using its ignored `.env.local`. A forced recreation of the contact worker reconnected to the existing local database. The existing Pos Logistics result was retained; the revised matching has not been rerun against that real company. Recreating the process-local dashboard cleared local browser sessions. No outreach was sent. Actual account billing remains unverified: Parallel's usage API requires an organization-admin OAuth token with `usage:read`; the runtime API key alone is not that token.

Verification: 78 synthetic backend tests passed, plus seven targeted tests after the final retry gate; 13 BFF checks and actual headless browser acceptance passed, including selecting a synthetic supported suggestion without email while keeping review open. Browser and backend fixtures were synthetic. For the local stack, from this checkout use `docker compose --env-file .env.local -p parallel-local-test -f compose.backend.yml -f compose.worker-pools.yml up -d --no-deps --build backend-api dashboard-dev backend-contacts`; do not commit the ignored credentials file.

### Pos Logistics revised matching check — 4 November 2026

After user sign-in, retried the existing local contact job through the dashboard. The Compose CONTACT_SEARCH pool completed one Entity Search and five source searches. The five returned suggestions are Malaysia/Pos Logistics Berhad-oriented; one is marked SUPPORTED: Siti Maryam Md Salleh, Head of People, cited to the company's leadership page. The same saved public excerpt lists Abdul Rahim Ali as Head of Operations, but he was not among this entity-search batch's suggestions. The other four suggestions remain UNVERIFIED, no email was inferred and no contact was selected. The run remains NEEDS_REVIEW / SUPPORTED_CONTACT_REQUIRED. No outreach sent. Billing was deliberately not investigated at the user's request.

## Official-page contact extraction — 4 November 2026

The contact worker now extracts adjacent name/role bullets from saved official leadership pages, ranks operations/fleet/logistics roles ahead of unrelated roles, flags ended or conflicting roles, and requires an explicit name/role pairing for source support. It leaves suggestions for human selection and does not infer email. The local Pos Logistics retry reprocessed saved Parallel checkpoints without new provider calls and placed ABDUL RAHIM ALI, HEAD OF OPERATIONS, first as a sourced suggestion from the company leadership page. The run remains NEEDS_REVIEW and no contact was selected. The final stricter pairing guard was separately tested against the same saved source excerpt; the worker image was rebuilt afterward.

Synthetic verification: 38 native-pipeline/contact tests passed before the final evidence guard; 12 focused tests passed after it, followed by the contact helper tests. Orca review planned the entire dirty worktree, including earlier unrelated Parallel preparation; the review was submitted as partial and rejected as unusable because that full scope has not been reviewed. It is not a merge-readiness pass. No merge or push occurred.

## Operator review of unverified contacts — 4 November 2026

Added an ADMIN/OPERATOR review action for unverified contact suggestions. The operator can keep one for further review, reject it, or leave it unresolved with a required note. The suggestion stays UNVERIFIED; reviewer identity, time and decision are retained in job history and, for versioned runs, a new immutable contact artifact. A name-and-URL check rejects stale indexed submissions. No primary contact, channel, scoring job, approval or outreach is created. The local API and dashboard were rebuilt from the isolated Compose checkout; dashboard process-local sessions were cleared. Synthetic PostgreSQL permission/isolation and artifact tests passed, as did BFF checks and headless browser acceptance. Earlier full-worktree Orca review remains partial; no merge or push occurred.

## Native operations console redesign — 5 November 2026

Worktree `C:/Projects/marketing-ui-redesign`, branch `feature/native-operations-console`, starts at `b7c6b8d` and contains a file-for-file copy of the uncommitted Parallel contact-discovery worktree as its baseline. The original worktrees were not changed. This is an uncommitted combined diff; compare against `C:/Projects/marketing-contact-discovery` to isolate redesign changes before integration.

The first pass replaces the green decorative treatment with neutral graphite surfaces and teal action/state accents, tightens shell and overview presentation, and reduces prominence of reassessment relative to acceptance. Existing request handlers and review gates are retained. The synthetic browser fixture now checks the full name/URL/index contact-selection payload. Thirteen BFF tests and the synthetic browser journey passed, including roles, stale refusal, contact continuation, responsive widths and keyboard checks. Screenshots are in `tmp/native-ui-review` (synthetic data). The browser upstream was mocked; real API/database/worker acceptance, full accessibility audit and broader redesign of individual workflows remain outstanding. The earlier Parallel review and backend suite failures remain unresolved. No paid calls, deployment or outreach were performed.

## Native dashboard redesign continuation — 5 November 2026

The isolated `feature/native-operations-console` worktree now uses a non-green blue accent on graphite, with revised shell, overview, evidence-first discovery, lead review, setup progress, draft decision layout, operations and delivery styling. Lead tabs retain keyboard focus; contact review without a channel remains marked as needing review. The overview status bars use native progress elements (CSP blocks inline widths). Background polling is deferred while evidence is open or a control is focused so it cannot erase an operator's review; it retries afterward.

Verification: synthetic BFF 13/13 and browser acceptance pass (including new polling/evidence preservation, stale selection, keyboard, 780px navigation, role/isolation and responsive checks); four Node UX suites pass. Backend disposable PostgreSQL suite passed 250 tests, one Chromium-specific skip. The synthetic real API/BFF/DB/restricted-worker HTTP acceptance passed after adding a guarded synthetic Parallel identity fixture. Browser viewing through the actual stack passed overview, lead, research and approval screens; the full real-service browser action journey is still under development by the bounded worker and is not a pass. Axe WCAG A/AA scans of seven main sections in light and dark themes had no automated violations at the last scan, but those scans predate the final polling change and do not replace manual screen-reader testing. The previously incomplete Orca review of the Parallel baseline remains incomplete; no release readiness is claimed. User-provided Dribbble reference was available as a text description, but direct visual retrieval did not succeed; visual similarity has not been verified against its image.

Local preview at localhost:8099 uses synthetic fixture responses. Disposable real-service stack `ui-redesign-acceptance2` and localhost gateway 8105 remain running for verification; no real provider or sending calls. Original worktrees and Pos Logistics database were not modified. Further work: complete the real-service browser action journey, finish visual and accessibility QA across all screens and states, update preview/screenshots and repeat relevant tests; then audit the entire objective before marking complete.

### Redesign verification continuation

The current synthetic dashboard suite passed again after the mobile navigation and scroll-region accessibility changes: 13 BFF checks, browser workflow and workspace-creation acceptance, plus the four Node UX suites. Automated mobile axe scans of seven sections in both themes reported no violations; these do not replace assistive-technology testing. Screenshots using synthetic data are in `tmp/native-ui-review`. A repeatable local-only preview launcher is `dashboard/scripts/native_synthetic_preview.py`; with dashboard dependencies installed, run it and visit http://127.0.0.1:8099, signing in as admin@example.com with synthetic. The preview uses in-memory mock responses. The Windows default Python installation failed at startup; a separate Python 3.13 environment under ignored `tmp/redesign-venv` was used for the latest dashboard checks.

The synthetic real-service browser journey subsequently passed against the disposable acceptance2 stack: a fresh workspace completed setup and discovery through the restricted synthetic worker, the candidate stayed out of leads until accepted, preparation reached pending approval, a separate reviewer saw the draft, and an outsider received the BFF's exact 409 workspace-change denial without lead data. The fixture explicitly routes only its new disposable workspace to Python and grants the synthetic reviewer membership; it does not change application defaults. No approval or message was sent. This does not complete the earlier full Orca review of the combined Parallel baseline, nor does automated accessibility scanning replace manual assistive-technology testing.

### Accessibility and review follow-up

The overview now uses correct singular count labels; the workspace loading message has status semantics and the lead tab panel is keyboard focusable. Following these changes, dashboard browser/BFF and four Node UX checks passed. Axe WCAG 2/2.1 A/AA scans found no automated violations in the seven main sections at desktop and 390px mobile widths, in both themes. This is not manual screen-reader verification. A local Orca submit produced a clean report, but its reviewer subsequently confirmed truncated review output and incomplete inspection of selected files; the report is not a complete review or merge-readiness pass. Full review of the combined Parallel baseline remains outstanding unless superseded by a complete later review.

### Full local Orca review

A subsequent bounded review covered all 40 files selected by Orca, including the untracked source and scripts; submit reported no P0/P1 and one P2 on contact evidence-search failures aborting the stage. The earlier clean report was incomplete and is superseded. The proposed broad catch is unsafe for Parallel transport or server errors: their reservations can be UNCERTAIN and must reach queue reconciliation. A definite 429 rejection may be handled differently, but deciding how to preserve partial results without issuing further calls or losing a safe retry remains follow-up work; the current fail-closed behavior is retained. Orca excludes the environment example and ai handoff documents. No merge or deployment has been authorized.

Final dashboard browser regression passed after adding an explicit assertion that the lead tab panel is keyboard-focusable and labelled by its selected tab. The final local result remains a combined, uncommitted redesign and contact-discovery worktree for human review. Manual screen-reader testing and visual comparison to the actual Dribbble image remain limitations; the reference image itself could not be retrieved. The local Orca P2 concerns underlying Parallel rate-limit behavior and is not resolved by the UI redesign.

## Integration checkout verification — 5 November 2026

`C:/Projects/marketing-local-integration` is an uncommitted copy of the UI worktree plus the Parallel handoff and Figma recovery reference. The contact checkout matches that UI baseline except for the UI's synthetic identity fixture, native JavaScript, browser fixture, and additional handoff entries. The identity fixture and BFF fixture differences were inspected; the UI fixture adds guarded synthetic identity and current stale-selection payload assertions. Original Parallel files differ in overlapping areas; inspection to date confirms additional entity-search, contact artifact compatibility and fail-closed recovery behavior, but the complete hunk-by-hunk reconciliation remains pending. Earlier merge-file output is exploratory only and is not a merge result.

Current integration checkout: 13 BFF tests passed, synthetic browser acceptance passed (including stale refusal, workspace isolation, responsive and keyboard checks), and four Node UX suites passed. Backend focused pytest invocation could not run because the existing dashboard environment does not have pytest installed. No actual backend/database/worker journey was run against this checkout, and prior results from other worktrees do not establish that result. Full Parallel Orca review retains its documented P2 and is not a clean release gate. No provider calls, outreach, push, merge or deployment.

## Integration PostgreSQL verification

Fresh disposable PostgreSQL migrated to head. Focused offline contact/evidence/provider/artifact checks passed 39 tests. Pipeline, product-line, worker and discovery checks initially reported 75 passed and four worker failures because WORKER_DB_PASSWORD was omitted from the test container; the worker suite was rerun with the synthetic migration password and all eight passed. Database and its isolated network were removed afterward. No real providers were contacted. The prior BFF/browser checks remain as recorded above. Original Parallel and contact differences are recorded in parallel-change/*reconciliation.diff; dashboard hunk-by-hunk review remains incomplete. No files were applied to the original checkout.

## Dashboard and current-worktree reconciliation

Compared the integration dashboard JavaScript with both contact-discovery and the current Parallel checkout. The contact-specific suggestion review and selection controls, name/URL stale-submission fields, role checks and no-outreach messaging are retained in the integration version. Other differences reorganize discovery decisions, overview summary, evidence presentation, lead navigation, setup and focus behavior; the integrated synthetic browser checks exercised these flows. The Parallel-only dashboard has no contact-suggestion controls; those were added in contact discovery and preserved in integration. Migration 019 and test_parallel_search.py match the current checkout ignoring line endings. The current checkout remains the Parallel-only dirty baseline; the integrated checkout is the combined result, and the saved comparison files show its differences. This is not a complete review of every backend behavior or proof of live provider behavior. Existing Orca P2 and real-API browser verification in this integration checkout remain open.

## Current checkout local rebuild — 5 November 2026

Removed the isolated contact-verification database container after confirming it was alone on its network; its volume remains. Backed up the parallel-local-test database to C:/Projects/marketing-system-recovery-20261105/database/parallel-pre-rebuild.dump and verified archive listing. Rebuilt the existing API, worker, discovery, contacts, scheduler, dashboard and migration images from C:/Projects/marketing-system, migrated successfully and recreated those services against the same database volume. Provider API keys were cleared and notifications disabled via C:/Projects/marketing-system-recovery-20261105/parallel-safe-rebuild.env; the original credentials remain in the archived prior configuration. API and dashboard health returned HTTP 200; the database, API, dashboard and four worker/scheduler services reported healthy. Pos Logistics still has its NEEDS_REVIEW / SUPPORTED_CONTACT_REQUIRED run and no pending/running/retry jobs were found. Health checks are not a full application journey. No provider searches or outreach were initiated.

## Local data reset — 5 November 2026

At the user's explicit request, stopped worker pools and cleared leads, jobs, preparation runs and dependent local records. This also cleared 71 linked provider-usage rows from the active database; they remain in the pre-reset backup C:/Projects/marketing-system-recovery-20261105/database/parallel-pre-rebuild.dump. Verified zero leads, jobs and preparation runs, while one account and one workspace remain. Worker pools were restarted with provider credentials still disabled. Do not enable paid provider calls until prior usage has been reconciled into spending controls: the active ledger no longer reflects earlier spend. No outreach or paid calls were initiated.

## Provider configuration restored — 5 November 2026

At user request, restored archived Parallel, model and Brave keys into the local worker containers; provider values were checked for presence only. API and dashboard health passed; jobs remain at zero. Scheduler is stopped to prevent autonomous scheduling while the active usage ledger is empty and no further paid searches are authorized. The user's Parallel export contains three rows for the single UTC day 2026-11-04: search $0.025, entity search $0.010 and responses $0.170, totaling $0.205. It does not establish full-month or other-provider spend and was not imported into the ledger. Notifications remain disabled because the archived configuration has no server URL or topic. Reconcile historical reservations and monthly totals before relying on budget controls.

## Public contact evidence work in progress

Added a conservative helper for literal public email candidates, retaining the source URL, excerpt, observation time and unverified status; eight contact-evidence unit tests pass without network access. It is not yet connected to a provider search, persisted artifacts, API selection or dashboard, and it does not unblock Pos Logistics. Source co-occurrence is not proof of ownership; the remaining workflow must preserve manual review, conflict/staleness handling, workspace isolation, durable reservations and the separate sending gate. No paid search or outreach was performed.

## Public email discovery connection — work in progress

Connected literal public-email extraction to the existing synthetic contact-search evidence results and the version 3 contact suggestion contracts. Candidates carry source, excerpt, observation time and an explicit unverified status; they are not automatically selected. Thirty-three offline contact, evidence and artifact-contract tests pass. The operator selection API, dashboard review, stale-candidate protection and complete disposable-database journey are not yet implemented; do not use this partial change for live contact resolution. Existing running containers have not been rebuilt. No paid searches or outreach were performed.

## Public email candidate review — 5 November 2026

Existing Parallel-backed contact-evidence search now asks for public business email and extracts literal candidates only from safe matching excerpts. Suggestions preserve candidate URL, excerpt, observation time and PUBLICLY_SOURCED_UNVERIFIED status in version 3 artifacts. The dashboard shows that evidence and requires an explicit selection. API checks workspace role, current run/context, suggestion identity, email value and source; older versioned contact artifacts reject the new selection so evidence is not lost. Selection can resume preparation but is not verification, approval or sending. Results may be false matches and require human review.

Synthetic validation: 64 contact, contract and PostgreSQL pipeline tests passed; a separate versioned-artifact selection test passed; 13 BFF tests, synthetic browser acceptance including candidate selection, and four Node UX checks passed. The browser fixture mocks the API; the PostgreSQL API test runs separately, so this is not a full real API/worker/browser journey. Rebuilt local API, dashboard, research worker and contact worker from this checkout; API and dashboard health returned 200. Pos Logistics remains NEEDS_REVIEW/SUPPORTED_CONTACT_REQUIRED because its existing saved search has no email candidates. No new paid search or outreach was initiated. Scheduler remains stopped and the cleared historical provider ledger still requires reconciliation before spending controls can reflect previous usage.

## Contact search retry cache correction

The Pos Logistics retry reused cached Parallel checkpoints from the earlier contact search and did not make new email-oriented searches. Contact evidence operations now include an explicit query version and retry generation, stable across a worker restart but distinct across deliberate retries. Retry refuses unresolved or uncheckpointed Parallel reservations and is limited to three generations. The dashboard warns that retrying may incur charges. Synthetic contact and pipeline checks: 46 passed, plus two targeted retry/reconciliation checks; 13 dashboard gateway tests and the synthetic browser journey passed. Rebuilt API, contact worker and dashboard; both health endpoints returned 200. Pos Logistics remains NEEDS_REVIEW with no queued jobs. No paid search was initiated by this correction; the historical usage ledger still requires reconciliation.

## Selected contact email search correction

Inspection of the latest Pos Logistics retries showed ten successful Parallel evidence-search requests across two generations, but Abdul Rahim Ali was sourced from the company leadership page after Parallel's five entity candidates were searched. Consequently, neither retry targeted his name specifically. A deliberate retry now also searches for the previously selected supported person using a generation-scoped checkpoint and records only literal matching excerpts as unverified candidates. It does not infer an email or automatically select one. Sixteen offline synthetic contact/evidence checks passed; the contact worker was rebuilt locally. No additional paid search was initiated by this change. The existing run remains in review; an operator-triggered retry can incur charges and is subject to the existing generation limit and unresolved-request guard. Previous provider usage remains unreconciled.

## Claude Code backend handoff — 8 November 2026

Primary checkout: C:/Projects/marketing-system, branch checkpoint/parallel-ai-preparation, HEAD b7c6b8d; substantial backend, dashboard, tests and documentation changes remain uncommitted. Source and current test runs take precedence over older entries above. Native backend lives in backend/marketing_backend; API endpoints are in api.py, discovery_api.py and native_api.py, workers in worker.py and stages.py, and durable provider reservations in providers.py and queue.py. Contact evidence search, explicit human selection and retry safeguards are local changes and need complete real-API/browser validation; the documented Orca P2 remains open. Do not infer email addresses, automatically approve or send, deploy, or run paid providers without authorization.

Docker project parallel-local-test was last stopped at user request. Its database volume is preserved. Provider config and the pre-reset database backup have copies under ignored tmp/cleanup-preserved; these include sensitive credentials and historical data. The active usage ledger was cleared and prior spend must be reconciled before its budget totals are trustworthy. Docker compose references to C:/Projects/marketing-system-recovery-20261105/parallel-enabled.env in earlier entries should be replaced with tmp/cleanup-preserved/parallel-enabled.env. Figma reference is under design-reference/. Five redundant local branches were removed; backup/project-state-2026-11-01 and develop remain. Folder deletion was rejected by automatic command review; the original recovery and archive folders remain.

Prior synthetic verification: 64 contact/contract/pipeline tests, versioned artifact selection, 13 dashboard BFF checks, browser fixture and four Node suites passed; the browser uses a mocked API. Later targeted selected-person contact evidence checks passed (16). A full real API/worker/browser journey and historical budget reconciliation remain open.

## Orca advisory fixes — 8 November 2026

A definitively rejected, rate-limited contact search now preserves already collected and official-page suggestions, reports the search as unavailable and stops further searches for that attempt. Uncertain transport/server failures still propagate for paid-request reconciliation. The dashboard retains pending refresh data and displays a status notice while open evidence or focus prevents replacing visible controls; it refreshes after the operator closes details and moves focus out. Synthetic checks: 37 offline contact/evidence/contract tests and 13 BFF tests passed; the mocked-API browser journey passed with a new stale-notice/refresh assertion. No real provider calls or outreach. The full Orca report has not been rerun against these changes.
