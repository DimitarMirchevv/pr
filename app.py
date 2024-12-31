from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class ServiceStation(BaseModel):
    station_id: int
    station_name: str
    address: str
    city_name: str
    max_capacity: int

class Vehicle(BaseModel):
    vehicle_id: int
    brand: str
    model_name: str
    year_of_manufacture: int
    plate_number: str
    assigned_stations: List[int]


stations = []
vehicles = []


@app.post("/stations", status_code=201)
def add_service_station(station: ServiceStation):
    stations.append(station)
    return station

@app.get("/stations", response_model=List[ServiceStation])
def list_service_stations(city_name: Optional[str] = None):
    if city_name:
        return [s for s in stations if s.city_name == city_name]
    return stations

@app.get("/stations/{station_id}", response_model=ServiceStation)
def get_station_details(station_id: int):
    station = next((s for s in stations if s.station_id == station_id), None)
    if not station:
        raise HTTPException(status_code=404, detail="Service station not found")
    return station

@app.put("/stations/{station_id}", response_model=ServiceStation)
def modify_service_station(station_id: int, updated_station: ServiceStation):
    index = next((i for i, s in enumerate(stations) if s.station_id == station_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Service station not found")
    stations[index] = updated_station
    return updated_station

@app.delete("/stations/{station_id}", status_code=204)
def remove_service_station(station_id: int):
    global stations
    stations = [s for s in stations if s.station_id != station_id]
    return


@app.post("/vehicles", status_code=201)
def register_vehicle(vehicle: Vehicle):
    vehicles.append(vehicle)
    return vehicle

@app.get("/vehicles", response_model=List[Vehicle])
def list_vehicles(brand: Optional[str] = None, station_id: Optional[int] = None, min_year: Optional[int] = None, max_year: Optional[int] = None):
    result = vehicles
    if brand:
        result = [v for v in result if v.brand == brand]
    if station_id:
        result = [v for v in result if station_id in v.assigned_stations]
    if min_year:
        result = [v for v in result if v.year_of_manufacture >= min_year]
    if max_year:
        result = [v for v in result if v.year_of_manufacture <= max_year]
    return result

@app.get("/vehicles/{vehicle_id}", response_model=Vehicle)
def get_vehicle_details(vehicle_id: int):
    vehicle = next((v for v in vehicles if v.vehicle_id == vehicle_id), None)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@app.put("/vehicles/{vehicle_id}", response_model=Vehicle)
def modify_vehicle(vehicle_id: int, updated_vehicle: Vehicle):
    index = next((i for i, v in enumerate(vehicles) if v.vehicle_id == vehicle_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    vehicles[index] = updated_vehicle
    return updated_vehicle

@app.delete("/vehicles/{vehicle_id}", status_code=204)
def deregister_vehicle(vehicle_id: int):
    global vehicles
    vehicles = [v for v in vehicles if v.vehicle_id != vehicle_id]
    return

