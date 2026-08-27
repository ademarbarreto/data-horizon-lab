"""Gera a dashboard do evento musical 2012 a partir da base limpa.

    python scripts/build_dashboard_002.py

Le `data_hygiene/002_clean_evento_2012.csv`, projeta as 180 apresentacoes num
bloco JSON e escreve `dashboards/002_dash_evento_2012.html`.

Guard rail do projeto: **nenhum numero e escrito a mao no template.** A pagina
recebe as linhas da base e agrega tudo em JavaScript, entao todo valor na tela
tem origem rastreavel numa linha do CSV. A dashboard e gerada -- editar o HTML
de saida a mao e perda garantida no proximo build.

As cores de pulseira e a ordem dos palcos saem do dado; a linguagem visual sai
de `dashboards/design_system/design_system.html`.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hygiene_lib import RAIZ  # noqa: E402

BASE = "data_hygiene/002_clean_evento_2012.csv"
QA = "data_hygiene/002_qa_evento_2012.md"
SAIDA = "dashboards/002_dash_evento_2012.html"
TEMPLATE = Path(__file__).resolve().parent / "dash_002_template.html"

# Ordem de progressao das pulseiras (nivel 1 a 7), do proprio dado.
ORDEM_CORES = ["Yellow", "Green", "Blue", "Pink", "Orange", "Purple", "Gold"]


def _num(linha, coluna):
    valor = linha[coluna]
    return float(valor) if valor != "" else 0.0


def _int(linha, coluna):
    return int(round(_num(linha, coluna)))


def ler_apresentacoes():
    """Projeta cada linha da base nos campos que a dashboard usa."""
    with open(RAIZ / BASE, encoding="utf-8", newline="") as fh:
        linhas = list(csv.DictReader(fh))
    saida = []
    for linha in linhas:
        saida.append({
            "id": linha["registro_id"],
            "data": linha["data_evento"],
            "dia": _int(linha, "dia_festival"),
            "regiao": linha["regiao"],
            "local": linha["local_evento"],
            "palco": linha["area_palco"],
            "radio": linha["radio_estacao"],
            "artista": linha["artista"],
            "faixa": linha["faixa_musical"],
            "estilo": linha["estilo_musical"],
            "cor": linha["pulseira_cor"],
            "nivel": _int(linha, "nivel_pulseira"),
            "categoria": linha["categoria_pulseira"],
            "capacidade": _int(linha, "capacidade_area"),
            "ingressos": _int(linha, "ingressos_emitidos"),
            "checkins": _int(linha, "checkins"),
            "pessoas": _int(linha, "pessoas_na_area"),
            "no_show": _int(linha, "no_show"),
            "ocupacao": _num(linha, "ocupacao_pct"),
            "preco": _num(linha, "preco_medio_ingresso_usd"),
            "rec_ing": _num(linha, "receita_ingressos_usd"),
            "rec_ab": _num(linha, "receita_alimentos_bebidas_usd"),
            "rec_merch": _num(linha, "receita_merch_usd"),
            "nota": _num(linha, "avaliacao_publico_0a10"),
            "incidentes": _int(linha, "incidentes_reportados"),
        })
    return saida


def ler_derivados():
    """Colunas cujo valor foi preenchido por calculo na higienizacao.

    Sai da secao "Preenchimentos por derivacao" do relatorio de QA. Vai para o
    rodape de procedencia: e o que separa dado lido de dado calculado.
    """
    texto = (RAIZ / QA).read_text(encoding="utf-8")
    bloco = texto.split("## Preenchimentos por derivacao")[1].split("\n## ")[0]
    derivados = {}
    for linha in bloco.splitlines():
        celulas = [c.strip() for c in linha.split("|")]
        if len(celulas) > 3 and celulas[2].isdigit():
            derivados[celulas[1]] = int(celulas[2])
    return dict(sorted(derivados.items(), key=lambda par: -par[1]))


def montar_payload(apresentacoes):
    por_palco = Counter()
    for a in apresentacoes:
        por_palco[a["palco"]] += a["ingressos"]
    cores_presentes = {a["cor"] for a in apresentacoes}
    return {
        # Palcos na ordem de ingressos do evento inteiro, para o ranking nao
        # reordenar (nem sumir palco) quando um filtro de cor esta ativo.
        "palcos": [p for p, _ in por_palco.most_common()],
        "cores": [c for c in ORDEM_CORES if c in cores_presentes],
        "apresentacoes": apresentacoes,
        "procedencia": {
            "base": BASE,
            "registros": len(apresentacoes),
            "script": "scripts/build_dashboard_002.py",
            "qa": QA,
            "gerado_em": datetime.now().strftime("%d/%m/%Y"),
            "derivados": ler_derivados(),
        },
    }


def main():
    apresentacoes = ler_apresentacoes()
    payload = montar_payload(apresentacoes)
    template = TEMPLATE.read_text(encoding="utf-8")
    if "__DADOS__" not in template:
        raise SystemExit(f"{TEMPLATE.name}: falta o marcador __DADOS__")
    dados = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    # `</script>` dentro do JSON fecharia a tag antes da hora.
    dados = dados.replace("</", "<\\/")
    html = template.replace("__DADOS__", dados)

    destino = RAIZ / SAIDA
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(html, encoding="utf-8", newline="\n")

    # Confere que nenhum numero de dado vazou para o markup escrito a mao. So
    # o corpo do HTML e olhado: CSS (rgba, cubic-bezier) e JS (1e6, 100) tem
    # numero legitimo que nao e dado.
    corpo = html.split("</style>", 1)[1].split('<script id="dados"', 1)[0]
    suspeitos = re.findall(r"\b\d{4,}\b|\b\d+[.,]\d+\b", corpo)
    print(f"{SAIDA}")
    print(f"  {len(apresentacoes)} apresentacoes projetadas de {BASE}")
    print(f"  {len(payload['palcos'])} palcos, {len(payload['cores'])} cores de pulseira")
    print(f"  payload: {len(dados):,} bytes | pagina: {len(html):,} bytes")
    print(f"  derivados na higienizacao: {payload['procedencia']['derivados']}")
    if suspeitos:
        print(f"  ATENCAO numeros no markup fora do JSON: {suspeitos[:8]}")
    else:
        print("  markup sem numero de dado escrito a mao: ok")


if __name__ == "__main__":
    main()
