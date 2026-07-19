# Agent Eval Kit sales site

This repository owns the root GitHub Pages host for Agent Eval Kit, downloadable offline B2B software sold under fixed Team and Individual licenses. It publishes the software release manifest and the terms, privacy, and refund pages required for Paddle domain review.

The site intentionally uses only static HTML and CSS. It has no package-manager dependency, analytics runtime, advertising pixel, account login, checkout script, or iframe. Paddle Checkout is added only after the software domain is approved and the client-side flow can be verified against an active software price.

The product source, tests, and standalone build are maintained separately from this public sales repository. The public `product-manifest.json` records the exact release name and SHA-256 without exposing the paid archive.

## Verify

```sh
python3 -m unittest discover -s tests -v
```

Also run `git diff --check` before publishing.
