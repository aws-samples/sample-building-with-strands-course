from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to the API"}


@app.get("/users")
def list_users():
    return [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
    ]


@app.get("/users/{user_id}")
def get_user(user_id: int):
    users = {1: "Alice", 2: "Bob"}
    if user_id in users:
        return {"id": user_id, "name": users[user_id]}
    return {"error": "User not found"}


@app.get("/health")
def health():
    return {"status": "healthy"}
