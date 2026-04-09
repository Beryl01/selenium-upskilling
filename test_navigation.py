"""
Navigation Tests - Sauce Demo
Tests the burger menu sidebar: open/close, link targets, and state reset.
Site: https://www.saucedemo.com
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
BASE_URL = "https://www.saucedemo.com"


class TestNavigation:
    """Covers the sidebar menu, inter-page navigation, and app state reset."""

    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self._login()

    def teardown_method(self):
        self.driver.quit()

    def _login(self):
        """Log in with the standard user before every test."""
        self.driver.get(BASE_URL)
        self.driver.find_element(By.ID, "user-name").send_keys("standard_user")
        self.driver.find_element(By.ID, "password").send_keys("secret_sauce")
        self.driver.find_element(By.ID, "login-button").click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))

    def _open_menu(self):
        """Click the burger button and wait for the sidebar items to be clickable."""
        self.driver.find_element(By.ID, "react-burger-menu-btn").click()
        self.wait.until(
            EC.element_to_be_clickable((By.ID, "inventory_sidebar_link"))
        )

    # ------------------------------------------------------------------
    # Sidebar open / close
    # ------------------------------------------------------------------

    def test_burger_menu_button_is_visible_on_inventory_page(self):
        """The burger menu icon must be visible after login."""
        assert self.driver.find_element(By.ID, "react-burger-menu-btn").is_displayed()

    def test_sidebar_opens_on_burger_click(self):
        """After clicking the burger button the sidebar links must become visible."""
        self._open_menu()
        assert self.driver.find_element(By.ID, "inventory_sidebar_link").is_displayed()
        assert self.driver.find_element(By.ID, "logout_sidebar_link").is_displayed()

    def test_sidebar_closes_on_x_button_click(self):
        """Clicking the X button should hide the sidebar."""
        self._open_menu()
        self.driver.find_element(By.ID, "react-burger-cross-btn").click()
        self.wait.until(
            EC.invisibility_of_element_located((By.ID, "react-burger-cross-btn"))
        )
        menu_wrap = self.driver.find_element(By.CLASS_NAME, "bm-menu-wrap")
        assert menu_wrap.get_attribute("aria-hidden") == "true"

    # ------------------------------------------------------------------
    # Link destinations (checked without navigating to external pages)
    # ------------------------------------------------------------------

    def test_about_link_points_to_saucelabs(self):
        """The About sidebar link's href must reference the Sauce Labs website."""
        self._open_menu()
        about = self.driver.find_element(By.ID, "about_sidebar_link")
        assert "saucelabs.com" in about.get_attribute("href")

    def test_all_items_link_navigates_to_inventory(self):
        """'All Items' from the sidebar must take the user back to /inventory."""
        # Navigate away to a product detail page first
        self.driver.find_element(By.CLASS_NAME, "inventory_item_name").click()
        self.wait.until(EC.presence_of_element_located((By.ID, "back-to-products")))
        self._open_menu()
        self.driver.find_element(By.ID, "inventory_sidebar_link").click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))
        assert "/inventory" in self.driver.current_url

    # ------------------------------------------------------------------
    # App state reset
    # ------------------------------------------------------------------

    def test_reset_app_state_clears_cart_badge(self):
        """'Reset App State' from the sidebar must clear the cart badge."""
        # Add an item so the badge appears
        self.driver.find_element(
            By.XPATH, "(//button[contains(text(),'Add to cart')])[1]"
        ).click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
        self._open_menu()
        self.driver.find_element(By.ID, "reset_sidebar_link").click()
        self.wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )
