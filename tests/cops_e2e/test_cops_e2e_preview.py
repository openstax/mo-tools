import requests
import pytest

import json
import urllib
from urllib.request import urlopen

from urllib.error import HTTPError, URLError
from requests.exceptions import ConnectionError

import time

from pages.cops.home import Home

"""
End to end test of cops(-staging).openstax.org
Creates jobs for 2 collections, verifies that they were successfully executed and pdf is created with content
Latest update on 03/06/2020
"""


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.nondestructive
@pytest.mark.parametrize(
    "colid, vers, style, serv",
    [("col11992", "1.8", "astronomy", "qa"), ("col26069", "latest", "chemistry", "staging")],
)
def test_create_cops_preview_jobs(selenium, cops_base_url, colid, vers, style, serv):

    # GIVEN: Selenium driver and the base url

    # GIVEN a cops base URL
    # WHEN making a request to cops

    try:

        # verifying that cops URL is active
        response = requests.get(cops_base_url)

    except HTTPError:
        pytest.exit("<<<<<<<<<< HTTP Error: COPS URL IS INVALID OR UNREACHABLE >>>>>>>>>>")
    except URLError:
        pytest.exit("<<<<<<<<<< URL Error: COPS URL IS INVALID OR UNREACHABLE >>>>>>>>>>")
    except ConnectionError:
        pytest.exit("<<<<<<<<<< Connection Error: COPS URL IS INVALID OR UNREACHABLE >>>>>>>>>>")

    else:

        # WHEN: The Home page is fully loaded
        home = Home(selenium, cops_base_url).open()

        # AND: Modal window opens
        modal = home.click_create_new_pdf_button()

        modal.click_distribution_preview_radio_button()

        # AND: Data is entered into the four fields
        modal.fill_collection_id_field_preview(colid)

        modal.fill_version_field(vers)
        modal.fill_style_field(style)
        modal.fill_server_field(serv)

        # AND: Create button is clicked
        modal.click_create_button()
        modal.click_create_button()

        # THEN: The modal window closes
        assert home.create_pdf_modal_is_closed
        assert home.is_create_new_pdf_button_displayed

        # THEN we should get successful connection
        assert response.status_code == 200


def test_verify_cops_preview_jobs(selenium, cops_api_url):

    # 60 minutes wait time before process times out
    start_time = time.time()
    wait_time = 3600

    while True:

        if time.time() > start_time + wait_time:
            pytest.exit("!!!!! SOMETHING WENT WRONG. PROCESS TIMED OUT AFTER 60 MINUTES !!!!!")

        api_page = urllib.request.urlopen(cops_api_url).read()

        # loading cops json file and extracting required data
        api_jdata = json.loads(api_page)

        newest0 = api_jdata[0]
        job_id0 = newest0["id"]
        collection_id0 = newest0["collection_id"]
        job_status0 = newest0["status"]["name"]

        newest1 = api_jdata[1]
        job_id1 = newest1["id"]
        collection_id1 = newest1["collection_id"]
        job_status1 = newest1["status"]["name"]

        if job_status0 == "failed" and job_status1 == "failed":
            pytest.exit(f"COPS JOB '{job_id0}' {job_status0} AND '{job_id1}' {job_status1}")

        if job_status0 == "failed" and job_status1 == "completed":
            pytest.exit(f"COPS JOB '{job_id0}' {job_status0} AND '{job_id1}' {job_status1}")

        if job_status0 == "completed" and job_status1 == "failed":
            pytest.exit(f"COPS JOB '{job_id0}' {job_status0} AND '{job_id1}' {job_status1}")

        if job_status0 == "completed" and job_status1 == "completed":
            assert collection_id0 == "col26069"
            assert job_status0 == "completed"

            assert collection_id1 == "col11992"
            assert job_status1 == "completed"

            print(f"COPS JOB '{job_id0}' {job_status0} AND '{job_id1}' {job_status1}")
            break

        continue


@pytest.mark.test_case("C606121")
def test_verify_cops_preview_json(selenium, cops_base_url, cops_api_url):

    api_page = urllib.request.urlopen(cops_api_url).read()
    api_jdata = json.loads(api_page)

    newest0 = api_jdata[0]
    json_url0 = newest0["pdf_url"]
    job_type0 = newest0["job_type"]
    job_type_value = job_type0["name"]

    if json_url0 is None:
        pytest.exit(">>>> JSON LINK IS MISSING <<<<")

    else:

        # verifies json url
        assert "archive-preview" in json_url0
        assert ".json" in json_url0
        assert job_type_value == "distribution-preview"
