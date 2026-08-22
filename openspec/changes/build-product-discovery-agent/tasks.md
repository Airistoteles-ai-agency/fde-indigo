# Tasks: Build Product Discovery Agent

Codex owns repository work. Sergio owns items labelled **HUMAN**. A checkbox is complete
only when its stated evidence exists.

## 1. Contract and source discovery

- [x] 1.1 Read all change artifacts, repository instructions, and the council handoff.
- [x] 1.2 Inspect the supplied CSV without copying it into the public repository.
- [x] 1.3 Record its 17-column mapping, 152-row profile, category aliases, optional fields,
  duplicates, stock, EUR price, and shipping rules in the design.
- [x] 1.4 Replace speculative IDs, URLs, images, summaries, free-text-only search, and
  fail-start catalog behavior in proposal, design, and delta specs.
- [x] 1.V Run strict OpenSpec validation after the replacement artifacts are complete.
- [ ] **HUMAN 1:** Decide whether the supplied CSV may be committed publicly. Until then,
  use `CATALOG_CSV_PATH` and the documented secret-file path.

## 2. Project skeleton and catalog lifecycle

- [x] 2.1 Add dependency manifests, package structure, settings, `.env.example`, and
  secret-safe `.gitignore` rules.
- [x] 2.2 Implement exact CSV normalization and immutable ready/degraded repositories.
- [x] 2.3 Implement category, detail, filtering, ranking, pagination, and duplicate-name
  suppression.
- [x] 2.4 Add public liveness/readiness endpoints and structured degraded behavior.
- [x] 2.V Test valid/invalid catalogs, aliases, optional values, duplicate IDs, zero-day
  shipping, hard filters, determinism, zero-score exclusion, and degraded startup.

## 3. Authenticated REST and OpenAPI

- [x] 3.1 Implement constant-time `X-API-Key` authentication.
- [x] 3.2 Implement `get_categories` and `get_products_by_category`.
- [x] 3.3 Implement `search_products` and `get_product_details`.
- [x] 3.4 Implement structured domain and validation errors.
- [x] 3.5 Add routing guidance, parameter bounds/examples, compact/full schemas, security,
  and `servers[0].url` to OpenAPI.
- [x] 3.6 Add deterministic `openapi.json` export with exactly four operations.
- [x] 3.V Test auth, all routes, bounds, errors, security, operation IDs, server URL, and
  secret absence.

## 4. Quality and deployment packaging

- [x] 4.1 Add request outcome/latency logging without keys or raw rows.
- [x] 4.2 Add Render native configuration using `$PORT`, `/healthz`, and documented env vars.
- [x] 4.3 Add an authenticated smoke script that reads the key only from the environment.
- [x] 4.4 Add README setup, architecture, data profile, operations, auth, deployment,
  Indigo connection, agent prompt, non-goals, and hardening notes.
- [x] 4.5 Add a versioned evaluation record and update the runbook/video/time templates.
- [x] 4.V Pass strict OpenSpec, Ruff, the complete pytest suite, OpenAPI export, secret
  scan, diff check, and a local process smoke test.

## 5. Public deployment and Indigo integration

- [ ] **HUMAN 5.1:** Rotate/create the production API key and configure it in Render.
- [ ] **HUMAN 5.2:** Choose the CSV distribution branch and deploy the service.
- [ ] **HUMAN 5.3:** Run the public smoke test and measure a cold start after inactivity.
- [ ] **HUMAN 5.4:** Import generated OpenAPI into Indigo and verify one tool call before
  completing agent configuration.
- [ ] **HUMAN 5.5:** Configure Product Discovery, General fallback, Welcome, memory, model,
  creativity, token limit, examples, and secret header while remaining in Draft.

## 6. Conversation evaluation

- [ ] **HUMAN 6.1:** Run the blocking AI cases from clean conversations and record tool
  order, arguments, outputs, response, model/configuration, and pass/fail.
- [ ] 6.2 Repair any backend/OpenAPI defect discovered by those cases and rerun tests.
- [ ] **HUMAN 6.3:** Rerun every blocking case twice after the last material change.
- [ ] **HUMAN 6.4:** Approve the evaluation record and publish Indigo.

## 7. Final evidence

- [ ] **HUMAN 7.1:** Replace live-link and measured-time placeholders in README/manuals.
- [ ] **HUMAN 7.2:** Verify API, OpenAPI, Indigo, repository, and video links signed out.
- [ ] **HUMAN 7.3:** Rewrite personal claims in Sergio's voice and confirm the AI-misstep
  and client-challenge accounts are truthful.
- [ ] **HUMAN 7.4:** Record and upload the 5–10 minute English video with no secrets visible.
- [ ] **HUMAN 7.5:** Confirm all core gates pass before considering any bonus.
