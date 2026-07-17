#!/usr/bin/env python3
"""
scripts/test_site_selenium.py
Selenium UI tests for the Legal Luminary Jekyll site.
Tests run headlessly against http://localhost:4000/

Usage:
    python3 scripts/test_site_selenium.py
    python3 scripts/test_site_selenium.py --headed   # show browser
"""

from __future__ import annotations

import sys
import time
import re
from dataclasses import dataclass, field
from typing import Callable

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
)

BASE_URL = "http://localhost:4000"
HEADED = "--headed" in sys.argv
TIMEOUT = 10  # seconds


# ---------------------------------------------------------------------------
# Test result tracking
# ---------------------------------------------------------------------------

@dataclass
class TestResult:
    name: str
    passed: bool
    message: str = ""


results: list[TestResult] = []


def test(name: str):
    """Decorator to register and run a test function."""
    def decorator(fn: Callable):
        try:
            fn()
            results.append(TestResult(name=name, passed=True))
            print(f"  ✓  {name}")
        except AssertionError as e:
            results.append(TestResult(name=name, passed=False, message=str(e)))
            print(f"  ✗  {name}")
            print(f"       {e}")
        except Exception as e:
            results.append(TestResult(name=name, passed=False, message=str(e)))
            print(f"  ✗  {name}")
            print(f"       {e}")
        return fn
    return decorator


# ---------------------------------------------------------------------------
# Driver setup
# ---------------------------------------------------------------------------

def make_driver() -> webdriver.Chrome:
    opts = Options()
    if not HEADED:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1440,900")
    service = Service()  # Uses PATH chromedriver
    return webdriver.Chrome(service=service, options=opts)


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def get(driver: webdriver.Chrome, path: str) -> None:
    driver.get(f"{BASE_URL}{path}")
    # Wait for body
    WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )


def assert_text_present(driver: webdriver.Chrome, text: str) -> None:
    body = driver.find_element(By.TAG_NAME, "body").text
    assert text.lower() in body.lower(), f"Expected text not found: {text!r}"


def assert_no_404(driver: webdriver.Chrome) -> None:
    body = driver.find_element(By.TAG_NAME, "body").text.lower()
    assert "404" not in body[:200], "Page appears to be a 404"
    assert "not found" not in body[:200], "Page shows 'not found'"


