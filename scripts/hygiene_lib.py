"""Primitivas de higienizacao das bases de `raw_data/`.

Toda normalizacao aqui e dirigida pelo spec de cada base
(`scripts/spec_00N_*.py`), que espelha o dicionario de dados
`data_hygiene/00N_index_*.md`. O dicionario e quem resolve as ambiguidades do
dado bruto: o mesmo texto significa coisas diferentes conforme a escala
declarada na coluna.

    "411,199"  em DECIMAL(10,3)  ->  411.199   (virgula decimal)
    "$2,370"   em DECIMAL(12,2)  ->  2370      (virgula de milhar)
    "4.330"    em INTEGER        ->  4330      (ponto de milhar)
"""

from __future__ import annotations

import csv
import io
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

VAZIOS = {"", "n/a", "na", "nan", "null", "none", "-", "--"}

# Unidades e simbolos que aparecem grudados no numero no dado bruto.
# A ordem importa: alternativas mais longas primeiro.
_UNIDADES = re.compile(
    r"(?i)(?:us\$|usd|r\$|\$|km/h|kmh|km|hp|pessoas|ocorrencias|minutos|min|sec|%|/10)"
)
# Um "s" solto de segundos logo depois do numero ("406.678 s").
_SUFIXO_S = re.compile(r"(?<=\d)\s*s\b", re.IGNORECASE)
# Primeiro token numerico, para valores com rotulo colado ("Dia 1").
_TOKEN_NUM = re.compile(r"-?\d[\d.,]*")


# --------------------------------------------------------------------------- #
# Leitura
# --------------------------------------------------------------------------- #

def ler_bruto(caminho):
    """Le um CSV de `raw_data/` desembrulhando as linhas citadas por fora.

    Parte das linhas do dado bruto vem inteira entre aspas duplas, com as
    aspas internas duplicadas. Um `csv.reader` padrao colapsa a linha toda no
    primeiro campo e devolve as outras colunas vazias -- sem erro nenhum. Aqui
    a aspa externa e removida e as internas voltam a aspa simples antes de
    entregar ao parser.

    Devolve `(colunas, linhas, n_desembrulhadas)`.
    """
    texto = Path(caminho).read_text(encoding="utf-8-sig")
    linhas_texto = texto.splitlines()
    saida, desembrulhadas = [linhas_texto[0]], 0
    for linha in linhas_texto[1:]:
        if not linha.strip():
            continue
        if linha.startswith('"') and linha.endswith('"'):
            saida.append(linha[1:-1].replace('""', '"'))
            desembrulhadas += 1
        else:
            saida.append(linha)
    leitor = csv.DictReader(io.StringIO("\n".join(saida)))
    return list(leitor.fieldnames), list(leitor), desembrulhadas


# --------------------------------------------------------------------------- #
# Parsers
# --------------------------------------------------------------------------- #

def normalizar_espacos(valor):
    """Tira espaco das pontas e colapsa espaco interno repetido."""
    return re.sub(r"\s+", " ", str(valor or "").strip())


def parse_num(valor, decimais, int_digitos=None):
    """Le um numero do bruto usando a escala declarada no dicionario.

    `decimais` e o que desfaz a ambiguidade de virgula/ponto. Sem ele nao ha
    como distinguir "411,199" (411.199 segundos) de "$2,370" (2370 creditos):
    os dois tem 3 digitos depois da virgula.

    `int_digitos` e o maximo de digitos inteiros que a coluna aceita, tirado
    da precisao declarada (`DECIMAL(5,2)` -> 3). Ele descarta a leitura de
    milhar quando ela nao cabe na coluna: em `ocupacao_pct`, "1.000" e a
    fracao 100%, nao mil.
    """
    if valor is None:
        return None
    texto = _SUFIXO_S.sub("", str(valor).strip())
    texto = _UNIDADES.sub("", texto).replace(" ", "")
    if texto.lower() in VAZIOS:
        return None
    # Valor com rotulo colado ("Dia1"): fica so o token numerico.
    if re.search(r"[^\d.,+-]", texto):
        achado = _TOKEN_NUM.search(texto)
        if not achado:
            return None
        texto = achado.group(0)
    negativo = texto.startswith("-")
    texto = texto.lstrip("+-")
    if "," in texto and "." in texto:
        # Os dois separadores presentes: o mais a direita e o decimal.
        decimal = "," if texto.rfind(",") > texto.rfind(".") else "."
        milhar = "." if decimal == "," else ","
        texto = texto.replace(milhar, "").replace(decimal, ".")
    elif "," in texto or "." in texto:
        sep = "," if "," in texto else "."
        cabeca, cauda = texto.rsplit(sep, 1)
        inteiro = cabeca.replace(sep, "")
        # 3 digitos depois do separador e milhar, salvo quando a coluna
        # aceita 3 casas decimais. Parte inteira "0" nunca e milhar:
        # 0.855 e fracao, nao 855. E a leitura de milhar tem de caber na
        # precisao declarada para a coluna.
        eh_milhar = (
            len(cauda) == 3
            and decimais < 3
            and inteiro.lstrip("0") != ""
            and (int_digitos is None or len(inteiro) + 3 <= int_digitos)
        )
        texto = inteiro + cauda if eh_milhar else inteiro + "." + cauda
    try:
        numero = float(texto)
    except ValueError:
        return None
    return -numero if negativo else numero


