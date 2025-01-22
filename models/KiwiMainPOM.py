from playwright.sync_api import Page
from time import sleep


class KiwiMainPOM:
    def __init__(self, page: Page):
        self.page = page
        self.cookie_button = 'button[data-test="CookiesPopup-Accept"]'
        self.trip_type_dropdown = (
            'div[data-test="SearchFormModesPicker-active-return"]'
        )

        self.origin_input = (
            'div[data-test="SearchFieldItem-origin"] input[data-test="SearchField-input"]'
        )
        self.origin_dropdown = (
            'div[data-test="PlacepickerModalOpened-origin"]'
        )
        self.destination_input = (
            'div[data-test="SearchFieldItem-destination"] input[data-test="SearchField-input"]'
        )
        self.destination_dropdown = (
            'div[data-test="PlacepickerModalOpened-destination"]'
        )

        self.place_picker = 'div[data-test="PlacePickerInputPlace"]'
        self.place_picker_close_button = 'div[data-test="PlacePickerInputPlace-close"]'

        self.departure_date_input = (
            'input[data-test="SearchFieldDateInput"][name="search-outboundDate"]'
        )
        self.return_date_input = (
            'input[data-test="SearchFieldDateInput"][name="search-inboundDate"]'
        )

        self.calendar = 'div[data-test="NewDatePickerOpen"]'

        self.booking_checkbox = "label.orbit-checkbox-label"

        self.search_button = 'a[data-test="LandingSearchButton"]'

    def search_flights(self, origin, destination):
        if self.page.is_visible(self.place_picker):
            self.page.click(kiwi.place_picker_close_button)
            page.wait_for_selector(self.place_picker, state="detached")

        self.page.type(self.origin_input, origin)
        self.select_airport_or_city(self.origin_dropdown, origin)

        self.page.type(self.destination_input, destination)
        self.select_airport_or_city(self.destination_dropdown, destination)

    def select_airport_or_city(self, drop_down_selector, location: str):
        self.page.wait_for_selector(drop_down_selector, state="visible")

        dropdown_item_selector = (
            'div[data-test="PlacePickerRow-station"][role="button"]'
        )
        self.page.wait_for_selector(dropdown_item_selector, state="visible")

        items = self.page.query_selector_all(dropdown_item_selector)

        for item in items:
            text = item.query_selector("div.flex-1").inner_text()

            if location in text:
                item.click()
                return

        raise Exception(f"'{location}' NOT FOUND")

    def choose_trip_type(self, trip_type):
        choices = ["return", "oneWay", "multicity", "nomad"]

        if trip_type not in choices:
            raise ValueError(f"Trip type must be one of {choices}")

        self.page.click(self.trip_type_dropdown)
        self.page.click(f'a[data-test="ModePopupOption-{trip_type}"]')

    def select_one_way_date(self, days_before_departure=0):
        self.page.click(self.departure_date_input)
        self.page.wait_for_selector(self.calendar, state="visible")

        date_element = 'div[data-type="DayContainer"]'
        self.page.wait_for_selector(date_element, state="visible")

        items = self.page.query_selector_all(date_element)
        num_of_items = len(items)

        if num_of_items == 0:
            raise ValueError("No days available")

        if num_of_items > days_before_departure:
            items[days_before_departure].click()
        else:
            while num_of_items < days_before_departure:
                prev_last_date = items[-1].get_attribute("data-value")
                days_before_departure -= num_of_items
                next_month = 'button[data-test="CalendarMoveNextButton"]'
                self.page.click(next_month)
                self.page.wait_for_selector(date_element, state="visible")
                items = self.page.query_selector_all(date_element)

                for i, elem in enumerate(items):
                    if elem.get_attribute("data-value") == prev_last_date:
                        items = items[i + 1 :]
                        break

                num_of_items = len(items)
                if num_of_items > days_before_departure:
                    items[days_before_departure].click()

        set_dates_button = 'button[data-test="SearchFormDoneButton"]'
        self.page.wait_for_selector(set_dates_button, state="visible")
        self.page.click(set_dates_button)

    def click_search_button(self):
        self.page.click(self.search_button)


if __name__ == "__main__":
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://kiwi.com")
        kiwi = KiwiMainPOM(page)
        kiwi.page.click(kiwi.cookie_button)
        kiwi.choose_trip_type("oneWay")
        kiwi.page.click(kiwi.booking_checkbox)

        kiwi.search_flights("RTM", "MAD")

        kiwi.select_one_way_date(90)

        kiwi.click_search_button()

        sleep(15)
        browser.close()
