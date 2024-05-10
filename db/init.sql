SELECT 'CREATE DATABASE replaceDBNAME' 
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'replaceDBNAME')\gexec
CREATE USER replaceREPLUSER WITH REPLICATION ENCRYPTED PASSWORD 'replaceREPLPASSWORD';
\c replaceDBNAME;
CREATE TABLE emails(
    id INT PRIMARY KEY,
    email VARCHAR(255) NOT NULL
);
CREATE TABLE phones(
    id INT PRIMARY KEY,
    phone VARCHAR(255) NOT NULL
);
INSERT INTO emails(id, email) VALUES(1, 'sasha@mail.ru');
INSERT INTO emails(id, email) VALUES(2, 'sasha2@mail.ru');
INSERT INTO emails(id, email) VALUES(3, 'sasha3@gmail.com');
INSERT INTO phones(id, phone) VALUES(1, '89111111111');
INSERT INTO phones(id, phone) VALUES(2, '89111111112');
INSERT INTO phones(id, phone) VALUES(3, '89111111113');