import hashlib

import pytest

from pullmc.core.http import HttpClient
from pullmc.core.http import Cancelled  # noqa: F401  (public API check)
from pullmc.errors import PullMCError


def test_download_resumes_with_range(server, workdir):
    data = b"0123456789" * 100
    server.route("/file.bin", data)
    dest = workdir / "client.jar"
    part = dest.with_name(dest.name + ".part")
    part.write_bytes(data[:500])
    assert HttpClient().download((server.url("/file.bin"),), dest, sha1=hashlib.sha1(data).hexdigest())
    assert dest.read_bytes() == data
    assert not part.exists()
    headers = [entry[1] for entry in server.requests if entry[0] == "/file.bin"]
    assert any(h.get("Range") == "bytes=500-" for h in headers)


def test_ignored_range_restarts_from_zero(server, workdir):
    data = b"abcdef" * 300
    server.route("/file.bin", data, ignore_range=True)
    dest = workdir / "client.jar"
    part = dest.with_name(dest.name + ".part")
    part.write_bytes(data[:400])
    assert HttpClient().download((server.url("/file.bin"),), dest)
    assert dest.read_bytes() == data
    assert not part.exists()


def test_get_json_skips_html_portal_page(server):
    server.route("/bad.json", b"<html>not a mirror</html>", headers={"Content-Type": "text/html"})
    server.route("/good.json", b'{"versions": []}', headers={"Content-Type": "application/json"})
    client = HttpClient()
    assert client.get_json((server.url("/bad.json"), server.url("/good.json"))) == {"versions": []}


def test_download_sha1_mismatch_raises(server, workdir):
    server.route("/file.bin", b"broken payload")
    dest = workdir / "client.jar"
    with pytest.raises(PullMCError) as info:
        HttpClient().download(
            (server.url("/file.bin"),),
            dest,
            sha1=hashlib.sha1(b"different").hexdigest(),
        )
    assert info.value.code == "download_failed"
    assert not dest.exists()
    assert not dest.with_name(dest.name + ".part").exists()
