import pandas as pd
import re
from datetime import datetime

MAPA_LOJAS = {
    "507": "V.V. 2021",
    "483": "Q. BLV",
    "464": "L. Botafogo",
    "252": "L. Niterói",
    "491": "Q. Tijuca",
    "486": "F. VIX - 410",
    "381": "V.V. 1031",
    "38":  "MDI",
    "443": "Q. SPC",
    "320": "V.V. 1071",
    "487": "Q. Niterói",
    "334": "L. MA",
    "285": "MDG",
    "416": "L. VIX - 416",
    "513": "Rio Design",
    "529": "L. SPC",
}

def processar_planilha_conferencia(arquivo):

    xls = pd.ExcelFile(arquivo)
    dados = []

    for nome_aba in xls.sheet_names:

        df = pd.read_excel(xls, sheet_name=nome_aba)

        for _, row in df.iterrows():

            if pd.isna(row.iloc[0]):
                continue

            loja_original = str(nome_aba)
            codigo_loja = re.split(r"\s*[-|]\s*", loja_original)[0].strip()
            nome_loja = MAPA_LOJAS.get(codigo_loja, loja_original)

            produto_completo = str(row.iloc[0])

            # separa código e nome do produto
            if "-" in produto_completo:
                codigo = produto_completo.split("-")[0].strip()
                produto = produto_completo.split("-", 1)[1].strip()
            else:
                codigo = ""
                produto = produto_completo
            status = str(row.iloc[2]) if not pd.isna(row.iloc[2]) else ""
            quantidade = int(float(row.iloc[1])) if not pd.isna(row.iloc[1]) else 0
            valor = float(row.iloc[5]) if not pd.isna(row.iloc[5]) else 0
            total = float(row.iloc[6]) if not pd.isna(row.iloc[6]) else 0
            # pegar data da planilha
            data = row.iloc[3]

            if isinstance(data, datetime):
                data_planilha = data.strftime("%Y-%m-%d")
            else:
                try:
                    data_obj = pd.to_datetime(data)
                    data_planilha = data_obj.strftime("%Y-%m-%d")
                except:
                    data_planilha = None

            dados.append({
                "loja": nome_loja,
                "codigo": codigo,
                "produto": produto,
                "quantidade": quantidade,
                "status": status,
                "valor": valor,
                "total": total,
                "data_planilha": data_planilha,
                "data_planilha": data_planilha
            })

    return pd.DataFrame(dados)

BLOCOS = {
    "VIX/SERRA": ["L. VIX", "F.VIX", "MDI", "MDG", "L. MA"],
    "VILA VELHA": ["V.V. 1031", "V.V. 1071", "V.V. 2021", "L. SPC", "Q. SPC", "Q. BLV"],
    "NITERÓI/RJ": ["L. NITERÓI", "Q. NITERÓI", "Q. TIJUCA", "RIO DESIGN", "L. BOTAFOGO"]
}

ERROS = [
    "Não encontrado",
    "Encomenda",
    "Pré-ordem",
    "Aguardando Cliente"
]

TIPOS = [
    "R$ 20,00",
    "R$ 25,00",
    "50%",
    "Garantia"
]