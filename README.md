# ICS-MP — Matriz com indicadores do IEGM

Página que apresenta a Matriz ICS-MP (REV05, 25 indicadores, 8 municípios) e propõe trocar os indicadores de baixo poder discriminatório por dimensões do IEGM (IRB/Atricon), para facilitar o diálogo com o TCE-MT.

Seções: diagnóstico do poder discriminatório, o IEGM, as substituições, a matriz proposta, a coleta das notas IEGM (com entrada de dados), o resultado (ICS-MP atual × proposto) e as notas metodológicas.

## Arquivos

| Arquivo | Uso |
|---|---|
| `index.html` | Versão independente. Abra no navegador ou publique pelo GitHub Pages. As notas IEGM digitadas ficam salvas só no navegador de quem abre, e o CSV é baixado direto. |
| `publicada/icsmp-iegm.html` | Cópia da versão publicada no claude.ai (https://claude.ai/artifact/2s84wC5dCZfW2rwwVdT1us). Lá as notas IEGM ficam compartilhadas entre quem tem acesso de edição. Aberto fora do claude.ai, funciona como o `index.html`, com as notas salvas só no navegador. |

## Aplicar a outros municípios

Na seção 5 da página ("Dados"):

1. **Planilha-modelo:** baixe o CSV (uma linha por município, uma coluna por indicador) e o dicionário de indicadores.
2. **Carregar a planilha preenchida:** salve como CSV separado por ponto e vírgula. A ferramenta calcula os níveis pelos limiares de cada indicador e lista os valores que não reconheceu. `=0`, `=1` ou `=2` informam o nível direto.
3. **Importar o CSV do IEGM:** selecione um ou mais arquivos exportados do painel IEGM Brasil (https://iegm.irbcontas.org.br/). Os municípios são identificados pelo nome e pela UF do tribunal.

O botão "Voltar para a amostra da dissertação" restaura os 8 municípios da REV05.

O **manual de aplicação** (seção 8 da página) traz o passo a passo, o guia de coleta de cada indicador (fonte, como preencher e limiares), as regras de cálculo, os cuidados e as perguntas frequentes.

Os dados da REV05 estão embutidos nas páginas. Nenhuma nota IEGM nova (i-Fiscal, i-Planejamento, i-Cidade, i-Amb) vem preenchida: elas devem ser coletadas no painel do IRB ou nos portais dos Tribunais de Contas.
