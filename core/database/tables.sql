CREATE TABLE jogadores(
	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    discord_id BIGINT UNIQUE NOT NULL,
	registrado_em TIMESTAMP DEFAULT current_timestamp,
	pointos INT DEFAULT 0
);

CREATE TABLE corridas(
	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	criador_id INT REFERENCES jogadores(id) ON DELETE SET NULL,
	criado_em TIMESTAMP DEFAULT current_timestamp,
	resultado TEXT
);

CREATE TABLE participantes(
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    jogador_id INT NOT NULL REFERENCES jogadores(id) ON DELETE CASCADE,
    corrida_id INT NOT NULL REFERENCES corridas(id) ON DELETE CASCADE,
    pontos INT DEFAULT 0,
    clipe TEXT NOT NULL,
    posicao INT NOT NULL
);