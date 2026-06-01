// src/config/db.js
const mongoose = require('mongoose');

async function conectarDB() {
  try {
    await mongoose.connect('mongodb://localhost:27017/api_produtos', {
      useNewUrlParser: true,
      useUnifiedTopology: true
    });
    console.log('✅ Conectado ao MongoDB');
  } catch (error) {
    console.error('❌ Erro ao conectar ao MongoDB:', error);
  }
}

module.exports = conectarDB;
