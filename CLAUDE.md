# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## O que este repositório é

Lab de dados. Não há `package.json`, `requirements.txt`, build, lint ou suíte de testes. Todo o
código está em `scripts/` (Python, só stdlib) e faz duas coisas: higieniza as bases brutas e
gera as dashboards. O caminho completo é `raw_data/` → base limpa → dashboard.

Python 3.14 está no `PATH` (`python`), sem dependências instaladas assumidas — use a stdlib
(`csv`, `collections`, `re`); confirme se `pandas` existe antes de usá-lo.

Idioma do projeto: **português**. Nomes de coluna, valores categóricos e documentação seguem
esse padrão — mantenha-o em qualquer arquivo novo.

## Estrutura e contrato de cada pasta

| Pasta | Papel | Regra |
|---|---|---|
| `raw_data/` | dado bruto | **Nunca editar.** É a fonte da verdade e a matéria-prima do exercício de higienização — "consertar" o CSV destrói o propósito do repositório. |
| `data_hygiene/` | dicionário (`*_index_*.md`), base limpa (`*_clean_*.csv`) e log (`*_qa_*.md`) | O `index` é especificação, não dado: é o **estado-alvo** da limpeza. O `clean` e o `qa` são **gerados** por `scripts/clean.py` — editar à mão é perda garantida no próximo reprocessamento. |
| `scripts/` | os pipelines | Higienização: `clean.py` orquestra, `hygiene_lib.py` tem os parsers, `spec_00N_*.py` transcreve o `index` da base coluna por coluna. Dashboard: `build_dashboard_002.py` + `dash_002_template.html`. Regra nova de limpeza entra no `spec`, não no bruto. |
| `dashboards/` | dashboards e insumos | `00N_dash_*.html` é **gerado** — editar à mão é perda no próximo build; mexa em `scripts/dash_00N_template.html`. `kpis/00N_kpis.md` traz as perguntas de negócio e as decisões de apuração; `design_system/design_system.html` é a linguagem visual de referência. |
| `_docs/` | conceitos transversais | `data_hygiene.md` define o conceito e o fluxo `bruto → mapeamento → higienização → informação → dashboard`. |

`readme.md` é o índice navegável do projeto — ao adicionar um dataset ou doc, atualize a tabela
de datasets e a árvore de estrutura lá.

### Nomenclatura

```
[id]_[componente]_[alias]_[ano].[extensão]
```

O `id` é a chave que liga os arquivos entre pastas: `002_data_*` ↔ `002_index_*` ↔
`002_clean_*` ↔ `002_qa_*` ↔ `002_kpis*` ↔ `002_dash_*`. Componentes em uso: `data` (base
bruta), `index` (dicionário), `clean` (base higienizada), `qa` (log da limpeza), `spec` (o
dicionário em Python), `kpis` (perguntas de negócio) e `dash` (dashboard gerada).

## Os CSVs são sujos de propósito — leia antes de parsear

Cada arquivo termina com uma linha `TOTAL_GERAL` cujo próprio texto diz
`"Resumo inserido propositalmente - filtrar esta linha na limpeza"`. A sujeira é injetada
deliberadamente. **Não trate anomalia como bug do arquivo.**

A armadilha principal, que invalida qualquer leitura ingênua:

> **Boa parte das linhas está inteira entre aspas duplas externas**, com as aspas internas
> duplicadas (`"RES-0004,RACE-001,...,""411,199"",..."`). Um leitor CSV padrão parseia a linha
> toda como **um único campo** — o registro cai inteiro em `resultado_id`/`registro_id` e todas
> as outras colunas voltam vazias. São 75 das 171 linhas em `001` e 109 das 186 em `002`.
> Um `csv.DictReader` "funciona" sem erro e entrega ~56% e ~41% de linhas úteis, silenciosamente.

Essas linhas precisam ser desembrulhadas (remover as aspas externas, colapsar `""` → `"`) e
reparseadas antes de qualquer análise. `hygiene_lib.ler_bruto()` já faz isso — use essa função
em vez de abrir o CSV na mão.

Também presentes, verificados nos dois arquivos:

