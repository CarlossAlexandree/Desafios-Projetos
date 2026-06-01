// Simulação de banco em memória
let produtos = [];

exports.criarProduto = (req, res) => {
  const { nome, preco } = req.body;
  const id = produtos.length + 1;
  const novoProduto = { id, nome, preco };
  produtos.push(novoProduto);
  res.status(201).json(novoProduto);
};

exports.listarProdutos = (req, res) => {
  res.json(produtos);
};

exports.editarProduto = (req, res) => {
  const { id } = req.params;
  const { nome, preco } = req.body;
  const produto = produtos.find(p => p.id == id);

  if (!produto) {
    return res.status(404).json({ mensagem: 'Produto não encontrado' });
  }

  produto.nome = nome;
  produto.preco = preco;
  res.json(produto);
};

exports.excluirProduto = (req, res) => {
  const { id } = req.params;
  produtos = produtos.filter(p => p.id != id);
  res.json({ mensagem: 'Produto removido com sucesso' });
};
