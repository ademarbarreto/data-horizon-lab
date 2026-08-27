"""Higieniza as bases de `raw_data/` e escreve a versao limpa em `data_hygiene/`.

    python scripts/clean.py          # todas as bases
    python scripts/clean.py 001      # so a base 001
    python scripts/clean.py 001 002

Para cada base gera dois arquivos em `data_hygiene/`:

    00N_clean_<alias>_<ano>.csv   dado limpo, mesmas colunas do bruto
    00N_qa_<alias>_<ano>.md       o que a limpeza fez, linha por linha

O dado bruto em `raw_data/` nunca e alterado: ele e a fonte da verdade e a
materia-prima do exercicio de higienizacao.
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import hygiene_lib as hl  # noqa: E402
import spec_001_corridas  # noqa: E402
import spec_002_evento  # noqa: E402

BASES = {
    spec_001_corridas.ID: spec_001_corridas,
    spec_002_evento.ID: spec_002_evento,
}

LINHA_RESUMO = "TOTAL_GERAL"


def _normalizar_celula(valor, regra, mapa_categorico):
    """Aplica ao valor bruto a regra declarada para a coluna no dicionario."""
    tipo = regra["tipo"]
    if tipo == "id":
        return hl.normalizar_espacos(valor).upper()
    if tipo == "url":
        return hl.normalizar_espacos(valor)
    if tipo == "categoria":
        return hl.aplicar_canonico(valor, mapa_categorico) or ""
    if tipo == "data":
        return hl.parse_data(valor) or ""
    if tipo == "hora":
        return hl.parse_hora(valor) or ""
    if tipo == "duracao":
        return hl.formatar_duracao(hl.parse_duracao(valor))
    if tipo == "booleano":
        return hl.formatar_bool(hl.parse_bool(valor))
    if tipo == "inteiro":
        return hl.formatar_inteiro(hl.parse_num(valor, 0))
    if tipo == "decimal":
        decimais = regra["decimais"]
        # Digitos inteiros que a coluna aceita: DECIMAL(5,2) -> 3.
        precisao = regra.get("precisao")
        int_digitos = None if precisao is None else precisao - decimais
        numero = hl.parse_num(valor, decimais, int_digitos)
        # Coluna que mistura percentual e fracao na mesma escala: 0.855 e 85.5%.
        if numero is not None and regra.get("fracao_pct") and 0 < numero <= 1.5:
            numero *= 100
        return hl.formatar_decimal(numero, decimais)
    raise ValueError(f"tipo desconhecido no spec: {tipo!r}")


def _deduplicar(linhas, chave, registro):
    """Remove linhas repetidas pelo id, mantendo a primeira ocorrencia."""
    contagem = Counter(linha[chave] for linha in linhas)
    primeira, saida = {}, []
    for linha in linhas:
        ident = linha[chave]
        if ident in primeira:
            if primeira[ident] != linha:
                # As copias do bruto sao identicas; se um dia deixarem de ser,
                # descartar em silencio perderia dado.
                registro.notas.append(
                    f"ATENCAO: `{ident}` aparece mais de uma vez com conteudo "
                    "DIFERENTE. A primeira ocorrencia foi mantida -- conferir "
                    "no arquivo bruto."
                )
            continue
        primeira[ident] = linha
        saida.append(linha)
    registro.duplicatas = [(i, n) for i, n in sorted(contagem.items()) if n > 1]
    return saida


def limpar(spec):
    """Roda o pipeline completo de uma base e escreve os dois arquivos."""
    registro = hl.Registro()
    colunas_esperadas = list(spec.COLUNAS)

    colunas, brutas, desembrulhadas = hl.ler_bruto(hl.RAIZ / spec.ENTRADA)
    if colunas != colunas_esperadas:
        faltando = set(colunas_esperadas) - set(colunas)
        sobrando = set(colunas) - set(colunas_esperadas)
        raise SystemExit(
            f"{spec.ENTRADA}: header nao casa com o spec.\n"
            f"  faltando no arquivo: {sorted(faltando)}\n"
            f"  fora do spec: {sorted(sobrando)}"
        )

    # A linha de resumo do proprio arquivo pede para ser filtrada na limpeza.
    resumo = [l for l in brutas
              if l[spec.CHAVE].strip().upper() == LINHA_RESUMO]
    brutas = [l for l in brutas
              if l[spec.CHAVE].strip().upper() != LINHA_RESUMO]

    # Grafia canonica dos categoricos: precisa da coluna inteira para eleger a
    # variante mais frequente, entao roda antes de normalizar celula a celula.
    mapas = {}
    for coluna, regra in spec.COLUNAS.items():
        if regra["tipo"] == "categoria":
            mapa, grupos = hl.mapa_canonico(l[coluna] for l in brutas)
            mapas[coluna] = mapa
            for chave, variantes in sorted(grupos.items()):
                if len(variantes) > 1:
                    registro.fusoes[coluna].append(
                        (mapa[chave], sorted(variantes))
                    )

    limpas = []
    for bruta in brutas:
        limpa = {}
        for coluna, regra in spec.COLUNAS.items():
            limpa[coluna] = _normalizar_celula(
                bruta[coluna], regra, mapas.get(coluna, {})
            )
        original = hl.normalizar_espacos(bruta[spec.CHAVE])
        if original != limpa[spec.CHAVE]:
            registro.ids_normalizados.append((bruta[spec.CHAVE],
                                              limpa[spec.CHAVE]))
        limpas.append(limpa)

    limpas = _deduplicar(limpas, spec.CHAVE, registro)
    spec.derivar(limpas, registro)

    for coluna in colunas_esperadas:
        vazios = [l[spec.CHAVE] for l in limpas if l[coluna] == ""]
        if vazios:
            registro.faltantes[coluna] = vazios
    for coluna, regra in spec.COLUNAS.items():
        if regra["tipo"] == "categoria":
            presentes = sorted({l[coluna] for l in limpas if l[coluna]})
            registro.dominios[coluna] = presentes
            quase = hl.detectar_quase_duplicatas(presentes)
            if quase:
                registro.ambiguidades[coluna] = quase

    registro.contagens = {
        "Linhas de dado no arquivo bruto": len(brutas) + len(resumo),
        "Citadas por fora (desembrulhadas)": desembrulhadas,
        f"Linha `{LINHA_RESUMO}` descartada": len(resumo),
        "Duplicatas removidas": sum(n - 1 for _, n in registro.duplicatas),
        "Ids normalizados": len(registro.ids_normalizados),
        "Registros na base limpa": len(limpas),
    }

    hl.escrever_csv(hl.RAIZ / spec.SAIDA_CSV, colunas_esperadas, limpas)
    hl.escrever_relatorio(hl.RAIZ / spec.SAIDA_QA, spec.TITULO, registro,
                          colunas_esperadas)

    preenchidos = sum(len(v) for v in registro.preenchidos.values())
    divergentes = sum(len(v) for v in registro.divergencias.values())
    print(f"[{spec.ID}] {spec.ENTRADA}")
    print(f"      -> {spec.SAIDA_CSV}  ({len(limpas)} registros, "
          f"{len(colunas_esperadas)} colunas)")
    print(f"      -> {spec.SAIDA_QA}")
    print(f"      {desembrulhadas} linhas desembrulhadas, "
          f"{sum(n - 1 for _, n in registro.duplicatas)} duplicatas removidas, "
          f"{preenchidos} valores preenchidos, "
          f"{divergentes} divergencias sinalizadas")
    return registro


def main(argv):
    pedidos = argv or ["all"]
    if pedidos == ["all"]:
        pedidos = sorted(BASES)
    desconhecidos = [p for p in pedidos if p not in BASES]
    if desconhecidos:
        raise SystemExit(
            f"base desconhecida: {', '.join(desconhecidos)}. "
            f"disponiveis: {', '.join(sorted(BASES))}, all"
        )
    for pedido in pedidos:
        limpar(BASES[pedido])


if __name__ == "__main__":
    main(sys.argv[1:])
