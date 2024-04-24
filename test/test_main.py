import unittest

from fastapi.testclient import TestClient
from mocks import app

client = TestClient(app)


class TestRegisterUser(unittest.TestCase):

    def test_successful_registration(self):
        response = client.post("/users/register", json={
            "username": "validUser",
            "email": "newuser@example.com",
            "password": "validPassword123"
        })
        assert response.status_code == 200
        assert response.json() == {"success": True, "userId": 1}

    def test_registration_with_duplicate_email(self):
        response = client.post("/users/register", json={
            "username": "validUser",
            "email": "existing@example.com",
            "password": "validPassword123"
        })
        assert response.status_code == 200
        assert response.json() == {"success": False, "message": "Email already in use"}

    def test_registration_with_short_password(self):
        response = client.post("/users/register", json={
            "username": "validUser",
            "email": "newuser@example.com",
            "password": "short"
        })
        assert response.status_code == 422
        expected_response = {
            'detail': [{
                'ctx': {'error': {}},
                'input': 'short',
                'loc': ['body', 'password'],
                'msg': 'Value error, Password must be at least 8 characters long',
                'type': 'value_error'
            }]
        }
        assert response.json() == expected_response

    def test_registration_without_username(self):
        response = client.post("/users/register", json={
            "username": "",
            "email": "newuser@example.com",
            "password": "validPassword123"
        })
        assert response.status_code == 400
        assert response.json() == {"detail": "Username is required"}

    def test_registration_with_invalid_email(self):
        response = client.post("/users/register", json={
            "username": "validUser",
            "email": "notanemail",
            "password": "validPassword123"
        })
        assert response.status_code == 422  # Проверка на некорректный формат email
        assert "value is not a valid email address" in response.json()["detail"][0]["msg"]


class TestLogin(unittest.TestCase):

    def test_successful_login(self):
        response = client.post("/users/login", json={"email": "user@example.com", "password": "correctpassword"})
        assert response.status_code == 200
        assert response.json() == {"success": True, "token": "some_jwt_token_here"}

    def test_login_with_incorrect_password(self):
        response = client.post("/users/login", json={"email": "user@example.com", "password": "wrongpassword"})
        assert response.status_code == 401
        assert response.json() == {"detail": "Incorrect password"}

    def test_login_with_nonexistent_email(self):
        response = client.post("/users/login", json={"email": "nonexistent@example.com", "password": "any_password"})
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}


class TestSearchBooks(unittest.TestCase):

    def test_search_books_gatsby(self):
        response = client.get("/books?query=gatsby")
        assert response.status_code == 200
        assert response.json() == {"success": True,
                                   "books": [{"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}]}

    def test_search_books_tolkien(self):
        response = client.get("/books?query=tolkien")
        assert response.status_code == 200
        assert response.json() == {"success": True, "books": [
            {"id": 2, "title": "The Lord of the Rings", "author": "J.R.R. Tolkien"}]}

    def test_search_books_empty_query(self):
        response = client.get("/books?query=")
        assert response.status_code == 400
        assert response.json() == {"detail": "Search query cannot be empty"}

    def test_search_books_no_results(self):
        response = client.get("/books?query=nonexistent")
        assert response.status_code == 200
        assert response.json() == {"success": True, "books": []}

    def test_search_books_no_query(self):
        response = client.get("/books")
        assert response.status_code == 400
        assert response.json() == {"detail": "Search query cannot be empty"}


class TestAddToCart(unittest.TestCase):

    def test_add_to_cart_success(self):
        response = client.post("/users/1/cart", json={"bookId": 100})
        assert response.status_code == 200
        assert response.json() == {"success": True, "message": "Book 100 added to user 1's cart"}

    def test_add_to_cart_invalid_user_id(self):
        response = client.post("/users/0/cart", json={"bookId": 100})
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}

    def test_add_to_cart_invalid_book_id(self):
        response = client.post("/users/1/cart", json={"bookId": 0})
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid book ID"}

    def test_add_to_cart_server_error(self):
        response = client.post("/users/999/cart", json={"bookId": 100})
        assert response.status_code == 500
        assert response.json() == {"detail": "Server error while adding to cart"}


class TestCheckout(unittest.TestCase):

    def test_checkout_success(self):
        response = client.post("/users/3/checkout", json={"payment_method": "credit_card"})
        assert response.status_code == 200
        assert response.json() == {"success": True, "amount": 29.99}

    def test_checkout_user_not_found(self):
        response = client.post("/users/0/checkout", json={"payment_method": "credit_card"})
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}

    def test_checkout_cart_empty(self):
        response = client.post("/users/1/checkout", json={"payment_method": "credit_card"})
        assert response.status_code == 200
        assert response.json() == {"success": False, "message": "Cart is empty"}

    def test_checkout_item_out_of_stock(self):
        response = client.post("/users/2/checkout", json={"payment_method": "credit_card"})
        assert response.status_code == 200
        assert response.json() == {"success": False, "message": "Item out of stock"}

    def test_checkout_server_error(self):
        response = client.post("/users/999/checkout", json={"payment_method": "credit_card"})
        assert response.status_code == 500
        assert response.json() == {"detail": "Server error during checkout"}
