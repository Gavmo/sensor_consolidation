import os
import sqlite3


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
