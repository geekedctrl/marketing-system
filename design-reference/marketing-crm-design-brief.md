# Marketing CRM: feature inventory and UX requirements

Baseline: local `develop` at `9ff05c38c3d0afe13238f512b4172a2523f958e2`, inspected 5 November 2026. This document describes the native application and its contracts; later dirty Parallel/contact-discovery worktrees are not part of that baseline. Source overrides older handoffs. No frontend implementation is implied by this design.

## Product and design direction

- Product: a workspace-scoped tool for operators to discover companies, prepare evidence-backed outreach and obtain human decisions.
- Character: precise, calm, accountable.
- World: an analyst's working desk: structured records, source annotations and clear decision trails.
- Moments: the candidate-to-lead decision and the evidence-to-draft review, where provenance and uncertainty are visible beside the action.
- Signature: a compact evidence/decision rail that connects each proposed action to its source and current review state.

Light-first neutral surfaces, restrained blue ink, accessible semantic states, compact typography and consistent 4px spacing. The direction follows Damir Sokolovsky's [Unslop](https://github.com/heydamir/unslop) discipline; it is not a copy of the present interface or reference products. Interaction inspiration: [Linear filters](https://linear.app/docs/filters) and [Attio views](https://attio.com/help/reference/managing-your-data/views/filter-and-sort-views); their saved views and advanced filters are not assumed to exist here.

## Implemented baseline

| Domain | Available behavior and constraints | Source |
| --- | --- | --- |
| Workspace | Authenticated memberships scope records and actions; product context and catalog affect preparation. | `backend/marketing_backend/auth.py`, `models.py`, `product_lines.py` |
| Discovery | List and inspect candidates; authorized people explicitly accept, reject or retry. Acceptance creates a lead and begins research; stale targeting/evidence is checked. | `discovery_api.py`, `pipeline.py` |
| Leads | Company name, website and workspace identity; server-paged lead list, search and current preparation status. Individual lead and preparation history. | `models.py`, `native_api.py`, `contracts.py` |
| Preparation | Setup → discovery → research → contact search → scoring → product matching → drafting. Jobs have state, attempts, events and failure codes; runs can stop for review, fail, become stale or await approval. | `pools.py`, `models.py`, `pipeline.py` |
| Evidence and contacts | Research and contact artifacts expose source citations and supported selection. Contact selection and a preparation step are separate decisions. Do not infer email addresses or claim that a source verifies current employment. | `native_api.py`, `stages.py`, `contracts.py` |
| Draft review | Draft snapshot, evidence and approval decisions; approval does not send. Revised drafts require a separate reviewer where applicable. | `native_api.py`, `models.py`, `dashboard/app/native.py` |
| Delivery | Sender configuration, suppression records, delivery snapshots, separate send authorization, attempts and history; social/messaging implementations are synthetic-only. | `sending_api.py`, `channels.py`, `models.py` |
| Operations | Automation status, jobs, stalled work, leases and recent provider reservations. Reservation estimates are not invoices or budget balances. | `native_api.py`, `contracts.py` |

## Roles and guardrails

Workspace membership is required for reads. ADMIN manages settings and can decide approvals; OPERATOR can run discovery/preparation and revise drafts; REVIEWER can review candidates and decide approvals; VIEWER is read-only. Exact per-endpoint checks are authoritative, including separate send authorization (`dashboard/app/native.py`, `auth.py`, `discovery_api.py`, `sending_api.py`). A review does not itself verify a person, select a contact or send a message. A stale submission must fail with context and a route back to current evidence. Different workspace data must never appear during or after switching.

## Metrics and feasibility

Available snapshots include lead total, current run status, pending drafts, current jobs and recent reservation records. Define each number's workspace, date/snapshot scope and any cap; do not present a capped list as a full population. Historical acquisition trends, conversion, revenue, replies, win rate and attribution lack confirmed aggregate contracts and must be marked future/needs backend work, not presented as operational facts. The native model does not provide an inbound conversation inbox, assignment, outcome attribution or CRM sync; milestone E remains backlog (`docs/ai/ROADMAP.md`, `TASK_BOARD.md`). Saved views, arbitrary sort, column configuration, bulk mutation and global search require explicit contract work unless a later source proves otherwise.

