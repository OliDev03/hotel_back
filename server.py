# from fastapi import FastAPI
# from app.routes.client.route_client import route_client
# from app.routes.hotel.hotel_rout_auth import hotel_auth_route
# from fastapi.middleware.cors import CORSMiddleware
# from app.model.order.route_order import route_order
# cors_origins = [
#     "http://localhost:5173"
# ]

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=cors_origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(route_client)
# app.include_router(hotel_auth_route)
# app.include_router(route_order)
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.client.route_client import route_client
from app.routes.hotel.hotel_rout_auth import hotel_auth_route
from app.routes.order.route_order import route_order

cors_origins = [
    "http://localhost:5173"
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

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )