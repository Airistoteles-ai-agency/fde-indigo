from __future__ import annotations

import re
from collections.abc import Iterable

from app.catalog.loader import normalize_text
from app.catalog.models import Product


def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", normalize_text(value)))


def score_product(product: Product, query: str) -> int:
    normalized_query = normalize_text(query)
    query_tokens = tokens(query)
    score = 1000 if normalize_text(product.name) == normalized_query else 0

    fields: list[tuple[Iterable[str], int]] = [
        (tokens(product.name), 20),
        (tokens(f"{product.category_name} {product.subcategory}"), 12),
        (tokens(product.brand), 10),
        (
            tokens(" ".join((product.recipient, *product.occasions, *product.tags))),
            8,
        ),
        (tokens(" ".join(filter(None, (product.color, product.material)))), 5),
        (tokens(product.description), 2),
    ]
    for field_tokens, weight in fields:
        score += len(query_tokens.intersection(field_tokens)) * weight
    return score