## UX requirements and proposed architecture

1. **Home:** actionable queue and truthful snapshot, with definitions and limited-data states; no invented trend charts.
2. **Discover:** candidate inbox with source, uncertainty, stale state and explicit accept/reject; acceptance is a meaningful transition, not a bulk shortcut.
3. **Companies:** searchable/paged workspace records; drill into a company dossier with evidence, contacts, qualification, product fit, draft and run history in context. Advanced filters, sort, saved views, columns and bulk actions are design opportunities requiring backend support.
4. **Review:** draft decision queue with side-by-side snapshot and supporting evidence; separate drafting, approval and delivery authorization.
5. **Operations:** current jobs, automation health, retries and reconciliation; make potentially paid actions and uncertain request outcomes clear.
6. **Workspace:** catalog, product setup, integrations and access; expose only actions permitted by role and the baseline contracts.

Use explicit breadcrumbs and predictable browser history, clear workspace context, accessible keyboard focus, non-color-only status, desktop/tablet/mobile layouts, and loading/empty/error/disabled/stale states. Current navigation replaces browser history and settings sections lack durable URLs (`dashboard/app/static/native.js`); the proposal should resolve these interaction problems without claiming they are implemented. Process-local native dashboard sessions are not a multi-worker production session solution (`docs/native-frontend.md`).

## Data relationships and decisions

Workspace → product context/catalog → discovery candidate → accepted company lead → preparation run → stage jobs/artifacts/evidence → draft snapshot → human approval → separate delivery authorization and attempts. A candidate is not an accepted lead. A suggested person is not automatically a verified contact. Research and scoring are tied to a run/context; later changes can make them stale. Delivery status is not proof of a prospect reply or conversion.

## Figma working file and current progress

Editable file: https://www.figma.com/design/ao0lL5hxuh5uongz2VC68P — selected team: Karthikean Pathmanathan's team. The file has nine named sections, light-first token variables, an initial component set, desktop overview, companies, company intelligence, discovery review, draft review and people/evidence, mobile overview and candidate review, state examples, a journey map and a developer handoff. Content is synthetic. The first overview and dossier exports were visually inspected; the expanded desktop section was moved away from other sections after an overlap was found.

This is work in progress, not a finished production design system. Full role/state variants, operational and workspace flows, responsive coverage, verified prototyping and thorough visual/accessibility review remain. The user-provided goal text ends mid-sentence in its lead detail section; do not infer additional unseen requirements. The Figma Starter plan permits one variable mode, so the dark theme is not established. Official Figma MCP reported a Starter plan call limit. A desktop bridge connects to the same file, but its in-memory canvas was observed to lag behind the Figma API (e.g. desktop section had five screens locally versus six in the API), and newly added local components had not yet appeared in the API export. Avoid overwriting or duplicating nodes until synchronization is verified. The attempted link from the dossier to people did not complete. No frontend implementation, provider call, outreach, push, merge or deployment was performed.

Synchronization update: the desktop bridge and Figma API eventually converged; the additional input/navigation components became visible in the saved file and the people/evidence screen appeared in the desktop bridge. The dossier-to-people prototype link was then created. The Activity & jobs screen was added and its export inspected; the Product setup screen was added afterward and still needs an export/visual check. Figma updates may take time to reach the REST export; verify persistence before repeating writes. The brief lives under the repository's ignored docs directory and is a local handoff, not a tracked commit.

Latest working state: the Figma file also contains desktop Activity & jobs, Product setup and Delivery authorization screens, a role/data-contract matrix, a button variant set, reusable input/navigation components and navigation links. The delivery authorization example was corrected to require a confirmation, matching `ApproveSend.confirmed`; its action is shown disabled until confirmation. Three screens now use button component instances, and the candidate prototype reaction survived replacement. The Figma REST screenshot service returned HTTP 429 during visual validation of the updated component library, while the desktop bridge remains responsive; this latest visual validation is pending. Do not call the design complete until all required screens, role and interaction states, reusable components, responsive layouts, prototypes and final visual/accessibility checks have been verified. The original attachment ended mid-sentence, and the user was asked whether more of the brief exists.

