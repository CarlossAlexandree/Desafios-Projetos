// src/validators/produtoValidator.js

// Função para validar dados de produto
function validarProduto(dados) {
  const erros = [];

  if (!dados.nome || typeof dados.nome !== 'string') {
    erros.push('Nome do produto é obrigatório e deve ser texto.');
  }

  if (!dados.preco || typeof dados.preco !== 'number') {
    erros.push('Preço do produto é obrigatório e deve ser número.');
  }

  return erros;
}

module.exports = { validarProduto };
