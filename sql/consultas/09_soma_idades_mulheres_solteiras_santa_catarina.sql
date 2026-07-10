-- 9. Qual é a soma das idades de todas as mulheres solteiras que residem em
-- Santa Catarina?
SELECT
    SUM(p.idade) AS soma_idades
FROM tb_paciente p
JOIN tb_estado_civil ec ON ec.cod_estado_civil = p.cod_estado_civil
JOIN tb_estado e ON e.cod_estado = p.cod_estado
WHERE p.genero = 'Feminino'
  AND ec.estado_civil = 'Solteiro'
  AND e.estado = 'Santa Catarina';
