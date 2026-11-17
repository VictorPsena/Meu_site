from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from PIL import Image, ImageOps, ImageTk, UnidentifiedImageError


LARGURA = 1500
ALTURA = 800
ESCALA = 50
CORES = ("#1464c0", "#c0392b", "#16834b", "#843ab5", "#9c6500")
ALGARISMOS = 6  # Precisão apenas do texto.

def separar_grupos(pontos):
    if not pontos:
        return []

    grupos = [[pontos[0]]]
    direcao = 0  # 0: indefinida; 1: direita; -1: esquerda.

    for ponto in pontos[1:]:
        anterior = grupos[-1][-1]
        dx = ponto[0] - anterior[0]

        if dx == 0:
            # Não colocamos dois pontos de mesmo x no mesmo grupo.
            grupos.append([ponto])
            direcao = 0
            continue

        nova_direcao = 1 if dx > 0 else -1

        if direcao == 0 or nova_direcao == direcao:
            grupos[-1].append(ponto)
        else:
            # Compartilhamos o ponto de virada entre os dois grupos.
            grupos.append([anterior, ponto])

        direcao = nova_direcao

    return grupos


def coefLagrange(pontos, x):
    """Avalia o polinômio na forma de Lagrange; x pode ser escalar ou vetor."""
    if not pontos:
        raise ValueError("Informe ao menos um ponto.")
    if len({xi for xi, _ in pontos}) != len(pontos):
        raise ValueError("Os valores de x devem ser distintos dentro do grupo.")
    x = np.asarray(x, dtype=float)
    soma = np.zeros_like(x)
    for k, (x_k, y_k) in enumerate(pontos):
        L_k = np.ones_like(x)
        for j, (x_j, _) in enumerate(pontos):
            if j != k:
                L_k *= (x - x_j) / (x_k - x_j)
        soma += y_k * L_k
    return soma.item() if soma.ndim == 0 else soma


def amostrar_lagrange(grupo):
    """Inclui todos os nós no desenho, inclusive em grupos traçados para a esquerda."""
    nos = sorted(x for x, _ in grupo)
    grade = np.unique(np.concatenate([
        np.linspace(a, b, max(30, int((b - a) * ESCALA) + 1))
        for a, b in zip(nos, nos[1:])
    ]))
    with np.errstate(over="ignore", invalid="ignore"):
        valores = coefLagrange(grupo, grade)
    return zip(grade, valores)


def formatar_lagrange(numero, grupo):
    """Exibe o mesmo produto usado em coefLagrange, termo por termo."""
    if len(grupo) == 1:
        x, y = grupo[0]
        return f"P{numero}(x) = {formatar_numero(y)} (um único nó: x = {formatar_numero(x)})"
    nos = [x for x, _ in grupo]
    linhas = [f"P{numero}(x) = Σ yₖ·Lₖ(x),   {formatar_numero(min(nos))} ≤ x ≤ {formatar_numero(max(nos))}"]
    termos = []
    for k, (xk, yk) in enumerate(grupo):
        sinal = ("−" if yk < 0 else "") if not termos else (" − " if yk < 0 else " + ")
        termos.append(f"{sinal}{formatar_numero(abs(yk))}·L{k}(x)")
        fatores = []
        for j, (xj, _) in enumerate(grupo):
            if j == k:
                continue
            base = f"(x {'+' if xj < 0 else '−'} {formatar_numero(abs(xj))})"
            fatores.append(f"[{base}/({formatar_numero(xk-xj)})]")
        linhas.append(f"L{k}(x) = " + " · ".join(fatores))
    linhas.insert(1, f"P{numero}(x) = " + "".join(termos))
    return "\n".join(linhas)


