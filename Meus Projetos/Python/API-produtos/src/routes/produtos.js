const express = require('express');
const router = express.Router();

// Importa controller
const produtosController = require('../controllers/produtosController');

// Rotas CRUD
router.post('/', produtosController.criarProduto);
router.get('/', produtosController.listarProdutos);
router.put('/:id', produtosController.editarProduto);
router.delete('/:id', produtosController.excluirProduto);

module.exports = router;
