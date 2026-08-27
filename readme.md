# Horizon 2012 — Lab de Dados

Projeto de estudo que percorre o caminho completo do dado: parte de bases brutas de
**corridas** e **eventos musicais** do Horizon 2012, passa pelo mapeamento semântico e pela
higienização, e termina em dashboard.

> Todos os registros são **sintéticos** (coluna `registro_sintetico`), gerados para fins de
> estudo a partir das fontes referenciadas em cada base.

## Índice

1. [Estrutura do projeto](#estrutura-do-projeto)
2. [Convenção de nomenclatura](#convenção-de-nomenclatura)
3. [Dicionário de componentes](#dicionário-de-componentes)
4. [Datasets](#datasets)
5. [Fluxo do dado](#fluxo-do-dado)
6. [Dashboards](#dashboards)
7. [Reprocessar](#reprocessar)
8. [Boas práticas](#boas-práticas)

## Estrutura do projeto

```
dashboard/
├── raw_data/                          dados brutos, intocados
│   ├── 001_data_corridas_2012.csv
│   └── 002_data_evento_2012.csv
├── data_hygiene/                      mapeamento semântico + dado limpo
│   ├── 001_index_corridas_2012.md     dicionário da base 001
│   ├── 001_clean_corridas_2012.csv    base 001 higienizada
│   ├── 001_qa_corridas_2012.md        log da limpeza da 001
│   ├── 002_index_evento_2012.md
│   ├── 002_clean_evento_2012.csv
│   └── 002_qa_evento_2012.md
├── dashboards/                        as dashboards e seus insumos
│   ├── 002_dash_evento_2012.html      dashboard do evento musical
│   ├── kpis/002_kpis.md               perguntas de negócio da 002
│   └── design_system/                 linguagem visual do projeto
├── scripts/                           tudo o que é reprocessável
│   ├── clean.py                       runner da higienização
│   ├── hygiene_lib.py                 parsers e canonicalização
│   ├── spec_001_corridas.py           espelha o dicionário da 001
│   ├── spec_002_evento.py             espelha o dicionário da 002
│   ├── build_dashboard_002.py         gera a dashboard da 002
│   └── dash_002_template.html         template da dashboard
├── _docs/                             conceitos e referências transversais
│   └── data_hygiene.md
└── readme.md                          este arquivo
```

| Pasta | O que guarda |
|---|---|
| [`raw_data/`](raw_data) | Dado bruto e intocado. É a fonte da verdade — nada aqui é editado. |
| [`data_hygiene/`](data_hygiene) | O dicionário de cada base (tipo, formato ideal e sentido de cada coluna) e o resultado da higienização: a base limpa e o log do que foi feito. |
| [`dashboards/`](dashboards) | As dashboards e o que as alimenta: as perguntas de negócio em `kpis/` e o design system. Ver [Dashboards](#dashboards). |
| [`scripts/`](scripts) | A higienização e a geração das dashboards em Python, para rodar de novo quando o dado mudar. Ver [Reprocessar](#reprocessar). |
| [`_docs/`](_docs) | Conceitos que valem para todo o projeto. Ver [data hygiene](_docs/data_hygiene.md). |

## Convenção de nomenclatura

```
[id]_[componente]_[alias]_[ano].[extensão]
```

Exemplo real — `001_data_corridas_2012.csv`:

| Campo | Valor | Papel |
|---|---|---|
| `id` | `001` | Amarra a base bruta ao seu mapeamento |
| `componente` | `data` | O que o arquivo é (ver dicionário abaixo) |
| `alias` | `corridas` | Assunto da base |
| `ano` | `2012` | Ano de referência do dado |

O `id` é a chave que liga os arquivos entre pastas:
`002_data_*` ↔ `002_index_*` ↔ `002_clean_*` ↔ `002_qa_*` ↔ `002_kpis*` ↔ `002_dash_*`.

## Dicionário de componentes

| Componente | Significado | Onde vive |
|---|---|---|
| `data` | Base de dados bruta | [`raw_data/`](raw_data) |
| `index` | Dicionário de dados da base — a especificação | [`data_hygiene/`](data_hygiene) |
| `clean` | Base higienizada, pronta para trabalhar | [`data_hygiene/`](data_hygiene) |
| `qa` | Log da higienização daquela base | [`data_hygiene/`](data_hygiene) |
| `spec` | Especificação da base em Python, espelha o `index` | [`scripts/`](scripts) |
| `kpis` | Perguntas de negócio que a dashboard responde | [`dashboards/kpis/`](dashboards/kpis) |
| `dash` | Dashboard gerada a partir da base limpa | [`dashboards/`](dashboards) |

## Datasets

| ID | Dataset | Bruto | Dicionário | Base limpa | QA | Dashboard | Colunas | Registros |
|---|---|---|---|---|---|---|---|---|
| `001` | Corridas | [csv](raw_data/001_data_corridas_2012.csv) | [index](data_hygiene/001_index_corridas_2012.md) | [csv](data_hygiene/001_clean_corridas_2012.csv) | [md](data_hygiene/001_qa_corridas_2012.md) | — | 37 | 171 → 166 |
| `002` | Evento musical | [csv](raw_data/002_data_evento_2012.csv) | [index](data_hygiene/002_index_evento_2012.md) | [csv](data_hygiene/002_clean_evento_2012.csv) | [md](data_hygiene/002_qa_evento_2012.md) | [html](dashboards/002_dash_evento_2012.html) | 33 | 186 → 180 |

A diferença de registros são as duplicatas exatas removidas (5 e 6) — o detalhe está em cada `qa`.

- **`001` — Corridas**: um registro por resultado de piloto em cada corrida, com dados do evento
  e da rota, requisito de pulseira, veículo utilizado, performance (tempo, gap, posição, `dnf`) e
  recompensas.
- **`002` — Evento musical**: um registro por apresentação nos palcos do festival, com programação
  (artista, faixa, estilo), público (ingressos, check-ins, ocupação), receita (ingressos,
  alimentos e bebidas, merch) e indicadores de experiência.

## Fluxo do dado

```
raw_data/       data_hygiene/      scripts/       data_hygiene/     dashboards/
00N_data_*  →   00N_index_*   →   clean.py   →   00N_clean_*   →   00N_dash_*
   dado          dicionário        higieniza      dado limpo        dado
   bruto       (especificação)                    + 00N_qa_*        visível
```

O dicionário não é só documentação: é a **especificação que dirige a limpeza**. É ele que diz a
escala de cada coluna, e sem isso o mesmo texto vira números diferentes — `"411,199"` em
`DECIMAL(10,3)` é `411.199`, mas `"$2,370"` em `DECIMAL(12,2)` é `2370`.

O conceito por trás da etapa de higienização está em [`_docs/data_hygiene.md`](_docs/data_hygiene.md).

## Dashboards

| Dashboard | Perguntas | Base |
|---|---|---|
| [`002_dash_evento_2012.html`](dashboards/002_dash_evento_2012.html) | [`kpis/002_kpis.md`](dashboards/kpis/002_kpis.md) | [`002_clean_evento_2012.csv`](data_hygiene/002_clean_evento_2012.csv) |

A dashboard da 002 conta o evento em três atos: qual palco dominou a venda (com filtro por cor
de pulseira e drill-down por palco), quem trouxe a multidão, e quais músicas o público amou.

Ela é **gerada**, nunca escrita à mão: o script embute as 180 apresentações da base limpa num
bloco JSON e a página agrega tudo no navegador. Nenhum número está digitado no HTML — é o que
sustenta o guard rail de não inventar dado. O rodapé da própria página declara a procedência,
inclusive quais colunas tiveram valor calculado na higienização.

Segue o [design system](dashboards/design_system/design_system.html) do projeto e não faz
nenhuma requisição externa — abre com duplo clique, sem servidor.

## Reprocessar

```bash
python scripts/clean.py                 # higieniza as duas bases
python scripts/clean.py 001             # só a base 001
python scripts/build_dashboard_002.py   # regera a dashboard da 002
```

Só stdlib do Python — nada para instalar. Os comandos reescrevem os arquivos gerados
(`00N_clean_*.csv`, `00N_qa_*.md`, `00N_dash_*.html`); rodar duas vezes dá exatamente o mesmo
resultado. O dado em [`raw_data/`](raw_data) nunca é alterado.

Para ajustar uma regra de limpeza, o arquivo é o `spec_00N_*.py` da base: ele transcreve o
`00N_index_*.md` coluna por coluna. Para ajustar a dashboard, é o
`scripts/dash_002_template.html`.

## Boas práticas

- **Sempre dar `id` aos componentes.** É o `id` que permite relacionar base bruta, mapeamento e
  qualquer artefato futuro sem depender do nome em prosa.
- **Manter a padronização de nomenclatura.** Todo arquivo novo segue
  `[id]_[componente]_[alias]_[ano]` — inclusive os que ainda não existem.
- **Não editar o dado bruto.** Correção de dado vira regra em `scripts/`, não edição em
  `raw_data/` — assim o tratamento fica reprodutível e auditável pelo `qa`.
- **Nunca sobrescrever valor presente em silêncio.** A limpeza preenche o que falta e apenas
  *sinaliza* quando o valor do arquivo discorda do cálculo.
- **Número na tela vem do dado, não do texto.** A dashboard recebe as linhas da base e agrega
  no navegador; nada é digitado no HTML. Quando duas leituras de uma pergunta discordam, as
  duas aparecem — esconder uma é escolher por quem lê.
