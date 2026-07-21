# Agent Eval Kit sales site

[Review the live product and Team License](https://iisacc-justmoong.github.io/) · [Inspect the exact Version 1.0.0 walkthrough](https://iisacc-justmoong.github.io/demo.html) · [Open the one-time USD 1,000 PayPal checkout](https://www.paypal.com/ncp/payment/2SHM4XZQ8BVE2)

This repository owns the root GitHub Pages host for Agent Eval Kit, downloadable offline B2B software sold under fixed Team and Individual licenses. It publishes the software release manifest and the terms, privacy, and refund pages used by supported payment processors.

The root page also publishes a canonical URL and script-free Open Graph and summary-card metadata so shared purchase links retain the exact product name, offline acceptance boundary, and one-time Team License positioning.

The site intentionally uses only static HTML and CSS. It has no package-manager dependency, analytics runtime, advertising pixel, account login, checkout script, or iframe. The Team CTA links directly to a verified one-time PayPal hosted payment page; the Individual License remains email intake. Paddle Checkout may be added after the software domain is approved and the client-side flow can be verified against an active software price.

The product source, tests, and standalone build are maintained separately from this public sales repository. The public `product-manifest.json` records the exact release name and SHA-256 without exposing the paid archive.

`demo.html` publishes a copyable Version 1.0.0 walkthrough generated from the reproducible release artifact: the example contract and evidence, the two exact CLI commands, the stable contract seal, all eight deterministic checks, and the final pass/reward fields. Keep it synchronized with the product examples and actual built output; do not hand-edit result values without rerunning the release archive.

## Verify the Team checkout

The exact Team checkout URL is pinned in `tests/test_site.py`. Before publishing a URL change, verify the PayPal-hosted page directly:

- Product name is `Agent Eval Kit Team License`.
- The price is a one-time USD 1,000 payment.
- Shipping and buyer-adjustable quantity are disabled.
- The return settings contain no Vincent URL, access key, or other product-specific secret.
- The hosted page is active at exactly `https://www.paypal.com/ncp/payment/<TOKEN>` with no query or fragment.

Keep the exact URL in `index.html` and `tests/test_site.py` synchronized, and leave the Individual License email intake unchanged. Review the diff and run the verification below before publishing.

## Verify

```sh
python3 -m unittest discover -s tests -v
```

Also run `git diff --check` before publishing.

When the demo changes, rebuild the product in its required `build/` directory and run both public commands before running the site tests. Confirm the demo's seal and evaluation result match that output exactly.
