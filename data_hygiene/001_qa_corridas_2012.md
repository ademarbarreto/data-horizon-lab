# QA da higienizacao -- base 001 corridas 2012
Relatorio gerado por `scripts/clean.py`. Nao editar a mao -- ele e
reescrito a cada reprocessamento.

## Resumo
| Etapa | Linhas |
|---|---|
| Linhas de dado no arquivo bruto | 172 |
| Citadas por fora (desembrulhadas) | 75 |
| Linha `TOTAL_GERAL` descartada | 1 |
| Duplicatas removidas | 5 |
| Ids normalizados | 9 |
| Registros na base limpa | 166 |

## Preenchimentos por derivacao
Valores que estavam vazios ou `N/A` e foram calculados a partir de
outras colunas da propria linha.

| Coluna | Preenchidos | Ids |
|---|---|---|
| gap_para_vencedor_seg | 7 | `RES-0023`, `RES-0046`, `RES-0069`, `RES-0092`, `RES-0115`, `RES-0138`, `RES-0161` |
| nivel_pulseira_minima | 6 | `RES-0027`, `RES-0054`, `RES-0081`, `RES-0108`, `RES-0135`, `RES-0162` |
| nivel_pulseira_piloto | 7 | `RES-0021`, `RES-0042`, `RES-0063`, `RES-0084`, `RES-0105`, `RES-0126`, `RES-0147` |
| tempo_formatado | 14 | `RES-0017`, `RES-0029`, `RES-0034`, `RES-0051`, `RES-0058`, `RES-0068`, `RES-0085`, `RES-0087`, `RES-0102`, `RES-0116`, `RES-0119`, `RES-0136` ... (+2) |
| velocidade_media_kmh | 11 | `RES-0014`, `RES-0028`, `RES-0042`, `RES-0056`, `RES-0070`, `RES-0084`, `RES-0098`, `RES-0112`, `RES-0126`, `RES-0140`, `RES-0154` |
| vencedor | 15 | `RES-0011`, `RES-0022`, `RES-0033`, `RES-0044`, `RES-0055`, `RES-0066`, `RES-0077`, `RES-0088`, `RES-0099`, `RES-0110`, `RES-0121`, `RES-0132` ... (+3) |

## Divergencias mantidas
O valor original foi **preservado**; a derivacao apenas discorda dele.
Sinalizado para inspecao, nao corrigido.

_Nenhum._

## Duplicatas removidas
Linhas com o mesmo id. Verificado que as copias sao identicas em
todas as colunas -- manter a primeira ocorrencia nao perde dado.

| Id | Copias no bruto |
|---|---|
| `RES-0014` | 2 |
| `RES-0042` | 2 |
| `RES-0076` | 2 |
| `RES-0116` | 2 |
| `RES-0147` | 2 |

## Ids normalizados
Espaco nas pontas e caixa inconsistente na chave primaria.

| No arquivo | Normalizado |
|---|---|
| `  res-0019  ` | `RES-0019` |
| `  res-0038  ` | `RES-0038` |
| `  res-0057  ` | `RES-0057` |
| `  res-0076  ` | `RES-0076` |
| `  res-0076  ` | `RES-0076` |
| `  res-0095  ` | `RES-0095` |
| `  res-0114  ` | `RES-0114` |
| `  res-0133  ` | `RES-0133` |
| `  res-0152  ` | `RES-0152` |

## Faltantes remanescentes
Vazios que nenhuma regra de derivacao alcanca.

_Nenhum._

