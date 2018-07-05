# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random
from urllib.parse import urljoin
from datetime import datetime

from tests import markers

from pages.webview.home import Home

_number_of_tested_books = 2


@markers.webview
@markers.test_case('C167405')
@markers.nondestructive
@markers.parametrize('width, height', [(1024, 768), (640, 480)])
def test_top_right_links_and_nav(width, height, webview_base_url, legacy_base_url, selenium):
    # GIVEN the webview URL, the legacy URL, and the Selenium driver with the window size set

    # WHEN the webview home page is fully loaded
    home = Home(selenium, webview_base_url).open()
    header = home.header

    # THEN the top right links, logos and nav are displayed and point to the correct URLs
    assert header.is_support_link_displayed
    assert header.support_url == 'http://openstax.force.com/support?l=en_US&c=Products%3ACNX'

    assert header.is_legacy_site_link_displayed
    expected_legacy_url = urljoin(legacy_base_url, '/content?legacy=true')
    assert header.legacy_site_url == expected_legacy_url, (
               'The legacy URL in the CNX home page did not match the legacy_base_url. '
               'Check that both webview_base_url and legacy_base_url point to the same environment.'
           )

    assert header.is_cnx_logo_displayed
    assert header.cnx_logo_url.rstrip('/') == webview_base_url

    assert header.is_nav_displayed

    if header.is_nav_button_displayed:
        assert not header.is_browse_link_displayed
        assert not header.is_about_us_link_displayed
        assert not header.is_donate_link_displayed
        assert not header.is_rice_logo_displayed
        header.click_nav_button()

    assert header.is_browse_link_displayed
    assert header.browse_url == urljoin(webview_base_url, '/browse')

    assert header.is_about_us_link_displayed
    assert header.about_us_url == urljoin(webview_base_url, '/about')

    assert header.is_donate_link_displayed
    assert header.donate_url == urljoin(webview_base_url, '/donate')

    assert header.is_rice_logo_displayed
    assert header.rice_logo_url.rstrip('/') == 'http://www.rice.edu'


@markers.webview
@markers.nondestructive
def test_splash_banner_loads(webview_base_url, selenium):
    # GIVEN the main website URL and the Selenium driver

    # WHEN The home page URL is fully loaded
    page = Home(selenium, webview_base_url).open()

    # THEN The splash text is correct
    assert 'Discover learning materials in an Open Space' in page.splash


@markers.webview
@markers.test_case('C176224', 'C176225')
@markers.nondestructive
def test_featured_books_load(webview_base_url, selenium):
    # GIVEN the webview base url and the Selenium driver

    # WHEN the home page is fully loaded
    page = Home(selenium, webview_base_url).open()

    # THEN there are featured books for both OpenStax and CNX
    assert len(page.featured_books.openstax_list) > 0
    assert len(page.featured_books.cnx_list) > 0


@markers.xfail(reason='https://trello.com/c/DL7xEWon', raises=AssertionError)
@markers.webview
@markers.test_case('C176226')
@markers.nondestructive
def test_featured_books_have_title_and_intro(webview_base_url, selenium):
    # GIVEN the webview base url and the Selenium driver

    # WHEN the home page is fully loaded
    home = Home(selenium, webview_base_url).open()

    # THEN all featured books have titles and intros
    books = home.featured_books.openstax_list + home.featured_books.cnx_list

    for book in books:
        assert book.title
        assert book.intro
        assert book.intro != '...'


@markers.xfail(reason='https://trello.com/c/mFRaZRqK', raises=AssertionError)
@markers.webview
@markers.test_case('C176227')
@markers.nondestructive
def test_read_more_loads_correct_page(webview_base_url, selenium):
    # GIVEN the webview base url and the Selenium driver

    # WHEN the home page is fully loaded,
    #      find the first OpenStax book and click the Read More link
    home = Home(selenium, webview_base_url).open()
    for i in range(_number_of_tested_books):
        # Can't use `for book in sample(home.featured_books.openstax_list, _number_of_tested_books)`
        # because it causes StaleElementReferenceExceptions
        book = random.choice(home.featured_books.openstax_list)
        book_title = book.title
        content_page = book.click_read_more()

        # THEN The book title from the home page matches the content page title
        assert book_title == content_page.title

        if i < _number_of_tested_books - 1:
            selenium.back()
            home = home.wait_for_page_to_load()


