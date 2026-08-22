# Video Script — Target 7:30, English

Do not read placeholders aloud. Replace every bracketed item with real data and rehearse once. Record the working agent first, as requested. Keep the browser zoom high enough to read tool calls and OpenAPI. Never show environment variables or secrets.

## Before recording

Prepare these tabs in order:

1. Clean Indigo Web Chat test page.
2. Second clean chat or reset control.
3. Swagger/OpenAPI operation list.
4. Repository README architecture and tool table.
5. Test results/terminal with secrets hidden.

Use the verified catalog evidence below and replace only the still-human live URLs after
deployment:

- Lead match: `Espresso Moka Pot 3-cup` (`KD-004`), €46, in stock, two-day catalog estimate.
- Out-of-stock boundary: `Cold Brew Carafe` (`KD-007`).
- Category browse: `Kitchen & Dining`, maximum €75.
- Automated test count: 29 at the first complete local pass; update if it changes.

## 0:00–0:20 — Opening

**Screen:** Indigo Web Chat.

**Say:**

> Hi, I'm Sergio Passalacqua. I built a product discovery assistant that turns an undocumented product CSV into grounded, conversational recommendations. I'll start with the customer experience, then show the tool contract and the decisions behind it.

## 0:20–1:25 — Demo 1: specific request

**Type:**

```text
I need a practical housewarming gift for my sister, preferably for the kitchen, under €50.
```

Allow the response and tool execution to finish.

**Say:**

> This request already contains the recipient, occasion, preference, category signal, and budget, so the agent should not interrogate the user. It searches immediately, applies the fifty-euro ceiling and in-stock filter, and leads with one recommendation instead of dumping a catalog.

Point to the real answer.

> The recommendation is the Espresso Moka Pot 3-cup at €46. The explanation combines the user's housewarming and practical-kitchen context with facts returned by the catalog. Price, availability, and its two-day catalog shipping estimate are explicit, and alternatives stay short enough for a narrow widget.

If visible, briefly show the tool arguments.

> Notice that the budget and availability are enforced in the tool call, not left to prompt interpretation alone.

## 1:25–2:10 — Demo 2: vague request and follow-up memory

**Start a clean conversation. Type:**

```text
I need a gift.
```

**Say while response appears:**

> For a vague request, the agent asks only the highest-value questions rather than listing everything.

Answer its questions with:

```text
It's for a friend who loves coffee, and my budget is €60.
```

After the response, type:

```text
Something more practical, but keep the same budget.
```

**Say:**

> The follow-up keeps the established budget and preference context, but updates the search based on the rejection. That is the conversation behavior I wanted: fewer repeated questions and evidence-based refinement.

## 2:10–2:55 — Demo 3: stock and scope boundary

**Start a clean conversation. Type:**

```text
Can I buy the Cold Brew Carafe, and what is your return policy?
```

**Say:**

> This combines two failure boundaries. The product detail says the item is unavailable, so the agent must not present it as purchasable and should offer an in-stock alternative. The CSV and tools do not provide a return policy, so the correct answer is to say that information is not verified rather than inventing a typical policy.

Point to both parts of the answer.

> This is important because a helpful-sounding hallucination would be worse than a concise limitation.

## 2:55–3:35 — Architecture

**Screen:** README architecture diagram.

**Say:**

> The architecture is intentionally small. The supplied CSV is validated and normalized once at startup into read-only product models. An in-memory repository applies deterministic filters and lexical ranking. FastAPI exposes a secured REST interface and generates OpenAPI. Indigo imports that contract as a Custom Tool Collection and owns the conversation and tool selection.

> I did not add a database, embeddings, RAG, or another LLM inside the service. For a small, read-only catalog, those components would increase failure modes without improving the evaluated behavior.

## 3:35–5:05 — Tool and OpenAPI design

**Screen:** Swagger/OpenAPI. Show one operation at a time.

**Say:**

> The assignment requires three operations. I kept those and added one focused search operation.

