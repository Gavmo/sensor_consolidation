from pydantic import BaseModel


class SensorIdent(BaseModel):
    name: str
    classification: str
    unit: str


class SensorData(BaseModel):
    sensor_id: int
    timestamp: int
    value: float
