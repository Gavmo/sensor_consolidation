import os
import sqlite3

from objects import SensorIdent, SensorData


class SensorDataBase:
    def __init__(self, db_file):
        #  If the DB file does not exist, build the pre defined schema
        if not os.path.exists(db_file):
            self.data = sqlite3.connect(db_file, check_same_thread=False)
            with open("db_build.sql", 'r') as db_definition:
                cursor = self.data.cursor()
                cursor.executescript(db_definition.read())
                self.data.commit()
                cursor.close()
        else:
            self.data = sqlite3.connect(db_file, check_same_thread=False)

    def register_sensor(self, name, classification, unit):
        cursor = self.data.cursor()
        # Check for existing records
        id = self.get_id(name, classification, unit)
        if len(id) != 0:
            return_val = id[0][0]
        else:
            cursor.execute(
                f"""
                    INSERT INTO sensor_ident (classification_id, unit_id, sensor_name) VALUES
                    (
                     (SELECT classification_id 
                      FROM classification_ref 
                      WHERE classification = '{classification}'
                      ),
                     (SELECT unit_id 
                      FROM unit_ref 
                      WHERE unit_name = '{unit}'
                      ),
                      '{name}'
                    );
                """
            )
            self.data.commit()
            return_val = self.get_id(name, classification, unit)[0][0]
        return return_val

        pass

    def get_id(self, name, classification, unit):
        cursor = self.data.cursor()
        cursor.execute(f"""SELECT sensor_id 
                           FROM sensor_ident 
                           WHERE classification_id=(SELECT classification_id 
                                                 FROM classification_ref 
                                                 WHERE classification = '{classification}')
                           AND sensor_name = '{name}'
                           AND unit_id = (SELECT unit_id 
                                          FROM unit_ref 
                                          WHERE unit_name = '{unit}');
                        """
                       )
        return cursor.fetchall()

    def record_sensor_data(self, sensor_id, timestamp, value):
        cursor = self.data.cursor()
        cursor.execute(
            f"""
            INSERT INTO sensor_data (sensor_id, timestamp, data_value) VALUES
            ({int(sensor_id)},
             '{timestamp}',
             '{value}'
            );
            """
        )
        self.data.commit()
        cursor.close()

    def retrieve_data(self, sensor_id, date_from=None):
        """Get the data from a given sensor.  Optionally provide a unix timestamp to gety everything after that date"""
        query = f"""
                SELECT sd.sensor_id,
                sid.sensor_name,
                cls.classification,
                sd.record_id,
                sd.timestamp,
                sd.data_value,
                units.unit_name, 
                units.unit_si
                FROM sensor_data sd
                INNER JOIN sensor_ident sid ON
                sid.sensor_id = sd.sensor_id
                INNER JOIN unit_ref units ON
                units.unit_id = sid.sensor_id
                INNER JOIN classification_ref cls ON
                cls.classification_id = sid.classification_id
                WHERE sd.sensor_id = {sensor_id}
                """
        # Append the date filter
        if date_from:
            query += f"""AND timestamp > {date_from}"""
        cursor = self.data.cursor()
        cursor.execute(query)
        # Use the first row to instantiate the return object
        first_row = cursor.fetchone()
        data = SensorIdent(name=first_row[1],
                           classification=first_row[2],
                           unit=first_row[6]
                           )
        data.add_sensor_data(SensorData(timestamp=first_row[4],
                                        value=first_row[5]
                                        )
                             )
        for record in cursor.fetchall():
            data.add_sensor_data(SensorData(timestamp=record[4],
                                            value=record[5]
                                            )
                                 )
        return data

    def hello_world(self, var):

        return var



# For testing
if __name__ == '__main__':
    try:
        db = SensorDataBase("tes.db")
    except:
        del db
        os.remove("tes.db")
    # Remove automatically during testing
    for row in db.data.cursor().execute("Select * from classification_ref;"):
        print(row)
    print(db.register_sensor("test_sensor", "Temperature", "Celsius"))
    print(db.register_sensor("test_sensor2", "Temperature", "Celsius"))
    print(db.register_sensor("test_sensor3", "Temperature", "Celsius"))
    db.record_sensor_data(2, 1234453, 444.4)
    print(db.data.cursor().execute("Select * from sensor_data;").fetchall()[0])
    # del db
    # os.remove("tes.db")
