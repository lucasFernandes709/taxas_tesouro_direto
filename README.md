# Tesouro Direto - Dados Públicos

## Visão Geral

Este projeto tem como objetivo criar um pipeline de engenharia de dados para obter dados públicos do portal [Tesouro Nacional Transparente](https://www.tesourotransparente.gov.br/) utilizando a infraestrutura da AWS.

## Etapa 1 - Dados históricos 

Objetivo: Baixar dados das **Taxas dos Títulos Ofertados pelo Tesouro Direto**, **Investidores do Tesouro Direto** e **Operações do Tesouro Direto** históricos para posterior ingestão no S3.

- Baixar arquivo CSV contendo dados históricos (atualização diária).
- Fazer o upload do arquivo CSV para um bucket S3 da Amazon.

## Pré-requisitos

- **Python**: Este projeto requer Python 3.7 ou superior.
- **Conta AWS**: É necessário ter uma conta AWS para acessar os serviços S3.
- **AWS CLI**: O AWS CLI deve estar configurado com as credenciais apropriadas.