"""Private per-thread store of inputs: attachedtomessageN / link_id_N / thread.json."""
import json
import os
import stat
import sys
from email.message import EmailMessage
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "agents"))

from meseeks import store  # noqa: E402

JPG = b"\xff\xd8\xff\xe0" + b"clip" * 50


def mail(mid, body, attachments=(), refs=None, subject="Fwd: KDH legal notices"):
    m = EmailMessage()
    m["From"], m["To"], m["Subject"], m["Message-ID"] = "Scott Weeden <sweeden.ttu@gmail.com>", "meseeks@legalluminary.com", subject, mid
    if refs:
        m["In-Reply-To"] = m["References"] = refs
    m.set_content(body)
    for name, data, maintype, subtype in attachments:
        m.add_attachment(data, maintype=maintype, subtype=subtype, filename=name)
    return m.as_bytes()


def test_thread_layout_dedupes_and_is_private(tmp_path):
    base = tmp_path / "mail_attachments"
    r1 = store.store(mail("<a@x>", "see https://app.audioscribe.io/share/abc", [("one.jpg", JPG, "image", "jpeg"), ("two.jpg", JPG + b"2", "image", "jpeg")]), base)
    r2 = store.store(mail("<b@x>", "same clipping again https://app.audioscribe.io/share/abc", [("one-copy.jpg", JPG, "image", "jpeg")], refs="<a@x>"), base)
    r3 = store.store(mail("<c@x>", "a new matter", [("pkg.zip", b"PK\x03\x04zip", "application", "zip")], subject="Waco filing"), base)
    assert r1["thread"] == r2["thread"] == "thread_id_0" and r3["thread"] == "thread_id_1"
    t0 = base / "thread_id_0"
    assert sorted(p.name for p in t0.iterdir()) == ["attachedtomessage1.jpg", "attachedtomessage2.jpg", "link_id_0", "thread.json"]
    assert (t0 / "link_id_0").read_text() == "https://app.audioscribe.io/share/abc"
    meta = json.loads((t0 / "thread.json").read_text())
    assert meta["messages"][1]["attachments"][0]["duplicate_of"] == "attachedtomessage1.jpg"
    assert (base / "thread_id_1" / "attachedtomessage1.zip").read_bytes() == b"PK\x03\x04zip"   # archives are kept, never opened
    assert stat.S_IMODE(os.stat(t0).st_mode) == 0o700 and stat.S_IMODE(os.stat(t0 / "attachedtomessage1.jpg").st_mode) == 0o600
    assert store.store(mail("<a@x>", "resent"), base).get("duplicate_message")
    store.record_output("thread_id_0", {"post": "042475922c", "category": "notice"}, base)
    assert json.loads((t0 / "thread.json").read_text())["outputs"][0]["post"] == "042475922c"


def test_existing_hand_made_folders_are_respected(tmp_path):
    base = tmp_path / "mail_attachments"
    (base / "thread_id_0").mkdir(parents=True)
    (base / "thread_id_1").mkdir()
    assert store.store(mail("<z@x>", "new"), base)["thread"] == "thread_id_2"
