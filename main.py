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

from fastapi import FastAPI

app = FastAPI()


def register_sensor():
    """
    Sensor reports name, classification, value, unit.

    DB check carried out to find an existing ID.  If no existing ID can be matched to name, classification, unit,
    then new entry is created and returned

    :return: integer
    """
    pass


def collect_data():
    """
    Provide to the API the sensor ID, timestamp, value.

    Probaly no need for a return value.  HTTP 200 is ok.
    :return:
    """
    pass
