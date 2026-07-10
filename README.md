# RPA0001_DADOS_CLINICOS_PY_DATA_ANALYSIS

Trabalho final da disciplina **Desenvolvimento e Projeto de Solução RPA I** (PUC Minas — Prof. Leandro Lessa).

**Integrantes:** Gabriel Brunet Dure, Guilherme Henrique Barros Assis, Samantha Araújo Fernandes de Souza

## Contexto

O projeto simula uma automação de fluxo de dados clínicos de pacientes para um projeto de pesquisa de saúde. A partir de três conjuntos de dados fictícios, o objetivo é integrar, tratar, armazenar e consultar as informações dos pacientes.

Datasets originais:

- **dados_clinicos**: id_cliente, peso, colesterol, genero
- **dados_pacientes**: id_cliente, idade, classe_trabalho, escolaridade, id_estado, estado_civil, raca, qtde_filhos, salario
- **dados_estados**: id_estado, sigla, estado, regiao, pais

## Etapas do trabalho

1. Coleta de dados
2. Integração dos dados (inner join entre os três conjuntos)
3. Correção de dados inconsistentes (ausentes, duplicados, incorretos)
4. Modelagem (DER) e persistência em banco de dados MySQL
5. Consultas SQL para responder ao questionário do trabalho

## Organização das branches

- `main` — versão final estável
- `develop` — integração do trabalho do grupo
- `feature/coleta-dados`
- `feature/integracao-dados`
- `feature/tratamento-dados`
- `feature/modelagem-mysql`
- `feature/consultas-sql`

## Estrutura de pastas

```
├── datasets/
│   ├── raw/            # dados originais, sem tratamento
│   └── processed/      # dados após tratamento e join
├── notebooks/          # .ipynb de exploração e desenvolvimento
├── src/                # código Python reutilizável (.py)
├── sql/
│   ├── ddl/             # scripts de criação das tabelas (DER)
│   └── consultas/       # as 10 consultas do questionário
├── docs/                # diagrama entidade-relacionamento e materiais de apoio
└── relatorio/           # PDF final com respostas, código SQL e resultados
```

## Como executar

### 1. Clonar e configurar o ambiente Python

```powershell
git clone https://github.com/walliots/RPA0001_DADOS_CLINICOS_PY_DATA_ANALYSIS.git
cd RPA0001_DADOS_CLINICOS_PY_DATA_ANALYSIS
git checkout develop

python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Rodar o pipeline de dados (coleta -> integração -> tratamento -> modelagem)

```powershell
cd src
python integracao.py
python tratamento.py
python modelagem.py
cd ..
```

Cada etapa lê o resultado da anterior e salva o próprio resultado em `datasets/processed/`. Se algum arquivo já existir, ele é sobrescrito — pode rodar quantas vezes quiser.

### 3. Persistir no MySQL

Você precisa de um MySQL rodando (local, XAMPP/Workbench, ou um container Docker descartável).

**Opção A — usando um MySQL que você já tem instalado:**

1. Copie `.env.example` para `.env` e preencha com suas credenciais reais (esse arquivo não é versionado):
   ```powershell
   Copy-Item .env.example .env
   ```
2. Rode:
   ```powershell
   cd src
   python db.py
   cd ..
   ```

**Opção B — subindo um MySQL descartável via Docker (não precisa instalar nada):**

```powershell
docker run --name rpa-mysql-teste -e MYSQL_ROOT_PASSWORD=teste123 -e MYSQL_DATABASE=dados_clinicos -p 3307:3306 -d mysql:8.0
docker exec rpa-mysql-teste mysqladmin ping -uroot -pteste123   # repita ate aparecer "mysqld is alive"
```

Crie o `.env` apontando para esse container:

```powershell
@"
DB_HOST=localhost
DB_PORT=3307
DB_USER=root
DB_PASSWORD=teste123
DB_NAME=dados_clinicos
"@ | Out-File -Encoding utf8 .env
```

Depois rode `python src/db.py` normalmente. Ao terminar, derrube o container com `docker rm -f rpa-mysql-teste`.

### 4. Conferir se deu certo

```powershell
docker exec rpa-mysql-teste mysql -uroot -pteste123 dados_clinicos -e "SELECT COUNT(*) FROM tb_paciente;"
```
(ou, se estiver usando seu próprio MySQL, rode a mesma consulta no Workbench/linha de comando). O esperado é 7999 pacientes carregados, sem erro de FK.
