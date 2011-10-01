CREATE TABLE tblTwitter (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    twitt VARCHAR(180) NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO tblTwitter (twitt) VALUES('Table for Supybot-Twitter-plugin on MySQL.');
