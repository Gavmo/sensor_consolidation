import os
import sqlite3


class SensorDataBase:
    def __init__(self, db_file):
        #  If the DB file does not exist, build the pre defined schema
        if not os.path.exists(db_file):
            self.data = sqlite3.connect(db_file)
            with open("db_build.sql", 'r') as db_definition:
                cursor = self.data.cursor()
                cursor.executescript(db_definition.read())
        else:
            self.data = sqlite3.connect(db_file)

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
    # del db
    # os.remove("tes.db")