def parse_data(valor):
    """Normaliza para `YYYY-MM-DD`.

    O bruto tem 4 grafias na mesma coluna: `YYYY-MM-DD`, `YYYY/MM/DD`,
    `DD-MM-YYYY` e `DD/MM/YYYY`. Quando o primeiro componente tem 4 digitos e
    ano-primeiro; senao e dia-primeiro.
    """
    texto = normalizar_espacos(valor)
    if texto.lower() in VAZIOS:
        return None
    partes = re.split(r"[-/.]", texto)
    if len(partes) != 3 or not all(p.isdigit() for p in partes):
        return None
    if len(partes[0]) == 4:
        ano, mes, dia = partes
    else:
        dia, mes, ano = partes
    try:
        return date(int(ano), int(mes), int(dia)).isoformat()
    except ValueError:
        return None


def parse_hora(valor):
    """Normaliza para `HH:MM:SS`. Aceita `HH:MM`, `HH:MM:SS` e `HHhMM`."""
    texto = normalizar_espacos(valor).lower()
    if texto in VAZIOS:
        return None
    partes = [p for p in re.split(r"[:h]", texto) if p != ""]
    if not partes or not all(p.isdigit() for p in partes):
        return None
    partes = (partes + ["0", "0"])[:3]
    hora, minuto, segundo = (int(p) for p in partes)
    if not (0 <= hora < 24 and 0 <= minuto < 60 and 0 <= segundo < 60):
        return None
    return f"{hora:02d}:{minuto:02d}:{segundo:02d}"


def parse_duracao(valor):
    """Le `MM:SS.mmm` ou `HH:MM:SS.mmm` e devolve o total em segundos."""
    texto = normalizar_espacos(valor)
    if texto.lower() in VAZIOS:
        return None
    partes = texto.split(":")
    if not 2 <= len(partes) <= 3:
        return None
    try:
        numeros = [float(p.replace(",", ".")) for p in partes]
    except ValueError:
        return None
    if len(numeros) == 2:
        minutos, segundos = numeros
        return minutos * 60 + segundos
    horas, minutos, segundos = numeros
    return horas * 3600 + minutos * 60 + segundos


_VERDADE = {"sim", "s", "1", "true", "verdadeiro", "yes", "y"}
_FALSIDADE = {"nao", "não", "n", "0", "false", "falso", "no"}


def parse_bool(valor):
    """Normaliza para `TRUE`/`FALSE`, o formato que o dicionario pede."""
    texto = normalizar_espacos(valor).lower()
    if texto in VAZIOS:
        return None
    if texto in _VERDADE:
        return True
    if texto in _FALSIDADE:
        return False
    return None


# --------------------------------------------------------------------------- #
# Categoricos
# --------------------------------------------------------------------------- #

def _pontuacao_caixa(texto):
    """Caixa mista pontua mais: e a grafia bem-formada de um rotulo."""
    if not texto.isupper() and not texto.islower():
        return 2
    return 1 if texto.isupper() else 0


def mapa_canonico(valores):
    """Elege a grafia canonica de cada variante de um categorico.

    Canonica = variante mais frequente do grupo, desempatando pela de caixa
    mista. `str.title()` nao serve como regra geral porque quebraria siglas
    (`AWD` -> `Awd`, `EDM` -> `Edm`, `Elite/VIP` -> `Elite/Vip`); ele entra
    so quando a eleita veio toda minuscula, que nunca e boa grafia de rotulo.

    Devolve `(mapa, grupos)`: o mapa vai de `casefold` para a canonica, e
    `grupos` guarda as variantes fundidas, para o relatorio de QA.
    """
    grupos = defaultdict(Counter)
    for valor in valores:
        limpo = normalizar_espacos(valor)
        if limpo and limpo.lower() not in VAZIOS:
            grupos[limpo.casefold()][limpo] += 1
    mapa = {}
    for chave, variantes in grupos.items():
        eleita = max(
            variantes.items(), key=lambda par: (par[1], _pontuacao_caixa(par[0]))
        )[0]
        if eleita.islower():
            eleita = eleita.title()
        mapa[chave] = eleita
    return mapa, grupos


