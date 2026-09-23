from fastapi import FastAPI

from api.routes.recommendation import router


app = FastAPI(
    title="Ecommerce Recommendation ML Service",
    version="1.0.0"
)


app.include_router(router)


@app.get("/")
def root():

    return {
        "service": "Ecommerce Recommendation ML Service",
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }