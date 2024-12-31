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


stations = []



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

