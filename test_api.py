"""
API Tests - DummyJSON API
Exercises REST API testing patterns against a public ecommerce API.
Mirrors the API test collection patterns from the Playwright project's OrangeHRM tests.

API site: https://dummyjson.com
Docs:     https://dummyjson.com/docs
"""

import time
import requests

BASE_API = "https://dummyjson.com"


# ==========================================================================
# Products
# ==========================================================================

class TestProductsAPI:
    """Tests for the /products endpoints — listing, filtering, sorting, and detail."""

    def test_get_all_products_returns_200(self):
        """GET /products must return HTTP 200."""
        response = requests.get(f"{BASE_API}/products")
        assert response.status_code == 200

    def test_get_all_products_response_has_pagination_fields(self):
        """Response must include products list plus total, skip, and limit metadata."""
        data = requests.get(f"{BASE_API}/products").json()
        for field in ["products", "total", "skip", "limit"]:
            assert field in data, f"Missing pagination field: '{field}'"

    def test_get_all_products_returns_non_empty_list(self):
        """The products array must be non-empty."""
        products = requests.get(f"{BASE_API}/products").json()["products"]
        assert isinstance(products, list)
        assert len(products) > 0

    def test_get_all_products_responds_within_five_seconds(self):
        """Products endpoint must respond within 5 seconds."""
        start = time.time()
        response = requests.get(f"{BASE_API}/products")
        elapsed = time.time() - start
        assert response.status_code == 200
        assert elapsed < 5, f"Response took {elapsed:.2f}s — exceeded 5s threshold"

    def test_get_single_product_returns_correct_id(self):
        """GET /products/1 must return the product with id=1."""
        response = requests.get(f"{BASE_API}/products/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1

    def test_product_has_all_required_fields(self):
        """A product object must contain id, title, price, description, category, rating."""
        product = requests.get(f"{BASE_API}/products/1").json()
        for field in ["id", "title", "price", "description", "category", "rating"]:
            assert field in product, f"Missing required field: '{field}'"

    def test_product_price_is_a_positive_number(self):
        """Product price must be a positive numeric value."""
        price = requests.get(f"{BASE_API}/products/1").json()["price"]
        assert isinstance(price, (int, float))
        assert price > 0

    def test_limit_parameter_returns_correct_count(self):
        """GET /products?limit=5 must return exactly 5 products."""
        data = requests.get(f"{BASE_API}/products?limit=5").json()
        assert len(data["products"]) == 5

    def test_skip_parameter_offsets_results(self):
        """?skip=10 should return products starting from the 11th item."""
        all_ids = [p["id"] for p in requests.get(f"{BASE_API}/products?limit=20").json()["products"]]
        skipped_ids = [p["id"] for p in requests.get(f"{BASE_API}/products?limit=5&skip=10").json()["products"]]
        assert skipped_ids[0] == all_ids[10]

    def test_search_products_returns_matching_results(self):
        """GET /products/search?q=phone should return results containing 'phone' in the title."""
        products = requests.get(f"{BASE_API}/products/search?q=phone").json()["products"]
        assert len(products) > 0
        assert any("phone" in p["title"].lower() for p in products)


# ==========================================================================
# Categories
# ==========================================================================

class TestCategoriesAPI:
    """Tests for product category endpoints."""

    def test_get_categories_returns_200(self):
        """GET /products/categories must return HTTP 200."""
        assert requests.get(f"{BASE_API}/products/categories").status_code == 200

    def test_categories_is_a_non_empty_list(self):
        """The categories response must be a non-empty list."""
        categories = requests.get(f"{BASE_API}/products/categories").json()
        assert isinstance(categories, list)
        assert len(categories) > 0

    def test_each_category_has_slug_name_and_url(self):
        """Every category object must have slug, name, and url fields."""
        categories = requests.get(f"{BASE_API}/products/categories").json()
        for cat in categories:
            assert "slug" in cat, f"Category missing 'slug': {cat}"
            assert "name" in cat, f"Category missing 'name': {cat}"
            assert "url" in cat, f"Category missing 'url': {cat}"

    def test_get_products_by_category_returns_200(self):
        """GET /products/category/smartphones must return HTTP 200."""
        assert requests.get(f"{BASE_API}/products/category/smartphones").status_code == 200

    def test_get_products_by_category_returns_non_empty_list(self):
        """Products filtered by category must return at least one product."""
        products = requests.get(f"{BASE_API}/products/category/smartphones").json()["products"]
        assert len(products) > 0

    def test_category_endpoint_respects_limit_parameter(self):
        """Category listing should honour the ?limit query parameter."""
        data = requests.get(f"{BASE_API}/products/category/smartphones?limit=2").json()
        assert len(data["products"]) == 2


# ==========================================================================
# Carts
# ==========================================================================

class TestCartsAPI:
    """Tests for the /carts endpoints — retrieval and creation."""

    def test_get_all_carts_returns_200(self):
        """GET /carts must return HTTP 200."""
        assert requests.get(f"{BASE_API}/carts").status_code == 200

    def test_get_all_carts_returns_a_list(self):
        """The carts response must contain a non-empty carts array."""
        carts = requests.get(f"{BASE_API}/carts").json()["carts"]
        assert isinstance(carts, list)
        assert len(carts) > 0

    def test_get_single_cart_has_required_fields(self):
        """A cart object must contain id, userId, total, discountedTotal, and products."""
        cart = requests.get(f"{BASE_API}/carts/1").json()
        for field in ["id", "userId", "total", "discountedTotal", "products"]:
            assert field in cart, f"Missing required field: '{field}'"

    def test_cart_products_field_is_a_list(self):
        """The 'products' field of a cart must be a list."""
        cart = requests.get(f"{BASE_API}/carts/1").json()
        assert isinstance(cart["products"], list)

    def test_cart_total_is_non_negative(self):
        """Cart total must be a non-negative number."""
        total = requests.get(f"{BASE_API}/carts/1").json()["total"]
        assert isinstance(total, (int, float))
        assert total >= 0

    def test_add_cart_returns_new_cart_with_id(self):
        """POST /carts/add with a valid payload must return a response containing an 'id'."""
        payload = {
            "userId": 1,
            "products": [
                {"id": 144, "quantity": 4},
                {"id": 98, "quantity": 1},
            ],
        }
        response = requests.post(f"{BASE_API}/carts/add", json=payload)
        assert response.status_code == 201
        assert "id" in response.json()

    def test_get_carts_by_user_returns_matching_carts(self):
        """GET /carts/user/1 must return carts belonging to user 1."""
        response = requests.get(f"{BASE_API}/carts/user/1")
        assert response.status_code == 200
        carts = response.json()["carts"]
        assert isinstance(carts, list)
        assert all(c["userId"] == 1 for c in carts)


# ==========================================================================
# Authentication
# ==========================================================================

class TestAuthAPI:
    """Tests for the /auth/login endpoint."""

    def test_valid_credentials_return_access_token(self):
        """POSTing valid credentials must return an accessToken string."""
        response = requests.post(
            f"{BASE_API}/auth/login",
            json={"username": "emilys", "password": "emilyspass"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "accessToken" in data
        assert isinstance(data["accessToken"], str)
        assert len(data["accessToken"]) > 0

    def test_login_response_includes_user_info(self):
        """Login response must include the authenticated user's id, username, and email."""
        response = requests.post(
            f"{BASE_API}/auth/login",
            json={"username": "emilys", "password": "emilyspass"},
        )
        data = response.json()
        for field in ["id", "username", "email"]:
            assert field in data, f"Missing user field in auth response: '{field}'"

    def test_invalid_credentials_return_400(self):
        """POSTing wrong credentials must return HTTP 400."""
        response = requests.post(
            f"{BASE_API}/auth/login",
            json={"username": "wronguser", "password": "wrongpass"},
        )
        assert response.status_code == 400

    def test_auth_response_time_is_acceptable(self):
        """The login endpoint should respond in under 5 seconds."""
        start = time.time()
        response = requests.post(
            f"{BASE_API}/auth/login",
            json={"username": "emilys", "password": "emilyspass"},
        )
        elapsed = time.time() - start
        assert response.status_code == 200
        assert elapsed < 5, f"Auth took {elapsed:.2f}s — exceeded 5s threshold"


# ==========================================================================
# Users
# ==========================================================================

class TestUsersAPI:
    """Tests for the /users endpoints."""

    def test_get_all_users_returns_200(self):
        """GET /users must return HTTP 200."""
        assert requests.get(f"{BASE_API}/users").status_code == 200

    def test_get_all_users_returns_a_list(self):
        """The users response must contain a non-empty users array."""
        users = requests.get(f"{BASE_API}/users").json()["users"]
        assert isinstance(users, list)
        assert len(users) > 0

    def test_user_has_required_fields(self):
        """A user object must include id, firstName, lastName, email, and username."""
        user = requests.get(f"{BASE_API}/users/1").json()
        for field in ["id", "firstName", "lastName", "email", "username"]:
            assert field in user, f"Missing required field: '{field}'"

    def test_user_email_contains_at_symbol(self):
        """User email must be a valid-looking address containing '@'."""
        email = requests.get(f"{BASE_API}/users/1").json()["email"]
        assert "@" in email
