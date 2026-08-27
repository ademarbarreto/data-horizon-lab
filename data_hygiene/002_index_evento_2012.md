# Mapeamento semântico do dataset de eventos musicais

## Mapeamento semântico das colunas

| Coluna | Tipo de dado | Data format ideal | Sentido semântico |
|---|---|---|---|
| `registro_id` | Texto / identificador | `VARCHAR` — `MUS-0001` | Identificador único de cada registro de evento/apresentação musical. |
| `data_evento` | Data | `DATE` — `YYYY-MM-DD` | Data em que a apresentação ou evento musical ocorreu. |
| `dia_festival` | Número inteiro / ordinal | `INTEGER` | Número sequencial do dia dentro do festival. Ex.: `1`, `2`, `3`. |
| `regiao` | Texto categórico | `VARCHAR` | Região do mapa onde a atividade musical ocorreu. |
| `local_evento` | Texto categórico | `VARCHAR` | Local físico ou ponto específico onde o evento aconteceu. |
| `area_palco` | Texto categórico | `VARCHAR` | Nome da área, palco ou estrutura utilizada para a apresentação. |
| `radio_estacao` | Texto categórico | `VARCHAR` | Estação de rádio associada à apresentação ou programação musical. |
| `artista` | Texto categórico | `VARCHAR` | Nome do artista, banda ou DJ responsável pela apresentação. |
| `faixa_musical` | Texto | `VARCHAR` | Música ou faixa associada ao artista e à apresentação. |
| `estilo_musical` | Texto categórico | `VARCHAR` | Gênero ou estilo musical da apresentação. Ex.: `EDM`, `Electro House`, `Drum & Bass`. |
| `tipo_apresentacao` | Texto categórico | `VARCHAR` | Formato da apresentação musical. Ex.: `DJ set`. |
| `horario_inicio` | Hora | `TIME` — `HH:MM:SS` | Horário de início da apresentação. |
| `duracao_min` | Número inteiro | `INTEGER` — minutos | Duração da apresentação em minutos. |
| `pulseira_cor` | Texto categórico | `VARCHAR` | Cor da pulseira associada ao público ou nível de progressão daquele evento. |
| `nivel_pulseira` | Número inteiro / ordinal | `INTEGER` | Representação numérica do nível da pulseira. |
| `categoria_pulseira` | Texto categórico / ordinal | `VARCHAR` | Categoria de acesso ou progressão relacionada à pulseira. Ex.: `Rookie`, `Intermediate`, `Elite`. |
| `capacidade_area` | Número inteiro | `INTEGER` | Capacidade máxima de pessoas suportada pela área do evento. |
| `ingressos_emitidos` | Número inteiro | `INTEGER` | Quantidade total de ingressos emitidos para a apresentação. |
| `checkins` | Número inteiro | `INTEGER` | Quantidade de pessoas com ingresso que efetivamente realizaram check-in. |
| `convidados` | Número inteiro | `INTEGER` | Quantidade de convidados presentes que não fazem parte do público regular de ingressos. |
| `staff` | Número inteiro | `INTEGER` | Quantidade de funcionários, produção, segurança e demais membros da equipe presentes. |
| `pessoas_na_area` | Número inteiro | `INTEGER` | Total de pessoas presentes na área do evento, considerando público, convidados e staff conforme a regra do dataset. |
| `no_show` | Número inteiro | `INTEGER` | Quantidade de ingressos emitidos que não resultaram em comparecimento/check-in. |
| `ocupacao_pct` | Número decimal / percentual | `DECIMAL(5,2)` — `90.50` | Percentual de ocupação da área em relação à sua capacidade máxima. |
| `preco_medio_ingresso_usd` | Número monetário | `DECIMAL(10,2)` — `54.47` | Valor médio pago por ingresso, em dólares. |
| `receita_ingressos_usd` | Número monetário | `DECIMAL(14,2)` — `1137551.48` | Receita total obtida com a venda de ingressos. |
| `consumo_medio_pessoa_usd` | Número monetário | `DECIMAL(10,2)` — `44.46` | Valor médio gasto por pessoa durante o evento, normalmente relacionado ao consumo no local. |
| `receita_alimentos_bebidas_usd` | Número monetário | `DECIMAL(14,2)` — `488910.98` | Receita gerada pela venda de alimentos e bebidas. |
| `receita_merch_usd` | Número monetário | `DECIMAL(14,2)` — `141417.92` | Receita gerada pela venda de merchandising e produtos relacionados ao evento/artistas. |
| `avaliacao_publico_0a10` | Número decimal | `DECIMAL(3,1)` — intervalo `0.0–10.0` | Nota média atribuída pelo público à experiência ou apresentação. |
| `incidentes_reportados` | Número inteiro | `INTEGER` | Quantidade de incidentes registrados durante a apresentação ou naquele espaço. |
| `registro_sintetico` | Booleano | `BOOLEAN` — `TRUE/FALSE` | Indica se o registro foi produzido artificialmente/sinteticamente. |
| `fonte_referencia` | URL | `VARCHAR/TEXT` — URL absoluta | Fonte utilizada como referência para os dados relacionados à música, artistas ou soundtrack. |

## Classificação geral do dataset

| Grupo semântico | Colunas |
|---|---|
| **Identificação** | `registro_id` |
| **Contexto temporal** | `data_evento`, `dia_festival`, `horario_inicio`, `duracao_min` |
| **Localização / estrutura do evento** | `regiao`, `local_evento`, `area_palco`, `capacidade_area` |
| **Programação musical** | `radio_estacao`, `artista`, `faixa_musical`, `estilo_musical`, `tipo_apresentacao` |
| **Progressão / acesso** | `pulseira_cor`, `nivel_pulseira`, `categoria_pulseira` |
| **Público / presença** | `ingressos_emitidos`, `checkins`, `convidados`, `staff`, `pessoas_na_area`, `no_show`, `ocupacao_pct` |
| **Receita / monetização** | `preco_medio_ingresso_usd`, `receita_ingressos_usd`, `consumo_medio_pessoa_usd`, `receita_alimentos_bebidas_usd`, `receita_merch_usd` |
| **Experiência / operação** | `avaliacao_publico_0a10`, `incidentes_reportados` |
| **Governança / origem dos dados** | `registro_sintetico`, `fonte_referencia` |
