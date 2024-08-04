CREATE TABLE IF NOT EXISTS ft_email_sending (
    id_email_sending INT UNIQUE,
    id_campaign INT,
    fl_email_opened BOOLEAN,
    fl_email_clicked BOOLEAN,
    send_date TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dm_email_sending (
    id_email_sending INT,
    receiver_email VARCHAR(255),
    receiver_user_type VARCHAR(255),
    email_token CHAR(32),
    email_sender VARCHAR(255),
    opened_at TIMESTAMP,
    clicked_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dm_email_campaign (
    id_campaign INT UNIQUE,
    company_name VARCHAR(255),
    email_subject VARCHAR(255)
);
