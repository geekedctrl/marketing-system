# Backend handoff for Claude Code

## Ownership and starting point

Work in `C:/Projects/marketing-system`, branch `checkpoint/parallel-ai-preparation`, HEAD `b7c6b8d`. The working tree contains substantial uncommitted backend, UI, test and documentation changes; inspect `git status` and preserve them. Read `AGENTS.md`, `docs/ai/HANDOFF.md`, `docs/ai/PROJECT_STATE.md`, and `docs/ai/TASK_BOARD.md`. Source and fresh test results override older handoff entries. Claude owns backend changes; coordinate shared API contract changes with the frontend owner. Codex will implement the frontend using the Figma reference and owns dashboard files unless explicitly agreed otherwise.

## Architecture and current behavior

The native Python backend is in `backend/marketing_backend/`: `api.py`, `native_api.py` and `discovery_api.py` provide APIs; `pipeline.py`, `worker.py`, `queue.py` and `stages.py` orchestrate durable preparation; `providers.py` handles reservations and providers; `contact_evidence.py` handles conservative contact evidence. Migrations are under `backend/migrations/versions/`. Read `parallel-change/contact-discovery-handoff.md` for history, noting later updates below supersede older statements.

Parallel-backed discovery and contact search, contact artifacts v3 and operator review are present locally. Suggestions remain unverified unless supported by evidence; support is not proof of current employment. Public-email candidates keep an excerpt, URL, observation time and unverified label. An authorized operator explicitly selects a candidate; selection can resume preparation but is not an approval or a send. Preserve role checks, workspace isolation, stale-submission checks, immutable artifacts, uncertain-request reconciliation and separate sending authorization. Never infer email addresses or treat third-party snippets as verified identity.

The selected-person email-search correction is implemented but has only focused synthetic testing: prior retries searched entity candidates but skipped a person added from the official page. Retry now targets the previously selected supported person with a generation-scoped checkpoint. Check current code and results before changing it. Pos Logistics was last left at NEEDS_REVIEW / SUPPORTED_CONTACT_REQUIRED; do not assume its current database state without inspecting it.

## Priority work and known limitations

1. Reconcile the provider spending ledger before trusting or using budget controls. The user explicitly cleared local leads and jobs, which also cleared 71 linked provider-usage rows. A pre-reset database backup is at ignored `tmp/cleanup-preserved/parallel-pre-rebuild.dump`; treat it as sensitive. The Parallel export under the user's Downloads covered only 2026-11-04 UTC and totaled $0.205, not the full monthly or cross-provider total. Preserve uncertain reservations and avoid duplicate paid calls.
2. Review and verify the full contact-email journey against a disposable PostgreSQL database, real API and restricted worker with synthetic providers, including workspace and viewer denial, stale submissions, source mismatch, conflicting/stale roles, artifact v1-v3 compatibility, uncertain calls and retry/restart behavior. Exercise browser/BFF integration separately; prior browser coverage used a mocked API. Review selected-person matching for false associations and verify provenance remains visible after selection.
3. Complete review of the entire intended diff. Prior Orca review documented a P2 around contact evidence-search failure handling; do not broadly catch uncertain paid-request failures. Evaluate the finding and document any unresolved limitation.
4. Coordinate backend contracts and state semantics with the Figma frontend. Avoid editing frontend-owned files without coordinating; the editable design reference and brief are in `design-reference/` (the copied `.fig` has not been reimport-tested, and cloud sync was previously unverified).

## Verification and local operation

Prior checks reported 64 synthetic contact/contract/PostgreSQL pipeline tests, a versioned-artifact selection test, 13 BFF tests and a synthetic browser journey; later retry checks reported 46 backend tests plus two targeted retry guards and 16 selected-person evidence checks. These are historical results, not proof of current behavior. Use disposable databases and synthetic providers; do not use the local real-data database for tests.

The local Docker project is `parallel-local-test`, last stopped at the user's request. Its volume is preserved. Configuration copies are under ignored `tmp/cleanup-preserved/parallel-enabled.env` and `parallel-safe-rebuild.env`; do not print or commit credentials. The scheduler was deliberately stopped, and the historical ledger is incomplete. Do not start paid searches, send messages, deploy, push or merge without explicit authorization. Approval is separate from sending.

## Workspace cleanup status

Five redundant local branches were removed. The active branch, `develop`, and `backup/project-state-2026-11-01` remain. The recovery/archive/dependency folders under `C:/Projects` remain because automatic command review rejected recursive deletion. Do not assume they were removed. A copy of the earlier Orca review and the local database backup was retained under ignored `tmp/cleanup-preserved`.

## Update: Orca advisory fixes

The earlier rate-limit and stale dashboard findings were addressed locally: definite contact-search 429s retain available suggestions and stop further search attempts; uncertain provider calls still fail closed. The dashboard warns while visible status is held during active review and refreshes after details close and focus leaves. See `docs/ai/HANDOFF.md` for synthetic validation. Rerun a full Orca review and real API/worker/browser verification; prior reports predate these fixes.
