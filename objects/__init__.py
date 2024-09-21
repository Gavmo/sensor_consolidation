from pydantic import BaseModel


class SensorData(BaseModel):
    timestamp: int
    value: float


class SensorIdent(BaseModel):
    name: str
    classification: str
    unit: str
    sensor_data: list = []

    def add_sensor_data(self, data: SensorData):
        if not hasattr(self, "sensor_data"):
            setattr(self, "sensor_data", [data])
        else:
            getattr(self, "sensor_data").append(data)
