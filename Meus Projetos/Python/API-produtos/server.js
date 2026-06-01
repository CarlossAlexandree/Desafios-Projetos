const express = require('express');
const app = express();

app.use(express.json());

// Importa função que carrega rotas
const { carregarRotas } = require('./src/index');
carregarRotas(app);

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
});
