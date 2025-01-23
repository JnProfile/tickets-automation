import pytest
from playwright.sync_api import sync_playwright
from pytest_bdd import scenarios, given, when, then
from pages.KiwiMainPOM import KiwiMainPOM, KiwiLocators, TripType

# Загружаем файл feature
scenarios("test_kiwi_ui.feature")


@pytest.fixture
def browser():
    """Fixture for browser initialization."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """Fixture for page initialization."""
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture
def kiwi(page):
    """Fixture for KiwiMainPOM initialization."""
    return KiwiMainPOM(page)


@given('As an not logged user navigate to homepage https://www.kiwi.com/en/')
def navigate_to_homepage(page, kiwi):
    """Navigate to Kiwi.com homepage."""
    page.goto("https://www.kiwi.com/en/")
    kiwi.accept_cookies()


@when('I select one-way trip type')
def select_one_way_trip(kiwi):
    """Choose one-way trip type."""
    kiwi.choose_trip_type(TripType.ONE_WAY)


@when('Set as departure airport RTM')
def set_departure_airport(kiwi):
    """Departure airport selection."""
    kiwi.search_departure(origin="RTM")


@when('Set the arrival Airport MAD')
def set_arrival_airport(kiwi):
    """Arrival airport selection."""
    kiwi.search_arrival(destination="MAD")


@when('Set the departure time 1 week in the future starting current date')
def set_departure_date(kiwi):
    """Set the departure date."""
    days_in_future = 7
    kiwi.select_one_way_date(days_in_future)


@when('Uncheck the `Check accommodation with booking.com` option')
def uncheck_booking_checkbox(kiwi):
    """Uncheck the booking.com option"""
    kiwi.page.click(KiwiLocators.BOOKING_CHECKBOX)


@when('Click the search button')
def click_search_button(kiwi):
    """Click the search button."""
    kiwi.click_search_button()


@then('I am redirected to search results page')
def verify_search_results(page):
    """Verify search results page."""
    assert "/search/results" in page.url, "User was not redirected to search results page"


