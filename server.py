from fastapi import FastAPI
from app.routes.client.route_client import route_client

app = FastAPI()

app.include_router(route_client)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)