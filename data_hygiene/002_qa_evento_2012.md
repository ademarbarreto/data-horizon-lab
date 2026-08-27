# QA da higienizacao -- base 002 evento musical 2012
Relatorio gerado por `scripts/clean.py`. Nao editar a mao -- ele e
reescrito a cada reprocessamento.

## Resumo
| Etapa | Linhas |
|---|---|
| Linhas de dado no arquivo bruto | 187 |
| Citadas por fora (desembrulhadas) | 109 |
| Linha `TOTAL_GERAL` descartada | 1 |
| Duplicatas removidas | 6 |
| Ids normalizados | 10 |
| Registros na base limpa | 180 |

## Preenchimentos por derivacao
Valores que estavam vazios ou `N/A` e foram calculados a partir de
outras colunas da propria linha.

| Coluna | Preenchidos | Ids |
|---|---|---|
| categoria_pulseira | 6 | `MUS-0029`, `MUS-0058`, `MUS-0087`, `MUS-0116`, `MUS-0145`, `MUS-0174` |
| dia_festival | 10 | `MUS-0018`, `MUS-0036`, `MUS-0054`, `MUS-0072`, `MUS-0090`, `MUS-0108`, `MUS-0126`, `MUS-0144`, `MUS-0162`, `MUS-0180` |
| nivel_pulseira | 8 | `MUS-0022`, `MUS-0044`, `MUS-0066`, `MUS-0088`, `MUS-0110`, `MUS-0132`, `MUS-0154`, `MUS-0176` |
| no_show | 12 | `MUS-0015`, `MUS-0030`, `MUS-0045`, `MUS-0060`, `MUS-0075`, `MUS-0090`, `MUS-0105`, `MUS-0120`, `MUS-0135`, `MUS-0150`, `MUS-0165`, `MUS-0180` |
| pessoas_na_area | 11 | `MUS-0016`, `MUS-0032`, `MUS-0048`, `MUS-0064`, `MUS-0080`, `MUS-0096`, `MUS-0112`, `MUS-0128`, `MUS-0144`, `MUS-0160`, `MUS-0176` |
| receita_ingressos_usd | 9 | `MUS-0019`, `MUS-0038`, `MUS-0057`, `MUS-0076`, `MUS-0095`, `MUS-0114`, `MUS-0133`, `MUS-0152`, `MUS-0171` |

## Divergencias mantidas
O valor original foi **preservado**; a derivacao apenas discorda dele.
Sinalizado para inspecao, nao corrigido.

| Coluna | Id | No arquivo | Calculado |
|---|---|---|---|
| ocupacao_pct | `MUS-0096` | 100.00 | 103.95 |
| pessoas_na_area | `MUS-0052` | 2944 | 2978 |
| pessoas_na_area | `MUS-0061` | 22080 | 22694 |
| pessoas_na_area | `MUS-0079` | 4992 | 5162 |
| pessoas_na_area | `MUS-0091` | 3300 | 3307 |
| pessoas_na_area | `MUS-0107` | 5304 | 5361 |
| pessoas_na_area | `MUS-0113` | 24000 | 24287 |
| pessoas_na_area | `MUS-0135` | 4992 | 5025 |

## Duplicatas removidas
Linhas com o mesmo id. Verificado que as copias sao identicas em
todas as colunas -- manter a primeira ocorrencia nao perde dado.

| Id | Copias no bruto |
|---|---|
| `MUS-0010` | 2 |
| `MUS-0038` | 2 |
| `MUS-0070` | 2 |
| `MUS-0108` | 2 |
| `MUS-0142` | 2 |
| `MUS-0165` | 2 |

## Ids normalizados
Espaco nas pontas e caixa inconsistente na chave primaria.

| No arquivo | Normalizado |
|---|---|
| ` mus-0017 ` | `MUS-0017` |
| ` mus-0034 ` | `MUS-0034` |
| ` mus-0051 ` | `MUS-0051` |
| ` mus-0068 ` | `MUS-0068` |
| ` mus-0085 ` | `MUS-0085` |
| ` mus-0102 ` | `MUS-0102` |
| ` mus-0119 ` | `MUS-0119` |
| ` mus-0136 ` | `MUS-0136` |
| ` mus-0153 ` | `MUS-0153` |
| ` mus-0170 ` | `MUS-0170` |