def aplicar_canonico(valor, mapa):
    limpo = normalizar_espacos(valor)
    if not limpo or limpo.lower() in VAZIOS:
        return None
    return mapa.get(limpo.casefold(), limpo)


def detectar_quase_duplicatas(canonicos):
    """Acha rotulos que podem ser a mesma categoria com grafia diferente.

    Compara ignorando tudo que nao e letra ou numero, o que junta
    `Electro / House` com `Electro House`. Nao funde nada -- so aponta, para
    decisao humana no relatorio de QA.
    """
    grupos = defaultdict(set)
    for valor in canonicos:
        grupos[re.sub(r"[^0-9a-z]", "", valor.casefold())].add(valor)
    return [sorted(v) for v in grupos.values() if len(v) > 1]


# --------------------------------------------------------------------------- #
# Formatacao de saida
# --------------------------------------------------------------------------- #

def formatar_decimal(numero, decimais):
    return "" if numero is None else f"{numero:.{decimais}f}"


def formatar_inteiro(numero):
    return "" if numero is None else str(int(round(numero)))


def formatar_bool(valor):
    return "" if valor is None else ("TRUE" if valor else "FALSE")


def formatar_duracao(segundos):
    """Emite `HH:MM:SS.mmm`, o formato ideal declarado no dicionario."""
    if segundos is None:
        return ""
    total = round(segundos, 3)
    horas, resto = divmod(total, 3600)
    minutos, seg = divmod(resto, 60)
    return f"{int(horas):02d}:{int(minutos):02d}:{seg:06.3f}"


def num_celula(linha, coluna):
    """Le uma celula ja normalizada como numero (ou `None` se vazia)."""
    valor = linha.get(coluna, "")
    if valor == "":
        return None
    try:
        return float(valor)
    except (TypeError, ValueError):
        return None


# --------------------------------------------------------------------------- #
# Registro da limpeza (alimenta o relatorio de QA)
# --------------------------------------------------------------------------- #

class Registro:
    """Acumula o que a limpeza fez, para virar `data_hygiene/00N_qa_*.md`."""

    def __init__(self):
        self.contagens = {}
        self.preenchidos = defaultdict(list)   # coluna -> [ids]
        self.divergencias = defaultdict(list)  # coluna -> [(id, bruto, calculado)]
        self.duplicatas = []                   # [(id, n_copias)]
        self.ids_normalizados = []             # [(bruto, normalizado)]
        self.faltantes = defaultdict(list)     # coluna -> [ids]
        self.dominios = {}                     # coluna -> [canonicos]
        self.fusoes = defaultdict(list)        # coluna -> [(canonica, [variantes])]
        self.ambiguidades = defaultdict(list)  # coluna -> [[variantes]]
        self.notas = []

    def preencher(self, coluna, ident):
        self.preenchidos[coluna].append(ident)

    def divergir(self, coluna, ident, bruto, calculado):
        self.divergencias[coluna].append((ident, bruto, calculado))


def aplicar_derivacao(linhas, registro, coluna, chave, calcular, formatar,
                      tolerancia=None):
    """Preenche `coluna` onde ela esta vazia, usando `calcular(linha)`.

    Nunca sobrescreve valor presente. Quando o que esta no arquivo discorda do
    calculo alem da `tolerancia`, o original e mantido e a linha entra no
    relatorio -- ha divergencia que e regra de negocio, nao erro (em
    `MUS-0052`, `pessoas_na_area` foi capado na capacidade da area).

    `tolerancia` recebe o valor calculado e devolve o desvio aceitavel;
    `None` exige igualdade do texto formatado.
    """
    for linha in linhas:
        calculado = calcular(linha)
        if calculado is None:
            continue
        texto = formatar(calculado)
        if texto == "":
            continue
        atual = linha.get(coluna, "")
        if atual == "":
            linha[coluna] = texto
            registro.preencher(coluna, linha[chave])
            continue
        if tolerancia is None:
            if atual != texto:
                registro.divergir(coluna, linha[chave], atual, texto)
            continue
        try:
            atual_num = float(atual)
        except ValueError:
            if atual != texto:
                registro.divergir(coluna, linha[chave], atual, texto)
            continue
        if abs(atual_num - float(calculado)) > tolerancia(float(calculado)):
            registro.divergir(coluna, linha[chave], atual, texto)


def _tabela(cabecalho, linhas):
    if not linhas:
        return "_Nenhum._\n"
    saida = ["| " + " | ".join(cabecalho) + " |",
             "|" + "|".join("---" for _ in cabecalho) + "|"]
    saida += ["| " + " | ".join(str(c) for c in linha) + " |" for linha in linhas]
    return "\n".join(saida) + "\n"


