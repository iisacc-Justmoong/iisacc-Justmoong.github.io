# Agent Eval Kit sales site

[Review the live product and Team License](https://iisacc-justmoong.github.io/) · [Inspect the exact Version 1.0.0 walkthrough](https://iisacc-justmoong.github.io/demo.html) · [Review security reporting](https://iisacc-justmoong.github.io/security.html) · [Open the SPDX SBOM](https://iisacc-justmoong.github.io/agent-eval-kit-1.0.0.spdx.json) · [Open the one-time USD 1,000 PayPal checkout](https://www.paypal.com/ncp/payment/2SHM4XZQ8BVE2)

This repository owns the root GitHub Pages host for Agent Eval Kit, downloadable offline B2B software sold under a fixed Team License. It publishes the software release manifest and the terms, privacy, and refund pages used by supported payment processors.

The root page also publishes a canonical URL, Open Graph and large-image card metadata, and non-executable Schema.org JSON-LD so shared links and product-aware crawlers retain the exact product name, offline acceptance boundary, and one-time Team License positioning. The JSON-LD describes one `Product` and `SoftwareApplication`, Version 1.0.0, Python 3.11 or newer, the public product image, and one active `Offer` whose USD 1,000 price and checkout URL match the buyer-visible Team License. It does not publish invented reviews, ratings, identifiers, seller registrations, or price-expiry dates.

The launch artwork is published under `assets/`: a 240 x 240 thumbnail and two 1270 x 760 gallery images. The first gallery image is also the buyer-visible product flow on the root page, so prospective purchasers can inspect the offline input-to-decision boundary without relying on social metadata. The SVG source artwork is maintained with the revenue-run records; the public PNG files are the immutable upload and URL-paste variants used by product-discovery surfaces.

The site intentionally uses static HTML and CSS with no executable client-side JavaScript. Its only `script` element is the non-executable `application/ld+json` product description. It has no package-manager dependency, analytics runtime, advertising pixel, account login, checkout script, or iframe. The Team CTA links directly to a verified one-time PayPal hosted payment page. License paths that require seller reauthentication are not published as active purchase options. Paddle Checkout may be added after the software domain is approved and the client-side flow can be verified against an active software price.

The product source, tests, and standalone build are maintained separately from this public sales repository. The public `product-manifest.json` records the exact release name and SHA-256 without exposing the paid archive. The public `agent-eval-kit-1.0.0.spdx.json` is an SPDX 2.3 JSON SBOM with one product root package, the matching archive checksum, and an explicit `DEPENDS_ON NONE` relationship for the reviewed third-party and bundled-runtime package scope. Python 3.11 or newer remains an external execution prerequisite; the release uses the Python standard library and contains no third-party packages or bundled runtime dependencies.

`demo.html` publishes a copyable Version 1.0.0 walkthrough generated from the reproducible release artifact: the example contract and evidence, the validate and passing-evaluation commands, the stable contract seal, all eight deterministic checks, and the final pass/reward fields. It also publishes the exact tamper-rejection command, its nonzero process exit, the failed pinned-commit check, and the zero-reward result. Keep it synchronized with the product examples and actual built output; do not hand-edit result values without rerunning the release archive.

## Buyer-visible product requirements

Keep the public product page and Terms synchronized with the release README and product contract. The supported runtime is Python 3.11 or newer, and the application has no third-party package dependencies. Email support is limited to installation questions and reproducible defects in the purchased version. The root page must also preserve the caller-run trust boundary and summarize the published remedy and refund path for material reproducible defects. These requirements and boundaries must remain visible before checkout.

The root page also explains when to use the software as a final acceptance gate. It must connect the verified product behavior to three buyer decisions: verify the pinned commit, exact command, and required checks before accepting an agent-produced change; re-run the same JSON contract and evidence offline at a team handoff; and reject changed or incomplete evidence with a nonzero exit and zero reward. This section describes only behavior covered by the public walkthrough and must stay before the Team License card.

The public security contract is `https://iisacc-justmoong.github.io/security.html`. It accepts reports for Version 1.0.0 at the published contact address, restates the offline/no-network/no-telemetry/no-arbitrary-execution boundary, and promises only reasonable best-effort handling without an acknowledgement, remediation, disclosure, or release SLA. Keep it linked from the root page and Terms. The matching SBOM is `https://iisacc-justmoong.github.io/agent-eval-kit-1.0.0.spdx.json`; its package name, version, artifact filename, checksum, runtime statement, and dependency relationship must remain synchronized with `product-manifest.json` and the product release.

## IndexNow discovery signal

The site exposes `https://iisacc-justmoong.github.io/85f6cd16c59495e50ef6232cdc8df61f.txt` for IndexNow ownership verification. Its 32-character value is a public ownership token, not a secret, and the root filename must always equal the file content.

The IndexNow endpoint is exactly `https://api.indexnow.org/indexnow`. The one-time submission list for this update contains only these freshly updated URLs:

- `https://iisacc-justmoong.github.io/`
- `https://iisacc-justmoong.github.io/demo.html`

Repeated submissions are avoided unless one of those URLs changes again. An IndexNow submission only signals discovery; it does not prove indexing or revenue.

Crawler discovery is also published through `https://iisacc-justmoong.github.io/robots.txt` and `https://iisacc-justmoong.github.io/sitemap.xml`. The robots file allows all crawlers and points to the absolute sitemap URL. The sitemap lists only the root page, demo, product manifest, SPDX SBOM, security, terms, privacy, and refunds URLs. No `lastmod` values are published because the repository does not maintain authoritative modification timestamps for these static resources.

## Verify the Team checkout

The exact Team checkout URL is pinned in `tests/test_site.py`. Before publishing a URL change, verify the PayPal-hosted page directly:

- Product name is `Agent Eval Kit Team License`.
- The price is a one-time USD 1,000 payment.
- Shipping and buyer-adjustable quantity are disabled.
- The return settings contain no Vincent URL, access key, or other product-specific secret.
- The hosted page is active at exactly `https://www.paypal.com/ncp/payment/<TOKEN>` with no query or fragment.

Keep the exact URL in `index.html`, `demo.html`, and `tests/test_site.py` synchronized. Review the diff and run the verification below before publishing.

## Verify

```sh
python3 -m unittest discover -s tests -v
```

Also run `git diff --check` before publishing.

When the demo changes, rebuild the product in its required `build/` directory and run both public commands before running the site tests. Confirm the demo's seal and evaluation result match that output exactly.
