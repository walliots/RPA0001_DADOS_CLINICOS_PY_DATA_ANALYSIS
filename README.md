# RPA0001_DADOS_CLINICOS_PY_DATA_ANALYSIS

Trabalho final da disciplina **Desenvolvimento e Projeto de Solução RPA I** (PUC Minas — Prof. Leandro Lessa).

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

> Documentação em construção — será complementada com integrantes do grupo e instruções de execução.
