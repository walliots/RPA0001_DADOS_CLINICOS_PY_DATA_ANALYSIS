-- 7. Qual estado civil possui a menor quantidade de filhos e qual é esse número?
-- Obs.: pergunta idêntica à questão 4 no enunciado original (repetida pelo
-- próprio questionário). Mantida como arquivo separado só para preservar a
-- numeração original das 10 perguntas no relatório.
SELECT
    ec.estado_civil,
    SUM(p.qtd_filho) AS total_filhos,
    AVG(p.qtd_filho) AS media_filhos_por_pessoa
FROM tb_paciente p
JOIN tb_estado_civil ec ON ec.cod_estado_civil = p.cod_estado_civil
GROUP BY ec.estado_civil
ORDER BY total_filhos ASC
LIMIT 1;
