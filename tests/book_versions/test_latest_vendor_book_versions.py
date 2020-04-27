from tests import markers
from pages.webview.content import Content

"""
Gets the latest versions of all vendor collections (vendor(-staging).cnx.org)
Latest update on 27/04/2020
"""


@markers.nondestructive
def test_vendor_book_versions(vendor_base_url, selenium, openstax_allbooks_uuids):

    # GIVEN a book
    content_vendor = Content(selenium, vendor_base_url, id=openstax_allbooks_uuids).open()

    version = content_vendor.book_version
    version_vendor = str(version)

    book_title_vendor = content_vendor.title

    print("\nVendor: Latest " f"'{book_title_vendor}'" " version: ", version_vendor)
