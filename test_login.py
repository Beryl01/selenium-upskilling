"""
Login Tests - Sauce Demo
Tests all authentication scenarios: valid, invalid, locked user, and edge cases.
Site: https://www.saucedemo.com
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
BASE_URL = "https://www.saucedemo.com"


class TestLogin:
    """Covers the login page and all authentication entry points."""

    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get(BASE_URL)

    def teardown_method(self):
        self.driver.quit()

    # ------------------------------------------------------------------
    # Page structure
    # ------------------------------------------------------------------

    def test_login_page_has_correct_title(self):
        """Browser tab title should be 'Swag Labs'."""
        assert "Swag Labs" in self.driver.title

    def test_login_form_elements_are_visible(self):
        """Username field, password field, and login button must all be visible."""
        assert self.driver.find_element(By.ID, "user-name").is_displayed()
        assert self.driver.find_element(By.ID, "password").is_displayed()
        assert self.driver.find_element(By.ID, "login-button").is_displayed()

    def test_password_field_is_masked(self):
        """Password input must have type='password' so characters are hidden."""
        pwd = self.driver.find_element(By.ID, "password")
        assert pwd.get_attribute("type") == "password"

    # ------------------------------------------------------------------
    # Successful authentication
    # ------------------------------------------------------------------

    def test_valid_credentials_redirect_to_inventory(self):
        """Logging in with standard_user should land on the /inventory page."""
        self.driver.find_element(By.ID, "user-name").send_keys("standard_user")
        self.driver.find_element(By.ID, "password").send_keys("secret_sauce")
        self.driver.find_element(By.ID, "login-button").click()
        self.wait.until(EC.url_contains("/inventory"))
        assert "/inventory" in self.driver.current_url

    # ------------------------------------------------------------------
    # Error states
    # ------------------------------------------------------------------

    def test_invalid_credentials_show_error_message(self):
        """Wrong username/password should display a descriptive error banner."""
        self.driver.find_element(By.ID, "user-name").send_keys("not_a_user")
        self.driver.find_element(By.ID, "password").send_keys("wrong_pass")
        self.driver.find_element(By.ID, "login-button").click()
        error = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        assert "Username and password do not match" in error.text

    def test_locked_out_user_sees_locked_message(self):
        """The locked_out_user account must display a 'locked out' specific error."""
        self.driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
        self.driver.find_element(By.ID, "password").send_keys("secret_sauce")
        self.driver.find_element(By.ID, "login-button").click()
        error = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        assert "Sorry, this user has been locked out" in error.text

    def test_empty_credentials_show_username_required(self):
        """Clicking Login without any input should show 'Username is required'."""
        self.driver.find_element(By.ID, "login-button").click()
        error = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        assert "Username is required" in error.text

    def test_missing_password_shows_password_required(self):
        """Submitting with only a username should show 'Password is required'."""
        self.driver.find_element(By.ID, "user-name").send_keys("standard_user")
        self.driver.find_element(By.ID, "login-button").click()
        error = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        assert "Password is required" in error.text

    def test_error_banner_can_be_dismissed(self):
        """Clicking the X on the error banner should remove it from view."""
        self.driver.find_element(By.ID, "login-button").click()
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        self.driver.find_element(By.CLASS_NAME, "error-button").click()
        self.wait.until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
