# Agent Eval Kit sales site

This repository owns the root GitHub Pages host for Agent Eval Kit, downloadable offline B2B software sold under fixed Team and Individual licenses. It publishes the software release manifest and the terms, privacy, and refund pages used by supported payment processors.

The site intentionally uses only static HTML and CSS. It has no package-manager dependency, analytics runtime, advertising pixel, account login, checkout script, or iframe. The Team CTA links directly to a verified one-time PayPal hosted payment page; the Individual License remains email intake. Paddle Checkout may be added after the software domain is approved and the client-side flow can be verified against an active software price.

The product source, tests, and standalone build are maintained separately from this public sales repository. The public `product-manifest.json` records the exact release name and SHA-256 without exposing the paid archive.

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
