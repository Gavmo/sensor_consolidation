
CREATE TABLE sensor_ident(
    sensor_id INTEGER PRIMARY KEY,
    classification_id INTEGER,
    unit_id INTEGER,
    sensor_name TEXT
);

CREATE TABLE classification_ref(
    classification_id INTEGER PRIMARY KEY,
    classification TEXT
);

CREATE TABLE sensor_data(
    record_id INTEGER PRIMARY KEY,
    sensor_id INTEGER,
    timestamp INTEGER,
    data_value REAL
);

CREATE TABLE unit_ref(
    unit_id INTEGER PRIMARY KEY,
    unit_name TEXT,
    unit_si TEXT
);

INSERT INTO unit_ref (unit_name, unit_si) VALUES (
    'Celsius',
    'C'
);

INSERT INTO unit_ref (unit_name, unit_si) VALUES (
    'Amps',
    'A'
);

INSERT INTO unit_ref (unit_name, unit_si) VALUES (
    'Volts',
    'V'
);

INSERT INTO classification_ref (classification) VALUES (
    'Temperature'
);

INSERT INTO classification_ref (classification) VALUES (
    'Voltage'
);

INSERT INTO classification_ref (classification) VALUES (
    'Current'
);