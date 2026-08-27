# Mapeamento semântico do dataset

## Mapeamento semântico das colunas

| Coluna | Tipo de dado | Data format ideal | Sentido semântico |
|---|---|---|---|
| `resultado_id` | Texto / identificador | `VARCHAR` — `RES-0001` | Identificador único de cada resultado individual de corrida. |
| `corrida_id` | Texto / identificador | `VARCHAR` — `RACE-001` | Identificador da corrida, permitindo relacionar vários resultados à mesma prova. |
| `data_corrida` | Data | `DATE` — `YYYY-MM-DD` | Data em que a corrida aconteceu. |
| `tipo_evento` | Texto categórico | `VARCHAR` | Categoria geral do evento. Ex.: `Festival Race`. |
| `nome_evento` | Texto categórico | `VARCHAR` | Nome específico ou comercial do evento. |
| `circuito_rota` | Texto categórico | `VARCHAR` | Nome do circuito ou rota utilizada na corrida. |
| `regiao` | Texto categórico | `VARCHAR` | Região do mapa onde o evento acontece. |
| `tipo_rota` | Texto categórico | `VARCHAR` | Tipo ou configuração da rota. Ex.: `Circuit`, `Dirt Cross`. |
| `piso` | Texto categórico | `VARCHAR` | Superfície predominante da pista. Ex.: `Asfalto`, `Terra`. |
| `distancia_km` | Número decimal | `DECIMAL(6,2)` — `5.20` | Distância da rota em quilômetros. |
| `voltas` | Número inteiro | `INTEGER` | Quantidade de voltas da corrida. |
| `pulseira_minima` | Texto categórico | `VARCHAR` | Pulseira mínima necessária para participar do evento. |
| `nivel_pulseira_minima` | Número inteiro / ordinal | `INTEGER` | Representação numérica do nível mínimo de progressão exigido. |
| `piloto` | Texto | `VARCHAR` | Nome do piloto participante. |
| `pulseira_piloto` | Texto categórico | `VARCHAR` | Pulseira de progressão pertencente ao piloto no momento da corrida. |
| `nivel_pulseira_piloto` | Número inteiro / ordinal | `INTEGER` | Nível numérico associado à pulseira do piloto. |
| `ano_carro` | Número inteiro / ano | `SMALLINT` — `YYYY` | Ano/model year do veículo utilizado. |
| `marca_carro` | Texto categórico | `VARCHAR` | Fabricante do veículo. |
| `modelo_carro` | Texto categórico | `VARCHAR` | Modelo específico do veículo. |
| `classe_carro` | Texto categórico / ordinal | `VARCHAR(2)` | Classe de desempenho do veículo. Ex.: `B`, `A`, `S`. |
| `tracao` | Texto categórico | `VARCHAR(3)` | Configuração de tração do veículo. Ex.: `RWD`, `AWD`. |
| `potencia_hp` | Número inteiro | `INTEGER` | Potência do veículo em horsepower. |
| `tempo_total_seg` | Número decimal | `DECIMAL(10,3)` — segundos | Tempo total necessário para concluir a corrida, em segundos. |
| `tempo_formatado` | Duração formatada | `TIME/DURATION` — `HH:MM:SS.mmm` | Representação legível do tempo total da corrida. |
| `gap_para_vencedor_seg` | Número decimal | `DECIMAL(10,3)` — segundos | Diferença de tempo entre o piloto e o vencedor. |
| `posicao` | Número inteiro / ordinal | `INTEGER` | Posição final do piloto na corrida. |
| `vencedor` | Booleano | `BOOLEAN` — `TRUE/FALSE` | Indica se o piloto venceu a corrida. |
| `dnf` | Booleano | `BOOLEAN` — `TRUE/FALSE` | Indica se o piloto não completou a corrida (`Did Not Finish`). |
| `pontos` | Número inteiro | `INTEGER` | Quantidade de pontos recebidos pelo resultado. |
| `creditos_usd` | Número monetário | `DECIMAL(12,2)` — `3000.00` | Recompensa financeira/créditos recebidos pelo piloto. |
| `velocidade_media_kmh` | Número decimal | `DECIMAL(6,2)` — `138.10` | Velocidade média do piloto em quilômetros por hora. |
| `clima` | Texto categórico | `VARCHAR` | Condição climática durante a corrida. |
| `hora_largada` | Hora | `TIME` — `HH:MM:SS` | Horário de início da corrida. |
| `registro_sintetico` | Booleano | `BOOLEAN` — `TRUE/FALSE` | Indica se o registro foi criado artificialmente/sinteticamente. |
| `fonte_eventos` | URL | `VARCHAR/TEXT` — URL absoluta | Fonte utilizada para obter informações sobre os eventos. |
| `fonte_carros` | URL | `VARCHAR/TEXT` — URL absoluta | Fonte utilizada para obter informações sobre os veículos. |
| `fonte_pulseiras` | URL | `VARCHAR/TEXT` — URL absoluta | Fonte utilizada para informações sobre pulseiras e progressão. |

## Classificação geral do dataset

| Grupo semântico | Colunas |
|---|---|
| **Identificação** | `resultado_id`, `corrida_id` |
| **Evento / corrida** | `data_corrida`, `tipo_evento`, `nome_evento`, `circuito_rota`, `regiao`, `tipo_rota`, `piso`, `distancia_km`, `voltas` |
| **Requisitos de progressão** | `pulseira_minima`, `nivel_pulseira_minima` |
| **Piloto** | `piloto`, `pulseira_piloto`, `nivel_pulseira_piloto` |
| **Veículo** | `ano_carro`, `marca_carro`, `modelo_carro`, `classe_carro`, `tracao`, `potencia_hp` |
| **Performance da corrida** | `tempo_total_seg`, `tempo_formatado`, `gap_para_vencedor_seg`, `posicao`, `vencedor`, `dnf`, `velocidade_media_kmh` |
| **Recompensas** | `pontos`, `creditos_usd` |
| **Contexto da corrida** | `clima`, `hora_largada` |
| **Governança / origem dos dados** | `registro_sintetico`, `fonte_eventos`, `fonte_carros`, `fonte_pulseiras` |
