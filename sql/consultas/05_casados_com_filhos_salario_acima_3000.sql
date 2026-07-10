-- 5. Quantas pessoas casadas possuem filhos e têm um salário acima de 3000?
SELECT
    COUNT(*) AS quantidade
FROM tb_paciente p
JOIN tb_estado_civil ec ON ec.cod_estado_civil = p.cod_estado_civil
WHERE ec.estado_civil = 'Casado'
  AND p.qtd_filho > 0
  AND p.salario > 3000;
