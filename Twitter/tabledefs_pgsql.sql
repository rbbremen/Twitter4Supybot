CREATE TABLE tblTwitter (
    id SERIAL NOT NULL
              PRIMARY KEY,
    twitt VARCHAR(180) NOT NULL
);

INSERT INTO tblTwitter (twitt) VALUES('Table for Supybot-Twitter-plugin on PostgreSQL.');
