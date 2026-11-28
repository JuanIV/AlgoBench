from fastapi import FastAPI, Request
from algobench.api.routes import algorithms
from fastapi.responses import JSONResponse
from algobench.core.exceptions import AlgorithmNotFoundError

app = FastAPI()

@app.exception_handler(AlgorithmNotFoundError)
async def algorithm_not_found_handler(request: Request, exc: AlgorithmNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "ALGORITHM_NOT_FOUND",
                "message": exc.message
            }
        }
    )


app.include_router(algorithms.router)

@app.get("/hello")
def say_hello():
    print("HI")
    return {"message" : "HI"}
