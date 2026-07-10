-- 2. Qual é a classe de trabalho com o maior número de pessoas e qual é o
-- número correspondente na base de dados?
SELECT
    ct.classe_trabalho,
    COUNT(*) AS quantidade
FROM tb_paciente p
JOIN tb_classe_trabalho ct ON ct.cod_classe_trabalho = p.cod_classe_trabalho
GROUP BY ct.classe_trabalho
ORDER BY quantidade DESC
LIMIT 1;