def linhas_visiveis(amostras):
    """Recorta as linhas ao intervalo vertical da tela sem achatar o gráfico."""
    limite = ALTURA / (2 * ESCALA)
    linha = []
    anterior = None
    for x, y in amostras:
        if not np.isfinite(y):
            if linha:
                yield linha
            anterior, linha = None, []
            continue
        if anterior is not None:
            a, b = anterior
            if max(y, b) < -limite or min(y, b) > limite:
                if linha:
                    yield linha
                linha = []
            else:
                def recortar(x1, y1, x2, y2):
                    yc = max(-limite, min(limite, y1))
                    if yc != y1:
                        x1 += (x2 - x1) * ((yc - y1) / (y2 - y1))
                    return (LARGURA / 2 + x1 * ESCALA, ALTURA / 2 - yc * ESCALA)
                inicio = recortar(a, b, x, y)
                fim = recortar(x, y, a, b)
                if linha and tuple(linha[-2:]) != inicio:
                    yield linha
                    linha = []
                if not linha:
                    linha.extend(inicio)
                linha.extend(fim)
        anterior = x, y
    if linha:
        yield linha


def texto_pontos(pontos):
    """TXT tabulado, com um bloco por grupo na ordem dos cliques."""
    linhas = ["# Pontos do plano (x, y), agrupados na ordem dos cliques.",
              "# Um ponto de virada aparece nos dois grupos que se encontram nele."]
    for numero, grupo in enumerate(separar_grupos(pontos), 1):
        linhas.extend(["", f"# Grupo {numero}", "x\ty"])
        linhas.extend(f"{x}\t{y}" for x, y in grupo)
    return "\n".join(linhas) + "\n"


def estimar_derivadas(grupo):
    """Estima dy/dx nos extremos de menor e maior x de um grupo.

    Usa interpolação quadrática local com espaçamento não necessariamente igual.
    As estimativas não são derivadas exatas de uma função desconhecida.
    """
    if len(grupo) < 2:
        raise ValueError("São necessários pelo menos dois pontos.")
    dados = np.asarray(sorted(grupo, key=lambda ponto: ponto[0]), dtype=float)
    if dados.ndim != 2 or dados.shape[1] != 2 or not np.isfinite(dados).all():
        raise ValueError("Use pontos (x, y) com coordenadas finitas.")
    x, y = dados[:, 0], dados[:, 1]
    h = np.diff(x)
    if np.any(h <= 0):
        raise ValueError("Cada grupo deve ter valores de x distintos.")

    inclinacoes = np.diff(y) / h
    if len(grupo) == 2:
        return float(inclinacoes[0]), float(inclinacoes[0])

    esquerda = (inclinacoes[0]
                - h[0] * (inclinacoes[1] - inclinacoes[0]) / (h[0] + h[1]))
    direita = (inclinacoes[-1]
               + h[-1] * (inclinacoes[-1] - inclinacoes[-2]) / (h[-2] + h[-1]))
    return float(esquerda), float(direita)


