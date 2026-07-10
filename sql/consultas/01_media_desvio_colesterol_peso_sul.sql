-- 1. Qual é a média e o desvio padrão do colesterol das pessoas que têm peso
-- superior a 120 kg e residem na região Sul do Brasil?
SELECT
    AVG(p.colesterol)        AS media_colesterol,
    STDDEV_SAMP(p.colesterol) AS desvio_padrao_colesterol
FROM tb_paciente p
JOIN tb_estado e ON e.cod_estado = p.cod_estado
WHERE p.peso > 120
  AND e.regiao = 'Sul';