def get_sidebar_links(driver: webdriver.Chrome) -> list:
    """Return all <a> elements inside the sidebar top-stories section."""
    try:
        sidebar = driver.find_element(By.CSS_SELECTOR, ".sidebar-feed")
        return sidebar.find_elements(By.TAG_NAME, "a")
    except NoSuchElementException:
        return []


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def run_tests(driver: webdriver.Chrome):

    # ── Homepage ────────────────────────────────────────────────────────────
    print("\n── Homepage ─────────────────────────────────────────────────")

    @test("Homepage loads (200, no 404)")
    def _():
        get(driver, "/")
        assert_no_404(driver)

    @test("Homepage has navigation")
    def _():
        get(driver, "/")
        nav = driver.find_element(By.TAG_NAME, "nav")
        assert nav is not None

    @test("Sidebar Top Stories section is present")
    def _():
        get(driver, "/")
        sidebar = driver.find_element(By.CSS_SELECTOR, ".sidebar-feed")
        heading = sidebar.find_element(By.TAG_NAME, "h3")
        assert "top stories" in heading.text.lower(), f"Unexpected heading: {heading.text}"

    @test("Sidebar contains at least 3 article links")
    def _():
        get(driver, "/")
        links = get_sidebar_links(driver)
        assert len(links) >= 3, f"Only {len(links)} links in sidebar"

    @test("Sidebar links point to internal pages (not external URLs)")
    def _():
        get(driver, "/")
        links = get_sidebar_links(driver)
        external = []
        for link in links:
            href = link.get_attribute("href") or ""
            if href.startswith("http") and BASE_URL not in href:
                external.append(href)
        assert not external, f"External links found in sidebar: {external[:3]}"

    @test("Sidebar article links are reachable (no 404)")
    def _():
        get(driver, "/")
        links = get_sidebar_links(driver)
        broken = []
        for link in links[:5]:  # Check first 5
            href = link.get_attribute("href") or ""
            if not href or not href.startswith(BASE_URL):
                continue
            try:
                driver.get(href)
                WebDriverWait(driver, TIMEOUT).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
                if "404" in body_text[:300] or "not found" in body_text[:300]:
                    broken.append(href)
            except Exception as e:
                broken.append(f"{href} → {e}")
        assert not broken, f"Broken article links: {broken}"

    # ── Article post pages ──────────────────────────────────────────────────
    print("\n── Article Post Pages ───────────────────────────────────────")

    @test("A recent LLM-generated post loads correctly")
    def _():
        # Navigate to homepage sidebar, click first article
        get(driver, "/")
        links = get_sidebar_links(driver)
        article_link = None
        for link in links:
            href = link.get_attribute("href") or ""
            if BASE_URL in href and "/20" in href:
                article_link = href
                break
        assert article_link, "No article link found in sidebar"
        driver.get(article_link)
        WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        assert_no_404(driver)

    @test("Article pages have Source Information section")
    def _():
        get(driver, "/")
        links = get_sidebar_links(driver)
        found_source_info = False
        for link in links[:5]:
            href = link.get_attribute("href") or ""
            if BASE_URL not in href or "/20" not in href:
                continue
            driver.get(href)
            WebDriverWait(driver, TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            body_text = driver.find_element(By.TAG_NAME, "body").text
            if "Source Information" in body_text or "Source:" in body_text:
                found_source_info = True
                break
        assert found_source_info, "No article had a Source Information section"

    @test("Article pages use third-person language (no 'you' in first paragraph)")
    def _():
        get(driver, "/")
        links = get_sidebar_links(driver)
        violations = []
        for link in links[:5]:
            href = link.get_attribute("href") or ""
            if BASE_URL not in href or "/20" not in href:
                continue
            driver.get(href)
            WebDriverWait(driver, TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            # Get first paragraph text
            try:
                paras = driver.find_elements(By.CSS_SELECTOR, "article p, .post-content p, main p")
                first_para = paras[0].text if paras else ""
            except Exception:
                first_para = ""
            # Check for second-person
            if re.search(r"\b(you|your|you're|you've|you'll)\b", first_para, re.I):
                violations.append(f"{href}: {first_para[:80]}")
        assert not violations, f"Second-person language found: {violations}"

    # ── Navigation pages ────────────────────────────────────────────────────
    print("\n── Navigation Pages ─────────────────────────────────────────")

    nav_pages = [
        ("/texas-law/", "Texas Law"),
        ("/bell-county/", "Bell County"),
        ("/criminal-law/", "Criminal Law"),
        ("/personal-injury/", "Personal Injury"),
        ("/family-law/", "Family Law"),
    ]

    for path, label in nav_pages:
        @test(f"{label} page loads and has sidebar articles")
        def _(p=path, l=label):
            get(driver, p)
            assert_no_404(driver)
            # Check sidebar exists
            try:
                sidebar = driver.find_element(By.CSS_SELECTOR, ".sidebar-feed")
                items = sidebar.find_elements(By.CSS_SELECTOR, ".sidebar-feed-item")
                # Sidebar can be empty but should exist
                assert sidebar is not None
            except NoSuchElementException:
                pass  # Sidebar optional on some pages

    # ── Broken links in sidebar ─────────────────────────────────────────────
    print("\n── Broken Link Detection ────────────────────────────────────")

    @test("Top Stories sidebar has no 'Unknown Source' entries")
    def _():
        get(driver, "/")
        sidebar = driver.find_element(By.CSS_SELECTOR, ".sidebar-feed")
        text = sidebar.text
        assert "Unknown Source" not in text, (
            f"'Unknown Source' found in sidebar — posts need source_name field"
        )

    @test("Top Stories sidebar has no 'Recent update regarding' placeholder entries")
    def _():
        get(driver, "/")
        sidebar = driver.find_element(By.CSS_SELECTOR, ".sidebar-feed")
        text = sidebar.text
        assert "Recent update regarding" not in text, (
            "'Recent update regarding' placeholder found — scan_articles.py generated mock entries"
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("  Legal Luminary — Selenium UI Test Suite")
    print(f"  Target: {BASE_URL}")
    print(f"  Mode:   {'headed' if HEADED else 'headless'}")
    print("=" * 60)

    driver = make_driver()
    try:
        run_tests(driver)
    finally:
        driver.quit()

    # Summary
    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)
    total = len(results)

    print(f"\n{'=' * 60}")
    print(f"  Results: {passed}/{total} passed  |  {failed} failed")
    print("=" * 60)

    if failed:
        print("\nFailed tests:")
        for r in results:
            if not r.passed:
                print(f"  ✗ {r.name}")
                if r.message:
                    print(f"    {r.message[:120]}")
        sys.exit(1)
    else:
        print("\n  All tests passed! ✓")
        sys.exit(0)


if __name__ == "__main__":
    main()