## Contract precision for overview and list design

The leads endpoint returns a `total` for the current query/filter and `as_of` snapshot; an unfiltered query can be labelled all companies in that workspace as of that snapshot. Workspace is route/session context, not a per-row field. Approvals are returned as up to the newest 100 records; any pending count derived from them must be explicitly labelled a count within that capped set, not a workspace-wide total. Recent jobs are similarly capped; current stalled and delayed IDs come from operations health, so combining categories requires a defined deduplication rule. There is no dedicated aggregate overview endpoint. Candidate list totals are scoped to the applied candidate filter. The role summary above is illustrative: candidates permit ADMIN, OPERATOR and REVIEWER; draft decisions ADMIN or REVIEWER; revisions and send authorization ADMIN or OPERATOR. The endpoint rules are authoritative.

## Continuation: expanded Figma design and validation

The file now includes a tablet company list; mobile company intelligence, contact evidence and draft review; a viewer-only draft state; workspace switch and stale-context recovery; a review-center queue; workspace members and invitation-link creation; connections; and a qualification/product-match screen. The current company list shows a matched offering only when the saved matching result exists. A separately labelled future concept explores global search, advanced filtering, sort, column selection and role-aware bulk actions; these controls require backend work. A separate synthetic analytics concept defines its weekly lead-created metric and clearly marks historical aggregation, revenue, replies and conversion attribution as unavailable in the baseline.

The file includes a button variant set (default, disabled, focus), a status set, inputs and navigation components, bound light tokens, typography styles, a metric dictionary, a role matrix, API mapping and accessibility handoff. The mobile and desktop representative paths have prototype reactions; the viewer example intentionally does not link into privileged prototype screens. A structural check found no clipped direct children of clipping frames across the then-current desktop and responsive frames, and 126 prototype reactions had no missing destination at the time checked. Figma Desktop visual checks covered the new screens; these checks are not an interactive accessibility audit or frontend test. Muted text was adjusted to #5F6C7A, calculated at 4.69:1 against #EDF0F3. Contrast should still be validated for every rendered state.

The earlier sync warning was transient: the desktop bridge and Figma API later converged. Figma's official MCP and REST screenshot endpoints continued to report rate limits, so subsequent visual validation used the connected Figma Desktop canvas. The file remains a design in progress; validate complete flows, all role/state variants, component bindings, responsive screens and the remaining truncated brief before claiming final source-of-truth readiness.

## 5 November continuation: prototype and responsive progress

Added a draft review example with a completed required note, enabled approval, and a separate recorded-decision state that explicitly says no message was sent. The original note input links to the filled example; approval links to the recorded example. This is a synthetic Figma prototype, not an API action. Corrected the overview's recent-company example so an unaccepted candidate is not simultaneously presented as an existing lead in the same snapshot.

Added a mobile companies list and a mobile navigation example, including a link from the list to the existing company dossier and back. The mobile navigation is a representative prototype: Activity & jobs and workspace-management destinations are identified as desktop designs and still need responsive designs; the review-center link opens an example draft rather than a mobile queue. Other unlinked controls and row actions are design affordances, not implemented behaviors. The prototype should not be treated as a complete end-to-end implementation.

Validated the new layouts visually in Figma Desktop. A Plugin API scan found 160 NODE prototype destinations with no missing target and no visible direct child extending beyond a clipping frame; this does not prove interaction correctness, responsive reflow, accessibility, or every screen's visual quality. A subsequent Figma file-data request returned the four newly added frames, confirming they reached the saved file. The screenshot export service still returned HTTP 429, so visual checks used the desktop canvas. The component library and state coverage remain incomplete, as do a full prototype audit, per-state contrast checks, and responsive coverage for all destinations. The goal attachment ends mid-sentence; any unseen requirements remain unknown.

Correction to scope: organization membership and invitations have implemented routes in `backend/marketing_backend/organization_api.py`; organization roles and workspace roles are distinct. Invitation creation yields a link and does not itself send an email. Endpoint checks remain authoritative.

