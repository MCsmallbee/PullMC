import re

from pullmc import __version__, __version_label__


def test_package_version_is_pep440_friendly() -> None:
    assert re.fullmatch(r"\d+(?:\.\d+){2,3}", __version__)


def test_public_version_label_follows_project_scheme() -> None:
    assert __version__ == "0.0.0.20261107"
    assert __version_label__ == "0.0.0.20261107_alpha(Biscuit)"
