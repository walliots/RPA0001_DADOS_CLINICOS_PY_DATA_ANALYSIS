-- 3. Qual é a classe de trabalho que apresenta a maior média de salários e
-- qual é o valor associado para as pessoas do estado de Pernambuco?

-- Passo 1: classe de trabalho com a maior média salarial (geral, todos os estados)
SELECT
    ct.classe_trabalho,
    AVG(p.salario) AS media_salario_geral
FROM tb_paciente p
JOIN tb_classe_trabalho ct ON ct.cod_classe_trabalho = p.cod_classe_trabalho
GROUP BY ct.classe_trabalho
ORDER BY media_salario_geral DESC
LIMIT 1;

-- Passo 2: média salarial dessa mesma classe de trabalho, apenas em Pernambuco
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
