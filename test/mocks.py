from fastapi import FastAPI, HTTPException, status, Query
import sys

sys.path.append('..')

from models import UserRegistration, UserLogin, AddToCart, Checkout

app = FastAPI()


@app.post("/users/register")
async def register_user(user: UserRegistration):
    if "existing" in user.email:
        return {"success": False, "message": "Email already in use"}
    elif len(user.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password too short"
        )
    elif not user.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is required"
        )
    else:
        return {"success": True, "userId": 1}


@app.post("/users/login")
async def login_user(user: UserLogin):
    if user.email == "nonexistent@example.com":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    elif user.password != "correctpassword":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    else:
        return {"success": True, "token": "some_jwt_token_here"}


@app.get("/books")
async def search_books(query: str = Query(None, description="Search query for books")):
    if query is None or query.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty"
        )
    elif query.lower() == "gatsby":
        return {"success": True, "books": [{"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}]}
    elif query.lower() == "tolkien":
        return {"success": True, "books": [{"id": 2, "title": "The Lord of the Rings", "author": "J.R.R. Tolkien"}]}
    else:
        return {"success": True, "books": []}


@app.post("/users/{userId}/cart")
async def add_to_cart(userId: int, cart: AddToCart):
    if userId <= 0:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    elif cart.bookId <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid book ID"
        )
    elif userId == 999:
        raise HTTPException(
            status_code=500,
            detail="Server error while adding to cart"
        )
    else:
        return {"success": True, "message": f"Book {cart.bookId} added to user {userId}'s cart"}


@app.post("/users/{userId}/checkout")
async def checkout(userId: int, checkout: Checkout):
    if userId <= 0:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    elif userId == 1:
        return {"success": False, "message": "Cart is empty"}
    elif userId == 2:
        return {"success": False, "message": "Item out of stock"}
    elif userId == 999:
        raise HTTPException(
            status_code=500,
            detail="Server error during checkout"
        )
    else:
        return {"success": True, "amount": 29.99}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
