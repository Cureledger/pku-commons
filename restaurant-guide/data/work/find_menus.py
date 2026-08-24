"""Find a posted-menu URL on each restaurant's own website.

Does not fetch guide.michelin.com. Writes one JSON line per kitchen to
data/work/menu-find/results.jsonl so it can resume.
"""
from __future__ import annotations

import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
REG = ROOT / "data" / "restaurants.json"
OUT = ROOT / "data" / "work" / "menu-find" / "results.jsonl"
DONE = {"asheville-nc-us", "copenhagen-dk", "dublin-ie", "orlando-fl-us"}

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 PhebeEats/1.0"
TIMEOUT = 8
WORKERS = 16

SKIP_HOST = (
    "instagram.com",
    "www.instagram.com",
    "facebook.com",
    "www.facebook.com",
    "m.facebook.com",
    "twitter.com",
    "x.com",
    "tripadvisor.com",
    "www.tripadvisor.com",
    "yelp.com",
    "www.yelp.com",
    "guide.michelin.com",
)

MENU_RE = re.compile(
    r"(menu|menus|carta|karte|speisekarte|a-la-carte|alacarte|"
    r"la-carte|our-menu|food-menu|dining-menu|lunch-menu|dinner-menu|"
    r"%E3%83%A1%E3%83%8B%E3%83%A5%E3%83%BC)",
    re.I,
)
NOT_MENU_RE = re.compile(
    r"(wine-menu|drink|cocktail|bar-menu|beverage|happy-hour|gift|job|careers|press)",
    re.I,
)
PATHS = (
    "/menu",
    "/menus",
    "/menu/",
    "/menus/",
    "/food",
    "/carta",
    "/la-carte",
    "/a-la-carte",
)


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        self._href = dict(attrs).get("href")
        self._text = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._href:
            self.links.append((self._href, "".join(self._text)))
            self._href = None


def host_of(url: str) -> str:
    return urlparse(url).netloc.lower().removeprefix("www.")


def is_skipped(url: str) -> bool:
    host = urlparse(url).netloc.lower()
    return any(host == s or host.endswith("." + s) for s in SKIP_HOST)


def fetch(url: str) -> tuple[int, str, str]:
    req = Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    try:
        with urlopen(req, timeout=TIMEOUT) as resp:
            final = resp.geturl()
            raw = resp.read(400_000)
            ctype = resp.headers.get("Content-Type", "")
            if "html" not in ctype.lower() and "text" not in ctype.lower():
                return resp.status, final, ""
            return resp.status, final, raw.decode("utf-8", "replace")
    except HTTPError as exc:
        return exc.code, url, ""
    except (URLError, TimeoutError, OSError):
        return 0, url, ""


def menu_from_html(base: str, html: str) -> str | None:
    parser = LinkParser()
    try:
        parser.feed(html)
    except Exception:
        return None
    scored: list[tuple[int, str]] = []
    for href, text in parser.links:
        if not href or href.startswith("#") or href.startswith("mailto:"):
            continue
        absolute = urljoin(base, href)
        if is_skipped(absolute):
            continue
        blob = f"{href} {text}"
        if NOT_MENU_RE.search(blob):
            continue
        if MENU_RE.search(blob):
            scored.append((2 if MENU_RE.search(text) else 1, absolute))
    if not scored:
        return None
    scored.sort(reverse=True)
    return scored[0][1]


def find_one(website: str) -> str | None:
    if is_skipped(website):
        return None
    status, final, html = fetch(website)
    if status and 200 <= status < 400 and html:
        hit = menu_from_html(final, html)
        if hit:
            return hit
        if MENU_RE.search(urlparse(final).path):
            return final
    origin = f"{urlparse(website).scheme}://{urlparse(website).netloc}"
    for path in PATHS:
        url = origin + path
        status, final, html = fetch(url)
        if status and 200 <= status < 400:
            return final or url
    return None


def load_done() -> set[str]:
    if not OUT.exists():
        return set()
    slugs = set()
    for line in OUT.read_text().splitlines():
        if not line.strip():
            continue
        slugs.add(json.loads(line)["slug"])
    return slugs


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    done = load_done()
    reg = json.loads(REG.read_text())
    jobs = []
    for restaurant in reg["restaurants"]:
        if restaurant["city_id"] in DONE:
            continue
        if restaurant.get("menu_urls"):
            continue
        website = (restaurant.get("website") or "").strip()
        if not website or restaurant["slug"] in done:
            continue
        jobs.append((restaurant["slug"], restaurant["city_id"], website))
    print(f"queued {len(jobs)} skipped {len(done)}", flush=True)
    found = missed = 0
    t0 = time.time()
    with OUT.open("a", encoding="utf-8") as fh, ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {
            pool.submit(find_one, website): (slug, cid, website)
            for slug, cid, website in jobs
        }
        for i, fut in enumerate(as_completed(futures), 1):
            slug, cid, website = futures[fut]
            try:
                menu = fut.result()
            except Exception:
                menu = None
            row = {
                "slug": slug,
                "city_id": cid,
                "website": website,
                "menu_url": menu,
            }
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            fh.flush()
            if menu:
                found += 1
            else:
                missed += 1
            if i % 50 == 0 or i == len(jobs):
                print(
                    f"{i}/{len(jobs)} found {found} miss {missed} "
                    f"{int(time.time() - t0)}s",
                    flush=True,
                )
    print(f"done found {found} miss {missed}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
