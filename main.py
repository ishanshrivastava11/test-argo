from fastapi import FastAPI, Response, Request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import uvicorn

app = FastAPI()

# Prometheus metric to count requests
REQUEST_COUNT = Counter("request_count", "Total number of HTTP requests")

@app.middleware("http")
async def count_requests(request: Request, call_next):
    REQUEST_COUNT.inc()
    response = await call_next(request)
    return response


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/metrics")
def metrics():
    # Expose Prometheus metrics
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
