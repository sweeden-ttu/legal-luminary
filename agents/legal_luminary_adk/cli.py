"""Command-line entry points used locally and in CI.

Examples
--------
python -m legal_luminary_adk.cli crawl --out site-map.json
python -m legal_luminary_adk.cli audit-sources _pages/texas-ag-race-26 --fail-on dead
python -m legal_luminary_adk.cli research "Who is Killeen's police chief?"
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from collections import Counter
from pathlib import Path

from google.adk.runners import InMemoryRunner
from google.genai import types

from . import tools, workflows


def _write(text: str) -> None:
    sys.stdout.write(text + "\n")


async def run_workflow(agent, text: str) -> list:
    """Run a workflow once in memory and return its events."""
    runner = InMemoryRunner(agent=agent, app_name="legal_luminary_adk")
    session = await runner.session_service.create_session(
        app_name="legal_luminary_adk", user_id="cli"
    )
    message = types.Content(role="user", parts=[types.Part(text=text)])
    return [
        e
        async for e in runner.run_async(
            user_id="cli", session_id=session.id, new_message=message
        )
    ]


def _final_text(events: list) -> str:
    texts = [
        p.text
        for e in events
        if e.content and e.content.parts
        for p in e.content.parts
        if p.text and not p.thought
    ]
    return texts[-1] if texts else ""


def cmd_crawl(args: argparse.Namespace) -> int:
    """Crawl a site and print counts by classification."""
    pages = tools.crawl_site(args.base, max_pages=args.max_pages)
    counts = Counter(p["classification"] for p in pages)
    orphans = sum(not p["in_sitemap"] for p in pages)
    _write(f"crawled {len(pages)} pages: {dict(counts)}; not in sitemap: {orphans}")
    if args.out:
        Path(args.out).write_text(json.dumps(pages, indent=1), encoding="utf-8")
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    """Check cited URLs; exit 1 on dead links when ``--fail-on dead``."""
    if args.llm:
        events = asyncio.run(
            run_workflow(workflows.build_source_audit_workflow(), "\n".join(args.paths))
        )
        _write(_final_text(events))
        report = None
    else:
        urls = workflows.collect_urls("\n".join(args.paths))
        report = tools.check_links(urls)
        _write(
            f"checked {report['checked']}: dead={len(report['dead'])} "
            f"manual={len(report['needs_manual_check'])} "
            f"redirected={len(report['redirected'])} ok={len(report['ok'])}"
        )
        for c in report["dead"]:
            _write(f"DEAD {c['status_code']} {c['url']}")
        for c in report["needs_manual_check"]:
            _write(f"CHECK {c['classification']} {c['status_code']} {c['url']}")
        if args.out:
            Path(args.out).write_text(json.dumps(report, indent=1), encoding="utf-8")
    if report and args.fail_on == "dead" and report["dead"]:
        return 1
    return 0


def cmd_research(args: argparse.Namespace) -> int:
    """Run the Claude research workflow for one question."""
    events = asyncio.run(
        run_workflow(workflows.build_research_workflow(), args.question)
    )
    _write(_final_text(events))
    if args.out:
        outputs = [e.output for e in events if isinstance(e.output, dict)]
        Path(args.out).write_text(
            json.dumps(outputs[-1] if outputs else {}, indent=1), encoding="utf-8"
        )
    return 0


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and dispatch to a subcommand."""
    parser = argparse.ArgumentParser(prog="legal_luminary_adk")
    sub = parser.add_subparsers(dest="command", required=True)

    crawl = sub.add_parser("crawl", help="map every public page on a site")
    crawl.add_argument("--base", default="https://legalluminary.com/")
    crawl.add_argument("--max-pages", type=int, default=500)
    crawl.add_argument("--out")
    crawl.set_defaults(func=cmd_crawl)

    audit = sub.add_parser("audit-sources", help="check every URL cited in pages")
    audit.add_argument("paths", nargs="+", help="markdown files, directories or URLs")
    audit.add_argument("--fail-on", choices=["dead", "never"], default="never")
    audit.add_argument(
        "--llm", action="store_true", help="have Claude write the fix list"
    )
    audit.add_argument("--out")
    audit.set_defaults(func=cmd_audit)

    research = sub.add_parser(
        "research", help="answer a question from official sources"
    )
    research.add_argument("question")
    research.add_argument("--out")
    research.set_defaults(func=cmd_research)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