def calcular_spline(grupo, derivadas=None):
    """Retorna x, a, b, c, d, com um coeficiente de cada tipo por intervalo.

    S_i(z) = a[i] + b[i]*(z-x[i]) + c[i]*(z-x[i])**2 + d[i]*(z-x[i])**3.

    derivadas=None: spline natural, com segunda derivada zero nos extremos.
    derivadas=(esquerda, direita): spline fixado, como no ex_spline.py.
    As derivadas são dy/dx nos extremos de menor e maior x, respectivamente.
    """
    if len(grupo) < 2:
        raise ValueError("São necessários pelo menos dois pontos.")

    # Um grupo desenhado para a esquerda é invertido para fazer o cálculo.
    dados = np.asarray(sorted(grupo, key=lambda ponto: ponto[0]), dtype=float)
    if dados.ndim != 2 or dados.shape[1] != 2 or not np.isfinite(dados).all():
        raise ValueError("Use pontos (x, y) com coordenadas finitas.")
    x, y = dados[:, 0], dados[:, 1]
    h = np.diff(x)
    if np.any(h <= 0):
        raise ValueError("Cada grupo deve ter valores de x distintos.")

    n = len(x)
    A = np.eye(n)
    B = np.zeros(n)

    # Equações interiores: continuidade de S' e S'' nas junções.
    for i in range(1, n - 1):
        A[i, i - 1] = h[i - 1]
        A[i, i] = 2 * (h[i - 1] + h[i])
        A[i, i + 1] = h[i]
        B[i] = 3 * ((y[i + 1] - y[i]) / h[i]
                    - (y[i] - y[i - 1]) / h[i - 1])

    if derivadas is not None:
        if len(derivadas) != 2 or not np.isfinite(derivadas).all():
            raise ValueError("Informe duas derivadas finitas: esquerda e direita.")
        # Estas são as condições de spline fixado do seu código original.
        A[0, 0], A[0, 1] = 2 * h[0], h[0]
        A[-1, -2], A[-1, -1] = h[-1], 2 * h[-1]
        B[0] = 3 * (y[1] - y[0]) / h[0] - 3 * derivadas[0]
        B[-1] = 3 * derivadas[1] - 3 * (y[-1] - y[-2]) / h[-1]
    # Sem derivadas fornecidas, as linhas dos extremos são c[0]=c[-1]=0.

    # Resolve A @ c = B diretamente, sem calcular a inversa de A.
    c = np.linalg.solve(A, B)
    a = y[:-1].copy()
    b = np.diff(y) / h - (h / 3) * (2 * c[:-1] + c[1:])
    d = np.diff(c) / (3 * h)
    return x, a, b, c[:-1], d


def amostrar_spline(coeficientes):
    """Avalia cada polinômio em vários pontos para desenhá-lo na tela."""
    x, a, b, c, d = coeficientes
    amostras = []

    for i in range(len(a)):
        quantidade = max(30, int((x[i + 1] - x[i]) * ESCALA) + 1)
        valores_x = np.linspace(x[i], x[i + 1], quantidade)
        deslocamento = valores_x - x[i]
        valores_y = (a[i] + b[i] * deslocamento
                     + c[i] * deslocamento**2 + d[i] * deslocamento**3)
        amostras.extend(zip(valores_x, valores_y))

    return amostras


def formatar_numero(valor):
    """Evita -0 e preserva números pequenos usando notação científica."""
    return format(0.0 if valor == 0 else valor, f".{ALGARISMOS}g")


def formatar_polinomio(xi, a, b, c, d):
    """Substitui os quatro coeficientes e xi pelos valores calculados."""
    sinal_x = "+" if xi < 0 else "-"
    base = f"(x {sinal_x} {formatar_numero(abs(xi))})"
    expressao = formatar_numero(a)
    for coeficiente, potencia in ((b, ""), (c, "²"), (d, "³")):
        sinal = "-" if coeficiente < 0 else "+"
        expressao += f" {sinal} {formatar_numero(abs(coeficiente))}·{base}{potencia}"
    return expressao


def formatar_spline(numero_grupo, coeficientes):
    """Monta a definição por partes, com uma linha por intervalo."""
    x, a, b, c, d = coeficientes
    indice = str(numero_grupo).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
    nome = f"S{indice}(x) = "
    quantidade = len(a)
    linhas = []
    for i in range(quantidade):
        polinomio = formatar_polinomio(x[i], a[i], b[i], c[i], d[i])
        # Cada nó interior pertence ao intervalo seguinte; o último é fechado.
        limite_direito = "≤" if i == quantidade - 1 else "<"
        intervalo = (f"{formatar_numero(x[i])} ≤ x {limite_direito} "
                     f"{formatar_numero(x[i + 1])}")
        if quantidade == 1:
            linhas.append(f"{nome}{polinomio},   {intervalo}")
        else:
            chave = "⎧" if i == 0 else ("⎩" if i == quantidade - 1 else "⎪")
            prefixo = nome if i == (quantidade - 1) // 2 else " " * len(nome)
            linhas.append(f"{prefixo}{chave} {polinomio},   {intervalo}")
    return "\n".join(linhas)


