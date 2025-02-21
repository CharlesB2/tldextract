"""tldextract integration tests."""

import sys

import pytest

from tldextract.cli import main
from tldextract.tldextract import PUBLIC_SUFFIX_LIST_URLS


def test_cli_no_input(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test CLI without args."""
    monkeypatch.setattr(sys, "argv", ["tldextract"])
    with pytest.raises(SystemExit) as ex:
        main()

    assert ex.value.code == 1


def test_cli_parses_args(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test CLI with nonsense args."""
    monkeypatch.setattr(sys, "argv", ["tldextract", "--some", "nonsense"])
    with pytest.raises(SystemExit) as ex:
        main()

    assert ex.value.code == 2


def test_cli_posargs(
    capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test CLI with basic, positional args."""
    monkeypatch.setattr(
        sys, "argv", ["tldextract", "example.com", "bbc.co.uk", "forums.bbc.co.uk"]
    )

    main()

    stdout, stderr = capsys.readouterr()
    assert not stderr
    assert stdout == " example com\n bbc co.uk\nforums bbc co.uk\n"


def test_cli_namedargs(
    capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test CLI with basic, positional args, and that it parses an optional argument (though it doesn't change output)."""
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tldextract",
            "--suffix_list_url",
            PUBLIC_SUFFIX_LIST_URLS[0],
            "example.com",
            "bbc.co.uk",
            "forums.bbc.co.uk",
        ],
    )

    main()

    stdout, stderr = capsys.readouterr()
    assert not stderr
    assert stdout == " example com\n bbc co.uk\nforums bbc co.uk\n"
