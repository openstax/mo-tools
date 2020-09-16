# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import pytest

import tldextract

from tests.utils import gen_from_file, skip_if_destructive_and_sensitive

import json
import urllib
from urllib.request import urlopen

DATA_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)), "data", "cops")


@pytest.fixture
def webview_base_url(request):
    """Return a base URL for CNX webview"""
    config = request.config
    base_url = config.getoption("webview_base_url") or config.getini("webview_base_url")
    if base_url is not None:
        skip_if_destructive_and_sensitive(request, base_url)
        return base_url


@pytest.fixture
def rex_base_url(request):
    """Return a base URL for REX used for integration testing"""
    config = request.config
    base_url = config.getoption("rex_base_url") or config.getini("rex_base_url")
    if base_url is not None:
        skip_if_destructive_and_sensitive(request, base_url)
        return base_url


@pytest.fixture
def cops_base_url(request):
    """Return a base URL for cops"""
    config = request.config
    base_url = config.getoption("cops_base_url") or config.getini("cops_base_url")
    if base_url is not None:
        skip_if_destructive_and_sensitive(request, base_url)
        return base_url


@pytest.fixture
def webview_instance(webview_base_url):
    url = tldextract.extract(webview_base_url)
    if url.subdomain:
        return url.subdomain
    else:
        return "prod"


@pytest.fixture
def s3_base_url(request):
    """Return a base URL for AWS S3 bucket"""
    config = request.config
    base_url = config.getoption("s3_base_url") or config.getini("s3_base_url")
    if base_url is not None:
        skip_if_destructive_and_sensitive(request, base_url)
        return base_url


@pytest.fixture(params=gen_from_file(os.path.join(DATA_DIR, "s3_books_uuids.txt")))
def s3_all_books_uuids(request):
    """Yields UUIDs for all books in aws s3 bucket
    """
    yield request.param


@pytest.fixture
def s3_books_url(s3_base_url, s3_all_books_uuids):
    """Return a base URL for AWS S3 bucket"""
    s3_url = f"{s3_base_url}/contents/{s3_all_books_uuids}.json"
    return s3_url


@pytest.fixture
def s3_books_titles():
    """Returns the book titles for books in aws s3 bucket
    """
    data_file = DATA_DIR + "/s3_books_titles.txt"

    with open(data_file, "r") as infile:
        data = infile.read()
    return data.strip()


@pytest.fixture
def cops_api_url(cops_base_url):
    """Return URL for cops api"""
    api_url = f"{cops_base_url}/api/jobs"
    return api_url


@pytest.fixture
def job_dialog_button():
    """  Return xpath of the 'Create a new pdf job' button """
    create_new_pdf_job = '// *[ @ id = "app"] / div[1] / main / div / div / div / div / div[1] / button / span / span'
    return create_new_pdf_job


@pytest.fixture
def create_button():
    """  Return xpath of the 'Create button' """
    create_button = '//*[@id="app"]/div[3]/div/div/div[3]/button[2]/span'
    return create_button


@pytest.fixture
def cops_json_data(cops_api_url):
    api_page = urllib.request.urlopen(cops_api_url).read()
    api_jdata = json.loads(api_page)
    return api_jdata


@pytest.fixture
def new_cops_job0(cops_json_data):
    new_job0 = cops_json_data[0]
    return new_job0


@pytest.fixture
def new_cops_job_id0(new_cops_job0):
    job_id0 = new_cops_job0["id"]
    return job_id0


@pytest.fixture
def new_cops_job1(cops_json_data):
    new_job1 = cops_json_data[1]
    return new_job1


@pytest.fixture
def new_cops_job_id1(new_cops_job1):
    job_id1 = new_cops_job1["id"]
    return job_id1


# @pytest.fixture
# def latest_job_json_data_for_pdf_verification(cops_api_url):
#     api_page = urllib.request.urlopen(cops_api_url).read()
#     api_jdata = json.loads(api_page)

#     newest0 = api_jdata[0]
#     pdf_url0 = newest0["pdf_url"]
#     id0 = newest0["id"]
#     collection_id0 = newest0["collection_id"]
#     collection_version0 = newest0["version"]
#     collection_server0 = newest0["content_server"]["name"]