## Faltantes remanescentes
Vazios que nenhuma regra de derivacao alcanca.

_Nenhum._

## Dominio dos categoricos
- `regiao` (8): `Carson`, `Clear Springs`, `Finley Dam`, `Gladstone`, `Main Stage`, `Montano Plains`, `Red Rock`, `Redfoot Ranch`
- `local_evento` (8): `Carson Street Hub`, `Clear Springs Park`, `Festival Central`, `Finley Dam Deck`, `Gladstone Outpost`, `Montano Fields`, `Red Rock Canyon`, `Redfoot Ranch Grounds`
- `area_palco` (8): `Palco Canyon`, `Palco Dam`, `Palco Norte`, `Palco Principal`, `Palco Pulse`, `Palco Ranch`, `Palco Sunset`, `Palco Urbano`
- `radio_estacao` (3): `Horizon Bass Arena`, `Horizon Pulse`, `Horizon Rocks`
- `artista` (62): `Arctic Monkeys`, `Avicii`, `Azari & III`, `Benny Benassi`, `Chase & Status`, `Chromeo`, `Cut Copy`, `DJ Fresh`, `Digitalism`, `Electric Guest`, `Empire of the Sun`, `Feed Me`, `Fenech-Soler`, `Fixers`, `Foster The People`, `Four Year Strong`, `Friendly Fires`, `Hooray for Earth`, `Hot Chip`, `Howler`, `LCD Soundsystem`, `Ladyhawke`, `Lostprophets`, `Madeon`, `Maverick Sabre` ...
- `faixa_musical` (67): `1901`, `Animal`, `Aroused`, `Awake`, `Away from Here`, `Back of Your Neck`, `Bass 4`, `Bite My Tongue (feat. Oli Sykes)`, `Black, White and Blue`, `Blind Faith (feat. Liam Bailey)`, `Blue Monday`, `Bom Bom`, `Bring Em Down`, `Bug`, `Cinema (Skrillex Remix)`, `Disparate Youth`, `Don't Stop (Color on the Walls)`, `Encore`, `Everyday (Netsky VIP Remix)`, `Farewell to the Fairground`, `Get Away`, `Give It Up`, `Had Enough`, `Hate To Say I Told You So`, `Hawaiian Air` ...
- `estilo_musical` (29): `Alternative Pop`, `Alternative Rock`, `Blues Rock`, `Dance Pop`, `Dance Punk`, `Drum & Bass`, `Dubstep`, `EDM`, `Electro`, `Electro / House`, `Electro Funk`, `Electro House`, `Electronic`, `Garage Rock`, `Indie Dance`, `Indie Electronic`, `Indie Pop`, `Indie Rock`, `Indietronica`, `New Wave`, `Noise Pop`, `PSYCHEDELIC ROCK`, `Pop Punk`, `Post Hardcore`, `Post Punk` ...
- `tipo_apresentacao` (3): `DJ set`, `Festival set`, `Live set`
- `pulseira_cor` (7): `Blue`, `Gold`, `Green`, `Orange`, `Pink`, `Purple`, `Yellow`
- `categoria_pulseira` (5): `Advanced`, `Elite`, `Elite/VIP`, `Intermediate`, `Rookie`

## Variantes fundidas
Grafias que diferiam so em caixa ou espaco e foram unificadas.

