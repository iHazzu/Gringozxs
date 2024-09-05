CREATE TABLE channels(
    id INT AUTO_INCREMENT PRIMARY KEY,
    discord_channel_id BIGINT UNIQUE,
    min_followers INT DEFAULT 0,
    max_followers INT,
    min_tweets INT DEFAULT 0,
    max_tweets INT
);