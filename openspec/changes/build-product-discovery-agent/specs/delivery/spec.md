# Delta for Delivery

## ADDED Requirements

### Requirement: Reproducible and secret-safe repository

The repository SHALL contain source, dependency manifests, tests, generated OpenAPI,
deployment configuration, and reviewer documentation without a real credential.

#### Scenario: Fresh setup
- **WHEN** a reviewer follows the README with their own environment values
- **THEN** installation, tests, startup, and OpenAPI export succeed without a real secret

### Requirement: Data distribution gate

The supplied catalog SHALL remain outside public Git until redistribution is approved.
The implementation SHALL support either a committed `data/gift-shop-catalog.csv` or a
configured local/Render secret-file path without code changes.

#### Scenario: Redistribution is not approved
- **WHEN** deployment is prepared
- **THEN** the CSV is supplied through `CATALOG_CSV_PATH` and remains ignored by Git

### Requirement: Early integration experiment

Before completing manual Indigo work, a human SHALL deploy a thin authenticated slice,
import its generated schema, and verify one real tool call. Any schema-version issue
SHALL be fixed in the application generator rather than by editing `openapi.json`.

#### Scenario: Indigo rejects the schema version
- **WHEN** the generated OpenAPI 3.1 schema is rejected specifically for version support
- **THEN** the application generates 3.0.3 and the exported JSON is not hand-edited

### Requirement: Public evidence

The final submission SHALL provide working HTTPS API, OpenAPI, Indigo test-page,
repository, and video links. Public health and OpenAPI SHALL require no secret; catalog
operations SHALL require the configured header.

#### Scenario: Signed-out reviewer
- **WHEN** the reviewer opens the public evidence without the creator's session
- **THEN** all public links work and protected catalog calls still require authentication

### Requirement: Complete README

The README SHALL explain architecture, exact data mapping, operations, authentication,
local setup, deployment, Indigo configuration, agent contract, tests, non-goals,
production hardening, time accounting, AI-assisted workflow, one truthful AI misstep,
and a respectful evidence-based response to a client challenge.

#### Scenario: README review
- **WHEN** a reviewer reads the repository documentation
- **THEN** they can reproduce the service and distinguish verified facts from personal claims

### Requirement: Reviewer-ready agent and video

Blocking conversation cases SHALL pass twice before publication. The 5–10 minute video
SHALL show the working agent first, explain decisions and tradeoffs, and expose no secret.

#### Scenario: Final media review
- **WHEN** the video is viewed signed out
- **THEN** it demonstrates the agent first, lasts 5–10 minutes, and reveals no credential

### Requirement: Cold-start verification

The final Indigo integration SHALL be tested after deployment inactivity. If wake-up
latency harms the reviewer flow, the review-window service SHALL use a non-suspending
configuration.

#### Scenario: First call after inactivity
- **WHEN** an Indigo request is made after the service has been idle
- **THEN** latency is recorded and an unacceptable timeout blocks final publication

### Requirement: Bonus gate

No landing page or MCP work SHALL begin until every core test, link, document, and video
gate passes and at least three hours remain.

#### Scenario: Core work is incomplete
- **WHEN** any core gate is red or less than three hours remain
- **THEN** bonus work is not started
