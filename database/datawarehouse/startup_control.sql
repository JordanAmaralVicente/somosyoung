CREATE TABLE IF NOT EXISTS startup_control (
    id SERIAL,
    startup_time TIMESTAMP
);

INSERT INTO startup_control (startup_time) VALUES (CURRENT_TIMESTAMP);
