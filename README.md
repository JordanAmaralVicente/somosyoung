# Teste Técnico - Jordan Ítalo Amaral
## Modelagem do Banco de Dados
Optado pelo modelo de star-schema para o banco, que foi divido da seguinte forma:
![image](https://github.com/user-attachments/assets/dc79094a-5c67-4bd5-b1d5-96af0c38b559)

Uma vez que o id já estava presente, as relações principais foram estabelecidas pelo contexto de cada informação.
## Organização do Projeto
O projeto conta com as pastas necessárias para funcionamento do airflow, sendo elas: config, plugins, logs e dags. E possui as pastas relativas ao banco de dados, a saber database/data_warehouse que contém os arquivos que realizam a criação da tabela no banco ao iniciá-lo.
As dags foram organizadas para estar na pasta src e, por fim, a pasta script que contém o script de criação das conexões no airflow

```text
root
  |-- config
  |-- database
    |-- data_warehouse
      |-- email_campaign.sql
      |-- startup_control.sql
  |-- logs
  |-- plugins
  |-- scripts
    |-- create_connection.sh
  |-- src
    |-- dags
      |-- main.py
```

## Mudanças
Algumas mudanças que agregariam ao projeto:
- Salvar os arquivos em um filesystem ao invés de passar pelo XCOM
- Usar HttpOperator para requisição
- Fazer a inserção dos dados em batch
- Criar operador para fazer o tratamento dos dados
 