## Dominio dos categoricos
- `tipo_evento` (2): `Festival Race`, `Star Showdown`
- `nome_evento` (26): `ADIDAS Urban Avalanche`, `BBS Japanese Trailblazers`, `BBS Showdown`, `Bondurant Valley Skirmish`, `Brembo Midnight Blast`, `Fatlace Chase`, `Fatlace Hot Hatch Hustle`, `Ford Challenge`, `G-Shock Super Sprint`, `GoPro Euro Cross`, `HORIZON presents The Gauntlet`, `Horizon Heats`, `Illest Eastern Steel`, `Oakley Blitz`, `Oakley Heat Wave`, `Old Spice US Muscle Mash`, `Recaro '70s Rockout`, `Recaro Rush`, `Rockstar Cliff Run`, `Star Showdown - Ali Howard`, `Star Showdown - Darius Flynt`, `Star Showdown - Duke Maguire`, `Star Showdown - Hailey Harper`, `Star Showdown - Marko Baran`, `Star Showdown - Ramona Cravache` ...
- `circuito_rota` (25): `Ali Challenge Route`, `Beaumont Sprint Circuit`, `Bunker Dirt Cross`, `Bunker Dirt Sprint`, `Carson Sprint Circuit`, `Clear Springs Run`, `Clifton Valley Mini Circuit`, `Darius Challenge Route`, `Duke Challenge Route`, `Festival Central Loop`, `Festival South Circuit`, `Finley Ram Circuit`, `Gladstone Canyon Run`, `Gladstone Dirt Cross`, `Gladstone Dirt Sprint`, `Hailey Challenge Route`, `Main Stage Run`, `Marko Challenge Route`, `Montano Dirt Cross`, `Ramona Challenge Route`, `Reservoir Trail`, `Route 24 Run`, `Route 27 Run`, `Steelworks Sprint Circuit`, `Zaki Challenge Route`
- `regiao` (17): `Beaumont`, `Bunker`, `Carson`, `Clear Springs`, `Clifton Valley`, `Festival Central`, `Festival South`, `Finley Dam`, `Gladstone`, `Gladstone Canyon`, `Industrial District`, `Main Stage`, `Montano Plains`, `Red Rock`, `Reservoir`, `Route 24`, `Route 27`
- `tipo_rota` (6): `Circuit`, `Dirt Cross`, `Dirt Sprint`, `Head-to-Head`, `Sprint`, `Trail`
- `piso` (3): `Asfalto`, `Misto`, `Terra`
- `pulseira_minima` (8): `Blue`, `Gold`, `Green`, `Orange`, `Pink`, `Purple`, `Sem pulseira`, `Yellow`
- `piloto` (23): `Alex Mercer`, `Ali Howard`, `Avery Scott`, `Cameron Price`, `Casey Turner`, `Darius Flynt`, `Drew Foster`, `Duke Maguire`, `Hailey Harper`, `Harper Diaz`, `Jamie Cole`, `Jordan Hayes`, `Logan Rivera`, `Marko Baran`, `Morgan Reed`, `Peyton Hughes`, `Quinn Parker`, `Ramona Cravache`, `Reese Morgan`, `Riley Grant`, `Skyler Bennett`, `Taylor Brooks`, `Zaki Malik`
- `pulseira_piloto` (7): `Blue`, `Gold`, `Green`, `Orange`, `Pink`, `Purple`, `Yellow`
- `marca_carro` (12): `Audi`, `BMW`, `Dodge`, `Ferrari`, `Ford`, `Lamborghini`, `Lexus`, `Mitsubishi`, `Nissan`, `Saleen`, `Subaru`, `Toyota`
- `modelo_carro` (21): `458 Italia`, `599XX`, `Aventador LP700-4`, `Challenger SRT8 392`, `Diablo SV`, `F-150 SVT Raptor`, `Focus RS500`, `GT`, `GT-R Black Edition`, `Impreza WRX STI`, `LFA`, `Lancer Evolution X GSR`, `M3`, `Mustang Boss 429`, `R8 GT`, `RS200 Evolution`, `S7`, `Skyline GT-R V-Spec II`, `Sport quattro`, `Supra RZ`, `Viper GTS`
- `classe_carro` (3): `A`, `B`, `S`
- `tracao` (3): `AWD`, `FWD`, `RWD`
- `clima` (5): `Chuva leve`, `Ensolarado`, `Nublado`, `Seco`, `Vento forte`

## Variantes fundidas
Grafias que diferiam so em caixa ou espaco e foram unificadas.

| Coluna | Canonica | Variantes no bruto |
|---|---|---|
| clima | `Chuva leve` | `Chuva leve`, `chuva leve` |
| clima | `Ensolarado` | `Ensolarado`, `ensolarado` |
| marca_carro | `Audi` | `AUDI`, `Audi` |
| marca_carro | `BMW` | `BMW`, `bmw` |
| marca_carro | `Dodge` | `Dodge`, `dodge` |
| marca_carro | `Ferrari` | `Ferrari`, `ferrari` |
| marca_carro | `Lamborghini` | `LAMBORGHINI`, `Lamborghini` |
| marca_carro | `Subaru` | `SUBARU`, `Subaru` |
| piso | `Asfalto` | `ASFALTO`, `Asfalto`, `asfalto` |
| piso | `Misto` | `MISTO`, `Misto`, `misto` |
| piso | `Terra` | `TERRA`, `Terra`, `terra` |
| pulseira_minima | `Blue` | `Blue`, `blue` |
| pulseira_minima | `Gold` | `Gold`, `gold` |
| pulseira_minima | `Green` | `Green`, `green` |
| pulseira_minima | `Yellow` | `Yellow`, `yellow` |
| pulseira_piloto | `Blue` | `BLUE`, `Blue` |
| pulseira_piloto | `Pink` | `PINK`, `Pink` |
| pulseira_piloto | `Purple` | `PURPLE`, `Purple` |
| regiao | `Bunker` | `BUNKER`, `Bunker` |
| regiao | `Carson` | `CARSON`, `Carson` |
| regiao | `Clear Springs` | `CLEAR SPRINGS`, `Clear Springs` |
| regiao | `Clifton Valley` | `CLIFTON VALLEY`, `Clifton Valley` |
| regiao | `Festival South` | `FESTIVAL SOUTH`, `Festival South` |
| regiao | `Finley Dam` | `FINLEY DAM`, `Finley Dam` |
| regiao | `Gladstone Canyon` | `GLADSTONE CANYON`, `Gladstone Canyon` |
| regiao | `Main Stage` | `MAIN STAGE`, `Main Stage` |
| regiao | `Montano Plains` | `MONTANO PLAINS`, `Montano Plains` |
| regiao | `Route 27` | `ROUTE 27`, `Route 27` |
| tipo_evento | `Festival Race` | `FESTIVAL RACE`, `Festival Race`, `festival race` |
| tipo_evento | `Star Showdown` | `STAR SHOWDOWN`, `Star Showdown`, `star showdown` |
| tracao | `AWD` | `AWD`, `awd` |
| tracao | `FWD` | `FWD`, `fwd` |
| tracao | `RWD` | `RWD`, `rwd` |
