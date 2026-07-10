-- 10. Qual o estado que possui a maior média de peso?
SELECT
    e.estado,
    AVG(p.peso) AS media_peso
FROM tb_paciente p
JOIN tb_estado e ON e.cod_estado = p.cod_estado
GROUP BY e.estado
ORDER BY media_peso DESC
LIMIT 1;
