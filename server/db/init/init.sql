CREATE DATABASE telemetry;
CREATE TABLE telemetry.telemetry(
    client_id BIGINT,
    created_at Float64, -- timestamp, milliseconds from January 1 1970
    data_key String, -- names of the metrics
    data_value BIGINT, -- values of the metrics
    d Date MATERIALIZED toDate(round(created_at/1000)), -- auto generate date from ts column
    dt DateTime MATERIALIZED toDateTime(round(created_at/1000)) -- auto generate date time from ts column
) ENGINE = MergeTree(d, client_id, 8192);