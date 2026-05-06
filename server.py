from fastapi import FastAPI
from app.routes.client.route_client import route_client
from app.routes.hotel.hotel_rout_auth import hotel_auth_route
from app.routes.order.route_order import route_order
from app.routes.product.route_product import route_product
from fastapi.middleware.cors import CORSMiddleware
cors_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "0.0.0.0:5173",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(route_client)
app.include_router(hotel_auth_route)
app.include_router(route_order)
app.include_router(route_product)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)