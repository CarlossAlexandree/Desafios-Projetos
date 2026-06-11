

USE ecommerce;

show tables;

INSERT INTO client (Fname, Minit, Lname, CPF, Address) VALUES
('Carlos', 'A', 'Silva', '12345678901', 'Rua A, 100'),
('Ana', 'B', 'Souza', '98765432100', 'Rua B, 200'),
('João', 'C', 'Pereira', '45678912300', 'Rua C, 300');


INSERT INTO product (Pname, Classification_kids, Category, Avaliacao, Size) VALUES
('Notebook', FALSE, 'Eletrônico', 4.5, 'M',NULL),
('Camisa', FALSE, 'Vestimenta', 4.0, 'G',NULL),
('Boneca', TRUE, 'Brinquedos', 5.0, 'P',NULL);


INSERT INTO supplier (socialName, CNPJ, contact) VALUES
('Tech Distribuidora', '11111111111111', '85999990001'),
('Moda Brasil', '22222222222222', '85999990002'),
('Eletrônica Santiago', '22222224444444', '85999991235');


INSERT INTO seller (socialName, AbstName, CNPJ, CPF, Location, contact) VALUES
('Vendas Online LTDA', 'VOL', '33333333333333', NULL, 'Fortaleza', '85999990003'),
('Marketplace XP', 'MXP', '44444444444444', NULL, 'São Paulo', '85999990004');


INSERT INTO productSeller (idSeller, idProduct, prodQuantity) VALUES
(1, 1, 10),
(1, 2, 20),
(2, 3, 15);


INSERT INTO productStorage (storageLocation, quantity) VALUES
('Rio de Janeiro', 100),
('São Paulo', 200)
('Brasilia', 60);


INSERT INTO storageLocation (idProduct, idProdStorage, quantity) VALUES
(1, 1, 'RJ'),
(2, 1, 'SP'),
(3, 2, 'CE');


INSERT INTO payments (idClient, id_payment, typePayment, limitAvailable) VALUES
(1, 1, 'Cartão', 5000),
(2, 1, 'Boleto', 2000),
(3, 1, 'Dois Cartões', 8000);


INSERT INTO orders 
(idOrdersClient, ordersStatus, ordersDescription, sendValue, paymentCash)
VALUES
(1, DEFAULT, 'compra via aplicativo', NULL, 1),
(2, DEFAULT, 'compra via aplicativo', 50, 0),
(3, 'Confirmado', NULL, NULL, 1),
(1, DEFAULT, 'compra via web site', 150, 0);

INSERT INTO productOrder 
(idProduct, idOrder, porQuantity, poStatus)
VALUES
(1, 5, 2, NULL),
(2, 5, 1, NULL),
(3, 6, 1, NULL);


SELECT * FROM client;
SELECT * FROM product;
SELECT * FROM seller;
SELECT * FROM orders;
SELECT * FROM productOrder;

-- JOIN clássico
SELECT 
    c.Fname,
    o.idOrder,
    o.ordersStatus,
    p.Pname,
    po.porQuantity
FROM orders o
JOIN client c ON o.idOrdersClient = c.idClient
JOIN productOrder po ON po.idOrder = o.idOrder
JOIN product p ON p.idProduct = po.idProduct;

SELECT COUNT(*) FROM client;
SELECT *
FROM client c
JOIN orders o
  ON c.idClient = o.idOrdersClient;

/* ==========================================
   QUANTOS PEDIDOS REALIZADO POR CLIENTE
============================================= */

SELECT 
    c.idClient,
    c.Fname,
    COUNT(o.idOrder) AS Number_of_orders
FROM client c
INNER JOIN orders o 
    ON c.idClient = o.idOrdersClient
INNER JOIN productOrder p 
    ON p.idOrder = o.idOrder
GROUP BY c.idClient, c.Fname;

/* ==========================================
   Clientes que fizeram mais de 1 pedido pago
============================================= */

SELECT c.nome,
       SUM(ip.quantidade * ip.preco_unitario) AS faturamento_total
FROM cliente c
JOIN pedido p ON c.id_cliente = p.id_cliente
JOIN item_pedido ip ON p.id_pedido = ip.id_pedido
GROUP BY c.nome
ORDER BY faturamento_total DESC;



