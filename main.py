from fastapi import FastAPI
from config.db import Base, engine
from routes.garage_router import garage_router
from routes.car_router import car_router
from routes.maintenance_router import maintenance_router

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(garage_router)
app.include_router(car_router)
app.include_router(maintenance_router)

for route in app.routes:
    print(f"{route.path} -> {route.name}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Movie API!"}
