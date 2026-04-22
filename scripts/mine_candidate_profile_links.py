#!/usr/bin/env python3
"""Ensure candidate JSON has facebook_url, linkedin_url, instagram_url, campaign_website.

Fills from existing articles[] when fields are missing or empty. Excludes government,
news, and aggregator hosts for campaign_website. Special-case delsina_west official site.
"""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1] / "_data" / "candidates"

EXCLUDE_WEB_EXACT = {
    "ballotpedia.org",
    "killeentexas.gov",
    "ethics.state.tx.us",
    "google.com",
    "facebook.com",
    "m.facebook.com",
    "l.facebook.com",
    "lm.facebook.com",
    "linkedin.com",
    "instagram.com",
    "twitter.com",
    "x.com",
    "youtube.com",
    "youtu.be",
    "goodparty.org",
    "kdhnews.com",
    "tdtnews.com",
    "news.google.com",
    "docs.google.com",
    "civicengage.com",
}


def _host(url: str) -> str:
    try:
        h = urlparse(url).netloc.lower()
        if h.startswith("www."):
            return h[4:]
        return h
    except Exception:
        return ""


def _excluded_campaign_host(host: str) -> bool:
    if not host or host in EXCLUDE_WEB_EXACT:
        return True
    if host.endswith(".gov") or host.endswith(".state.tx.us"):
        return True
    return False


def mine_from_articles(articles: list) -> tuple[str, str, str, str]:
    fb = li = ig = web = ""
    for a in articles or []:
        url = (a.get("url") or "").strip()
        if not url:
            continue
        ul = url.lower()
        if not fb and "facebook.com" in ul and "/sharer/" not in ul:
            fb = url.split("?")[0].rstrip("/")
        if not li and "linkedin.com/in/" in ul:
            li = url.split("?")[0].rstrip("/")
        if not ig and "instagram.com/" in ul:
            ig = url.split("?")[0].rstrip("/")
        if not web:
            h = _host(url)
            if h and not _excluded_campaign_host(h):
                web = url.split("?")[0].rstrip("/")
    return fb, li, ig, web


def main() -> None:
    for city_dir in sorted(ROOT.iterdir()):
        if not city_dir.is_dir() or city_dir.name.startswith("."):
            continue
        for path in sorted(city_dir.glob("*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            articles = data.get("articles") or []
            slug = (data.get("candidate_slug") or "").strip()
            fbm, lim, igm, webm = mine_from_articles(articles)
            if slug == "delsina_west":
                webm = "https://www.delsinawestforkilleen.com/"
                fbm = "https://www.facebook.com/61588057174550"
                lim = lim or "https://www.linkedin.com/in/delsina-west-0ab0a9110"
            changed = False
            if slug == "delsina_west":
                for key, val in (
                    ("facebook_url", fbm),
                    ("linkedin_url", lim),
                    ("instagram_url", igm),
                    ("campaign_website", webm),
                ):
                    if data.get(key) != val:
                        data[key] = val
                        changed = True
            else:
                for key, mined in (
                    ("facebook_url", fbm),
                    ("linkedin_url", lim),
                    ("instagram_url", igm),
                    ("campaign_website", webm),
                ):
                    cur = data.get(key)
                    if cur is None or (isinstance(cur, str) and cur.strip() == ""):
                        if mined:
                            data[key] = mined
                            changed = True
                        elif key not in data:
                            data[key] = ""
                            changed = True
                    elif key not in data:
                        data[key] = cur if isinstance(cur, str) else ""
                        changed = True
                for key in (
                    "facebook_url",
                    "linkedin_url",
                    "instagram_url",
                    "campaign_website",
                ):
                    if key not in data:
                        data[key] = ""
                        changed = True
            if changed:
                path.write_text(
                    json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )


if __name__ == "__main__":
    main()
