# 📊 Pipeline de Dados de Óbitos do Brasil- Portal da Transparência

Este é um projeto de pipeline de dados que coleta, transforma e armazena registros de óbitos públicos disponibilizados pela API do [Portal da Transparência do Registro Civil](https://transparencia.registrocivil.org.br/). O objetivo é permitir a análise estruturada e confiável da mortalidade no Brasil desde 2015 até os dias atuais, com arquitetura modular, incremental e preparada para produção, permitindo análises posteriores com ferramentas como o Power BI.

## 📦 Funcionalidades

- Extração paralela de dados de óbitos por estado, ano e mês via API.
- Criação automática do banco de dados e das tabelas no PostgreSQL.
- Estrutura relacional com tabelas de dimensões: `states`, `cities`, `years`.
- Armazenamento incremental com controle de duplicidade.
- Sobrescrita segura dos dados do mês atual.
- Organização modular com separação clara de responsabilidades.
- Logging estruturado para facilitar debugging e monitoramento.

## 🚀 Tecnologias Utilizadas

- Python 3.11+
- Pandas
- SQLAlchemy
- psycopg2
- PostgreSQL
- dotenv
- Requests
- Concurrent Futures

## 🧱 Estrutura do Projeto

```bash
brazil-deaths-data-pipeline/
├── .env.example               # Exemplo de configuração de variáveis de ambiente
├── main.py                   # Script principal para execução da pipeline
├── requirements.txt          # Dependências do projeto
├── README.md                 # Documentação do projeto
├── imgs/                     # Imagens utilizadas no README
│   └── banner.png
└── src/
    ├── __init__.py
    ├── api_client.py         # Módulo de extração de dados via API
    ├── loader.py             # Módulo de envio ao banco de dados
    ├── transform.py          # Transformação de dados brutos
    ├── settings.py           # Configurações globais e credenciais
    ├── pipeline/
    │   ├── __init__.py
    │   ├── control_logic.py  # Lógica de controle da coleta (primeira execução vs atualizações)
    │   └── run.py            # Orquestrador da pipeline
    ├── populate/
    │   ├── __init__.py
    │   ├── populate_all.py   # População das tabelas dimensionais
    │   ├── populate_states.py
    │   ├── populate_cities.py
    │   └── populate_years.py
    └── schemas/
        ├── __init__.py
        ├── create_all.py     # Criação de todas as tabelas
        ├── create_states_table.py
        ├── create_cities_table.py
        ├── create_years_table.py
        └── create_deaths_table.py
```

## ⚙️ Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Crie o arquivo `.env` na raiz do projeto com as variáveis do banco

```env
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=pipeline
POSTGRES_TABLE=deaths
```

## ▶️ Como Executar

Com tudo configurado, rode o pipeline com:

```bash
python main.py
```

## 🔁 Lógica de Execução

- Na **primeira execução**, a pipeline coleta todos os dados desde 2015 até o mês atual e popula completamente o banco.
- Em execuções **subsequentes**, somente os dados do **mês atual** são buscados e **sobrescritos** com segurança.
- Dados anteriores ao mês atual são preservados, evitando duplicatas por meio da restrição `UNIQUE(city_id, year_id, month)`.

## 🧪 Exemplo de Estrutura Relacional

```plaintext
years         cities           states          deaths
┌────┐       ┌────┐           ┌────┐          ┌────┐
│ id │◄──────│ id │           │ id │◄─────────│    │
│year│       │name│──────────►│ uf │          │    │
└────┘       │state_id────────┘    │          │    │
             └────┘                └────┘      month, quantity...
```

O script fará:

1. Coleta de dados da API
2. Tratamento com pandas
3. Salvamento local do arquivo
4. Carga no PostgreSQL

## 🖼️ Tabela criada no Postgres após rodar o pipeline

![Postgres rodando local](./imgs/exemplo-postgres.png)

## 📡 Fonte dos Dados

Os dados são obtidos do [Portal da Transparência do Registro Civil](https://transparencia.registrocivil.org.br/).

## 📊 Uso com Power BI

1. Abra o Power BI Desktop
2. Selecione "Obter Dados" → "Banco de Dados PostgreSQL"
3. Insira:
   - Servidor: localhost:5432
   - Banco de dados: seu_banco_de_dados
4. Autentique com o usuário `seu_usuario`
5. Selecione a tabela `sua_tabela`

Agora você pode montar dashboards com filtros por período, localidade, cidade e quantidade de óbitos.

## 🖼️ Exemplos de Dashboards

### Visão Geral - Brasil

![Dashboard Geral](./imgs/analise-geral-brasil.png)

### Visão por Estado - São Paulo

![Filtro por Estado](./imgs/analise-estado-sp.png)

### Visão por Cidade - São Paulo

![Filtro por Cidade](./imgs/analise-cidade-sp.png)

## ✅ TODO

- [ ] Implementar versão com Docker

## 📄 Licença

Este projeto é de uso pessoal e acadêmico. Consulte o Portal da Transparência para regras de uso dos dados.

## 🙌 Autor

Desenvolvido por [Victor Augusto Goveia da Rocha](https://github.com/victorgoveia)  
Contato: [victor.goov@gmail.com](mailto:victor.goov@gmail.com)
