# Supplied Catalog Profile

Source inspected locally: `gift-shop-catalog.csv` supplied for the Indigo assignment.
The source remains outside Git pending a redistribution decision.

## Shape

- Encoding: UTF-8 without BOM.
- Delimiter: comma.
- Line endings: CRLF.
- Rows: 152 products.
- Columns: 17.
- Product IDs: 152 present, 152 unique.
- Price range: €6.50–€899; no invalid or negative values.
- Stock range: 0–999; 11 zero-stock rows.
- Shipping estimates: 0–7 days; 48 products at two days.
- Categories: 11 after normalization.

## Column mapping

| Source | Canonical | Rule |
| --- | --- | --- |
| `product_id` | `product_id` | Preserve; missing/duplicate is fatal. |
| `name` | `name` | Required trimmed string. |
| `category` | `category_id`, `category_name` | Normalize whitespace, case, and `and`/`&`. |
| `subcategory` | `subcategory` | Required trimmed string. |
| `brand` | `brand` | Required trimmed string. |
| `price_eur` | `price`, `currency` | Non-negative decimal; currency literal `EUR`. |
| `stock` | `stock_quantity`, `stock_status` | Integer; zero is out of stock. |
| `rating` | `rating` | Nullable 0–5 number. |
| `reviews_count` | `reviews_count` | Nullable non-negative integer. |
| `recipient` | `recipient` | Required normalized string. |
| `occasion` | `occasions` | Nullable pipe-delimited list. |
| `tags` | `tags` | Nullable pipe-delimited list. |
| `color` | `color` | Nullable string. |
| `material` | `material` | Nullable string. |
| `gift_wrap` | `gift_wrap_available` | `yes`/`no` to boolean. |
| `shipping_days` | `shipping_days` | Integer 0–7; zero is valid. |
| `description` | `description` | Required source text; no generated summary. |

## Quality observations

- Five products have both rating and review count blank.
- Three products have no occasion.
- Color/material are blank for two digital gift cards.
- `gift_wrap` is yes for 139 rows and no for 13.
- Two name/description pairs occur under different source IDs and categories:
  `HL-021`/`KD-024` Herb Garden Kit and `HL-024`/`KD-023` Amber Glass Tumbler Set.
- There are no product or image URL columns.
- Source descriptions range from 7 to 142 characters, so `short_description` would be an
  invented transformation with little value.

## Verified retrieval examples

- Practical kitchen housewarming, recipient `her`, maximum €50, in stock, maximum two
  days → `KD-004` Espresso Moka Pot 3-cup, €46.
- Chef's knife under €100 → no exact chef's knife; `KD-001` costs €149. `KD-002` is a €69
  paring knife and must be described as a different alternative.
- Cold Brew Carafe `KD-007` is out of stock.

## Unsupported facts

The API cannot truthfully provide product pages, images, returns, warranties, payment
terms, carriers, or general delivery guarantees. `shipping_days` is only the supplied
product-level estimate.
