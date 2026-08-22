from __future__ import annotations

import argparse
import os
import sys

import httpx


def expect(response: httpx.Response, status: int, label: str) -> None:
    if response.status_code != status:
        raise RuntimeError(
            f"{label} returned {response.status_code}, expected {status}: {response.text[:300]}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Smoke-test a deployed catalog API.")
    parser.add_argument("--base-url", required=True)
    args = parser.parse_args()
    api_key = os.getenv("CATALOG_API_KEY")
    if not api_key:
        raise RuntimeError("Set CATALOG_API_KEY in the process environment.")

    base_url = args.base_url.rstrip("/")
    headers = {"X-API-Key": api_key}
    with httpx.Client(base_url=base_url, timeout=30) as client:
        expect(client.get("/healthz"), 200, "health")
        expect(client.get("/openapi.json"), 200, "OpenAPI")
        expect(client.get("/v1/categories"), 401, "missing-key rejection")

        categories = client.get("/v1/categories", headers=headers)
        expect(categories, 200, "categories")
        category_id = categories.json()["results"][0]["category_id"]

        browse = client.get(
            f"/v1/categories/{category_id}/products", headers=headers
        )
        expect(browse, 200, "category browse")
        if not browse.json()["results"]:
            raise RuntimeError("Category browse returned no products for smoke test.")
        product_id = browse.json()["results"][0]["product_id"]

        expect(client.get(f"/v1/products/{product_id}", headers=headers), 200, "detail")
        expect(
            client.get("/v1/search/products", params={"query": "gift"}, headers=headers),
            200,
            "search",
        )
    print("Smoke test passed: health, auth, categories, browse, detail, and search.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, httpx.HTTPError) as exc:
        print(f"Smoke test failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