Visual/prototype follow-up: added token-bound Auto Layout components for a source excerpt and a human-review notice, with editable source and excerpt text on the former. Inspected both on the Figma canvas. In the Figma prototype player, clicked Overview → Review draft → review-note field → Approve draft and observed the filled note, enabled approval, and approved/no-message-sent outcome. This validates that one synthetic prototype path only; it does not exercise a real API or verify other decisions. No outreach occurred.

## 5 November continuation: dossier depth and mobile queues

Added desktop Research findings and Company activity frames, with links from the company dossier and between its Summary, Research, People and Activity tabs. The research view displays synthetic findings, cited excerpts, unknowns, page coverage and an unavailable source. It uses instances of the reusable evidence component. The activity view shows synthetic preparation events and explicitly avoids representing them as outreach or replies. The underlying baseline contracts support research facts, pages, unknowns and coverage, and dated job history; exact field mapping and edge-case behavior still need implementation review.

Added mobile Review center and Activity & jobs examples. The mobile drawer links to them, and the review queue links into the existing example draft and back. These remain representative screens: job drill-down, responsive workspace administration, draft decision variants and other controls still need complete design and prototype coverage. Inspected the new frames in Figma Desktop and re-scanned the document: 199 NODE reactions resolved and no visible direct children exceeded clipping-frame bounds. This is structural evidence only, not an accessibility or full interaction pass.

Figma's desktop editor reported that some changes could not sync until reconnecting, and the subsequent file-data request was rate limited (HTTP 429). The four latest frames are visible via the connected local desktop bridge, but their server-side persistence has not yet been independently verified. Do not duplicate them when retrying; verify IDs 27:2048, 27:2161, 27:2281 and 27:2315 after reconnection. No external provider calls or application data changes were made.

Contract correction: `discovery_api.Review` allows an empty note for acceptance, but rejection explicitly requires at least five characters (and the request caps notes at 1,000). The previous candidate-review labels incorrectly called the note optional without distinguishing the decision. Desktop and mobile labels now explain the difference and show rejection disabled while the note is empty. Visual checks covered both; a filled-note rejection state and error handling still need a full prototype. The desktop bridge still reports pending synchronization, so independent persistence verification remains outstanding.

## Accessibility review and prototype targets

A focused Figma component audit identified that the search input had no designed focus state. It is now a component set (27:2353) with default, 2px focus and disabled variants, a visible focus treatment, and keyboard/label implementation guidance. The component audit measured the focus stroke at 6.9:1 against its test background. Persistent visible search labels were added to the desktop and mobile company-list examples. This is a design inspection, not proof of WCAG conformance.

The mobile prototype used text-sized hotspots for many links. The 23 text reactions were moved into at-least-44px frames and the remaining 42px contact-review control was increased to 44px; the visible layout was inspected and a bounds check found no clipped direct children. This measurement covers prototype reaction nodes only, not every action or actual frontend hit target. The mobile prototype player was opened, but clicking the candidate-review target did not navigate in the attempted check. A nearly transparent hit surface was subsequently added to the target frames; because Figma still reports unsynchronized changes, retest the live prototype after synchronization before claiming the targets work. Do not assume that the hit-surface change fixed the interaction. Removed the duplicate mobile flow starting point introduced by cloning the overview.

The component audit also noted incomplete button states and missing structured accessibility annotations. Priority implementation checks remain keyboard navigation and focus order, accessible names and form errors, screen-reader announcements, zoom/reflow, mobile touch spacing and per-state contrast. The Figma file has no implemented DOM, so semantic behavior and AA conformance cannot be verified here. The REST file-data request again returned 429 and the editor continued to report pending sync; retain the open Figma session and verify saved state before closing/reloading it.

## Local recovery copy and mobile target verification