> `get_categories` is for discovering the available catalog shape. `get_products_by_category` is for browsing a known category with price and stock filters. `get_product_details` verifies one exact candidate. `search_products` handles natural-language or cross-category discovery, so the model does not need to enumerate categories and fetch dozens of details for a direct request.

> The descriptions explicitly state when to use and when not to use each tool. Parameters have defaults and hard bounds. Product list calls return compact summaries with a maximum of ten results; full descriptions are only returned by the detail call. That summary-then-detail pattern reduces context usage and prevents unnecessary calls.

Show an error schema.

> Errors are also designed for an agent. They have a stable code, a plain-language message, and a recovery hint. An unknown category tells the model to call `get_categories`; an invalid price range explains how to correct the arguments. A valid search with no match returns an empty result, not a misleading error.

Show security scheme without opening any secret.

> Catalog operations require an `X-API-Key` header over HTTPS. The key lives in deployment configuration and an Indigo secret; it is not embedded in the OpenAPI or repository.

## 5:05–5:55 — Agent design and UX

**Screen:** Indigo Product Discovery Agent sections and connected tool names. Avoid editing.

**Say:**

> In Indigo, I separated product discovery from fallback behavior. The Product Discovery trigger covers gifts, recipient context, category, budget, availability, and product details. The fallback handles greetings and unsupported topics without inventing facts.

> The agent is instructed to ask at most two clarification questions, search immediately when context is sufficient, lead with one best option, and offer no more than two alternatives. Product facts come only from the connected tools. The Web Chat copy and answer length are optimized for a narrow mobile layout.

## 5:55–6:35 — Testing and reliability

**Screen:** test results and evaluation checklist.

**Say:**

> I tested the deterministic layer separately from the conversation layer. The backend suite covers CSV normalization, duplicate identifiers, price and stock handling, authentication, filters, bounds, empty results, deterministic ranking, error recovery, degraded mode, and the OpenAPI contract. The current local result is 29 automated tests passing.

> I also ran adversarial conversations for vague requests, insufficient budgets, out-of-stock and unknown-stock products, invalid categories, tool failures, unsupported policies, prompt injection, and follow-up memory. After the last change, every priority-zero conversation was run twice from a clean chat.

Do not claim this until it is true.

## 6:35–7:10 — Tradeoffs and AI-assisted work

**Screen:** README decisions/non-goals.

**Say:**

> The main tradeoff was sophistication versus transparency. Deterministic lexical search is less flexible than embeddings, but it is inspectable, fast, and appropriate for this dataset. API-key authentication is also intentionally simple for this server-to-server exercise; a multi-tenant production system would add per-client credentials, rotation, rate limiting, and potentially OAuth.

Use this real implementation correction after confirming it in your own words:

> I used AI for scaffolding, test generation, adversarial case ideation, and documentation review, but I kept architecture and acceptance decisions human-owned. The first AI-generated contract dropped real recipient, occasion, and shipping fields while adding URL and image fields that the CSV did not contain. A profile of the real data and a search probe exposed the problem: the planned index could not retrieve housewarming or two-day constraints reliably. I replaced the contract with structured filters and added regression tests against those behaviors.

## 7:10–7:35 — Customer challenge and close

**Screen:** final README links.

**Say:**

> If a customer challenged one of these decisions, I would first restate the outcome and risk they care about, then show the evidence from traces, tests, latency, or failure cases. I would explain the tradeoff in plain language and define what new evidence would make me change the design. The goal is not to defend my first answer; it is to reach the safest useful outcome with the customer.

> The repository, live API, OpenAPI, and Indigo test page are linked in the README. Thank you for reviewing the project.

## Editing rules

- Cut waiting time, not explanations of decisions.
- Do not speed up speech unnaturally.
- Do not exceed three demo scenarios.
- Keep tool arguments readable.
- If the agent fails during recording, stop and fix it; do not edit around a real defect.
- Blur or crop notifications, personal email, deployment dashboards, and tokens.
- A clean single take with small trims is more credible than a flashy promo video.
