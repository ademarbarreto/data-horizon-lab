"""Especificacao da base 001 -- corridas do Horizon 2012.

Espelha `data_hygiene/001_index_corridas_2012.md`: cada entrada de `COLUNAS`
transcreve a coluna "Data format ideal" do dicionario. E esse pareamento pelo
id do arquivo (001 <-> 001) que da a limpeza a escala de cada numero.
"""

from hygiene_lib import (
    aplicar_derivacao,
    formatar_bool,
    formatar_decimal,
    formatar_duracao,
    num_celula,
)

ID = "001"
ALIAS = "corridas"
ANO = "2012"
TITULO = "QA da higienizacao -- base 001 corridas 2012"
ENTRADA = "raw_data/001_data_corridas_2012.csv"
SAIDA_CSV = "data_hygiene/001_clean_corridas_2012.csv"
SAIDA_QA = "data_hygiene/001_qa_corridas_2012.md"
CHAVE = "resultado_id"

COLUNAS = {
    "resultado_id":          {"tipo": "id"},
    "corrida_id":            {"tipo": "id"},
    "data_corrida":          {"tipo": "data"},
    "tipo_evento":           {"tipo": "categoria"},
    "nome_evento":           {"tipo": "categoria"},
    "circuito_rota":         {"tipo": "categoria"},
    "regiao":                {"tipo": "categoria"},
    "tipo_rota":             {"tipo": "categoria"},
    "piso":                  {"tipo": "categoria"},
    "distancia_km":          {"tipo": "decimal", "decimais": 2, "precisao": 6},
    "voltas":                {"tipo": "inteiro"},
    "pulseira_minima":       {"tipo": "categoria"},
    "nivel_pulseira_minima": {"tipo": "inteiro"},
    "piloto":                {"tipo": "categoria"},
    "pulseira_piloto":       {"tipo": "categoria"},
    "nivel_pulseira_piloto": {"tipo": "inteiro"},
    "ano_carro":             {"tipo": "inteiro"},
    "marca_carro":           {"tipo": "categoria"},
    "modelo_carro":          {"tipo": "categoria"},
    "classe_carro":          {"tipo": "categoria"},
    "tracao":                {"tipo": "categoria"},
    "potencia_hp":           {"tipo": "inteiro"},
    "tempo_total_seg":       {"tipo": "decimal", "decimais": 3, "precisao": 10},
    "tempo_formatado":       {"tipo": "duracao"},
    "gap_para_vencedor_seg": {"tipo": "decimal", "decimais": 3, "precisao": 10},
    "posicao":               {"tipo": "inteiro"},
    "vencedor":              {"tipo": "booleano"},
    "dnf":                   {"tipo": "booleano"},
    "pontos":                {"tipo": "inteiro"},
    "creditos_usd":          {"tipo": "decimal", "decimais": 2, "precisao": 12},
    "velocidade_media_kmh":  {"tipo": "decimal", "decimais": 2, "precisao": 6},
    "clima":                 {"tipo": "categoria"},
    "hora_largada":          {"tipo": "hora"},
    "registro_sintetico":    {"tipo": "booleano"},
    "fonte_eventos":         {"tipo": "url"},
    "fonte_carros":          {"tipo": "url"},
    "fonte_pulseiras":       {"tipo": "url"},
}

# Progressao de pulseiras do Horizon. Verificado como bijecao completa nas duas
# bases: nao ha cor com mais de um nivel nem nivel com mais de uma cor.
NIVEL_POR_COR = {
    "Sem pulseira": 0,
    "Yellow": 1,
    "Green": 2,
    "Blue": 3,
    "Pink": 4,
    "Orange": 5,
    "Purple": 6,
    "Gold": 7,
}


def derivar(linhas, registro):
    """Preenche o que da para calcular a partir de outras colunas da linha."""

    # Nivel de pulseira a partir da cor -- vale para o requisito da corrida e
    # para a pulseira do piloto.
    for coluna_cor, coluna_nivel in (
        ("pulseira_minima", "nivel_pulseira_minima"),
        ("pulseira_piloto", "nivel_pulseira_piloto"),
    ):
        aplicar_derivacao(
            linhas, registro, coluna_nivel, CHAVE,
            calcular=lambda linha, c=coluna_cor: NIVEL_POR_COR.get(linha.get(c, "")),
            formatar=str,
        )

    # Vencedor e quem chegou em primeiro. Verificado: 156 linhas com os dois
    # campos preenchidos, zero contradicao.
    aplicar_derivacao(
        linhas, registro, "vencedor", CHAVE,
        calcular=lambda linha: (num_celula(linha, "posicao") == 1
                                if linha.get("posicao", "") != "" else None),
        formatar=formatar_bool,
    )

    # Tempo formatado e so a apresentacao de tempo_total_seg.
    aplicar_derivacao(
        linhas, registro, "tempo_formatado", CHAVE,
        calcular=lambda linha: num_celula(linha, "tempo_total_seg"),
        formatar=formatar_duracao,
    )

    # Gap = tempo do piloto menos o tempo do vencedor da MESMA corrida.
    # Contra o vencedor (posicao == 1) a identidade fecha em 118/0; contra o
    # menor tempo da corrida ela divergia em 21 linhas.
    tempo_do_vencedor = {}
    for linha in linhas:
        if num_celula(linha, "posicao") == 1:
            tempo = num_celula(linha, "tempo_total_seg")
            if tempo is not None:
                tempo_do_vencedor[linha.get("corrida_id", "")] = tempo

    def gap(linha):
        tempo = num_celula(linha, "tempo_total_seg")
        referencia = tempo_do_vencedor.get(linha.get("corrida_id", ""))
        if tempo is None or referencia is None:
            return None
        return round(tempo - referencia, 3)

    aplicar_derivacao(
        linhas, registro, "gap_para_vencedor_seg", CHAVE,
        calcular=gap,
        formatar=lambda v: formatar_decimal(v, 3),
        tolerancia=lambda _: 0.05,
    )

    corridas = {linha.get("corrida_id", "") for linha in linhas}
    sem_vencedor = sorted(c for c in corridas if c and c not in tempo_do_vencedor)
    if sem_vencedor:
        registro.notas.append(
            f"`gap_para_vencedor_seg` ficou vazio em {len(sem_vencedor)} corrida(s) "
            "sem linha de `posicao` 1 no bruto: "
            + ", ".join(f"`{c}`" for c in sem_vencedor)
            + ". Sem o tempo do vencedor nao ha referencia para o gap."
        )

    # Velocidade media = distancia total / tempo. Identidade exata: 134/0.
    def velocidade(linha):
        distancia = num_celula(linha, "distancia_km")
        voltas = num_celula(linha, "voltas")
        tempo = num_celula(linha, "tempo_total_seg")
        if None in (distancia, voltas, tempo) or not tempo:
            return None
        return round(distancia * voltas / (tempo / 3600), 2)

    aplicar_derivacao(
        linhas, registro, "velocidade_media_kmh", CHAVE,
        calcular=velocidade,
        formatar=lambda v: formatar_decimal(v, 2),
        tolerancia=lambda _: 0.6,
    )
