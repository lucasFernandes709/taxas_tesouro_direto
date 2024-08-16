# Tesouro Direto - Dados Públicos

## Visão Geral

Este projeto tem como objetivo criar um pipeline de engenharia de dados para obter dados públicos do portal [Tesouro Nacional Transparente](https://www.tesourotransparente.gov.br/) utilizando a infraestrutura da AWS.

## Como utilizar ?

1. Inicialmente, crie acesse o console AWS e crie um usuário e chave de acesso através do IAM. Em seguida, crie um bucket no S3 para salvar os dados que serão extraídos.
2. Crie um arquivo `.env` no diretório raiz, e insira o valor das respectivas variáveis, conforme exemplificado no arquivo `.env_template`.
3. Crie um ambiente virtual e instale as bibliotecas necessárias, disponíveis no arquivo `requirements.txt`: `pip install -r requirements.txt`. Se estiver utilizando `poetry`, basta executar `poetry install`.

### Ingestão de dados históricos 

Objetivo: Baixar dados das **Taxas dos Títulos Ofertados pelo Tesouro Direto**, **Investidores do Tesouro Direto** e **Operações do Tesouro Direto** históricos para posterior ingestão no S3.

- Baixar arquivos contendo dados históricos.
- Descompactar arquivo baixado (no caso de .zip).
- Fazer o upload do arquivo CSV para um bucket S3 da AWS.

Execute o script de ingestão dos dados, `src/ingest_data.py` e aguarde o processo finalizar.
- Informações sobre a execução serão salvas no arquivo `log.log`
- Os arquivos são grandes, dependendo da infraestrutura e conexão com a internet, pode levar bastante tempo para a conclusão.
- Tamanho estimado (14-08-2024):
    - Taxas dos Títulos Ofertados pelo Tesouro Direto: 11.6 Mb
    - Investidores do Tesouro Direto: 4.2 Gb (descompactado)
    - Operações do Tesouro Direto: 2.6 Gb (descompactado)

### Consolidação e ETL dos dados no ambiente AWS

Os notebooks `src\etl_raw_data_compilation.ipynb` e `src\etl_data_specialization.ipynb` devem ser executados.
No ambiente AWS, pode-se optar pelo **AWS Glue** ou **EMR** para configurar e executar os códigos.

Uma vez que os dados especializados estiverem salvos nas camadas mais refinadas do S3 (silver/gold), pode-se utilizar um cliente SQL (como o **AWS Athena**) para realizar consultas e conectar-se com *data warehouses* e ferramentas de visualização e reporte (como o **Quicksight**).

Para facilitar a criação e manutenção dos catálogos, schemas e tabelas necessários no Athena, os **Crawlers** e **Catálogos** do Glue são ferramentas bastante úteis.

## Pré-requisitos

- **Python**: Este projeto requer Python 3.7 ou superior.
- **Conta AWS**: É necessário ter uma conta AWS para acessar os serviços S3.

## Contribuições

Contribuições são sempre bem-vindas! Para contribuir com esse projeto, faça um fork, modifique e crie um pull request.

## Licença

MIT License (MIT)