from __future__ import unicode_literals

import pytest

from pip_reqs.parser import RequirementsParser

from ..compat import get_requirement_tracker


DEFAULT_INDEX_URL = "https://pypi.org/simple"

SETUP_PY = """
from setuptools import setup, find_packages

setup(
    name = 'Test Package',
    version = '1.0.0',
    url = 'https://github.com/test.git',
    author = 'Author Name',
    author_email = 'author@gmail.com',
    description = 'Description of test package',
    packages = find_packages(),
    install_requires = {requirements!r},
)
"""


@pytest.mark.parametrize(
    "reqs,expected_ext,expected_local",
    [
        ("", [], []),
        ("django", ["django"], []),
        ("django==2.0", ["django==2.0"], []),
        (
            "https://github.com/django/django/master.zip",
            ["https://github.com/django/django/master.zip"],
            [],
        ),
        (
            "https://github.com/django/django/master.zip#egg=django==3.1.4",
            ["https://github.com/django/django/master.zip#egg=django==3.1.4"],
            [],
        ),
        (
            "django @ https://files.pythonhosted.org/packages/12/13/78e8622180f101e95297965045ff1325ea7301c1b80f756debbeaa84c3be/Django-4.2.1-py3-none-any.whl",  # NOQA
            [
                "https://files.pythonhosted.org/packages/12/13/78e8622180f101e95297965045ff1325ea7301c1b80f756debbeaa84c3be/Django-4.2.1-py3-none-any.whl",  # NOQA
            ],
            [],
        ),
    ],
)
def test_requirements_parser_parse(reqs, expected_ext, expected_local, tmp_path):
    reqs_in = tmp_path / "requirements.in"
    reqs_in.write_text(reqs)

    with get_requirement_tracker() as req_tracker:
        parser = RequirementsParser(
            req_tracker=req_tracker, index_url=DEFAULT_INDEX_URL
        )
        ext_reqs, local_reqs = parser.parse(str(reqs_in))

    assert ext_reqs == expected_ext
    assert local_reqs == expected_local


@pytest.mark.parametrize(
    "local_reqs,expected_ext,expected_local",
    [(["django"], ["django"], ["-e file://{tmpdir}/local"])],
)
def test_requirements_parser_parse_local(
    local_reqs, expected_ext, expected_local, tmp_path
):
    expected_local = [e.format(tmpdir=tmp_path) for e in expected_local]

    pkg = tmp_path / "local"
    pkg.mkdir()
    (pkg / "setup.py").write_text(SETUP_PY.format(requirements=local_reqs))

    reqs_in = tmp_path / "requirements.in"
    reqs_in.write_text("-e {}".format(pkg))

    with get_requirement_tracker() as req_tracker:
        parser = RequirementsParser(
            req_tracker=req_tracker, index_url=DEFAULT_INDEX_URL
        )
        ext_reqs, local_reqs = parser.parse(str(reqs_in))

    assert ext_reqs == expected_ext
    assert local_reqs == expected_local


@pytest.mark.parametrize("reqs", ["-e git+https://github.com/project.git#egg=test"])
def test_requirements_parser_parse_error(reqs, tmp_path):
    reqs_in = tmp_path / "requirements.in"
    reqs_in.write_text(reqs)

    with get_requirement_tracker() as req_tracker:
        parser = RequirementsParser(
            req_tracker=req_tracker, index_url=DEFAULT_INDEX_URL
        )
        with pytest.raises(NotImplementedError):
            parser.parse(str(reqs_in))
