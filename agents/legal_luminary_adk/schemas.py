"""Typed records passed between workflow nodes."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Classification = Literal[
    "ok",
    "redirected",
    "unverified",
    "blocked",
    "dead",
    "server_error",
    "unreachable",
    "not_allowed",
]


class LinkCheck(BaseModel):
    """Result of requesting one URL."""

    url: str
    classification: Classification
    status_code: int | None = None
    final_url: str | None = None
    error: str | None = None


class SourceAuditReport(BaseModel):
    """Every URL found in a set of pages, grouped by outcome."""

    checked: int
    dead: list[LinkCheck] = Field(default_factory=list)
    needs_manual_check: list[LinkCheck] = Field(default_factory=list)
    redirected: list[LinkCheck] = Field(default_factory=list)
    ok: list[LinkCheck] = Field(default_factory=list)


class Finding(BaseModel):
    """One factual claim with the exact source text that supports it."""

    claim: str = Field(description="The fact, stated neutrally in one sentence.")
    source_url: str = Field(description="The page the quote was copied from.")
    quote: str = Field(
        description="Verbatim text copied from the page that supports the claim."
    )
    source_type: Literal[
        "primary_government", "court_record", "news", "candidate", "other"
    ]
    as_of: str | None = Field(
        default=None, description="Date shown on the source, if any."
    )


class Findings(BaseModel):
    """Structured output of the research step."""

    question: str
    findings: list[Finding] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)


class VerifiedFinding(Finding):
    """A finding after the quote was re-checked against the live page."""

    verified: bool
    check: LinkCheck


class ResearchReport(BaseModel):
    """Final research output: verified findings kept, unverifiable ones set aside."""

    question: str
    verified: list[VerifiedFinding] = Field(default_factory=list)
    rejected: list[VerifiedFinding] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
