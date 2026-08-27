"""Especificacao da base 002 -- eventos musicais do Horizon 2012.

Espelha `data_hygiene/002_index_evento_2012.md`: cada entrada de `COLUNAS`
transcreve a coluna "Data format ideal" do dicionario.
"""

from hygiene_lib import (
    aplicar_derivacao,
    formatar_decimal,
    formatar_inteiro,
    num_celula,
)

ID = "002"
ALIAS = "evento"
ANO = "2012"
TITULO = "QA da higienizacao -- base 002 evento musical 2012"
ENTRADA = "raw_data/002_data_evento_2012.csv"
SAIDA_CSV = "data_hygiene/002_clean_evento_2012.csv"
SAIDA_QA = "data_hygiene/002_qa_evento_2012.md"
CHAVE = "registro_id"

COLUNAS = {
    "registro_id":                   {"tipo": "id"},
    "data_evento":                   {"tipo": "data"},
    "dia_festival":                  {"tipo": "inteiro"},
    "regiao":                        {"tipo": "categoria"},
    "local_evento":                  {"tipo": "categoria"},
    "area_palco":                    {"tipo": "categoria"},
    "radio_estacao":                 {"tipo": "categoria"},
    "artista":                       {"tipo": "categoria"},
    "faixa_musical":                 {"tipo": "categoria"},
    "estilo_musical":                {"tipo": "categoria"},
    "tipo_apresentacao":             {"tipo": "categoria"},
    "horario_inicio":                {"tipo": "hora"},
    "duracao_min":                   {"tipo": "inteiro"},
    "pulseira_cor":                  {"tipo": "categoria"},
    "nivel_pulseira":                {"tipo": "inteiro"},
    "categoria_pulseira":            {"tipo": "categoria"},
    "capacidade_area":               {"tipo": "inteiro"},
    "ingressos_emitidos":            {"tipo": "inteiro"},
    "checkins":                      {"tipo": "inteiro"},
    "convidados":                    {"tipo": "inteiro"},
    "staff":                         {"tipo": "inteiro"},
    "pessoas_na_area":               {"tipo": "inteiro"},
    "no_show":                       {"tipo": "inteiro"},
    # No bruto essa coluna mistura percentual (89.5), percentual com unidade
    # ("73.0 %") e fracao (0.855). `fracao_pct` reescala a fracao para %.
    "ocupacao_pct":                  {"tipo": "decimal", "decimais": 2,
                                      "precisao": 5, "fracao_pct": True},
    "preco_medio_ingresso_usd":      {"tipo": "decimal", "decimais": 2, "precisao": 10},
    "receita_ingressos_usd":         {"tipo": "decimal", "decimais": 2, "precisao": 14},
    "consumo_medio_pessoa_usd":      {"tipo": "decimal", "decimais": 2, "precisao": 10},
    "receita_alimentos_bebidas_usd": {"tipo": "decimal", "decimais": 2, "precisao": 14},
    "receita_merch_usd":             {"tipo": "decimal", "decimais": 2, "precisao": 14},
    "avaliacao_publico_0a10":        {"tipo": "decimal", "decimais": 1, "precisao": 3},
    "incidentes_reportados":         {"tipo": "inteiro"},
    "registro_sintetico":            {"tipo": "booleano"},
    "fonte_referencia":              {"tipo": "url"},
}

NIVEL_POR_COR = {
    "Yellow": 1,
    "Green": 2,
    "Blue": 3,
    "Pink": 4,
    "Orange": 5,
    "Purple": 6,
    "Gold": 7,
}

# `Elite` (nivel 6) e `Elite/VIP` (nivel 7) sao categorias DISTINTAS -- a
# grafia parecida nao as torna variantes uma da outra.
CATEGORIA_POR_NIVEL = {
    1: "Rookie",
    2: "Rookie",
    3: "Intermediate",
    4: "Intermediate",
    5: "Advanced",
    6: "Elite",
    7: "Elite/VIP",
}

# O festival de 2012 ocorreu entre 19 e 25 de outubro; o dia do mes da o dia
# do festival numa relacao 1:1 verificada no dado.
DIA_FESTIVAL_POR_DIA_DO_MES = {19: 1, 20: 2, 21: 3, 22: 4, 23: 5, 24: 6, 25: 7}


