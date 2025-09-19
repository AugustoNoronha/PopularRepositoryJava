# Relatório – Qualidade de Repositórios (gerado em 2025-09-19 10:53)

## (i) Introdução e hipóteses informais

- **RQ01 (Popularidade ↔ Qualidade):** hipótese: repositórios com mais estrelas tendem a ter *ligeiramente* menor acoplamento (CBO), menor LCOM e DIT moderado.

- **RQ02 (Maturidade ↔ Qualidade):** hipótese: repositórios mais antigos exibem métricas de qualidade mais estáveis (CBO/LCOM menores em média).

- **RQ03 (Atividade ↔ Qualidade):** hipótese: mais releases está associado a práticas de release melhores e possivelmente menor LCOM.

- **RQ04 (Tamanho ↔ Qualidade):** hipótese: LOC maior tende a correlacionar com CBO/LCOM maiores (complexidade/acoplamento aumentam com tamanho).


## (ii) Metodologia

1. Métricas de **processo** por repositório: Popularidade (`stars`), Maturidade (`idade_anos`), Atividade (`releases`), Tamanho (`loc`, `locComment`).

2. Métricas de **qualidade** (CK, por classe, agregadas por repo): `cbo` (Coupling), `dit` (Depth of Inheritance Tree), `lcom` (Lack of Cohesion of Methods).

3. O `unified_metrics.csv` contém uma linha por repositório com médias de CK (agregadas por classe) e as métricas de processo via GitHub.

4. Resumos por medida central (média, mediana, desvio-padrão) foram calculados **entre repositórios** para cada métrica. Correlações **Spearman** entre processo×qualidade.


## (iii) Resultados

### Estatísticas descritivas (entre repositórios)

| metric     |     mean |   median |       std |
|:-----------|---------:|---------:|----------:|
| stars      | 9374.97  | 5661.5   | 11504.7   |
| releases   |   13.493 |   10     |    13.013 |
| idade_anos |    9.649 |    9.75  |     3.034 |
| loc        |   50.708 |   43.759 |    32.884 |
| locComment |    0     |    0     |     0     |
| cbo        |    5.286 |    5.241 |     1.86  |
| dit        |    1.461 |    1.397 |     0.358 |
| lcom       |  121.039 |   23.292 |  1809.69  |


### Correlações de Spearman – processo × qualidade

| process_metric   | quality_metric   |   spearman |
|:-----------------|:-----------------|-----------:|
| stars            | cbo              |      0.018 |
| stars            | dit              |     -0.026 |
| stars            | lcom             |      0.043 |
| releases         | cbo              |      0.392 |
| releases         | dit              |      0.236 |
| releases         | lcom             |      0.321 |
| idade_anos       | cbo              |      0.005 |
| idade_anos       | dit              |      0.278 |
| idade_anos       | lcom             |      0.193 |
| loc              | cbo              |      0.428 |
| loc              | dit              |      0.385 |
| loc              | lcom             |      0.737 |
| locComment       | cbo              |    nan     |
| locComment       | dit              |    nan     |
| locComment       | lcom             |    nan     |


## (iv) Discussão

- **Popularidade (estrelas):** se as correlações com `cbo`/`lcom` forem **negativas** (mesmo fracas), isso apoia a ideia de que projetos populares tendem a modularizar/acoplar melhor. Se forem **próximas de zero**, popularidade não explica qualidade diretamente (pode haver variáveis de confusão, p.ex. domínio, equipe, tempo).

- **Maturidade (idade_anos):** correlação **negativa** com `lcom` e **baixa** com `dit`/`cbo` indicariam que o envelhecimento traz coesão. Correlação nula sugere que só idade não basta; práticas de engenharia importam mais.

- **Atividade (releases):** se `releases` correlacionar **negativamente** com `lcom`, pode ser efeito de entregas frequentes forçando refino/coesão. Se for **positiva** com `cbo`, pode sinalizar evolução com mais dependências.

- **Tamanho (loc/locComment):** espera-se correlação **positiva** com `cbo` e `lcom` (quanto maior o sistema, maior risco de acoplamento e baixa coesão). Comentários (`locComment`) muito altos podem indicar áreas densas/complexas ou apenas política de documentação.


> **Nota:** correlações fracas não implicam causalidade; servem como indício. Recomenda-se inspeção por amostras e segmentação (domínio, linguagem, org).
