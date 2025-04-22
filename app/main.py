from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Lambda"}


# Entry point for AWS Lambda
handler = Mangum(app)
