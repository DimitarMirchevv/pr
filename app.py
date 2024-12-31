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

class ServiceRequest(BaseModel):
    request_id: int
    vehicle_id: int
    service_category: str
    date_of_service: str
    station_id: int


stations = []
vehicles = []
service_requests = []

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

@app.post("/service-requests", status_code=201)
def create_service_request(request: ServiceRequest):
    station = next((s for s in stations if s.station_id == request.station_id), None)
    if not station:
        raise HTTPException(status_code=404, detail="Service station not found")
    overlapping_requests = [r for r in service_requests if r.station_id == request.station_id and r.date_of_service == request.date_of_service]
    if len(overlapping_requests) >= station.max_capacity:
        raise HTTPException(status_code=400, detail="No available slots at the station on the selected date")
    service_requests.append(request)
    return request

@app.get("/service-requests", response_model=List[ServiceRequest])
def list_service_requests(vehicle_id: Optional[int] = None, station_id: Optional[int] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
    result = service_requests
    if vehicle_id:
        result = [r for r in result if r.vehicle_id == vehicle_id]
    if station_id:
        result = [r for r in result if r.station_id == station_id]
    if start_date:
        result = [r for r in result if r.date_of_service >= start_date]
    if end_date:
        result = [r for r in result if r.date_of_service <= end_date]
    return result

@app.get("/service-requests/{request_id}", response_model=ServiceRequest)
def get_service_request_details(request_id: int):
    request = next((r for r in service_requests if r.request_id == request_id), None)
    if not request:
        raise HTTPException(status_code=404, detail="Service request not found")
    return request

@app.put("/service-requests/{request_id}", response_model=ServiceRequest)
def update_service_request(request_id: int, updated_request: ServiceRequest):
    index = next((i for i, r in enumerate(service_requests) if r.request_id == request_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Service request not found")
    station = next((s for s in stations if s.station_id == updated_request.station_id), None)
    if not station:
        raise HTTPException(status_code=404, detail="Service station not found")
    overlapping_requests = [r for r in service_requests if r.station_id == updated_request.station_id and r.date_of_service == updated_request.date_of_service and r.request_id != request_id]
    if len(overlapping_requests) >= station.max_capacity:
        raise HTTPException(status_code=400, detail="No available slots at the station on the selected date")
    service_requests[index] = updated_request
    return updated_request

@app.delete("/service-requests/{request_id}", status_code=204)
def cancel_service_request(request_id: int):
    global service_requests
    service_requests = [r for r in service_requests if r.request_id != request_id]
    return

