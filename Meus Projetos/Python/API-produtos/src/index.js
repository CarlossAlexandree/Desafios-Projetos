const express = require('express');
const produtosRoutes = require('./routes/produtos');

const app = express();
const port = 3000;

app.use(express.json());
app.use('/api/products', produtosRoutes);

app.listen(port, () => {
  console.log(`API rodando em http://localhost:${port}`);
});
