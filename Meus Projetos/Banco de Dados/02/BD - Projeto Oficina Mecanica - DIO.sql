/* ==========================================
   BASE DE DADOS - OFICINA 
============================================= */

CREATE DATABASE oficina_mecanica;
USE oficina_mecanica;

CREATE TABLE cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100)
);

CREATE TABLE veiculo (
    id_veiculo INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(10) UNIQUE NOT NULL,
    modelo VARCHAR(50),
    ano INT,
    id_cliente INT,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

CREATE TABLE funcionario (
    id_funcionario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    cargo VARCHAR(50)
);

CREATE TABLE ordem_servico (
    id_ordem INT AUTO_INCREMENT PRIMARY KEY,
    data_abertura DATE,
    status VARCHAR(30),
    id_veiculo INT,
    id_funcionario INT,
    FOREIGN KEY (id_veiculo) REFERENCES veiculo(id_veiculo),
    FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario)
);

CREATE TABLE servico (
    id_servico INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(100),
    valor DECIMAL(10,2)
);

CREATE TABLE peca (
    id_peca INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    valor DECIMAL(10,2)
);

CREATE TABLE ordem_servico_servico (
    id_ordem INT,
    id_servico INT,
    PRIMARY KEY (id_ordem, id_servico),
    FOREIGN KEY (id_ordem) REFERENCES ordem_servico(id_ordem),
    FOREIGN KEY (id_servico) REFERENCES servico(id_servico)
);

CREATE TABLE ordem_servico_peca (
    id_ordem INT,
    id_peca INT,
    quantidade INT,
    PRIMARY KEY (id_ordem, id_peca),
    FOREIGN KEY (id_ordem) REFERENCES ordem_servico(id_ordem),
    FOREIGN KEY (id_peca) REFERENCES peca(id_peca)
);

INSERT INTO cliente (nome, telefone, email) VALUES
('João Silva', '99999-1111', 'joao@email.com'),
('Maria Souza', '98888-2222', 'maria@email.com');

INSERT INTO veiculo (placa, modelo, ano, id_cliente) VALUES
('ABC-1234', 'Onix', 2020, 1),
('DEF-5678', 'Corolla', 2019, 2);

INSERT INTO funcionario (nome, cargo) VALUES
('Carlos Mecânico', 'Mecânico'),
('Ana Gestora', 'Atendente');

INSERT INTO servico (descricao, valor) VALUES
('Troca de óleo', 120.00),
('Alinhamento', 150.00),
('Revisão completa', 500.00);

INSERT INTO peca (nome, valor) VALUES
('Filtro de óleo', 40.00),
('Pastilha de freio', 200.00);

INSERT INTO ordem_servico (data_abertura, status, id_veiculo, id_funcionario) VALUES
('2025-01-10', 'Finalizada', 1, 1),
('2025-01-15', 'Em andamento', 2, 1);

INSERT INTO ordem_servico_servico (id_ordem, id_servico)
SELECT os.id_ordem, s.id_servico
FROM ordem_servico os, servico s
WHERE os.id_ordem = 1 AND s.descricao = 'Troca de óleo'
UNION ALL
SELECT os.id_ordem, s.id_servico
FROM ordem_servico os, servico s
WHERE os.id_ordem = 1 AND s.descricao = 'Alinhamento'
UNION ALL
SELECT os.id_ordem, s.id_servico
FROM ordem_servico os, servico s
WHERE os.id_ordem = 2 AND s.descricao = 'Revisão completa';



INSERT INTO ordem_servico_peca (id_ordem, id_peca, quantidade)
VALUES (1,1,1)
ON DUPLICATE KEY UPDATE
quantidade = quantidade + VALUES(quantidade);


/* ==========================================
   TOTAL FATURADO POR ORDEM DE SERVIÇO
============================================= */

SELECT 
    os.id_ordem,
    SUM(s.valor) + SUM(p.valor * osp.quantidade) AS total_ordem
FROM ordem_servico os
JOIN ordem_servico_servico oss ON os.id_ordem = oss.id_ordem
JOIN servico s ON oss.id_servico = s.id_servico
JOIN ordem_servico_peca osp ON os.id_ordem = osp.id_ordem
JOIN peca p ON osp.id_peca = p.id_peca
GROUP BY os.id_ordem;

/* ==========================================
   Clientes que gastaram mais de R$ 500,00
============================================= */

SELECT 
    c.nome,
    SUM(s.valor) + SUM(p.valor * osp.quantidade) AS total_gasto
FROM cliente c
JOIN veiculo v ON c.id_cliente = v.id_cliente
JOIN ordem_servico os ON v.id_veiculo = os.id_veiculo
JOIN ordem_servico_servico oss ON os.id_ordem = oss.id_ordem
JOIN servico s ON oss.id_servico = s.id_servico
JOIN ordem_servico_peca osp ON os.id_ordem = osp.id_ordem
JOIN peca p ON osp.id_peca = p.id_peca
GROUP BY c.id_cliente
HAVING total_gasto > 500;

/* ==========================================
   Funcionarios com mais de uma Ordem de Serviço
============================================= */

SELECT 
    f.nome,
    COUNT(os.id_ordem) AS total_ordens
FROM funcionario f
JOIN ordem_servico os ON f.id_funcionario = os.id_funcionario
GROUP BY f.id_funcionario
HAVING total_ordens > 1;

/* ==========================================
   Serviço mais realizado
============================================= */

SELECT descricao
FROM servico
WHERE id_servico = (
    SELECT id_servico
    FROM ordem_servico_servico
    GROUP BY id_servico
    ORDER BY COUNT(*) DESC
    LIMIT 1
);

/* ===============================================
   O.s em andamento com valor maior que R$ 300,00
=============================================== */

SELECT 
    os.id_ordem,
    SUM(s.valor) AS total_servicos
FROM ordem_servico os
JOIN ordem_servico_servico oss ON os.id_ordem = oss.id_ordem
JOIN servico s ON oss.id_servico = s.id_servico
WHERE os.status = 'Em andamento'
GROUP BY os.id_ordem
HAVING total_servicos > 300;

Show tables;











