"""
Sauce Demo - Login and Product Tests
Test Site: https://www.saucedemo.com/
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class TestSauceDemo:
    """Test class for Sauce Demo website"""
    
    def setup_method(self):
        """Initialize WebDriver before each test"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
    
    def teardown_method(self):
        """Clean up after each test"""
        self.driver.quit()
    
    def test_login_successful(self):
        """Test successful login to Sauce Demo"""
        # Navigate to Sauce Demo
        self.driver.get("https://www.saucedemo.com/")
        
        # Enter username
        username_field = self.driver.find_element(By.ID, "user-name")
        username_field.send_keys("standard_user")
        
        # Enter password
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys("secret_sauce")
        
        # Click login button
        login_button = self.driver.find_element(By.ID, "login-button")
        login_button.click()
        
        # Wait for products page to load and verify
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
        )
        
        # Verify we're on the products page
        page_title = self.driver.find_element(By.CLASS_NAME, "title")
        assert "Products" in page_title.text
        print("✓ Login successful!")
    
    def test_add_to_cart(self):
        """Test adding products to cart"""
        # Login first
        self.driver.get("https://www.saucedemo.com/")
        self.driver.find_element(By.ID, "user-name").send_keys("standard_user")
        self.driver.find_element(By.ID, "password").send_keys("secret_sauce")
        self.driver.find_element(By.ID, "login-button").click()
        
        # Wait for products to load
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
        )
        
        # Add first product to cart
        add_to_cart_button = self.driver.find_element(
            By.XPATH, 
            "//button[contains(text(), 'Add to cart')]"
        )
        add_to_cart_button.click()
        
        # Verify cart count updated
        cart_badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert cart_badge.text == "1"
        print("✓ Product added to cart successfully!")
    
    def test_logout(self):
        """Test logout functionality"""
        # Login first
        self.driver.get("https://www.saucedemo.com/")
        self.driver.find_element(By.ID, "user-name").send_keys("standard_user")
        self.driver.find_element(By.ID, "password").send_keys("secret_sauce")
        self.driver.find_element(By.ID, "login-button").click()
        
        # Wait for page to load
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
        )
        
        # Click menu button
        menu_button = self.driver.find_element(By.ID, "react-burger-menu-btn")
        menu_button.click()
        
        # Click logout
        logout_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
        )
        logout_button.click()
        
        # Verify we're back on login page
        self.wait.until(
            EC.presence_of_element_located((By.ID, "login-button"))
        )
        print("✓ Logout successful!")


if __name__ == "__main__":
    # Run tests manually if needed
    test = TestSauceDemo()
    
    print("\n🧪 Running Sauce Demo Tests...\n")
    
    # Test 1: Login
    print("Test 1: Testing login...")
    test.setup_method()
    try:
        test.test_login_successful()
    except Exception as e:
        print(f"✗ Login test failed: {e}")
    finally:
        test.teardown_method()
    
    # Test 2: Add to cart
    print("\nTest 2: Testing add to cart...")
    test.setup_method()
    try:
        test.test_add_to_cart()
    except Exception as e:
        print(f"✗ Add to cart test failed: {e}")
    finally:
        test.teardown_method()
    
    # Test 3: Logout
    print("\nTest 3: Testing logout...")
    test.setup_method()
    try:
        test.test_logout()
    except Exception as e:
        print(f"✗ Logout test failed: {e}")
    finally:
        test.teardown_method()
    
    print("\n✅ All tests completed!")
