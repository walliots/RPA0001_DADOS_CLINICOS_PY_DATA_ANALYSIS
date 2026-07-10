# Respostas do Questionário

Trabalho Final — Desenvolvimento e Projeto de Solução RPA I (PUC Minas — Prof. Leandro Lessa)

Todas as consultas foram executadas contra o MySQL 8, com os dados já tratados e
modelados (`datasets/processed/dados_tratados.csv` → tabelas `tb_paciente` +
tabelas de domínio, ver `sql/ddl/schema.sql`). Os arquivos `.sql` completos estão
em `sql/consultas/`.

> Este arquivo é um rascunho em Markdown — convertam para PDF (ex.: extensão
> "Markdown PDF" do VS Code, ou imprimir como PDF pelo navegador) para a entrega
> final, complementando com a introdução/conclusão exigidas no enunciado.

---

## 1. Qual é a média e o desvio padrão do colesterol das pessoas que têm peso superior a 120 kg e residem na região Sul do Brasil?

```sql
SELECT
    AVG(p.colesterol)        AS media_colesterol,
    STDDEV_SAMP(p.colesterol) AS desvio_padrao_colesterol
FROM tb_paciente p
JOIN tb_estado e ON e.cod_estado = p.cod_estado
WHERE p.peso > 120
  AND e.regiao = 'Sul';
```

**Resultado:** média de colesterol = **206,96**; desvio padrão = **21,89**

---

## 2. Qual é a classe de trabalho com o maior número de pessoas e qual é o número correspondente na base de dados?

```sql
SELECT
    ct.classe_trabalho,
    COUNT(*) AS quantidade
FROM tb_paciente p
JOIN tb_classe_trabalho ct ON ct.cod_classe_trabalho = p.cod_classe_trabalho
GROUP BY ct.classe_trabalho
ORDER BY quantidade DESC
LIMIT 1;
```

**Resultado:** **Funcionário Setor Privado**, com **5.769** pessoas

---

## 3. Qual é a classe de trabalho que apresenta a maior média de salários e qual é o valor associado para as pessoas do estado de Pernambuco?

```sql
SELECT
    ct.classe_trabalho,
    AVG(p.salario) AS media_salario_geral
FROM tb_paciente p
JOIN tb_classe_trabalho ct ON ct.cod_classe_trabalho = p.cod_classe_trabalho
GROUP BY ct.classe_trabalho
ORDER BY media_salario_geral DESC
LIMIT 1;
```

```sql
SELECT
    ct.classe_trabalho,
    AVG(p.salario) AS media_salario_pernambuco
FROM tb_paciente p
JOIN tb_classe_trabalho ct ON ct.cod_classe_trabalho = p.cod_classe_trabalho
JOIN tb_estado e ON e.cod_estado = p.cod_estado
WHERE e.estado = 'Pernambuco'
  AND ct.classe_trabalho = (
      SELECT ct2.classe_trabalho
      FROM tb_paciente p2
      JOIN tb_classe_trabalho ct2 ON ct2.cod_classe_trabalho = p2.cod_classe_trabalho
      GROUP BY ct2.classe_trabalho
      ORDER BY AVG(p2.salario) DESC
      LIMIT 1
  )
GROUP BY ct.classe_trabalho;
```

**Resultado:** a classe com maior média salarial geral é **Empresário** (média geral = **R$ 10.190,62**); em Pernambuco, a média salarial dos Empresários é **R$ 11.871,60**

---

## 4. Qual estado civil possui a menor quantidade de filhos e qual é esse número?

```sql
SELECT
    ec.estado_civil,
    SUM(p.qtd_filho) AS total_filhos,
    AVG(p.qtd_filho) AS media_filhos_por_pessoa
FROM tb_paciente p
JOIN tb_estado_civil ec ON ec.cod_estado_civil = p.cod_estado_civil
GROUP BY ec.estado_civil
ORDER BY total_filhos ASC
LIMIT 1;
```

**Resultado:** **União Estável**, com **284** filhos no total (média de 2,65 filhos por pessoa nessa categoria — é o menor total porque é também a categoria com menos pessoas: 107 no total)

---

## 5. Quantas pessoas casadas possuem filhos e têm um salário acima de 3000?

```sql
SELECT
    COUNT(*) AS quantidade
FROM tb_paciente p
JOIN tb_estado_civil ec ON ec.cod_estado_civil = p.cod_estado_civil
WHERE ec.estado_civil = 'Casado'
  AND p.qtd_filho > 0
  AND p.salario > 3000;
```

**Resultado:** **1.218** pessoas

---

## 6. Qual é a média salarial das pessoas casadas que possuem ensino superior completo e trabalham como Funcionário de Setor Privado?

```sql
SELECT
    AVG(p.salario) AS media_salario
FROM tb_paciente p
JOIN tb_estado_civil ec ON ec.cod_estado_civil = p.cod_estado_civil
JOIN tb_escolaridade esc ON esc.cod_escolaridade = p.cod_escolaridade
JOIN tb_classe_trabalho ct ON ct.cod_classe_trabalho = p.cod_classe_trabalho
WHERE ec.estado_civil = 'Casado'
  AND esc.escolaridade = 'Superior Completo'
  AND ct.classe_trabalho = 'Funcionário Setor Privado';
```

**Resultado:** **R$ 11.025,00**

---

## 7. Qual estado civil possui a menor quantidade de filhos e qual é esse número?

> Pergunta idêntica à questão 4 (repetida no enunciado original).

**Resultado:** **União Estável**, com **284** filhos no total

---

## 8. Quantas pessoas casadas possuem filhos e têm um salário acima de 3000?

> Pergunta idêntica à questão 5 (repetida no enunciado original).

**Resultado:** **1.218** pessoas

---

## 9. Qual é a soma das idades de todas as mulheres solteiras que residem em Santa Catarina?

```sql
SELECT
    SUM(p.idade) AS soma_idades
FROM tb_paciente p
JOIN tb_estado_civil ec ON ec.cod_estado_civil = p.cod_estado_civil
JOIN tb_estado e ON e.cod_estado = p.cod_estado
WHERE p.genero = 'Feminino'
  AND ec.estado_civil = 'Solteiro'
  AND e.estado = 'Santa Catarina';
```

**Resultado:** **1.521** anos (soma das idades)

---

## 10. Qual o estado que possui a maior média de peso?

```sql
SELECT
    e.estado,
    AVG(p.peso) AS media_peso
FROM tb_paciente p
JOIN tb_estado e ON e.cod_estado = p.cod_estado
GROUP BY e.estado
ORDER BY media_peso DESC
LIMIT 1;
```

**Resultado:** **Espírito Santo**, com média de peso de **130,20 kg**