def preparar_imagem(caminho):
    """Carrega o primeiro quadro, corrige a orientação e ajusta à área de desenho.

    A imagem mantém sua proporção e é centralizada pelo Canvas. Apenas a cópia
    usada na tela é redimensionada; o arquivo original não é alterado.
    """
    with Image.open(caminho) as original:
        imagem = ImageOps.exif_transpose(original).convert("RGBA")
        return ImageOps.contain(
            imagem, (LARGURA, ALTURA), method=Image.Resampling.LANCZOS,
        )


def main():
    pontos = []
    grupos_calculados = []  # Triplas (pontos, coeficientes, derivadas estimadas).
    janela_splines = None
    texto_splines = None
    imagem_fundo = None  # Referência persistente para evitar descarte pelo Tkinter.
    janela = tk.Tk()
    janela.title("Splines — desenhar sobre uma imagem")
    janela.resizable(False, False)
    metodo = tk.StringVar(master=janela, value="Spline fixado")
    mostrar_pontos = tk.BooleanVar(master=janela, value=True)
    mostrar_curvas = tk.BooleanVar(master=janela, value=True)
    mostrar_coordenadas = tk.BooleanVar(master=janela, value=True)

    barra = tk.Frame(janela, bg="white")
    barra.pack(fill="x")
    opcoes = tk.Frame(janela, bg="white")
    opcoes.pack(fill="x")

    tela = tk.Canvas(
        janela, width=LARGURA, height=ALTURA,
        bg="white", highlightthickness=0,
    )
    tela.pack()

    status = tk.Label(
        janela, text="Adicione uma imagem ou clique no fundo branco. Esc: limpar pontos.",
        bg="white", anchor="w", padx=10,
    )
    status.pack(fill="x")

    def atualizar_formulas():
        if janela_splines is None or not janela_splines.winfo_exists():
            return
        posicao = texto_splines.yview()[0]
        texto_splines.config(state="normal")
        texto_splines.delete("1.0", "end")
        if not grupos_calculados:
            texto_splines.insert("end", "Adicione pontos na tela para formar os interpoladores.")

        for i, (grupo, coeficientes, derivadas) in enumerate(grupos_calculados):
            cor = CORES[i % len(CORES)]
            etiqueta = f"grupo_{i}"
            texto_splines.tag_configure(etiqueta, foreground=cor)
            texto_splines.insert("end", f"{metodo.get()} do grupo {i + 1}\n", etiqueta)
            if metodo.get() == "Lagrange":
                texto_splines.insert("end", formatar_lagrange(i + 1, grupo) + "\n\n", etiqueta)
            elif coeficientes is None:
                x, y = grupo[0]
                texto_splines.insert(
                    "end", f"Apenas um ponto: ({formatar_numero(x)}, {formatar_numero(y)}). "
                    "São necessários pelo menos dois pontos neste grupo.\n\n", etiqueta,
                )
            else:
                extremos = coeficientes[0]
                texto_splines.insert(
                    "end", "Derivadas fixadas (estimadas dos pontos): "
                    f"S'({formatar_numero(extremos[0])}) = {formatar_numero(derivadas[0])}; "
                    f"S'({formatar_numero(extremos[-1])}) = {formatar_numero(derivadas[1])}.\n",
                    etiqueta,
                )
                texto_splines.insert(
                    "end", formatar_spline(i + 1, coeficientes) + "\n\n", etiqueta,
                )
        texto_splines.config(state="disabled")
        texto_splines.yview_moveto(posicao)

    def ver_splines():
        nonlocal janela_splines, texto_splines
        if janela_splines is not None and janela_splines.winfo_exists():
            janela_splines.lift()
            atualizar_formulas()
            return

        janela_splines = tk.Toplevel(janela)
        janela_splines.title("Interpoladores — fórmulas por grupo")
        largura = min(1100, janela.winfo_screenwidth() - 80)
        altura = min(560, janela.winfo_screenheight() - 100)
        janela_splines.geometry(f"{largura}x{altura}+30+30")
        janela_splines.configure(bg="white")

        tk.Label(
            janela_splines, text="Fórmulas do interpolador selecionado", bg="white",
            font=("DejaVu Sans", 14, "bold"), anchor="w",
        ).pack(fill="x", padx=14, pady=(12, 4))
        tk.Label(
            janela_splines,
            text=f"Valores exibidos com até {ALGARISMOS} algarismos significativos. "
                 "As fórmulas se atualizam a cada clique.",
            bg="white", anchor="w",
        ).pack(fill="x", padx=14, pady=(0, 10))

        painel = tk.Frame(janela_splines, bg="white")
        painel.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        painel.rowconfigure(0, weight=1)
        painel.columnconfigure(0, weight=1)
        texto_splines = tk.Text(
            painel, wrap="none", font=("DejaVu Sans Mono", 11),
            bg="white", padx=10, pady=10, borderwidth=0,
            state="disabled", cursor="arrow",
        )
        vertical = tk.Scrollbar(painel, orient="vertical", command=texto_splines.yview)
        horizontal = tk.Scrollbar(painel, orient="horizontal", command=texto_splines.xview)
        texto_splines.config(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        texto_splines.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        atualizar_formulas()

    def redesenhar():
        tela.delete("all")
        # A imagem é recriada primeiro, para ficar atrás dos pontos e das curvas.
        if imagem_fundo is not None:
            tela.create_image(
                LARGURA / 2, ALTURA / 2, image=imagem_fundo, anchor="center",
                tags="fundo",
            )
        grupos = separar_grupos(pontos)
        grupos_calculados.clear()

        for indice, grupo in enumerate(grupos):
            cor = CORES[indice % len(CORES)]
            if len(grupo) >= 2 and metodo.get() == "Spline fixado":
                derivadas = estimar_derivadas(grupo)
                coeficientes = calcular_spline(grupo, derivadas=derivadas)
            else:
                derivadas = None
                coeficientes = None
            grupos_calculados.append((grupo, coeficientes, derivadas))
            pixels = [
                (LARGURA / 2 + x * ESCALA, ALTURA / 2 - y * ESCALA)
                for x, y in grupo
            ]

            if len(pixels) >= 2 and mostrar_curvas.get():
                amostras = (amostrar_spline(coeficientes) if coeficientes is not None
                            else amostrar_lagrange(grupo))
                for coordenadas in linhas_visiveis(amostras):
                    if imagem_fundo is not None:
                        tela.create_line(*coordenadas, fill="white", width=4)
                    tela.create_line(*coordenadas, fill=cor, width=2)

            if mostrar_pontos.get():
                for (x, y), (px, py) in zip(grupo, pixels):
                    tela.create_oval(px - 4, py - 4, px + 4, py + 4,
                                     fill=cor, outline="white" if imagem_fundo else cor)
                    if mostrar_coordenadas.get():
                        # O texto do Canvas já tem fundo transparente.
                        tela.create_text(px + 8, py - 10,
                                         text=f"({x:.2f}, {y:.2f})",
                                         anchor="w", fill=cor)

        botao_exportar.config(state="normal" if pontos else "disabled")
        botao_desfazer.config(state="normal" if pontos else "disabled")
        controle_coordenadas.config(state="normal" if mostrar_pontos.get() else "disabled")
        status.config(text=(
            f"Pontos: {len(pontos)} | Grupos: {len(grupos)} | "
            "Ctrl+Z: remover último ponto. Esc: limpar pontos."
        ))
        atualizar_formulas()

    def adicionar_ponto(evento):
        x = (evento.x - LARGURA / 2) / ESCALA
        y = (ALTURA / 2 - evento.y) / ESCALA
        pontos.append((x, y))
        redesenhar()

    def limpar(evento=None):
        pontos.clear()
        redesenhar()

    def remover_ultimo_ponto(evento=None):
        if pontos:
            pontos.pop()
            # Refaz os grupos: retirar um ponto de virada pode eliminar um grupo.
            redesenhar()
        return "break"

    def exportar_pontos():
        if not pontos:
            return
        caminho = filedialog.asksaveasfilename(
            parent=janela, title="Exportar pontos por grupo",
            defaultextension=".txt", initialfile="pontos_por_grupo.txt",
            filetypes=[("Arquivo de texto", "*.txt")],
        )
        if not caminho:
            return
        try:
            Path(caminho).write_text(texto_pontos(pontos), encoding="utf-8")
        except OSError as erro:
            messagebox.showerror("Falha na exportação", str(erro), parent=janela)
            return
        status.config(text=f"Pontos exportados para {Path(caminho).name}.")

    def adicionar_imagem():
        nonlocal imagem_fundo
        caminho = filedialog.askopenfilename(
            parent=janela, title="Escolha a imagem de fundo",
            filetypes=[
                ("Imagens", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff *.webp *.gif"),
                ("Todos os arquivos", "*"),
            ],
        )
        if not caminho:
            return
        try:
            imagem = preparar_imagem(caminho)
            nova_imagem = ImageTk.PhotoImage(imagem, master=janela)
        except (OSError, UnidentifiedImageError, ValueError,
                Image.DecompressionBombError, tk.TclError):
            messagebox.showerror(
                "Não foi possível abrir a imagem",
                "Escolha uma imagem válida, como PNG ou JPEG, que possa ser aberta neste computador.",
                parent=janela,
            )
            return
        # Troca somente após o carregamento bem-sucedido. Os pontos são mantidos.
        imagem_fundo = nova_imagem
        botao_remover.config(state="normal")
        redesenhar()

    def remover_imagem():
        nonlocal imagem_fundo
        imagem_fundo = None
        botao_remover.config(state="disabled")
        redesenhar()

    tk.Button(barra, text="Adicionar imagem", command=adicionar_imagem).pack(
        side="left", padx=(10, 5), pady=6,
    )
    botao_remover = tk.Button(
        barra, text="Remover imagem", command=remover_imagem, state="disabled",
    )
    botao_remover.pack(side="left", padx=5, pady=6)
    botao_desfazer = tk.Button(
        barra, text="Remover último ponto", command=remover_ultimo_ponto, state="disabled",
    )
    botao_desfazer.pack(side="left", padx=5, pady=6)
    tk.Button(barra, text="Limpar pontos", command=limpar).pack(
        side="left", padx=5, pady=6,
    )
    botao_exportar = tk.Button(barra, text="Exportar pontos (.txt)", command=exportar_pontos,
                              state="disabled")
    botao_exportar.pack(side="left", padx=5, pady=6)
    tk.Button(barra, text="Ver fórmulas", command=ver_splines).pack(
        side="left", padx=5, pady=6,
    )

    tk.Label(opcoes, text="Interpolação:", bg="white").pack(side="left", padx=(10, 0))
    for nome in ("Spline fixado", "Lagrange"):
        tk.Radiobutton(opcoes, text=nome, value=nome, variable=metodo,
                       command=redesenhar, bg="white", activebackground="white").pack(side="left")
    tk.Checkbutton(
        opcoes, text="Mostrar pontos", variable=mostrar_pontos,
        command=redesenhar, bg="white", activebackground="white",
    ).pack(side="left", padx=(10, 5), pady=(0, 5))
    tk.Checkbutton(
        opcoes, text="Mostrar curvas", variable=mostrar_curvas,
        command=redesenhar, bg="white", activebackground="white",
    ).pack(side="left", padx=5, pady=(0, 5))
    controle_coordenadas = tk.Checkbutton(
        opcoes, text="Mostrar coordenadas", variable=mostrar_coordenadas,
        command=redesenhar, bg="white", activebackground="white",
    )
    controle_coordenadas.pack(side="left", padx=5, pady=(0, 5))

    tela.bind("<Button-1>", adicionar_ponto)
    janela.bind("<Escape>", limpar)
    janela.bind("<Control-z>", remover_ultimo_ponto)
    janela.mainloop()


if __name__ == "__main__":
    main()
