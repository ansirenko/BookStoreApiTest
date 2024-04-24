from fastapi import FastAPI

from models import UserRegistration, UserLogin, BookSearch, AddToCart, Checkout

app = FastAPI()


@app.post("/users/register")
async def register_user(user: UserRegistration):
    return {"success": True, "userId": 1}


@app.post("/users/login")
async def login_user(user: UserLogin):
    return {"success": True, "token": "some_jwt_token_here"}


@app.get("/books")
async def search_books(query: BookSearch):
    return {"success": True, "books": [{"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}]}


@app.post("/users/{userId}/cart")
async def add_to_cart(userId: int, cart: AddToCart):
    return {"success": True}


@app.post("/users/{userId}/checkout")
async def checkout(userId: int, checkout: Checkout):
    return {"success": True, "amount": 29.99}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
