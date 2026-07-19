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
    def test_root_presents_two_fixed_scope_services_and_public_evidence(self):
        source, parser, text = parse("index.html")

        for phrase in (
            "Independent Agent Evaluation",
            "USD 1,000",
            "48 hours",
            "USD 250",
            "6 hours",
            "Cleared payment",
            "Public evidence",
        ):
            self.assertIn(phrase, text)

        self.assertIn(
            "https://iisacc-justmoong.github.io/agent-task-verifier-sample/offer.html",
            parser.links,
        )
        self.assertIn(
            "https://iisacc-justmoong.github.io/agent-task-verifier-sample/task-pack.html",
            parser.links,
        )
        stylesheet = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn("styles.css", parser.links)
        self.assertIn("overflow-wrap: anywhere", stylesheet)
        self.assertIn("minmax(0, 1fr)", stylesheet)

    def test_root_exposes_local_commercial_policies_and_email_intake(self):
        _, parser, text = parse("index.html")

        for link in ("terms.html", "privacy.html", "refunds.html"):
            self.assertIn(link, parser.links)
        self.assertTrue(
            any(
                link.startswith(
                    "mailto:andudyun0504@gmail.com?subject=Independent%20Agent%20Evaluation"
                )
                for link in parser.links
            )
        )
        self.assertIn("Billing contact", text)

    def test_policy_pages_cover_paddle_review_requirements(self):
        expectations = {
            "terms.html": (
                "Terms of Service",
                "Scope and acceptance criteria",
                "Authorized code and data",
                "Paddle",
            ),
            "privacy.html": (
                "Privacy Notice",
                "billing contact",
                "Paddle",
                "payment credentials",
            ),
            "refunds.html": (
                "Refund Policy",
                "full refund",
                "seven calendar days",
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

    def test_site_has_no_third_party_runtime_before_checkout_approval(self):
        for page_name in ("index.html", "terms.html", "privacy.html", "refunds.html"):
            with self.subTest(page=page_name):
                source, parser, _ = parse(page_name)
                self.assertEqual([], parser.scripts)
                self.assertNotIn("<iframe", source.lower())
                self.assertNotIn("http://", source.lower())


if __name__ == "__main__":
    unittest.main()
