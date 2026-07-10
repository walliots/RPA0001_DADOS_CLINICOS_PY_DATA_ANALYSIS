-- 6. Qual é a média salarial das pessoas casadas que possuem ensino superior
-- completo e trabalham como Funcionário de Setor Privado?
SELECT
    AVG(p.salario) AS media_salario
FROM tb_paciente p
JOIN tb_estado_civil ec ON ec.cod_estado_civil = p.cod_estado_civil
JOIN tb_escolaridade esc ON esc.cod_escolaridade = p.cod_escolaridade
JOIN tb_classe_trabalho ct ON ct.cod_classe_trabalho = p.cod_classe_trabalho
WHERE ec.estado_civil = 'Casado'
  AND esc.escolaridade = 'Superior Completo'
  AND ct.classe_trabalho = 'Funcionário Setor Privado';