| Coluna | Canonica | Variantes no bruto |
|---|---|---|
| area_palco | `Palco Canyon` | `Palco Canyon`, `palco canyon` |
| area_palco | `Palco Dam` | `Palco Dam`, `palco dam` |
| area_palco | `Palco Pulse` | `Palco Pulse`, `palco pulse` |
| area_palco | `Palco Urbano` | `Palco Urbano`, `palco urbano` |
| categoria_pulseira | `Advanced` | `Advanced`, `advanced` |
| categoria_pulseira | `Elite` | `Elite`, `elite` |
| categoria_pulseira | `Elite/VIP` | `Elite/VIP`, `elite/vip` |
| categoria_pulseira | `Intermediate` | `Intermediate`, `intermediate` |
| categoria_pulseira | `Rookie` | `Rookie`, `rookie` |
| estilo_musical | `Alternative Pop` | `ALTERNATIVE POP`, `Alternative Pop` |
| estilo_musical | `Alternative Rock` | `ALTERNATIVE ROCK`, `Alternative Rock`, `alternative rock` |
| estilo_musical | `Dance Punk` | `Dance Punk`, `dance punk` |
| estilo_musical | `Drum & Bass` | `Drum & Bass`, `drum & bass` |
| estilo_musical | `Dubstep` | `DUBSTEP`, `Dubstep`, `dubstep` |
| estilo_musical | `EDM` | `EDM`, `edm` |
| estilo_musical | `Electro Funk` | `Electro Funk`, `electro funk` |
| estilo_musical | `Electro House` | `ELECTRO HOUSE`, `Electro House`, `electro house` |
| estilo_musical | `Electronic` | `ELECTRONIC`, `Electronic` |
| estilo_musical | `Indie Dance` | `Indie Dance`, `indie dance` |
| estilo_musical | `Indie Electronic` | `INDIE ELECTRONIC`, `Indie Electronic` |
| estilo_musical | `Indie Pop` | `INDIE POP`, `Indie Pop`, `indie pop` |
| estilo_musical | `Indie Rock` | `INDIE ROCK`, `Indie Rock`, `indie rock` |
| estilo_musical | `Indietronica` | `INDIETRONICA`, `Indietronica`, `indietronica` |
| estilo_musical | `Post Punk` | `POST PUNK`, `Post Punk` |
| estilo_musical | `PSYCHEDELIC ROCK` | `PSYCHEDELIC ROCK`, `psychedelic rock` |
| estilo_musical | `Synthpop` | `Synthpop`, `synthpop` |
| local_evento | `Carson Street Hub` | `CARSON STREET HUB`, `Carson Street Hub` |
| local_evento | `Clear Springs Park` | `CLEAR SPRINGS PARK`, `Clear Springs Park` |
| local_evento | `Festival Central` | `FESTIVAL CENTRAL`, `Festival Central` |
| local_evento | `Finley Dam Deck` | `FINLEY DAM DECK`, `Finley Dam Deck` |
| local_evento | `Gladstone Outpost` | `GLADSTONE OUTPOST`, `Gladstone Outpost` |
| pulseira_cor | `Blue` | `Blue`, `blue` |
| pulseira_cor | `Gold` | `Gold`, `gold` |
| pulseira_cor | `Green` | `Green`, `green` |
| pulseira_cor | `Orange` | `Orange`, `orange` |
| pulseira_cor | `Pink` | `Pink`, `pink` |
| pulseira_cor | `Purple` | `Purple`, `purple` |
| pulseira_cor | `Yellow` | `Yellow`, `yellow` |
| radio_estacao | `Horizon Bass Arena` | `HORIZON BASS ARENA`, `Horizon Bass Arena` |
| radio_estacao | `Horizon Pulse` | `Horizon Pulse`, `horizon pulse` |
| regiao | `Carson` | `Carson`, `carson` |
| regiao | `Clear Springs` | `Clear Springs`, `clear springs` |
| regiao | `Finley Dam` | `Finley Dam`, `finley dam` |
| regiao | `Gladstone` | `Gladstone`, `gladstone` |
| regiao | `Main Stage` | `Main Stage`, `main stage` |
| regiao | `Red Rock` | `Red Rock`, `red rock` |
| regiao | `Redfoot Ranch` | `Redfoot Ranch`, `redfoot ranch` |

## Ambiguidades para decisao humana
Rotulos que **podem** ser a mesma categoria com grafia diferente.
A limpeza nao os une -- decida e, se for o caso, ajuste o bruto.

| Coluna | Candidatos |
|---|---|
| estilo_musical | `Electro / House` vs `Electro House` |

## Notas
- Teto de ocupacao: a base nao admite `ocupacao_pct` acima de 100%. Em 7 linha(s) `pessoas_na_area` esta exatamente igual a `capacidade_area` (publico capado na capacidade) e em 8 linha(s) a ocupacao esta em 100%. As divergencias listadas acima vem dai -- valores preservados, nada corrigido.
