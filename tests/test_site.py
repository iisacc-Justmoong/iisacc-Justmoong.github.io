import json
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.text_parts = []
        self.styles = []
        self.scripts = []
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a" and "href" in attributes:
            self.links.append(attributes["href"])
        if tag == "link" and attributes.get("rel") == "stylesheet":
            self.links.append(attributes.get("href", ""))
        if tag == "script":
            self.scripts.append(attributes)
        if tag == "style":
            self._in_style = True

    def handle_endtag(self, tag):
        if tag == "style":
            self._in_style = False

    def handle_data(self, data):
        if self._in_style:
            self.styles.append(data)
        else:
            self.text_parts.append(data)


def parse(page_name):
    source = (ROOT / page_name).read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(source)
    text = " ".join(" ".join(parser.text_parts).split())
    return source, parser, text


class SalesSiteTests(unittest.TestCase):
    def test_root_presents_downloadable_software_and_two_licenses(self):
        _, parser, text = parse("index.html")

        for phrase in (
            "Downloadable B2B software",
            "Agent Eval Kit Team License",
            "USD 1,000",
            "25 internal users",
            "Agent Eval Kit Individual License",
            "USD 250",
            "one internal user",
            "Version 1.0.0",
            "Perpetual internal-use license",
            "No consulting",
            "No custom development",
            "71580501a6004ae63e2443a5b8bac61dd84411b3dccdd5ad532f002e45e515d7",
        ):
            self.assertIn(phrase, text)

        self.assertIn(
            "https://github.com/iisacc-Justmoong/agent-task-verifier-sample",
            parser.links,
        )
        self.assertIn("product-manifest.json", parser.links)
        manifest = json.loads((ROOT / "product-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual("downloadable_software", manifest["product_type"])
        self.assertEqual("1.0.0", manifest["version"])
        self.assertEqual("agent-eval-kit-1.0.0.pyz", manifest["artifact"])
        self.assertEqual(
            "71580501a6004ae63e2443a5b8bac61dd84411b3dccdd5ad532f002e45e515d7",
            manifest["sha256"],
        )
        stylesheet = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn("styles.css", parser.links)
        self.assertIn("overflow-wrap: anywhere", stylesheet)
        self.assertIn("minmax(0, 1fr)", stylesheet)

    def test_root_exposes_local_commercial_policies_and_purchase_intake(self):
        _, parser, text = parse("index.html")

        for link in ("terms.html", "privacy.html", "refunds.html"):
            self.assertIn(link, parser.links)
        self.assertTrue(
            any(
                link.startswith(
                    "mailto:andudyun0504@gmail.com?subject=Agent%20Eval%20Kit%20Team%20License"
                )
                for link in parser.links
            )
        )
        self.assertTrue(
            any(
                link.startswith(
                    "mailto:andudyun0504@gmail.com?subject=Agent%20Eval%20Kit%20Individual%20License"
                )
                for link in parser.links
            )
        )
        self.assertIn("Purchasing legal entity", text)

    def test_policy_pages_cover_software_license_and_paddle_requirements(self):
        expectations = {
            "terms.html": (
                "Terms of Sale and Software License",
                "Perpetual internal-use license",
                "No professional services",
                "Paddle",
            ),
            "privacy.html": (
                "Privacy Notice",
                "billing contact",
                "No telemetry",
                "Paddle",
            ),
            "refunds.html": (
                "Refund Policy",
                "downloadable software",
                "14 calendar days",
                "Paddle",
            ),
        }

        for page_name, phrases in expectations.items():
            with self.subTest(page=page_name):
                _, parser, text = parse(page_name)
                for phrase in phrases:
                    self.assertIn(phrase, text)
                self.assertIn("index.html", parser.links)
                self.assertIn("mailto:andudyun0504@gmail.com", parser.links)

    def test_site_does_not_market_unsupported_human_services(self):
        prohibited = (
            "independent evaluation engineering",
            "written scope",
            "delivery window",
            "custom deliverables",
            "request the usd 1,000 audit",
            "work third",
        )
        for page_name in ("index.html", "terms.html", "privacy.html", "refunds.html"):
            with self.subTest(page=page_name):
                source = (ROOT / page_name).read_text(encoding="utf-8").lower()
                for phrase in prohibited:
                    self.assertNotIn(phrase, source)

    def test_site_has_no_third_party_runtime_before_checkout_approval(self):
        for page_name in ("index.html", "terms.html", "privacy.html", "refunds.html"):
            with self.subTest(page=page_name):
                source, parser, _ = parse(page_name)
                self.assertEqual([], parser.scripts)
                self.assertNotIn("<iframe", source.lower())
                self.assertNotIn("http://", source.lower())


if __name__ == "__main__":
    unittest.main()
