# Delta for Catalog API

## ADDED Requirements

### Requirement: Exact source mapping

The service SHALL map the 17 observed CSV columns without inventing product facts.

#### Scenario: Valid source
- **GIVEN** the supplied 152-row catalog
- **WHEN** it is loaded
- **THEN** source IDs, EUR prices, stock quantities, shipping days, recipient, occasion,
  tags, optional attributes, and descriptions are preserved
- **AND** observed category aliases normalize to 11 stable categories

#### Scenario: Invalid structure
- **GIVEN** a missing required header, empty catalog, duplicate ID, or invalid required value
- **WHEN** loading completes
- **THEN** the entire catalog is marked unavailable
- **AND** no partial or synthetic catalog is served

### Requirement: Degraded lifecycle

The process SHALL remain live but not ready when the catalog is unavailable.

#### Scenario: Catalog load failure
- **WHEN** the configured CSV is missing, unreadable, empty, or invalid
- **THEN** `/healthz` returns HTTP 200 with `status=alive`
- **AND** `/readyz` returns HTTP 503 with `catalog_status=degraded`
- **AND** authenticated catalog operations return `CATALOG_UNAVAILABLE`

#### Scenario: Missing security configuration
- **WHEN** `CATALOG_API_KEY` is absent or blank
- **THEN** application construction fails with a clear configuration error

### Requirement: API-key security

All four catalog operations SHALL require `X-API-Key` and compare it in constant time.

#### Scenario: Missing or invalid key
- **WHEN** the header is missing or incorrect
- **THEN** the service returns `AUTHENTICATION_REQUIRED` or `INVALID_API_KEY`
- **AND** neither the configured nor received value is logged or returned

### Requirement: Four catalog operations

The service SHALL expose exactly `get_categories`, `get_products_by_category`,
`search_products`, and `get_product_details` as OpenAPI operations.

#### Scenario: Category discovery
- **WHEN** `get_categories` is called
- **THEN** all categories are returned with total count, in-stock count, EUR price range,
  and no pagination

#### Scenario: Category browse
- **WHEN** a valid category is browsed with price, stock, or shipping filters
- **THEN** all hard filters are satisfied before pagination

#### Scenario: Exact detail
- **WHEN** a known source `product_id` is requested
- **THEN** all useful source-derived facts and recommendation eligibility are returned

#### Scenario: Contextual search
- **WHEN** a concise query and structured constraints are supplied
- **THEN** category, price, stock, recipient, occasion, and shipping constraints run
  before lexical ranking
- **AND** zero-score candidates are excluded
- **AND** duplicate normalized names appear at most once in the search page

### Requirement: Honest stock and shipping

Collection operations SHALL default to in-stock products and SHALL expose shipping days
as a catalog estimate.

#### Scenario: Default discovery
- **WHEN** no stock option is passed
- **THEN** zero-stock products are excluded

#### Scenario: Two-day requirement
- **WHEN** `max_shipping_days=2` is passed
- **THEN** no returned product has a higher value

### Requirement: Compact grounded responses

Collection summaries SHALL contain enough source facts for a reasoned recommendation,
while detail SHALL be the only operation returning every product field.

#### Scenario: Collection response
- **THEN** each item includes ID, name, category/subcategory, EUR price, stock status,
  shipping days, recipient, occasions, rating, and description
- **AND** the response includes totals, offset, next offset, and applied filters

### Requirement: Structured failures

All API validation and domain failures SHALL use one error envelope with `code`,
`message`, and `recovery_hint`.

#### Scenario: Empty valid search
- **WHEN** no product matches valid constraints
- **THEN** HTTP 200 is returned with an empty results list

#### Scenario: Invalid price range
- **WHEN** minimum price exceeds maximum price
- **THEN** `INVALID_PRICE_RANGE` is returned with an actionable hint

### Requirement: LLM-readable OpenAPI

The exported schema SHALL contain stable operation IDs, routing guidance, parameter
bounds, response/error models, API-key security, and the configured HTTPS server URL.

#### Scenario: Schema review
- **WHEN** only `openapi.json` is inspected
- **THEN** a caller can select and invoke the four operations correctly
- **AND** health routes and secret values are absent
