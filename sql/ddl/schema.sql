-- Esquema do banco de dados dados_clinicos
-- Segue o DER do enunciado: tb_paciente como tabela fato, com FKs para
-- as tabelas de dominio (classe_trabalho, estado_civil, raca, escolaridade, estado).

CREATE TABLE IF NOT EXISTS tb_estado (
    cod_estado INT PRIMARY KEY,
    estado VARCHAR(45) NOT NULL,
    sigla CHAR(2) NOT NULL,
    regiao VARCHAR(45) NOT NULL,
    pais VARCHAR(45) NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_classe_trabalho (
    cod_classe_trabalho INT PRIMARY KEY,
    classe_trabalho VARCHAR(45) NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_estado_civil (
    cod_estado_civil INT PRIMARY KEY,
    estado_civil VARCHAR(45) NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_raca (
    cod_raca INT PRIMARY KEY,
    raca VARCHAR(45) NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_escolaridade (
    cod_escolaridade INT PRIMARY KEY,
    escolaridade VARCHAR(45) NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_paciente (
    cod_paciente INT PRIMARY KEY,
    cod_estado_civil INT NOT NULL,
    cod_raca INT NOT NULL,
    cod_escolaridade INT NOT NULL,
    cod_classe_trabalho INT NOT NULL,
    cod_estado INT NOT NULL,
    genero VARCHAR(45) NOT NULL,
    idade INT NOT NULL,
    qtd_filho INT NOT NULL,
    salario DECIMAL(10, 2) NOT NULL,
    peso DECIMAL(10, 2) NOT NULL,
    colesterol DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_paciente_estado_civil FOREIGN KEY (cod_estado_civil) REFERENCES tb_estado_civil (cod_estado_civil),
    CONSTRAINT fk_paciente_raca FOREIGN KEY (cod_raca) REFERENCES tb_raca (cod_raca),
    CONSTRAINT fk_paciente_escolaridade FOREIGN KEY (cod_escolaridade) REFERENCES tb_escolaridade (cod_escolaridade),
    CONSTRAINT fk_paciente_classe_trabalho FOREIGN KEY (cod_classe_trabalho) REFERENCES tb_classe_trabalho (cod_classe_trabalho),
    CONSTRAINT fk_paciente_estado FOREIGN KEY (cod_estado) REFERENCES tb_estado (cod_estado)
);
