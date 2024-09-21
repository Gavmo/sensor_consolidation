from pydantic import BaseModel


class SensorIdent(BaseModel):
    name: str
    classification: str
    unit: str