The mobile overview's enlarged candidate-review target was retested in the Figma prototype player and navigated to the Northstar Freight candidate screen. This proves that one target in the current session; remaining mobile targets still require individual interaction checks. Figma Desktop continued to show a synchronization warning and a file-data request again returned HTTP 429. To protect the current session, used Figma's File → Save local copy to create `C:\Projects\marketing-crm-figma\marketing-crm-design-backup.fig` (409,563 bytes). Its ZIP container was inspected and contains `canvas.fig`, `thumbnail.png` and `meta.json`; an independent re-import has not yet been tested. This backup does not prove the online file is synchronized. Keep the open Figma session until server-side synchronization has been confirmed.

Candidate rejection is now represented by a filled-reason state (27:2402) and a recorded-rejection state (27:2479). The latter changes the queue to All candidates, reduces the ready count in the synthetic example, and states that no lead or research was started. Plugin API inspection confirms the note-field and rejection reactions point to the intended frames; a full player click-through of this desktop path is still pending. Both frames were visually inspected.

A newer local recovery copy, `C:\Projects\marketing-crm-figma\marketing-crm-design-backup-rejection.fig`, was saved after those edits (413,867 bytes); its archive contains canvas.fig, thumbnail.png and meta.json. As with the earlier copy, re-import has not yet been independently verified. Figma still reports unsynchronized changes and the file-data endpoint remains rate limited. Keep the editor open and avoid assuming online persistence.

Prototype verification update: in the Figma player, switched to Fit width and height, clicked the candidate review note field, then clicked Reject. The player displayed the filled reason and the rejected outcome. This is a synthetic Figma-only path; no API request was sent. The file-data API again returned HTTP 429, and the desktop editor still reports pending synchronization. The local recovery copy remains the latest backup of the Figma changes at this point.

## Contact channel contract correction

A fresh source check found that baseline `native_api.py` rejects contact selection unless the selected person has an email or a supported LinkedIn profile. The previous desktop/mobile Alex Tan example had no displayed channel yet showed an enabled selection action and suggested it might merely need later review. Both examples now explicitly say there is no supported email or LinkedIn profile, explain that a supported outreach channel is required, and show selection disabled. This corrects the `develop` design baseline; later feature worktrees can have different semantics and require a separate contract review. Visual inspection and text bounds checks passed, but frontend behavior has not been tested because this is a design-only task.

The desktop rejection path was exercised in the prototype player: selecting the note field showed the filled state and selecting Reject showed the rejected state. An updated recovery copy after the channel correction is `C:\Projects\marketing-crm-figma\marketing-crm-design-backup-channel.fig` (413,882 bytes); its ZIP container includes canvas.fig, thumbnail.png and meta.json. It has not been re-imported. The online file-data endpoint still returns HTTP 429 and the editor still reports pending synchronization.

The baseline contact API has two distinct cases: no supported email or LinkedIn profile cannot be selected; a saved researched person can be selected without email if an eligible saved LinkedIn profile is present or selected. Added a separate synthetic Figma state, 27:2561, showing the latter with a source excerpt and a reminder that this does not enable live social delivery. The state was visually inspected; it is a static example, not a tested API interaction. A new local recovery file after this edit is `C:\Projects\marketing-crm-figma\marketing-crm-design-backup-profile.fig` (418,504 bytes); its ZIP container was inspected, but re-import remains untested. The Figma online file-data endpoint again returned HTTP 429 and the desktop synchronization warning persists.

## Role-specific draft states

Added Figma states for an Operator viewing a pending draft (27:2623) and a Reviewer who previously edited that draft (27:2687). The Operator sees that an Admin or Reviewer must decide and that revision follows a changes-requested decision. The editor/Reviewer state disables approval and explains that a different reviewer must approve, while leaving the other decision affordances visible. This reflects the `develop` role checks and self-approval guard in `native_api.py`; these are static design examples, not permission tests. Both panels were inspected in Figma Desktop.

Latest local recovery copy: `C:\Projects\marketing-crm-figma\marketing-crm-design-backup-roles.fig`, 422,831 bytes. Its ZIP entries were inspected; independent Figma re-import is untested. The editor still reports unsynchronized changes and the file-data API returned HTTP 429; the server-side state is not verified.

## Draft revision state