def derivar(linhas, registro):
    """Preenche o que da para calcular a partir de outras colunas da linha."""

    aplicar_derivacao(
        linhas, registro, "nivel_pulseira", CHAVE,
        calcular=lambda linha: NIVEL_POR_COR.get(linha.get("pulseira_cor", "")),
        formatar=str,
    )

    aplicar_derivacao(
        linhas, registro, "categoria_pulseira", CHAVE,
        calcular=lambda linha: CATEGORIA_POR_NIVEL.get(
            int(num_celula(linha, "nivel_pulseira"))
            if num_celula(linha, "nivel_pulseira") is not None else None
        ),
        formatar=str,
    )

    def dia_festival(linha):
        data = linha.get("data_evento", "")
        if len(data) != 10:
            return None
        return DIA_FESTIVAL_POR_DIA_DO_MES.get(int(data[8:10]))

    aplicar_derivacao(
        linhas, registro, "dia_festival", CHAVE,
        calcular=dia_festival,
        formatar=str,
    )

    # Publico total da area. Identidade em 168 linhas; as 7 divergentes tem o
    # valor capado na capacidade da area -- regra do dataset, nao erro.
    def pessoas(linha):
        partes = [num_celula(linha, c)
                  for c in ("checkins", "convidados", "staff")]
        if any(p is None for p in partes):
            return None
        return sum(partes)

    aplicar_derivacao(
        linhas, registro, "pessoas_na_area", CHAVE,
        calcular=pessoas,
        formatar=formatar_inteiro,
        tolerancia=lambda _: 1,
    )

    # No-show = ingresso emitido que nao virou check-in. Identidade exata: 173/0.
    def no_show(linha):
        emitidos = num_celula(linha, "ingressos_emitidos")
        checkins = num_celula(linha, "checkins")
        if None in (emitidos, checkins):
            return None
        return emitidos - checkins

    aplicar_derivacao(
        linhas, registro, "no_show", CHAVE,
        calcular=no_show,
        formatar=formatar_inteiro,
        tolerancia=lambda _: 1,
    )

    # Ocupacao mede pessoas_na_area contra a capacidade -- nao os check-ins
    # (essa variante divergia nas 186 linhas).
    def ocupacao(linha):
        pessoas_area = num_celula(linha, "pessoas_na_area")
        capacidade = num_celula(linha, "capacidade_area")
        if None in (pessoas_area, capacidade) or not capacidade:
            return None
        return round(pessoas_area / capacidade * 100, 2)

    aplicar_derivacao(
        linhas, registro, "ocupacao_pct", CHAVE,
        calcular=ocupacao,
        formatar=lambda v: formatar_decimal(v, 2),
        tolerancia=lambda _: 0.6,
    )

    # Receita de ingresso = preco medio x check-ins (nao x emitidos: essa
    # variante divergia em 176 linhas). Identidade exata: 176/0.
    def receita(linha):
        preco = num_celula(linha, "preco_medio_ingresso_usd")
        checkins = num_celula(linha, "checkins")
        if None in (preco, checkins):
            return None
        return round(preco * checkins, 2)

    aplicar_derivacao(
        linhas, registro, "receita_ingressos_usd", CHAVE,
        calcular=receita,
        formatar=lambda v: formatar_decimal(v, 2),
        tolerancia=lambda calculado: max(2.0, abs(calculado) * 0.002),
    )

    # As divergencias que sobram tem todas a mesma causa: a base nunca deixa a
    # ocupacao passar de 100%. Ou `pessoas_na_area` foi capado na capacidade da
    # area, ou a ocupacao foi capada em 100% com o publico acima dela. E regra
    # do dataset, entao o valor original fica -- so registrado aqui.
    capados = [linha[CHAVE] for linha in linhas
               if linha["pessoas_na_area"] == linha["capacidade_area"] != ""]
    no_teto = [linha[CHAVE] for linha in linhas
               if num_celula(linha, "ocupacao_pct") == 100.0]
    if capados or no_teto:
        registro.notas.append(
            "Teto de ocupacao: a base nao admite `ocupacao_pct` acima de 100%. "
            f"Em {len(capados)} linha(s) `pessoas_na_area` esta exatamente igual "
            "a `capacidade_area` (publico capado na capacidade) e em "
            f"{len(no_teto)} linha(s) a ocupacao esta em 100%. As divergencias "
            "listadas acima vem dai -- valores preservados, nada corrigido."
        )
