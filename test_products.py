"""
Product Tests - Sauce Demo
Tests the inventory listing page: item count, sorting, prices, and detail pages.
Site: https://www.saucedemo.com
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
BASE_URL = "https://www.saucedemo.com"


class TestProducts:
    """Covers the inventory page and product detail pages."""

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

    # ------------------------------------------------------------------
    # Inventory listing
    # ------------------------------------------------------------------

    def test_products_page_displays_six_items(self):
        """The default product listing must show exactly 6 items."""
        items = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(items) == 6

    def test_all_products_have_non_empty_names(self):
        """Every product card must display a non-empty product name."""
        names = self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        assert all(name.text.strip() for name in names)

    def test_all_products_have_dollar_prices(self):
        """Each product price must be present and start with '$'."""
        prices = self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        assert len(prices) == 6
        for price in prices:
            assert price.text.startswith("$"), f"Unexpected price format: '{price.text}'"

    def test_all_products_have_add_to_cart_buttons(self):
        """Each of the 6 products must have its own 'Add to cart' button."""
        buttons = self.driver.find_elements(
            By.XPATH, "//button[contains(text(),'Add to cart')]"
        )
        assert len(buttons) == 6

    # ------------------------------------------------------------------
    # Sorting
    # ------------------------------------------------------------------

    def test_sort_by_name_z_to_a(self):
        """Selecting Z→A should reverse the alphabetical order of product names."""
        sort = Select(self.driver.find_element(By.CLASS_NAME, "product_sort_container"))
        sort.select_by_value("za")
        names = [el.text for el in self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
        assert names == sorted(names, reverse=True)

    def test_sort_by_price_low_to_high(self):
        """Price low→high sort should order products from cheapest to most expensive."""
        sort = Select(self.driver.find_element(By.CLASS_NAME, "product_sort_container"))
        sort.select_by_value("lohi")
        prices = [
            float(el.text.replace("$", ""))
            for el in self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        ]
        assert prices == sorted(prices)

    def test_sort_by_price_high_to_low(self):
        """Price high→low sort should order products from most to least expensive."""
        sort = Select(self.driver.find_element(By.CLASS_NAME, "product_sort_container"))
        sort.select_by_value("hilo")
        prices = [
            float(el.text.replace("$", ""))
            for el in self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        ]
        assert prices == sorted(prices, reverse=True)

    # ------------------------------------------------------------------
    # Product detail page
    # ------------------------------------------------------------------

    def test_clicking_product_name_opens_detail_page(self):
        """Clicking a product name should open its detail page with the same name."""
        first = self.driver.find_element(By.CLASS_NAME, "inventory_item_name")
        expected_name = first.text
        first.click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_details")))
        detail_name = self.driver.find_element(By.CLASS_NAME, "inventory_details_name")
        assert detail_name.text == expected_name

    def test_product_detail_page_has_back_to_products_button(self):
        """The product detail page must include a 'Back to products' button."""
        self.driver.find_element(By.CLASS_NAME, "inventory_item_name").click()
        self.wait.until(EC.presence_of_element_located((By.ID, "back-to-products")))
        assert self.driver.find_element(By.ID, "back-to-products").is_displayed()

    def test_back_to_products_returns_to_inventory(self):
        """Clicking 'Back to products' should navigate back to /inventory."""
        self.driver.find_element(By.CLASS_NAME, "inventory_item_name").click()
        self.wait.until(EC.presence_of_element_located((By.ID, "back-to-products")))
        self.driver.find_element(By.ID, "back-to-products").click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))
        assert "/inventory" in self.driver.current_url
