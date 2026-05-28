# RELATÓRIO DE IMPLEMENTAÇÃO DE SERVIÇOS AWS

**Data:** 01 de maio de 2026  
**Empresa:** Abstergo Industries  
**Responsável:** Carlos Alexandre Fonseca Santiago  

---

## 1. Introdução
Este relatório apresenta um modelo de processo de implementação de ferramentas na empresa Abstergo Industries (Ficticia). O objetivo do projeto foi elencar 3 serviços AWS, com a finalidade de realizar diminuição de custos imediatos e otimização da infraestrutura computacional.

---

## 2. Descrição do Projeto
O projeto de implementação de ferramentas foi dividido em 3 etapas, cada uma com seus objetivos específicos focados em eficiência financeira e técnica. A seguir, serão descritas as etapas do projeto:

### Etapa 1
* **Nome da ferramenta:** Amazon EC2 Auto Scaling.
* **Foco da ferramenta:** Escalabilidade horizontal automática e otimização contínua de gastos com capacidade computacional.
* **Descrição de caso de uso:** Configuração de um Grupo de Auto Scaling (*Auto Scaling Group*) integrado a instâncias Amazon EC2 de Uso Geral para o servidor de aplicação principal da empresa. O sistema foi parametrizado com políticas de *Dynamic Scaling* (Scaling Dinâmico), permitindo que a infraestrutura aumente ou reduza o número de instâncias ativas baseando-se na demanda real de tráfego de usuários (como picos de acessos em horários comerciais). Isso elimina completamente o custo com capacidade ociosa subutilizada em períodos de baixa demanda (finais de semana e madrugadas), gerando economia imediata no faturamento.

### Etapa 2
* **Nome da ferramenta:** Amazon Simple Storage Service (Amazon S3).
* **Foco da ferramenta:** Armazenamento de objetos de alta durabilidade e gerenciamento inteligente de ciclo de vida de dados com foco em custo-benefício.
* **Descrição de caso de uso:** Migração de todo o repositório de arquivos não estruturados da empresa (backups, logs, relatórios antigos e mídias de sistemas) para Buckets do Amazon S3. Foi implementada a classe de armazenamento *S3 Intelligent-Tiering*, que monitora os padrões de acesso de forma automatizada e move arquivos que não são abertos há mais de 30 dias para camadas de acesso infrequente (*Infrequent Access*). Adicionalmente, dados de auditoria que precisam ser retidos por conformidade legal foram direcionados para a classe *S3 Glacier Deep Archive* (com retenção de longo prazo e custo drasticamente reduzido), diminuindo os custos com storages tradicionais caros.

### Etapa 3
* **Nome da ferramenta:** AWS Lambda.
* **Foco da ferramenta:** Computação Serverless (sem servidor) com cobrança estrita por tempo de execução.
* **Descrição de caso de uso:** Substituição de servidores virtuais ligados 24 horas por dia (24/7), que realizavam apenas rotinas agendadas (scripts de sincronização, processamento de relatórios diários em lote e limpeza de bancos de dados), por funções serverless isoladas. Com o AWS Lambda, o código é executado estritamente quando engatado por eventos específicos, e a Abstergo Industries passa a pagar apenas pelos milissegundos exatos em que o processamento está ocorrendo, reduzindo a zero o custo de servidores ligados esperando por execuções em segundo plano.

---

## 3. Conclusão
A implementação de ferramentas na empresa Abstergo Industries tem como esperado uma redução imediata nas faturas de TI, o provisionamento dinâmico e elástico de recursos alinhados ao negócio e a eliminação de custos com servidores ociosos, o que aumentará a eficiência e a produtividade da empresa. Recomenda-se a continuidade da utilização das ferramentas implementadas e a busca por novas tecnologias gerenciadas que possam melhorar ainda mais os processos e as margens de lucro da empresa.

---

## 4. Anexos
* **Anexo A:** Topologia de Arquitetura de Rede e Computação AWS (Diagrama VPC).
* **Anexo B:** Planilha de Estimativa de Custos de Infraestrutura Antiga vs. Nova (Calculadora de Preços AWS).
* **Anexo C:** Manual Técnico de Políticas de Ciclo de Vida do Amazon S3.
* **Anexo D:** Guia de Monitoramento e Logs de Execução do AWS Lambda.

---

**Assinatura do Responsável pelo Projeto:**  
Carlos Alexandre Fonseca Santiago  
