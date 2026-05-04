from fastapi import FastAPI

from app.api import login, user

app = FastAPI()


# Infrastructure route/status (Root)
@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Engenharia do Zero, API ativa e conectada ao banco"}


app.include_router(login.router, prefix="/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/users", tags=["Users"])
