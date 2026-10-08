from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from scrapper import get_manga_list

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/users/{user_id}")
def get_info(user_id: int):
    manga_list = get_manga_list(user_id)

    return {
        "status": "success",
        "manga_list": manga_list
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )