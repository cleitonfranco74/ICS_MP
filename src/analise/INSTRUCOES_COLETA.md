# Instruções da coleta regional (ICS-MP)

Tarefa para uma sessão com acesso de rede às bases públicas: coletar os indicadores dos 48 municípios do panorama regional (`src/data/regional.json`) e rodar o desenho A (logit ordenado). **Nunca estime, interpole ou invente valores.** O que não estiver na fonte fica em branco e é registrado.

## 1. Domínios necessários

Liberar em **Network access › Allowed domains** do ambiente (não no Setup script):

```
apisidra.ibge.gov.br
servicodados.ibge.gov.br
ftp.ibge.gov.br
idsc.cidadessustentaveis.org.br
igm.cfa.org.br
atlasbrasil.org.br
apidatalake.tesouro.gov.br
```

`apidatalake.tesouro.gov.br` é a API de dados abertos do Siconfi (Tesouro Nacional), usada nos indicadores de despesa e receita da Proposta B.

Primeiro passo: testar cada domínio com `curl` e registrar o resultado em `src/analise/README_coleta.md`. Se algum estiver bloqueado, pule só as fontes dele.

## 2. Contexto do repositório

- Página: `src/page.html` (modelo), montada com `python3 src/build.py`.
- Indicadores da Matriz REV05: `src/data/rev05.json`.
- Regras de classificação: objetos `RULES`, `PROP_B` e funções `classify()`, `bValue()`, `bLevels()` em `src/page.html`. Use exatamente essas regras.
- Guia de coleta: objeto `MANUAL` e lista `PROP_B` em `src/page.html`.
- Use o código IBGE de 7 dígitos (via `servicodados.ibge.gov.br/api/v1/localidades`) para cruzar as bases.

## 3. Indicadores a coletar

### Matriz atual (REV05)
- **Censo 2022 (SIDRA, nível municipal n6):** D2-02 (tabela 9890 ÷ total de domicílios, conferir a tabela 6326), D2-03 (tabela 9930), D2-04 (esgotamento sanitário adequado, identificar a tabela), D3-05 (tabela 9839).
- **MUNIC 2024 (ftp.ibge.gov.br):** D1-02 (MTIC272), D2-01 (MHAB07), D4-04 (MTRA24b), D2-05 se houver variável correspondente.
- **IDSC-BR:** D1-03 e D1-04 (ODS 16), D4-01 (ODS 11), D4-02 (ODS 6), D4-03 (ODS 7), D5-04.
- **IGM-CFA:** D1-01 (dimensão Gestão).
- **Atlas Brasil:** D4-05 (IDHM 2010).
- **Coleta manual** (deixar em branco e marcar): D3-01, D3-02, D3-03, D5-01, D5-02, D5-03, D5-05.

### Proposta B (indicadores de execução)
- **D3-01 Urbanismo por habitante (Siconfi):** despesa liquidada na função 15 (Urbanismo), média de três exercícios, ÷ população. Fonte: Declaração de Contas Anuais (DCA), anexo de despesas por função, na API do Siconfi (`apidatalake.tesouro.gov.br/ords/siconfi/tt/dca`). Confira o nome exato do anexo e da conta na resposta da API antes de usar.
- **D3-02 IPTU por habitante (Siconfi):** receita arrecadada de IPTU, média dos mesmos três exercícios, ÷ população. Fonte: DCA, anexo de receitas orçamentárias.
- **D5-01 Lei de inovação (implementação):** para quem tem lei, verificar se há **despesa liquidada na função 19 (Ciência e Tecnologia)** nos últimos 3 exercícios (mesmo anexo da DCA). Despesa maior que zero conta como instrumento funcionando (“Instrumento: despesa na função 19 em AAAA”). Os demais instrumentos (fundo, edital, CPSI, conselho) ficam para coleta manual.
- **D3-03 Pavimentação e arborização (SIDRA):** % de domicílios com via pavimentada e % com arborização no entorno, Censo 2022, Pesquisa Urbanística do Entorno. Identifique as tabelas; se a arborização não existir em 2022, registre e colete só a pavimentação.
- **D2-01 MCMV por 1.000 domicílios:** unidades contratadas no Minha Casa, Minha Vida no período fixado (ex.: 2023 a 2025) ÷ domicílios particulares permanentes ocupados (Censo 2022) × 1.000. A fonte (dados abertos do Ministério das Cidades) não está na lista de domínios; se não estiver acessível, marque como coleta manual.
- **População** para os per capita: use a mesma referência para todos os municípios e registre qual (Censo 2022 ou estimativa do ano dos dados).
- Registre os exercícios usados (ex.: 2022 a 2024) em `src/analise/README_coleta.md`.

## 4. Saídas

- `src/data/regional_indicadores.csv`: formato da planilha-modelo da página (separador `;`, UTF-8 com BOM, mesmo cabeçalho da planilha-modelo regional, incluindo as colunas da Proposta B: `MCMV_UH_por_mil_dom;Urbanismo_per_capita;IPTU_per_capita;Pavimentacao_pct;Arborizacao_pct;Lei_inovacao_nivel`). Números com vírgula decimal e sem separador de milhar.
- `src/data/regional_fontes.csv`: uma linha por município × indicador, com status (coletado / vazio na fonte / coleta manual / domínio bloqueado), fonte exata (tabela, anexo, conta ou variável, URL) e data de acesso.
- Validação: compare o coletado com a REV05 para os municípios da amostra (Sinop, Lucas do Rio Verde, Sorriso, Rondonópolis, Primavera do Leste, Palmas, Rio Verde, Dourados) e registre divergências. Carregue o CSV na página com Playwright (Chromium em `/opt/pw-browsers/chromium`, input `#tplFile`) e confirme que não há erros.

## 5. Análise (desenho A)

Script `src/analise/desenho_a.py` e relatório `src/analise/desenho_a.md` (statsmodels e scipy):
- Explicativa: ICS-MP REV05 calculado com as regras da página, sem o D1-05 (i-Gov-TI).
- Dependente: faixa oficial do IEGM geral (C < C+ < B < B+ < A), de `regional.json`.
- Modelos: logit e probit ordenados (`OrderedModel`), logit binário (C+ ou melhor × C), Spearman com a nota contínua do IEGM.
- Amostra principal: municípios com IEGM e com dado em pelo menos 3 de cada 5 indicadores por dimensão (sem contar os de coleta manual). Sensibilidade: só indicadores de bases automáticas; sem Palmas (exercício 2023).
- Se houver dados suficientes da Proposta B, repetir com o ICS-MP da Proposta B (sem i-Gov-TI e i-Fiscal, para evitar circularidade com o IEGM).
- Reportar n, número por faixa, coeficientes, erros-padrão, p, razão de chances por 10 pontos com IC 95%, convergência, sinais de separação e a regra de cerca de 10 eventos por variável. Resumo em português para a orientadora e a banca, sem exagerar conclusões.

## 6. Entrega

Commit e push no branch indicado pela sessão. Não abrir pull request nem fazer merge sem autorização.
