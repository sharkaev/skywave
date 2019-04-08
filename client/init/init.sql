CREATE schema telemetry;
SET search_path TO telemetry;

CREATE TABLE telemetry (
    id serial,
    created_at NUMERIC DEFAULT EXTRACT(EPOCH FROM CURRENT_TIMESTAMP),
    data_key TEXT,
    data_value TEXT
);