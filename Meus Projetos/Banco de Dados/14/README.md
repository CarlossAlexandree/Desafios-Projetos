## Análise de Sentimentos com Language Studio no Azure AI

📌 Sobre o Projeto:

- Projeto prático de Análise de Sentimento utilizando o Azure AI Language Studio. Demonstrando como configurar recursos no Azure, acessar o Language Studio e aplicar técnicas de Processamento de Linguagem Natural (PLN) para analisar textos.

---

## 🚀 Objetivos:

- Entender a diferença entre recursos Text Analytics e Azure AI Language.

- Configurar corretamente um recurso de Language no Azure.

- Utilizar o Language Studio para análise de sentimento.

- Explorar casos de uso aplicáveis em projetos reais.

---

## Configuração do Recurso no Azure

Durante este laboratório, foi criado o recurso **idiomasantiago** no Azure, com as seguintes características:

- Nome do recurso: idiomasantiago
- Grupo de recursos: Santiago.profissional-rg
- Assinatura: Azure subscription 1
- Região: East US
- Tipo de API: TextAnalytics (modelo antigo)
- Faixa de preço: Gratuito (F0)
- Endpoint: https://idiomasantiago.cognitiveservices.azure.com/

⚠️ Observação: Este recurso foi criado na camada gratuita (F0) e está ativo, porém não pôde ser utilizado diretamente no **Language Studio**, pois o Studio exige recursos do tipo **Azure AI Language**.  
Essa limitação foi registrada como parte da prática, servindo de aprendizado sobre a diferença entre **TextAnalytics** e **Language** dentro do Azure.

---

## Consumir via API

Exemplo em Python:

<img width="570" height="354" alt="image" src="https://github.com/user-attachments/assets/72c905c6-5673-41ae-ad18-1e5f1a60e00c" />



response = requests.post(url, headers=headers, json=body)
print(response.json())"

---

## 📊 Resultados Esperados

- Textos positivos → retornam sentimento positivo.

- Textos negativos → retornam sentimento negativo.

- Textos neutros → retornam sentimento neutro.

---

## 🎯 Aplicações

- Monitoramento de redes sociais.

- Análise de feedback de clientes.

- Suporte em call centers.

- Estudos acadêmicos em PLN

