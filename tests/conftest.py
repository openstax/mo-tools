# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os

import pytest

from dotenv import load_dotenv


# Import fixtures
pytest_plugins = (
    "fixtures.base",
    "fixtures.github",
    "fixtures.snapshot",
    "fixtures.archive",
    "fixtures.cops",
    "fixtures.webview",
)
# "fixtures.applitools",


def get_custom_markers():
    """Function used to register custom markers.

    """
    return (
        "slow: mark tests that are slow",
        "rex: mark tests that are REX specific",
        "requires_publishing: mark tests that require publishing being deployed",
        "requires_varnish_routing: mark tests that require varnish routing",
        "requires_complete_dataset: mark tests that require the complete dataset",
        "requires_deployment: mark tests that require deployment",
        "awss3: mark tests that target collections in aws s3 bucket",
        "archive: mark tests that target archive",
    )


# Load environment variables from .env file
DOTENV_PATH = os.path.join(os.path.realpath(os.path.dirname(__file__)), "../.env")
load_dotenv(dotenv_path=DOTENV_PATH)


def pytest_configure(config):
    for marker in get_custom_markers():
        config.addinivalue_line("markers", marker)


def pytest_addoption(parser):
    group = parser.getgroup("selenium", "selenium")
    group.addoption(
        "--disable-dev-shm-usage",
        action="store_true",
        default=os.getenv("DISABLE_DEV_SHM_USAGE", False),
        help="disable chrome's usage of /dev/shm. (used by Travis)",
    )
    group.addoption(
        "--headless",
        action="store_true",
        default=os.getenv("HEADLESS", False),
        help="enable headless mode for chrome. So chrome does not interrupt you.",
    )
    group.addoption(
        "--no-sandbox",
        action="store_true",
        default=os.getenv("NO_SANDBOX", False),
        help="disable chrome's sandbox. (used by Travis)",
    )
    group.addoption(
        "--print-page-source-on-failure",
        action="store_true",
        default=os.getenv("PRINT_PAGE_SOURCE_ON_FAILURE", False),
        help="print page source to stdout when a test fails. (used by Travis)",
    )
    parser.addoption(
        "--github-token",
        default=os.getenv("GITHUB_TOKEN", None),
        help="OAuth token used to login to GitHub.",
    )
    # parser.addoption(
    #     "--applitools-key",
    #     default=os.getenv("APPLITOOLS_API_KEY", None),
    #     help="OAuth key used to login to Applitools.",
    # )
    parser.addoption(
        "--runslow",
        action="store_true",
        default=os.getenv("RUNSLOW", False),
        help="run slow tests (necessary for legacy tests).",
    )
    # Adapted from:
    # https://github.com/pytest-dev/pytest-base-url/blob/master/pytest_base_url/plugin.py#L51
    parser.addini("archive_base_url", help="base url for CNX archive.")
    parser.addoption(
        "--archive_base_url",
        metavar="url",
        default=os.getenv("ARCHIVE_BASE_URL", None),
        help="base url for CNX archive.",
    )
    # Adapted from:
    # https://github.com/pytest-dev/pytest-base-url/blob/master/pytest_base_url/plugin.py#L51
    parser.addini("archive2_base_url", help="base url for CNX archive.")
    parser.addoption(
        "--archive2_base_url",
        metavar="url",
        default=os.getenv("ARCHIVE2_BASE_URL", None),
        help="base url for CNX archive.",
    )
    parser.addini("webview_base_url", help="base url for CNX webview.")
    parser.addoption(
        "--webview_base_url",
        metavar="url",
        default=os.getenv("WEBVIEW_BASE_URL", None),
        help="base url for CNX webview.",
    )
    parser.addini("webview2_base_url", help="base url for CNX webview.")
    parser.addoption(
        "--webview2_base_url",
        metavar="url",
        default=os.getenv("WEBVIEW2_BASE_URL", None),
        help="base url for CNX webview.",
    )
    parser.addini("rex_base_url", help="base url for REX.")
    parser.addoption(
        "--rex_base_url",
        metavar="url",
        default=os.getenv("REX_BASE_URL", None),
        help="base url for REX.",
    )
    parser.addini("vendor_base_url", help="base url for Vendor cnx books.")
    parser.addoption(
        "--vendor_base_url",
        metavar="url",
        default=os.getenv("VENDOR_BASE_URL", None),
        help="base url for Vendor cnx books.",
    )
    parser.addini("s3_base_url", help="base url for cnx books in aws s3 bucket.")
    parser.addoption(
        "--s3_base_url",
        metavar="url",
        default=os.getenv("S3_BASE_URL", None),
        help="base url for cnx books in aws s3 bucket.",
    )
    parser.addini("cops_base_url", help="base url for cops.")
    parser.addoption(
        "--cops_base_url",
        metavar="url",
        default=os.getenv("COPS_BASE_URL", None),
        help="base url for cops.",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


# https://docs.pytest.org/en/latest/example/simple.html#making-test-result-information-available-in-fixtures
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can be "setup", "call", "teardown"
    # can be used by yield fixtures to determine if the test failed (see selenium fixture)
    setattr(item, "rep_{when}".format(when=rep.when), rep)


@pytest.hookimpl(hookwrapper=True)
def pytest_terminal_summary(terminalreporter):
    yield

    for report in terminalreporter.getreports(""):
        if report.when == "teardown":
            for (name, value) in report.user_properties:
                if name == "terminal_summary_message":
                    print(value)
