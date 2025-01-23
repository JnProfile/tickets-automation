from playwright.sync_api import Page
from enum import Enum


class TripType(Enum):
    RETURN = "return"
    ONE_WAY = "oneWay"
    MULTICITY = "multicity"
    NOMAD = "nomad"


class KiwiLocators:
    COOKIE_BUTTON = 'button[data-test="CookiesPopup-Accept"]'
    TRIP_TYPE_DROPDOWN = 'div[data-test="SearchFormModesPicker-active-return"]'
    ORIGIN_INPUT = (
        'div[data-test="SearchFieldItem-origin"] input[data-test="SearchField-input"]'
    )
    DESTINATION_INPUT = 'div[data-test="SearchFieldItem-destination"] input[data-test="SearchField-input"]'
    ORIGIN_DROPDOWN = (
        'div[data-test="PlacepickerModalOpened-origin"] div[class="w-full"]'
    )
    DESTINATION_DROPDOWN = (
        'div[data-test="PlacepickerModalOpened-destination"] div[class="w-full"]'
    )
    PLACE_PICKER = 'div[data-test="PlacePickerInputPlace"]'
    PLACE_PICKER_CLOSE_BUTTON = 'div[data-test="PlacePickerInputPlace-close"]'
    DEPARTURE_DATE_INPUT = (
        'input[data-test="SearchFieldDateInput"][name="search-outboundDate"]'
    )
    RETURN_DATE_INPUT = (
        'input[data-test="SearchFieldDateInput"][name="search-inboundDate"]'
    )
    CALENDAR = 'div[data-test="NewDatePickerOpen"]'
    CALENDAR_CONTAINER = 'div[data-test="CalendarContainer"]'
    BOOKING_CHECKBOX = "label.orbit-checkbox-label"
    SEARCH_BUTTON = 'a[data-test="LandingSearchButton"]'
    DROPDOWN_ITEM = 'div[data-test="PlacePickerRow-station"][role="button"]'
    NEXT_MONTH_BUTTON = 'button[data-test="CalendarMoveNextButton"]'
    SET_DATES_BUTTON = 'button[data-test="SearchFormDoneButton"]'


class KiwiMainPOM:
    def __init__(self, page: Page):
        self.page = page

    def _close_place_picker(self):
        if self.page.is_visible(KiwiLocators.PLACE_PICKER):
            self.page.click(KiwiLocators.PLACE_PICKER_CLOSE_BUTTON)
            self.page.wait_for_selector(KiwiLocators.PLACE_PICKER, state="detached")

    def _wait_for_all_items_availability(self, elements_locator):
        clickable_chec_func = f"""
            () => {{
                const items = Array.from(document.querySelectorAll('{elements_locator}'));
                return items.every(element => element.isConnected && element.offsetParent !== null);
            }}
        """
        self.page.wait_for_function(clickable_chec_func)

    def _enter_location(self, input_selector, dropdown_selector, location):
        self.page.type(input_selector, location)
        self.select_dropdown_item(dropdown_selector, location)

    def _wait_and_click(self, selector):
        self.page.wait_for_selector(selector, state="visible")
        self.page.click(selector)

    def accept_cookies(self):
        if self.page.is_visible(KiwiLocators.COOKIE_BUTTON):
            self.page.click(KiwiLocators.COOKIE_BUTTON)

    def search_departure(self, origin):
        self._close_place_picker()
        self._enter_location(
            KiwiLocators.ORIGIN_INPUT, KiwiLocators.ORIGIN_DROPDOWN, origin
        )

    def search_arrival(self, destination):
        self._enter_location(
            KiwiLocators.DESTINATION_INPUT,
            KiwiLocators.DESTINATION_DROPDOWN,
            destination,
        )

    def search_flights(self, origin, destination):
        self.search_departure(origin)
        self.search_arrival(destination)

    def select_dropdown_item(self, dropdown_selector, location):
        self.page.wait_for_selector(dropdown_selector, state="visible")
        self.page.wait_for_selector(KiwiLocators.DROPDOWN_ITEM, state="visible")

        self._wait_for_all_items_availability(KiwiLocators.DROPDOWN_ITEM)

        retries = 3
        for i in range(retries):
            try:
                items = self.page.query_selector_all(KiwiLocators.DROPDOWN_ITEM)

                for item in items:
                    text = item.query_selector("div.flex-1").inner_text()
                    if location in text:
                        item.click()
                        return

                raise ValueError(f"Location '{location}' not found in dropdown {items}")
            except ValueError as e:
                if i == retries - 1:
                    raise e

    def choose_trip_type(self, trip_type: TripType):
        self._wait_and_click(KiwiLocators.TRIP_TYPE_DROPDOWN)
        self.page.click(f'a[data-test="ModePopupOption-{trip_type.value}"]')

    def select_one_way_date(self, days_before_departure=0):
        self.page.click(KiwiLocators.DEPARTURE_DATE_INPUT)
        self.page.wait_for_selector(KiwiLocators.CALENDAR, state="visible")
        self.page.wait_for_selector(KiwiLocators.CALENDAR_CONTAINER, state="visible")

        date_element = 'div[data-test="CalendarDay"]'

        # Wait for all elements of calendar to be clickable
        self._wait_for_all_items_availability(date_element)

        items = self.page.query_selector_all(date_element)
        num_of_items = len(items)

        if num_of_items == 0:
            raise ValueError("Dates was not loaded")

        if num_of_items > days_before_departure:
            items[days_before_departure].click()
        else:
            while num_of_items < days_before_departure:
                prev_last_date = items[-1].get_attribute("data-value")
                days_before_departure -= num_of_items

                next_month = 'button[data-test="CalendarMoveNextButton"]'
                self.page.click(next_month)

                self._wait_for_all_items_availability(date_element)
                items = self.page.query_selector_all(date_element)

                for i, elem in enumerate(items):
                    if elem.get_attribute("data-value") == prev_last_date:
                        items = items[i + 1 :]
                        break

                num_of_items = len(items)
                if num_of_items > days_before_departure:
                    items[days_before_departure].click()

        set_dates_button = 'button[data-test="SearchFormDoneButton"]'
        self._wait_and_click(set_dates_button)

    def click_search_button(self):
        self._wait_and_click(KiwiLocators.SEARCH_BUTTON)

    def click_booking_checkbox(self):
        self.page.click(KiwiLocators.BOOKING_CHECKBOX)
