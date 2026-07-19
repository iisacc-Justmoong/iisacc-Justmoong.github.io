# Independent Agent Evaluation sales site

This repository owns the root GitHub Pages host for Muyeong Yun's fixed-scope independent AI-agent evaluation services. It provides a public service summary and the terms, privacy, and refund pages required before requesting live Paddle domain approval.

The site intentionally uses only static HTML and CSS. It has no package-manager dependency, analytics runtime, advertising pixel, account login, checkout script, or iframe. Paddle Checkout will be added only after the live domain is approved and the client-side flow can be verified against the active catalog price.

## Verify

```sh
python3 -m unittest discover -s tests -v
```

Also run `git diff --check` before publishing.
