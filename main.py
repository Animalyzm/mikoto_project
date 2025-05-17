from fastapi import FastAPI
from pydantic import BaseModel


class Data(BaseModel):
    data: str


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/test")
async def post_test(data: Data):
    print(type(data), data)
    return {"message": "data received"}


# サーバー起動: uvicorn main:app --reload --port 8010
