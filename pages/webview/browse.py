# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.webview.base import Page
from regions.webview.base import Region

from pages.webview.search_results import SearchResults


class Browse(Page):
    URL_TEMPLATE = "/browse"
    _search_input_locator = (By.ID, "find-content-input")
    _advanced_search_link_locator = (By.CSS_SELECTOR, "a.advanced-search")
    _main_content_locator = (By.ID, "main-content")
    _browse_content_locator = (By.CSS_SELECTOR, "div.browse-content")
    _search_category_locator = (By.CLASS_NAME, "search-category")

    @property
    def is_search_input_displayed(self):
        return self.is_element_displayed(*self._search_input_locator)

    @property
    def is_advanced_search_link_displayed(self):
        return self.is_element_displayed(*self._advanced_search_link_locator)

    @property
    def search_input(self):
        return self.find_element(*self._search_input_locator)

    @property
    def is_main_content_displayed(self):
        main_content = self.find_element(*self._main_content_locator)
        return main_content.is_displayed()

    @property
    def search_category_list(self):
        items = self.find_elements(*self._search_category_locator)
        return [self.Subject(self, el) for el in items]

    @property
    def advanced_search_link(self):
        return self.find_element(*self._advanced_search_link_locator)

    @property
    def loaded(self):
        # The search page is fully loaded when the subject list is displayed
        # There's no need to check for the search field/button (which load before the list)
        return (
            len(self.search_category_list) > 0
            and self.search_category_list[0].name
            and self.is_main_content_displayed
        )

    def search(self, query):
        self.search_input.send_keys(query)
        from selenium.webdriver.common.keys import Keys

        self.search_input.send_keys(Keys.ENTER)
        return SearchResults(self.driver, self.base_url, self.timeout).wait_for_page_to_load()

    def click_advanced_search_link(self):
        self.advanced_search_link.click()
        from pages.webview.advanced_search import AdvancedSearch

        advanced_search = AdvancedSearch(self.driver, self.base_url, self.timeout)
        return advanced_search.wait_for_page_to_load()

    class Subject(Region):
        _name_locator = (By.CSS_SELECTOR, "h2")
        _pages_div_locator = (By.CSS_SELECTOR, 'div[data-l10n-id="search-pages"]')
        _books_div_locator = (By.CSS_SELECTOR, 'div[data-l10n-id="search-books"]')

        @property
        def pages_div(self):
            return self.find_element(*self._pages_div_locator)

        @property
        def books_div(self):
            return self.find_element(*self._books_div_locator)

        @property
        def name(self):
            return self.find_element(*self._name_locator).text

        def get_count(self, div):
            import json

            return json.loads(div.get_attribute("data-l10n-args"))["count"]

        @property
        def pages_count(self):
            return self.get_count(self.pages_div)

        @property
        def books_count(self):
            return self.get_count(self.books_div)

        def click(self):
            self.root.click()
            search_results = SearchResults(self.driver, self.page.base_url, self.page.timeout)
            return search_results.wait_for_page_to_load()
