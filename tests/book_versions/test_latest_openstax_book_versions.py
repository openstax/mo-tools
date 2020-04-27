from tests import markers
from pages.webview.home import Home
from urllib.request import urlopen
import json
import urllib

"""
Gets the latest versions of all openstax collections (cnx.org)
Latest update on 27/01/2020
"""


@markers.nondestructive
def test_openstax_book_versions(webview_base_url, archive_base_url, selenium):

    home = Home(selenium, webview_base_url).open()

    for cnx_book in home.featured_books.openstax_list:

        book_title = cnx_book.title
        book_id = cnx_book.cnx_id
        print(book_id)
        url = f"{archive_base_url}" + "/contents/" + f"{book_id}" + ".json"

        page = urllib.request.urlopen(url).read()
        jdata = json.loads(page)

        raw_ver = {v for k, v in jdata.items() if k == "version"}

        version = str(raw_ver)[2:-2]

        ver = {}
        ver[book_title] = version

        print("\nLatest " f"'{book_title}'" " version: ", version)