- **Encoding/EOL**: UTF-8 **com BOM** (`\xef\xbb\xbf`) e CRLF. Abrir com `encoding="utf-8-sig"`.
- **Datas na mesma coluna em 4 formatos**: `YYYY-MM-DD`, `YYYY/MM/DD`, `DD-MM-YYYY`, `DD/MM/YYYY`.
- **Horas em 4 formatos**: `HH:MM`, `HH:MM:SS`, `HHhMM` (`19h45`) e com espaços em volta.
- **Booleanos como texto inconsistente**: `Sim`, `sim`, ` sim `, `Nao`, `NAO` (o mapeamento pede `BOOLEAN`).
- **Decimal com vírgula e unidade embutida no valor**: `"5,2 km"`, `560 HP`, `"131,8 km/h"`, `60 min`, `"72,9%"`.
- **Moeda com símbolo e separador de milhar**: `"$2,370"`, `"US$ 573.433,10"`, `"43,38 USD"`.
- **Sentinelas textuais**: `N/A` em colunas numéricas/categóricas (`tempo_formatado`, `categoria_pulseira`).
- **Categóricos com caixa e espaço inconsistentes**: `FESTIVAL RACE` / `  Festival Race ` / `Festival  Race`; `Asfalto` / `asfalto` / `ASFALTO`.
- **Escalas misturadas**: `ocupacao_pct` aparece como `89.5`, `73.0 %` e `0.855`/`1.000` (fração).
- **Ordinal como texto**: `dia_festival` como `5` e como `Dia 1`.
- **IDs com espaço e caixa suja**: `'  res-0076  '`, `' mus-0136 '` (13 em `001`, 14 em `002`).
- **IDs duplicados**: 5 pares em `001` e 6 em `002`, todos com as cópias **idênticas** em todas
  as colunas — desduplicar mantendo a primeira não perde dado.

### O ponto que só o dicionário resolve

A sujeira numérica é **ambígua por natureza** e o `*_index_*.md` é o que a desfaz. O mesmo texto
vira números diferentes conforme o tipo declarado na coluna:

| Valor bruto | Coluna | Tipo declarado | Leitura correta |
|---|---|---|---|
| `"411,199"` | `tempo_total_seg` | `DECIMAL(10,3)` | `411.199` — vírgula decimal |
| `"$2,370"` | `creditos_usd` | `DECIMAL(12,2)` | `2370` — vírgula de milhar |
| `"4.330"` | `ingressos_emitidos` | `INTEGER` | `4330` — ponto de milhar |
| `"1.000"` | `ocupacao_pct` | `DECIMAL(5,2)` | `1.0` → 100% — só cabem 3 dígitos inteiros |
| `"US$ 573.433,10"` | `receita_ingressos_usd` | `DECIMAL(14,2)` | `573433.10` — pt-BR |
| `"$195,830.53"` | `receita_ingressos_usd` | `DECIMAL(14,2)` | `195830.53` — en-US, **mesma coluna** |

Um parser genérico erra ~25% das linhas numéricas, em silêncio, por fator de 1000. É por isso que
`spec_00N_*.py` declara `decimais` e `precisao` de cada coluna: `parse_num()` precisa dos dois.
Ao escrever qualquer leitura numérica desses arquivos, passe pelo spec — não invente heurística.

Outra armadilha de canonicalização: **não use `.title()`** em categóricos. Ele destrói `AWD`,
`EDM` e `Elite/VIP`. `hygiene_lib.mapa_canonico()` elege a variante mais frequente da coluna.

## Relações verificadas entre colunas

Toda coluna faltante das duas bases é **derivável** de outras da mesma linha — nenhum vazio
sobrou depois da limpeza. As identidades abaixo foram conferidas contra as linhas onde os dois
lados existem e fecham com **zero divergência**; estão implementadas em `spec_00N_*.derivar()`:

- `001`: `velocidade_media_kmh = distancia_km * voltas / (tempo_total_seg/3600)`;
  `tempo_formatado` = apresentação de `tempo_total_seg`; `vencedor = (posicao == 1)`;
  `gap_para_vencedor_seg = tempo_total_seg −` tempo da linha `posicao == 1` do mesmo `corrida_id`
  (**contra o vencedor, não contra o menor tempo** — essa variante divergia em 21 linhas).
