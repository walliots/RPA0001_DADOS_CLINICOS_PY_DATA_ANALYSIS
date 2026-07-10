-- 4. Qual estado civil possui a menor quantidade de filhos e qual é esse número?
-- Obs.: "quantidade" interpretado como soma total de filhos por estado civil.
-- Também exibimos a média por pessoa, caso o enunciado se refira a ela.
SELECT
    ec.estado_civil,
    SUM(p.qtd_filho) AS total_filhos,
    AVG(p.qtd_filho) AS media_filhos_por_pessoa
FROM tb_paciente p
JOIN tb_estado_civil ec ON ec.cod_estado_civil = p.cod_estado_civil
GROUP BY ec.estado_civil
ORDER BY total_filhos ASC
LIMIT 1;