def escrever_relatorio(caminho, titulo, registro, colunas):
    """Gera o `00N_qa_*.md` da base."""
    p = []
    p.append(f"# {titulo}\n")
    p.append("Relatorio gerado por `scripts/clean.py`. Nao editar a mao -- ele e\n"
             "reescrito a cada reprocessamento.\n")

    p.append("\n## Resumo\n")
    p.append(_tabela(["Etapa", "Linhas"],
                     list(registro.contagens.items())))

    p.append("\n## Preenchimentos por derivacao\n")
    p.append("Valores que estavam vazios ou `N/A` e foram calculados a partir de\n"
             "outras colunas da propria linha.\n\n")
    p.append(_tabela(
        ["Coluna", "Preenchidos", "Ids"],
        [(col, len(ids), ", ".join(f"`{i}`" for i in ids[:12])
          + (f" ... (+{len(ids) - 12})" if len(ids) > 12 else ""))
         for col, ids in sorted(registro.preenchidos.items())]))

    p.append("\n## Divergencias mantidas\n")
    p.append("O valor original foi **preservado**; a derivacao apenas discorda dele.\n"
             "Sinalizado para inspecao, nao corrigido.\n\n")
    linhas_div = []
    for col, itens in sorted(registro.divergencias.items()):
        for ident, bruto, calculado in itens:
            linhas_div.append((col, f"`{ident}`", bruto, calculado))
    p.append(_tabela(["Coluna", "Id", "No arquivo", "Calculado"], linhas_div))

    p.append("\n## Duplicatas removidas\n")
    p.append("Linhas com o mesmo id. Verificado que as copias sao identicas em\n"
             "todas as colunas -- manter a primeira ocorrencia nao perde dado.\n\n")
    p.append(_tabela(["Id", "Copias no bruto"],
                     [(f"`{i}`", n) for i, n in registro.duplicatas]))

    p.append("\n## Ids normalizados\n")
    p.append("Espaco nas pontas e caixa inconsistente na chave primaria.\n\n")
    p.append(_tabela(["No arquivo", "Normalizado"],
                     [(f"`{b}`", f"`{n}`") for b, n in registro.ids_normalizados]))

    p.append("\n## Faltantes remanescentes\n")
    p.append("Vazios que nenhuma regra de derivacao alcanca.\n\n")
    p.append(_tabela(
        ["Coluna", "Vazios", "Ids"],
        [(col, len(ids), ", ".join(f"`{i}`" for i in ids[:12])
          + (f" ... (+{len(ids) - 12})" if len(ids) > 12 else ""))
         for col, ids in sorted(registro.faltantes.items())]))

    p.append("\n## Dominio dos categoricos\n")
    for col in colunas:
        if col in registro.dominios:
            vals = registro.dominios[col]
            p.append(f"- `{col}` ({len(vals)}): "
                     + ", ".join(f"`{v}`" for v in vals[:25])
                     + (" ..." if len(vals) > 25 else "") + "\n")

    p.append("\n## Variantes fundidas\n")
    p.append("Grafias que diferiam so em caixa ou espaco e foram unificadas.\n\n")
    linhas_fus = []
    for col, itens in sorted(registro.fusoes.items()):
        for canonica, variantes in itens:
            linhas_fus.append((col, f"`{canonica}`",
                               ", ".join(f"`{v}`" for v in variantes)))
    p.append(_tabela(["Coluna", "Canonica", "Variantes no bruto"], linhas_fus))

    if registro.ambiguidades:
        p.append("\n## Ambiguidades para decisao humana\n")
        p.append("Rotulos que **podem** ser a mesma categoria com grafia diferente.\n"
                 "A limpeza nao os une -- decida e, se for o caso, ajuste o bruto.\n\n")
        linhas_amb = []
        for col, grupos in sorted(registro.ambiguidades.items()):
            for grupo in grupos:
                linhas_amb.append((col, " vs ".join(f"`{v}`" for v in grupo)))
        p.append(_tabela(["Coluna", "Candidatos"], linhas_amb))

    if registro.notas:
        p.append("\n## Notas\n")
        p += [f"- {n}\n" for n in registro.notas]

    Path(caminho).write_text("".join(p), encoding="utf-8", newline="\n")


def escrever_csv(caminho, colunas, linhas):
    """Escreve o CSV limpo: UTF-8 sem BOM, LF, virgula, aspas so onde precisa."""
    with open(caminho, "w", encoding="utf-8", newline="") as fh:
        escritor = csv.DictWriter(fh, fieldnames=colunas, lineterminator="\n",
                                  quoting=csv.QUOTE_MINIMAL)
        escritor.writeheader()
        escritor.writerows(linhas)
