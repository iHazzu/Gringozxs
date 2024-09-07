CREATE TABLE jogadores(
	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    discord_id BIGINT UNIQUE NOT NULL,
	registrado_em TIMESTAMP DEFAULT current_timestamp,
	pointos INT DEFAULT 0
);