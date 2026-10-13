"""Shared fixtures for the ADK agent tests."""

import sys
from pathlib import Path

import httpx
import pytest
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.genai import types

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "agents"))

from legal_luminary_adk import tools  # noqa: E402


class FakeLlm(BaseLlm):
    """Returns scripted text responses in order and records every request."""

    def __init__(self, responses: list[str]):
        super().__init__(model="fake-claude")
        self._responses = list(responses)
        self._requests = []

    @property
    def requests(self):
        return self._requests

    async def generate_content_async(self, llm_request, stream=False):
        self._requests.append(llm_request)
        yield LlmResponse(
            content=types.Content(
                role="model", parts=[types.Part(text=self._responses.pop(0))]
            )
        )


def html(title: str, body: str, links: tuple[str, ...] = ()) -> str:
    anchors = "".join(f'<a href="{u}">{u}</a>' for u in links)
    return (
        f"<html><head><title>{title}</title><script>var x='hidden';</script></head>"
        f"<body><p>{body}</p>{anchors}</body></html>"
    )


def make_pdf(text: str) -> bytes:
    """Build a one-page PDF whose page shows ``text`` in Helvetica."""
    stream = f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET".encode()
    objects = [
        b"<</Type/Catalog/Pages 2 0 R>>",
        b"<</Type/Pages/Kids[3 0 R]/Count 1>>",
        b"<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R"
        b"/Resources<</Font<</F1 5 0 R>>>>>>",
        b"<</Length %d>>stream\n" % len(stream) + stream + b"\nendstream",
        b"<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % i + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
    out += b"".join(b"%010d 00000 n \n" % o for o in offsets)
    out += b"trailer <</Size %d/Root 1 0 R>>\nstartxref\n%d\n%%%%EOF\n" % (
        len(objects) + 1,
        xref,
    )
    return bytes(out)


@pytest.fixture
def mock_web(monkeypatch):
    """Route HTTP requests to an in-memory site: {url: (status, html or PDF bytes, location)}."""
    routes: dict[str, tuple] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        status, body, location = routes.get(url, (404, "not found", None))
        if isinstance(body, bytes):
            headers = {"content-type": "application/pdf"}
            response = httpx.Response(status, content=body, headers=headers)
        else:
            headers = {"content-type": "text/html; charset=utf-8"}
            response = httpx.Response(status, text=body, headers=headers)
        if location:
            response.headers["location"] = location
        return response

    monkeypatch.setattr(tools, "HTTP_TRANSPORT", httpx.MockTransport(handler))
    return routes
