# Proposal: Build Product Discovery Agent

## Intent

Turn the supplied 152-row gift catalog CSV into a publicly deployable, authenticated,
LLM-readable API and connect it to an Indigo Product Discovery Agent. Recommendations
must be concise, respect hard user constraints, and use only facts returned by tools.

## Scope

- FastAPI and Pydantic service with an immutable in-memory catalog.
- Exact source mapping for all 17 CSV columns; currency is always EUR.
- Four authenticated operations: `get_categories`, `get_products_by_category`,
  `search_products`, and `get_product_details`.
- Deterministic structured filters and lexical ranking.
- Separate liveness and readiness behavior so a missing catalog starts degraded.
- Generated OpenAPI with an HTTPS server URL, API-key security, and compact schemas.
- Render-compatible deployment configuration and an early Indigo import/tool-call probe.
- Backend tests, versioned conversation cases, README, runbook, and video script.

## Non-goals

- Database, embeddings, RAG, LLM calls inside the service, MCP, or landing page.
- Cart, checkout, accounts, inventory mutation, or unsupported store policies.
- Invented product URLs, images, summaries, IDs, shipping guarantees, or policies.
- Automated use of human credentials, deployment, Indigo publication, or video recording.

## Success criteria

The change succeeds when the service loads the supplied schema deterministically,
keeps budget/stock/recipient/occasion/shipping constraints hard, exposes exactly four
secured catalog operations, starts diagnostically when the catalog is unusable, and
generates an OpenAPI document that Indigo can import. A reviewer must be able to run
the project from the README and verify the documented agent behavior without finding
secrets or unsupported claims.

## Data and security decisions

- Preserve every source `product_id`; duplicate or missing IDs make the catalog unusable.
- Normalize observed category spelling/case aliases to 11 stable categories.
- Keep the supplied CSV outside Git until its redistribution status is approved. Tests
  use synthetic fixtures with the same schema. Deployment may use a Render secret file.
- `CATALOG_API_KEY` is mandatory and compared in constant time.
- Missing or invalid security configuration fails startup. Missing or unusable catalog
  enters degraded mode and never serves synthetic replacement data.

## Delivery risks

- Prove OpenAPI/Indigo compatibility with a thin vertical slice before polishing.
- Measure Render cold-start behavior from Indigo before the review window.
- Keep Indigo in Draft until all blocking conversation cases pass twice after the last
  prompt, tool, or model change.
- Rotate credentials that were ever shared outside the target secret stores.
