from pullmc.errors import PullMCError


def test_error_carries_code_message_detail():
    err = PullMCError(
        "net_timeout",
        "下载超时",
        "GET https://example/1.20.1.json",
    )
    assert err.code == "net_timeout"
    assert str(err) == "下载超时"
    assert err.detail == "GET https://example/1.20.1.json"
    assert isinstance(err, Exception)
