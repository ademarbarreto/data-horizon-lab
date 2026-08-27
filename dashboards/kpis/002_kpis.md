# Perguntas de negócio
- Qual palco foi vendido mais ingressos
  -> Quanto foi vendido por pulseiras (filtro por todas, ou por cor)
  -> Valor arrecadado total pelo palco
  -> Principais do Palco 
- Quem foram os top 3 artistas que mais trouxeram gente pra acompanhar
- Quais foram as musicas queridinhas do evento


# Regras
- a base utilizada será [`data_hygiene/002_clean_evento_2012.csv`](../../data_hygiene/002_clean_evento_2012.csv)
  (a base 002 higienizada — o bruto `002_data_evento_2012.csv` não é legível direto:
  109 das 186 linhas vêm inteiras entre aspas e um leitor CSV devolve só 77 linhas úteis)
- o design system utilizado será [`dashboards/design_system/design_system.html`](../design_system/design_system.html)


# Guard rails
- nunca invente dados
- organize a dashboard de uma maneira visual focada em storytelling


# Entrega
- dashboard: [`dashboards/002_dash_evento_2012.html`](../002_dash_evento_2012.html)
- gerada por `python scripts/build_dashboard_002.py` — o HTML não é editado à mão

## Decisões tomadas na apuração
- **"Principais do Palco"** = ranking de atrações do palco selecionado (artista, público,
  faixa e nota), não resumo operacional.
- **"Músicas queridinhas"** = as duas leituras juntas, porque discordam: `Silicone Lube`
  tem a maior nota (9,17) e `Levels (Skrillex Mix)` o maior público (31.096, nota 8,23).
- **Frequência de execução ficou fora** como métrica de música: toda faixa tocou 2 ou 3
  vezes, então ranquear por isso é ranquear pelo critério de desempate.
- **Top 3 artistas por volume total**, como a pergunta pede — com a ressalva na própria
  dashboard de que por média de público por show o pódio muda inteiro.