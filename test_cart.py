"""
Shopping Cart Tests - Sauce Demo
Tests adding items, removing items, cart badge counts, and cart page behaviour.
Site: https://www.saucedemo.com
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
BASE_URL = "https://www.saucedemo.com"


class TestCart:
    """Covers the shopping cart: badge counts, cart page items, and navigation."""

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

    def _add_first_item(self):
        """Click 'Add to cart' on the first product."""
        self.driver.find_element(
            By.XPATH, "(//button[contains(text(),'Add to cart')])[1]"
        ).click()

    # ------------------------------------------------------------------
    # Badge count
    # ------------------------------------------------------------------

    def test_adding_one_item_shows_badge_count_of_one(self):
        """Cart badge must display '1' after a single item is added."""
        self._add_first_item()
        badge = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )
        assert badge.text == "1"

    def test_adding_three_items_shows_badge_count_of_three(self):
        """Cart badge must reflect the total number of items added."""
        buttons = self.driver.find_elements(
            By.XPATH, "//button[contains(text(),'Add to cart')]"
        )
        for btn in buttons[:3]:
            btn.click()
        badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert badge.text == "3"

    def test_removing_item_from_inventory_clears_badge(self):
        """After adding then removing an item the cart badge should disappear."""
        self._add_first_item()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Remove')]").click()
        self.wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )

    # ------------------------------------------------------------------
    # Cart page content
    # ------------------------------------------------------------------

    def test_cart_page_shows_added_item(self):
        """The cart page should list the exact product that was added."""
        product_name = self.driver.find_element(By.CLASS_NAME, "inventory_item_name").text
        self._add_first_item()
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cart_item")))
        cart_name = self.driver.find_element(By.CLASS_NAME, "inventory_item_name").text
        assert cart_name == product_name

    def test_cart_item_shows_quantity_of_one(self):
        """An item added once must show quantity '1' in the cart."""
        self._add_first_item()
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cart_item")))
        qty = self.driver.find_element(By.CLASS_NAME, "cart_quantity")
        assert qty.text == "1"

    def test_removing_item_from_cart_page_empties_cart(self):
        """Removing the only cart item directly from the cart page should leave it empty."""
        self._add_first_item()
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cart_item")))
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Remove')]").click()
        items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(items) == 0

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def test_continue_shopping_returns_to_inventory(self):
        """'Continue Shopping' from the cart must navigate back to /inventory."""
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        self.wait.until(EC.presence_of_element_located((By.ID, "continue-shopping")))
        self.driver.find_element(By.ID, "continue-shopping").click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))
        assert "/inventory" in self.driver.current_url
