from PIL import Image, ImageDraw, ImageFont
import textwrap
import pandas as pd


def gerar_relatorio_conferencia_imagem(df, loja):

    cor_fundo = "white"
    cor_titulo = "black"
    cor_cabecalho = (0, 102, 204)

    # fontes menores
    try:
        font = ImageFont.truetype("arial.ttf", 13)
        font_bold = ImageFont.truetype("arialbd.ttf", 16)
    except:
        font = ImageFont.load_default()
        font_bold = ImageFont.load_default()

    colunas = ["Data", "Código", "Produto", "Qtd", "Valor", "Total"]
    larguras = [110, 110, 420, 70, 110, 110]

    largura = sum(larguras) + 40

    # =========================
    # CALCULAR ALTURA REAL
    # =========================

    altura = 160

    for _, row in df.iterrows():

        texto_produto = str(row["produto"])

        linhas = textwrap.wrap(texto_produto, width=55)

        altura += max(len(linhas), 1) * 18 + 10

    # =========================
    # CRIAR IMAGEM
    # =========================

    img = Image.new("RGB", (largura, altura), cor_fundo)
    draw = ImageDraw.Draw(img)

    y = 20

    # título
    draw.text((20, y), "RELATÓRIO CONFERÊNCIA", font=font_bold, fill=cor_titulo)
    y += 30

    draw.text((20, y), f"Loja: {loja}", font=font, fill=cor_titulo)
    y += 30

    # =========================
    # CABEÇALHO
    # =========================

    x = 20

    for i, col in enumerate(colunas):

        w = larguras[i]

        draw.rectangle([x, y, x + w, y + 30], fill=cor_cabecalho)

        draw.text((x + 5, y + 7), col, font=font_bold, fill="white")

        x += w

    y += 35

    total_geral = 0

    # =========================
    # LINHAS
    # =========================

    for _, row in df.iterrows():

        x = 20

        data = pd.to_datetime(row["data_planilha"]).strftime("%d/%m/%Y")

        valores = [
            data,
            row["codigo"],
            row["produto"],
            row["quantidade"],
            f'R$ {row["valor"]:.2f}',
            f'R$ {row["total"]:.2f}'
        ]

        altura_linha = 0

        for i, v in enumerate(valores):

            largura_coluna = larguras[i]

            texto = str(v)

            limite = int(largura_coluna / 7)

            linhas = textwrap.wrap(texto, width=limite)

            for linha_idx, linha in enumerate(linhas):

                draw.text(
                    (x + 5, y + (linha_idx * 16)),
                    linha,
                    font=font,
                    fill="black"
                )

            altura_linha = max(altura_linha, len(linhas) * 16)

            x += largura_coluna

        y += altura_linha + 8

        total_geral += row["total"]

    # =========================
    # TOTAL
    # =========================

    y += 10

    draw.text(
        (20, y),
        f"Total Geral: R$ {total_geral:.2f}",
        font=font_bold,
        fill="black"
    )

    return img