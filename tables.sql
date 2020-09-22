CREATE TABLE IF NOT EXISTS employment (
    id integer PRIMARY KEY,
    entry_date timestamptz NOT NULL,
    date_from date,
    date_to date,
    place text
);