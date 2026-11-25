CREATE TABLE plantas (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    pais VARCHAR(100) NOT NULL,
    capacidad DECIMAL(10,2) None
);

CREATE TABLE salmon_production (
    planta VARCHAR(100) NOT NULL,
    fecha DATE NOT NULL,
    toneladas DECIMAL(10,2) NOT NULL,
    calidad VARCHAR(10) NOT NULL,
    planta_id INTEGER REFERENCES plantas(id),
    PRIMARY KEY (planta, fecha)
);
