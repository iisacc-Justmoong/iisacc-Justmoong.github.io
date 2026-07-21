import json
import re
import struct
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEAM_CHECKOUT_URL = "https://www.paypal.com/ncp/payment/2SHM4XZQ8BVE2"
PUBLIC_ORIGIN = "https://iisacc-justmoong.github.io"
INDEXNOW_KEY = "85f6cd16c59495e50ef6232cdc8df61f"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.canonical_links = []
        self.meta = {}
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
        if tag == "link" and attributes.get("rel") == "canonical":
            self.canonical_links.append(attributes.get("href", ""))
        if tag == "meta":
            key = attributes.get("property") or attributes.get("name")
            if key:
                self.meta[key] = attributes.get("content", "")
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


def relative_luminance(hex_color):
    if len(hex_color) == 4:
        hex_color = "#" + "".join(channel * 2 for channel in hex_color[1:])
    channels = [int(hex_color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4 for channel in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(first, second):
    lighter, darker = sorted((relative_luminance(first), relative_luminance(second)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


class SalesSiteTests(unittest.TestCase):
    def test_indexnow_ownership_key_is_unique_and_self_describing(self):
        key_files = [
            path
            for path in ROOT.glob("*.txt")
            if re.fullmatch(r"[0-9a-fA-F]{32}", path.stem)
        ]

        self.assertEqual([ROOT / f"{INDEXNOW_KEY}.txt"], key_files)
        self.assertEqual(
            f"{INDEXNOW_KEY}\n",
            key_files[0].read_text(encoding="utf-8"),
        )
        self.assertEqual(
            key_files[0].stem,
            key_files[0].read_text(encoding="utf-8").strip(),
        )

    def test_readme_documents_indexnow_submission_contract(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        section = readme.split("## IndexNow discovery signal", 1)[1].split("\n## ", 1)[0]

        self.assertIn("https://api.indexnow.org/indexnow", section)
        self.assertIn(f"{PUBLIC_ORIGIN}/{INDEXNOW_KEY}.txt", section)
        submission_urls = re.findall(r"^- `(https://[^`]+)`$", section, re.MULTILINE)
        self.assertEqual(
            [f"{PUBLIC_ORIGIN}/", f"{PUBLIC_ORIGIN}/demo.html"],
            submission_urls,
        )
        self.assertNotIn(f"{PUBLIC_ORIGIN}/product-manifest.json", section)
        self.assertNotIn(
            f"{PUBLIC_ORIGIN}/assets/product-hunt-gallery-01.png",
            section,
        )
        self.assertIn("public ownership token, not a secret", section)
        self.assertIn("does not prove indexing or revenue", section)
        self.assertIn("Repeated submissions are avoided", section)

    def test_sitemap_lists_only_canonical_public_pages_without_lastmod(self):
        sitemap_path = ROOT / "sitemap.xml"
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        namespace = {"sitemap": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locations = [
            element.text for element in root.findall("sitemap:url/sitemap:loc", namespace)
        ]

        self.assertEqual(
            [
                f"{PUBLIC_ORIGIN}/",
                f"{PUBLIC_ORIGIN}/demo.html",
                f"{PUBLIC_ORIGIN}/product-manifest.json",
                f"{PUBLIC_ORIGIN}/terms.html",
                f"{PUBLIC_ORIGIN}/privacy.html",
                f"{PUBLIC_ORIGIN}/refunds.html",
            ],
            locations,
        )
        self.assertEqual([], root.findall(".//sitemap:lastmod", namespace))
        self.assertEqual(len(locations), len(root.findall("sitemap:url", namespace)))

    def test_robots_allows_all_and_points_to_absolute_sitemap(self):
        robots_lines = (ROOT / "robots.txt").read_text(encoding="utf-8").splitlines()

        self.assertEqual(
            [
                "User-agent: *",
                "Allow: /",
                f"Sitemap: {PUBLIC_ORIGIN}/sitemap.xml",
            ],
            robots_lines,
        )

    def test_readme_documents_sitemap_and_robots_files(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn(f"{PUBLIC_ORIGIN}/sitemap.xml", readme)
        self.assertIn(f"{PUBLIC_ORIGIN}/robots.txt", readme)
        self.assertIn("No `lastmod` values", readme)

    def test_primary_checkout_button_meets_wcag_aa_contrast(self):
        stylesheet = (ROOT / "styles.css").read_text(encoding="utf-8")
        primary_rule = re.search(r"\.button-primary\s*\{(?P<body>[^}]*)\}", stylesheet, re.DOTALL)

        self.assertIsNotNone(primary_rule)
        colors = dict(
            re.findall(
                r"^\s*(background|color):\s*(#[0-9a-fA-F]{3,6})\s*;",
                primary_rule.group("body"),
                re.MULTILINE,
            )
        )
        self.assertGreaterEqual(contrast_ratio(colors["background"], colors["color"]), 4.5)

    def test_root_presents_downloadable_software_and_team_license(self):
        _, parser, text = parse("index.html")

        for phrase in (
            "Downloadable B2B software",
            "Agent Eval Kit Team License",
            "USD 1,000",
            "25 internal users",
            "Version 1.0.0",
            "Perpetual internal-use license",
            "No consulting",
            "No custom development",
            "payment processor confirms a completed, cleared payment",
            "within 24 hours",
            "71580501a6004ae63e2443a5b8bac61dd84411b3dccdd5ad532f002e45e515d7",
        ):
            self.assertIn(phrase, text)

        self.assertNotIn(
            "https://github.com/iisacc-Justmoong/agent-task-verifier-sample",
            parser.links,
        )
        self.assertIn("demo.html", parser.links)
        self.assertIn("product-manifest.json", parser.links)
        manifest = json.loads((ROOT / "product-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual("downloadable_software", manifest["product_type"])
        self.assertEqual("1.0.0", manifest["version"])
        self.assertEqual("agent-eval-kit-1.0.0.pyz", manifest["artifact"])
        self.assertEqual(
            "71580501a6004ae63e2443a5b8bac61dd84411b3dccdd5ad532f002e45e515d7",
            manifest["sha256"],
        )
        self.assertEqual(
            [{"internal_users": 25, "name": "Team License", "price_usd": 1000}],
            manifest["license_options"],
        )
        self.assertNotIn("Agent Eval Kit Individual License", text)
        self.assertNotIn("USD 250", text)
        stylesheet = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn("styles.css", parser.links)
        self.assertIn("overflow-wrap: anywhere", stylesheet)
        self.assertIn("minmax(0, 1fr)", stylesheet)

    def test_root_exposes_local_commercial_policies_and_direct_team_checkout(self):
        _, parser, text = parse("index.html")

        for link in ("terms.html", "privacy.html", "refunds.html"):
            self.assertIn(link, parser.links)
        self.assertEqual(2, parser.links.count(TEAM_CHECKOUT_URL))
        self.assertRegex(
            TEAM_CHECKOUT_URL,
            r"^https://www\.paypal\.com/ncp/payment/[A-Z0-9]+$",
        )
        self.assertFalse(
            any(
                link.startswith(
                    "mailto:andudyun0504@gmail.com?subject=Agent%20Eval%20Kit%20Team%20License"
                )
                for link in parser.links
            )
        )
        self.assertIn("Buy the Team License", text)
        self.assertIn("Checkout is hosted by PayPal", text)
        self.assertNotIn("Request the Team purchase link", text)
        self.assertFalse(
            any("Agent%20Eval%20Kit%20Individual%20License" in link for link in parser.links)
        )
        self.assertIn("licensed legal entity", text)

        source = (ROOT / "index.html").read_text(encoding="utf-8")
        hero = source[
            source.index('<section class="shell hero">') : source.index("</section>", source.index('<section class="shell hero">'))
        ]
        self.assertIn(TEAM_CHECKOUT_URL, hero)
        self.assertIn("Buy Team License · USD 1,000", hero)
        self.assertIn('href="demo.html"', hero)

    def test_root_publishes_canonical_social_purchase_metadata(self):
        _, parser, _ = parse("index.html")

        self.assertEqual(
            ["https://iisacc-justmoong.github.io/"],
            parser.canonical_links,
        )
        self.assertEqual("website", parser.meta["og:type"])
        self.assertEqual(
            "Agent Eval Kit | Offline Verification Software",
            parser.meta["og:title"],
        )
        self.assertEqual(
            "https://iisacc-justmoong.github.io/",
            parser.meta["og:url"],
        )
        self.assertIn("one-time Team License", parser.meta["og:description"])
        self.assertEqual(
            "https://iisacc-justmoong.github.io/assets/product-hunt-gallery-01.png",
            parser.meta["og:image"],
        )
        self.assertEqual("1270", parser.meta["og:image:width"])
        self.assertEqual("760", parser.meta["og:image:height"])
        self.assertEqual("summary_large_image", parser.meta["twitter:card"])
        self.assertEqual(parser.meta["og:image"], parser.meta["twitter:image"])

    def test_launch_artwork_has_exact_png_dimensions(self):
        expected_dimensions = {
            "product-hunt-thumbnail.png": (240, 240),
            "product-hunt-gallery-01.png": (1270, 760),
            "product-hunt-gallery-02.png": (1270, 760),
        }

        for filename, expected in expected_dimensions.items():
            with self.subTest(filename=filename):
                data = (ROOT / "assets" / filename).read_bytes()
                self.assertEqual(b"\x89PNG\r\n\x1a\n", data[:8])
                self.assertEqual(b"IHDR", data[12:16])
                self.assertEqual(expected, struct.unpack(">II", data[16:24]))

    def test_demo_publishes_reproducible_product_input_and_output(self):
        source, parser, text = parse("demo.html")

        for phrase in (
            "Exact Version 1.0.0 walkthrough",
            "python3 agent-eval-kit-1.0.0.pyz validate contract.json",
            "python3 agent-eval-kit-1.0.0.pyz evaluate contract.json passing-evidence.json",
            "fac5f172f0f48e750505e208354a8a2d6f7d3c12882f40519189852e92050aca",
            '"name": "command_exact"',
            '"passed": true',
            '"reward": 1.0',
            "The application validates recorded evidence; it does not execute customer code.",
        ):
            self.assertIn(phrase, text)

        self.assertIn("index.html", parser.links)
        self.assertEqual(2, parser.links.count(TEAM_CHECKOUT_URL))
        self.assertIn("styles.css?v=walkthrough-2", parser.links)
        self.assertEqual([], parser.scripts)
        self.assertNotIn("<iframe", source.lower())
        self.assertLess(source.index(TEAM_CHECKOUT_URL), source.index("<h2>1. Versioned task contract</h2>"))

    def test_policy_pages_cover_software_license_and_supported_payment_processors(self):
        expectations = {
            "terms.html": (
                "Terms of Sale and Software License",
                "Perpetual internal-use license",
                "No professional services",
                "Paddle",
                "PayPal",
            ),
            "privacy.html": (
                "Privacy Notice",
                "billing contact",
                "No telemetry",
                "Paddle",
                "PayPal",
            ),
            "refunds.html": (
                "Refund Policy",
                "downloadable software",
                "14 calendar days",
                "payment processor",
            ),
        }

        for page_name, phrases in expectations.items():
            with self.subTest(page=page_name):
                _, parser, text = parse(page_name)
                for phrase in phrases:
                    self.assertIn(phrase, text)
                self.assertIn("Effective July 21, 2026", text)
                self.assertIn("index.html", parser.links)
                self.assertIn("mailto:andudyun0504@gmail.com", parser.links)

        _, _, terms_text = parse("terms.html")
        self.assertIn("within 24 hours", terms_text)
        self.assertNotIn("Individual License", terms_text)

    def test_site_does_not_market_unsupported_human_services(self):
        prohibited = (
            "independent evaluation engineering",
            "written scope",
            "delivery window",
            "custom deliverables",
            "request the usd 1,000 audit",
            "work third",
        )
        for page_name in ("index.html", "demo.html", "terms.html", "privacy.html", "refunds.html"):
            with self.subTest(page=page_name):
                source = (ROOT / page_name).read_text(encoding="utf-8").lower()
                for phrase in prohibited:
                    self.assertNotIn(phrase, source)

    def test_payment_policies_keep_paypal_and_paddle_roles_distinct(self):
        for page_name in ("terms.html", "privacy.html", "refunds.html"):
            with self.subTest(page=page_name):
                source = (ROOT / page_name).read_text(encoding="utf-8")
                self.assertIn("Supplier remains the seller", source)
                self.assertIn("Paddle", source)
                self.assertIn("merchant of record", source)
                self.assertNotIn("PayPal acts as merchant of record", source)

    def test_site_keeps_a_static_no_embed_security_boundary(self):
        for page_name in ("index.html", "terms.html", "privacy.html", "refunds.html"):
            with self.subTest(page=page_name):
                source, parser, _ = parse(page_name)
                self.assertEqual([], parser.scripts)
                self.assertNotIn("<iframe", source.lower())
                self.assertNotIn("http://", source.lower())


if __name__ == "__main__":
    unittest.main()