Added `Revise draft · operator · changes requested · synthetic` (27:2759). It shows the existing reviewer feedback, subject, body, revision note and a saved-source citation, with the baseline request limits and a clear statement that submitting a revision creates a new review version and does not send. The source endpoint requires an Admin or Operator, a current changes-requested version, 3–200 subject characters, 30–3,000 body characters, a 5–1,000 character note and 1–10 citations; it also checks freshness and validates citations. The screen is a static Figma state: its controls and error paths are not a working implementation or complete prototype. It was visually inspected in Figma Desktop.

Saved a new local recovery copy after this edit: `C:\Projects\marketing-crm-figma\marketing-crm-design-backup-revision.fig` (434,771 bytes). The ZIP container contains canvas.fig, thumbnail.png and meta.json. Re-import is still untested; Figma Desktop still reports pending synchronization, so server-side persistence is not confirmed.

## Revision prototype journey

Added an Operator changes-requested handoff (27:2867), connected it to the revision form (27:2759), and connected submission to an Operator pending-review outcome (27:2933). The outcome says no message was sent and correctly limits the independent-reviewer rule to approval. Added a named Figma starting point for the Operator revision journey. The Figma player was used to click Revise draft → Submit revision for review and visibly reached the pending-review outcome. This synthetic prototype uses fixed sample content and does not exercise editing, validation, stale context, or a real API.

A newer recovery copy, `C:\Projects\marketing-crm-figma\marketing-crm-design-backup-journey.fig`, was saved after these changes (439,071 bytes). Its ZIP container includes canvas.fig, thumbnail.png and meta.json; re-import remains untested. Figma Desktop continued to show a pending synchronization warning, so do not assume the online file has the latest changes.

## Metric consistency correction

The jobs list (`api.py`) and operations health (`native_api.py`) are separate requests, so a count combining failed IDs from the newest 100 jobs with stalled IDs is a non-atomic union, not a single database snapshot. Updated the Figma metric dictionary to say so and changed the overview sublabel to `Recent failed jobs + stalled`. The count must deduplicate by job ID and surface freshness appropriately; a consistent atomic aggregate would require backend work. The updated Figma label was visually inspected. This change does not validate the complete dashboard or its backend implementation.

After the metric correction, saved `C:\Projects\marketing-crm-figma\marketing-crm-design-backup-metrics.fig` (439,640 bytes); its ZIP container includes canvas.fig, thumbnail.png and meta.json. A new structural scan found 227 NODE reactions with existing destinations and no visible direct children outside clipping frames. This does not establish correct behavior for every link, visual quality, or accessibility. Re-import of the recovery copy remains untested.

## Revision validation design

Added `Revise draft · validation errors · synthetic` (27:2999): a short subject, short body and empty revision note show a three-field summary, specific inline guidance and a disabled submit control. This is a static design example; focus behavior, error announcement and the form's validation timing require implementation and assistive-technology testing. The accessibility handoff now asks for an error summary and removes the unsupported blanket assertion that all body and action colors have passed contrast testing. The error state and updated handoff were visually inspected in Figma Desktop.

Latest recovery copy: `C:\Projects\marketing-crm-figma\marketing-crm-design-backup-validation.fig` (442,584 bytes). The ZIP container includes canvas.fig, thumbnail.png and meta.json; re-import is not tested. Figma Desktop continues to report unsynchronized changes, so online persistence remains unverified.

### Component-state audit continuation (2026-11-05)
Added a keyboard-focus primary button variant and converted the unused text-input component into default, focus, error, and disabled variants. The handoff specifies visible labels, error association, and semantic disabled explanations. Visually inspected the input variants in Figma Desktop. The component audit is heuristic, not a full accessibility or WCAG assessment; implementation needs keyboard, screen-reader, and contrast testing in context.

Latest local recovery copy: `C:\Projects\marketing-crm-figma\marketing-crm-design-backup-components.fig` (443,801 bytes); archive contains canvas.fig, thumbnail.png, and meta.json. Reimport has not been tested. The editor still reports that some changes will not sync until Figma reconnects, so cloud persistence of recent edits remains unverified. Keep the editor open and verify synchronization before relying on the shared file.