@markers.xfail(reason='https://trello.com/c/mFRaZRqK', raises=AssertionError)
@markers.webview
@markers.test_case('C176228')
@markers.nondestructive
def test_book_cover_loads_correct_page(webview_base_url, selenium):
    # GIVEN the webview base url and the Selenium driver

    # WHEN the home page is fully loaded,
    #      find the first OpenStax book and click the book cover link
    home = Home(selenium, webview_base_url).open()
    for i in range(_number_of_tested_books):
        # Can't use `for book in sample(home.featured_books.openstax_list, _number_of_tested_books)`
        # because it causes StaleElementReferenceExceptions
        book = random.choice(home.featured_books.openstax_list)
        book_title = book.title
        content_page = book.click_book_cover()

        # THEN The book title from the home page matches the content page title
        assert book_title == content_page.title

        if i < _number_of_tested_books - 1:
            selenium.back()
            home = home.wait_for_page_to_load()


@markers.xfail(reason='https://trello.com/c/mFRaZRqK', raises=AssertionError)
@markers.webview
@markers.test_case('C176229')
@markers.nondestructive
def test_title_link_loads_correct_page(webview_base_url, selenium):
    # GIVEN the webview base url and the Selenium driver

    # WHEN the home page is fully loaded,
    #      find the first OpenStax book and click the title link
    home = Home(selenium, webview_base_url).open()
    for i in range(_number_of_tested_books):
        # Can't use `for book in sample(home.featured_books.openstax_list, _number_of_tested_books)`
        # because it causes StaleElementReferenceExceptions
        book = random.choice(home.featured_books.openstax_list)
        book_title = book.title
        content_page = book.click_title_link()

        # THEN The book title from the home page matches the content page title
        assert book_title == content_page.title

        if i < _number_of_tested_books - 1:
            selenium.back()
            home = home.wait_for_page_to_load()


@markers.webview
@markers.test_case('C176230')
@markers.nondestructive
def test_logo_link_stays_on_home_page(webview_base_url, selenium):
    # GIVEN the home page
    home = Home(selenium, webview_base_url).open()

    # WHEN the OpenStax CNX logo is clicked
    home = home.header.click_cnx_logo()

    # THEN we are still in the home page
    assert type(home) is Home


@markers.webview
@markers.test_case('C167406')
@markers.nondestructive
def test_footer_has_correct_content_and_links(webview_base_url, selenium):
    # GIVEN the home page
    home = Home(selenium, webview_base_url).open()

    # WHEN we scroll to the footer
    footer = home.footer
    footer.scroll_to()

    # THEN the links point to the correct urls and all the content is displayed
    assert footer.is_licensing_link_displayed
    assert footer.licensing_url == urljoin(webview_base_url, '/license')

    assert footer.is_terms_of_use_link_displayed
    assert footer.terms_of_use_url == urljoin(webview_base_url, '/tos')

    assert footer.is_accessibility_statement_link_displayed
    assert footer.accessibility_statement_url == 'https://openstax.org/accessibility-statement'

    assert footer.is_contact_link_displayed
    assert footer.contact_url == urljoin(webview_base_url, '/about/contact')

    assert footer.is_foundation_support_paragraph_displayed
    assert footer.foundation_support_text == (
        'Supported by William & Flora Hewlett Foundation, Bill & Melinda Gates Foundation,'
        ' Michelson 20MM Foundation, Maxfield Foundation, Open Society Foundations, and'
        ' Rice University. Powered by OpenStax CNX.')

    assert footer.is_ap_paragraph_displayed
    assert footer.ap_text == (
        'Advanced Placement® and AP® are trademarks registered and/or owned by the College Board,'
        ' which was not involved in the production of, and does not endorse, this site.')

    assert footer.is_copyright_statement_paragraph_displayed
    year = datetime.now().year
    assert footer.copyright_statement_text == (
        '© 1999-{year}, Rice University. Except where otherwise noted, content created on this site'
        ' is licensed under a Creative Commons Attribution 4.0 License.'.format(year=year))

    assert footer.is_android_app_link_displayed
    assert footer.android_app_url == (
        'https://play.google.com/store/apps/details?id=org.openstaxcollege.android')

    webview_url = urljoin(webview_base_url, '/')

    assert footer.is_facebook_link_displayed
    assert footer.facebook_url == (
        'https://facebook.com/sharer/sharer.php?u={webview_url}'.format(webview_url=webview_url))

    assert footer.is_twitter_link_displayed
    assert footer.twitter_url == ('https://twitter.com/share?url={webview_url}&text=An%20OpenStax'
                                  '%20CNX%20book&via=cnxorg'.format(webview_url=webview_url))

    assert footer.is_email_link_displayed
    assert footer.email_url == 'mailto:support@openstax.org'

    footer_text = footer.text
    assert 'Dev Blog' not in footer_text
    assert 'iTunes U' not in footer_text
    assert 'Google Plus' not in footer_text
