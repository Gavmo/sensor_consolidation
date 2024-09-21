"""
Use fast API to provide an endpoint to collect data points from field deployed equipment.

Deployed equipment should provide:
  - Classification (temp, voltage, etc)
  - Name
  - ID
  - value
  - unit
  - timestamp

API will load this data to the DB.

On first contact with the API, the field equipment must provide its identity.  DB will provide the equipment with its
ID.  Field equipment then only needs to send that ID.

Security requirement is low and can be a pre shared key


"""
import os

from fastapi import FastAPI
from objects import SensorIdent, SensorData

from db import SensorDataBase


sensor_db = SensorDataBase('db/tes.db')


app = FastAPI(title="API")


@app.post("/api/sensor/register")
def register_sensor(sensor_ident: SensorIdent):
    """
    Sensor reports name, classification, value, unit.

    DB check carried out to find an existing ID.  If no existing ID can be matched to name, classification, unit,
    then new entry is created and returned

    :return: integer
    """
    return sensor_db.register_sensor(sensor_ident.name,
                                     sensor_ident.classification,
                                     sensor_ident.unit
                                     )


@app.post("/api/send_data")
def collect_data(sensor_id, timestamp, value):
    """
    Provide to the API the sensor ID, timestamp, value.

    Probaly no need for a return value.  HTTP 200 is ok.
    :return:
    """

    return sensor_db.record_sensor_data(sensor_id,
                                        timestamp,
                                        value
                                        )


@app.post("/api/getsensordata")
def get_sensor_data(sensor_id, date_from=None):
    try:
        return sensor_db.retrieve_data(sensor_id, date_from=date_from)
    except Exception as e:
        return e.args
