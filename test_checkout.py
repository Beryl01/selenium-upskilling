"""
Checkout Tests - Sauce Demo
Tests the full multi-step checkout flow and form validation on step 1.
Site: https://www.saucedemo.com
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
BASE_URL = "https://www.saucedemo.com"


class TestCheckout:
    """Covers the checkout form, order overview, confirmation, and cancel flows."""

    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self._login_add_item_and_open_cart()

    def teardown_method(self):
        self.driver.quit()

    def _login_add_item_and_open_cart(self):
        """Log in, add the first product to the cart, and navigate to the cart page."""
        self.driver.get(BASE_URL)
        self.driver.find_element(By.ID, "user-name").send_keys("standard_user")
        self.driver.find_element(By.ID, "password").send_keys("secret_sauce")
        self.driver.find_element(By.ID, "login-button").click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))
        self.driver.find_element(
            By.XPATH, "(//button[contains(text(),'Add to cart')])[1]"
        ).click()
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cart_item")))

    def _go_to_step_one(self):
        """Navigate from the cart to checkout step 1."""
        self.driver.find_element(By.ID, "checkout").click()
        self.wait.until(EC.presence_of_element_located((By.ID, "first-name")))

    def _fill_step_one(self, first="Jane", last="Smith", zip_code="12345"):
        """Fill the customer information form on step 1."""
        self.driver.find_element(By.ID, "first-name").send_keys(first)
        self.driver.find_element(By.ID, "last-name").send_keys(last)
        self.driver.find_element(By.ID, "postal-code").send_keys(zip_code)

    # ------------------------------------------------------------------
    # Cart → Checkout entry
    # ------------------------------------------------------------------

    def test_checkout_button_is_visible_on_cart_page(self):
        """A 'Checkout' button must be present and visible on the cart page."""
        assert self.driver.find_element(By.ID, "checkout").is_displayed()

    # ------------------------------------------------------------------
    # Step 1 — customer information form
    # ------------------------------------------------------------------

    def test_step_one_shows_all_form_fields(self):
        """Checkout step 1 must display first name, last name, and postal code fields."""
        self._go_to_step_one()
        assert self.driver.find_element(By.ID, "first-name").is_displayed()
        assert self.driver.find_element(By.ID, "last-name").is_displayed()
        assert self.driver.find_element(By.ID, "postal-code").is_displayed()

    def test_empty_form_shows_first_name_required_error(self):
        """Submitting step 1 with no input must show 'First Name is required'."""
        self._go_to_step_one()
        self.driver.find_element(By.ID, "continue").click()
        error = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        assert "First Name is required" in error.text

    def test_missing_last_name_shows_last_name_required_error(self):
        """Providing only first name should show 'Last Name is required'."""
        self._go_to_step_one()
        self.driver.find_element(By.ID, "first-name").send_keys("John")
        self.driver.find_element(By.ID, "continue").click()
        error = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        assert "Last Name is required" in error.text

    def test_missing_postal_code_shows_postal_code_required_error(self):
        """Providing name but no postal code should show 'Postal Code is required'."""
        self._go_to_step_one()
        self.driver.find_element(By.ID, "first-name").send_keys("John")
        self.driver.find_element(By.ID, "last-name").send_keys("Doe")
        self.driver.find_element(By.ID, "continue").click()
        error = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        assert "Postal Code is required" in error.text

    def test_cancel_from_step_one_returns_to_cart(self):
        """Clicking Cancel on step 1 must return the user to the cart page."""
        self._go_to_step_one()
        self.driver.find_element(By.ID, "cancel").click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cart_item")))
        assert "/cart" in self.driver.current_url

    # ------------------------------------------------------------------
    # Step 2 — order overview
    # ------------------------------------------------------------------

    def test_valid_step_one_advances_to_step_two(self):
        """Completing the customer info form correctly should land on /checkout-step-two."""
        self._go_to_step_one()
        self._fill_step_one()
        self.driver.find_element(By.ID, "continue").click()
        self.wait.until(EC.url_contains("/checkout-step-two"))
        assert "/checkout-step-two" in self.driver.current_url

    def test_step_two_displays_total_price(self):
        """The order overview must show a total price label."""
        self._go_to_step_one()
        self._fill_step_one()
        self.driver.find_element(By.ID, "continue").click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label")))
        total = self.driver.find_element(By.CLASS_NAME, "summary_total_label")
        assert "Total:" in total.text

    # ------------------------------------------------------------------
    # Step 3 — order confirmation
    # ------------------------------------------------------------------

    def test_finishing_order_shows_confirmation_message(self):
        """Clicking Finish should display the 'Thank you for your order!' header."""
        self._go_to_step_one()
        self._fill_step_one()
        self.driver.find_element(By.ID, "continue").click()
        self.wait.until(EC.presence_of_element_located((By.ID, "finish")))
        self.driver.find_element(By.ID, "finish").click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "complete-header")))
        header = self.driver.find_element(By.CLASS_NAME, "complete-header")
        assert "Thank you for your order" in header.text

    def test_back_home_from_confirmation_goes_to_inventory(self):
        """'Back Home' on the confirmation page must return the user to /inventory."""
        self._go_to_step_one()
        self._fill_step_one()
        self.driver.find_element(By.ID, "continue").click()
        self.wait.until(EC.presence_of_element_located((By.ID, "finish")))
        self.driver.find_element(By.ID, "finish").click()
        self.wait.until(EC.presence_of_element_located((By.ID, "back-to-products")))
        self.driver.find_element(By.ID, "back-to-products").click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))
        assert "/inventory" in self.driver.current_url