- `002`: `no_show = ingressos_emitidos − checkins`;
  `receita_ingressos_usd = preco_medio_ingresso_usd * checkins` (**× check-ins, não × emitidos**);
  `ocupacao_pct = pessoas_na_area / capacidade_area * 100` (**pessoas, não check-ins**);
  `dia_festival` = dia do mês (19→1 … 25→7).
- Pulseira, nas duas bases: cor → nível é bijeção (`Yellow` 1 … `Gold` 7, `Sem pulseira` 0), e em
  `002` nível → categoria é determinístico (1–2 `Rookie`, 3–4 `Intermediate`, 5 `Advanced`,
  6 `Elite`, 7 `Elite/VIP`). `Elite` e `Elite/VIP` são categorias **distintas** — não unificar.

A limpeza **preenche vazio, nunca sobrescreve valor presente.** As 8 divergências que sobram em
`002` são uma regra do dataset, não erro: a base não admite ocupação acima de 100%, então ou
`pessoas_na_area` foi capado na `capacidade_area`, ou a ocupação foi travada em 100%.

## Comandos úteis

Não há build/test/lint. O que se roda aqui:

```bash
# reprocessar a higienização (idempotente; reescreve clean + qa)
python scripts/clean.py          # as duas bases
python scripts/clean.py 001      # só uma

# regerar a dashboard da 002 (idempotente; reescreve o html)
python scripts/build_dashboard_002.py

# leitura correta de um CSV bruto (BOM + desembrulho; nunca use cut -d, ou awk -F,)
python -c "import sys;sys.path.insert(0,'scripts');import hygiene_lib as h;c,r,n=h.ler_bruto('raw_data/001_data_corridas_2012.csv');print(len(c),len(r),n)"

# quantas linhas vêm inteiras entre aspas (a armadilha acima)
awk 'NR>1 && /^"/ {n++} END {print n+0}' raw_data/001_data_corridas_2012.csv

# checar que todos os links relativos do readme resolvem
grep -o ']([^)#][^)]*)' readme.md | sed 's/^](//; s/)$//' | sort -u | xargs -I{} sh -c 'test -e "{}" || echo "FALTA {}"'
```

`cut -d,` e `awk -F,` dão resultados errados nesses arquivos por causa dos campos entre aspas
com vírgula dentro — as colunas deslocam sem aviso.

## Dashboards são geradas, não escritas

`dashboards/00N_dash_*.html` sai de `scripts/build_dashboard_00N.py` + um template. O script
projeta as linhas da base limpa num bloco `<script id="dados" type="application/json">` e a
página agrega tudo em JavaScript no navegador. **Nenhum número é digitado no HTML** — é assim
que o guard rail de não inventar dado fica verificável: o build falha o próprio check se um
número de dado aparecer no markup.

Consequências práticas ao mexer nisso:

- Editar o HTML de saída é perda garantida. O arquivo a editar é `scripts/dash_00N_template.html`.
- Sem bibliotecas e sem requisição externa: o design system é explícito quanto a isso, e a
  página tem de abrir com duplo clique. Gráficos em CSS/SVG puro; formatação pt-BR via `Intl`.
- Para validar mudança no JS sem navegador, `node` está disponível: dá para executar o script
  da página com um stub de `document` e capturar o que cada `id` renderizou.
- Ao ordenar por média, arredonde antes de desempatar. Duas médias que aparecem iguais na tela
  (`9,07`) podem diferir na 15ª casa e produzir uma ordem que o leitor não consegue explicar.
- Quando duas leituras de uma pergunta discordam, mostre as duas. A dashboard da 002 faz isso
  em dois pontos: música mais amada × mais lotada, e artista por volume × por média de show.

## Estado do git

O commit inicial (`d2f837f`) tinha `horizon_corridas_lab.csv` e `horizon_evento_lab.csv` na raiz;
eles foram movidos e renomeados para `raw_data/00N_data_*.csv` e ainda não foram commitados. Nada
depois disso foi commitado, então `git status` mostra dois deletes e todo o resto do repositório
como untracked. Os `data_hygiene/00N_clean_*.csv` e `00N_qa_*.md` são gerados: se preferir não
versioná-los, o `.gitignore` é o lugar — mas eles são o entregável da higienização.
