SELECT 'CREATE DATABASE replacedbname' 
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'replacedbname')\gexec
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_user WHERE usename = 'replacerepluser') THEN
        CREATE USER replacerepluser WITH REPLICATION ENCRYPTED PASSWORD 'replacereplpassword'; 
    END IF; 
END $$;

\c replacedbname;
CREATE TABLE IF NOT EXISTS emails(
    id INT PRIMARY KEY,
    email VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS phones(
    id INT PRIMARY KEY,
    phone VARCHAR(255) NOT NULL
);
INSERT INTO emails(id, email) VALUES(1, 'sasha@mail.ru') ON CONFLICT DO NOTHING;
INSERT INTO emails(id, email) VALUES(2, 'sasha2@mail.ru') ON CONFLICT DO NOTHING;
INSERT INTO emails(id, email) VALUES(3, 'sasha3@gmail.com') ON CONFLICT DO NOTHING;
INSERT INTO phones(id, phone) VALUES(1, '89111111111') ON CONFLICT DO NOTHING;
INSERT INTO phones(id, phone) VALUES(2, '89111111112') ON CONFLICT DO NOTHING;
INSERT INTO phones(id, phone) VALUES(3, '89111111113') ON CONFLICT DO NOTHING;