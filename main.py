import tkinter as tk
from tkinter import messagebox

# Importa as implementações dos algoritmos de compressão
from elias_gamma_module import EliasGamma
from fibonacci_module import Fibonacci
from golomb_module import Golomb
from huffman_module import Huffman

# ========================
# INSTANCIAÇÃO DOS ALGORITMOS
# ========================

# Criamos objetos de cada algoritmo para reutilizar suas funções
golomb = Golomb()
elias_gamma = EliasGamma()
huffman = Huffman()
fibonacci = Fibonacci()

# Variável global para guardar a árvore do Huffman
# IMPORTANTE:
# Diferente dos outros algoritmos, o Huffman precisa da árvore para decodificar
huffman_raiz = None


def executar_opcao(algoritmo, acao):
    """
    Função principal da aplicação.

    Ela decide:
    - qual algoritmo usar
    - se vai codificar ou decodificar
    """

    global huffman_raiz

    # ========================
    # ENTRADA DO USUÁRIO
    # ========================
    
    # Pega o texto digitado e remove espaços extras
    mensagem = entrada_mensagem.get().strip()

    # Validação básica: não permite entrada vazia
    if not mensagem:
        messagebox.showerror("Erro", "Por favor, digite uma mensagem ou bits.")
        return

    resultado = ""

    # ========================
    # CODIFICAÇÃO
    # ========================
    
    if acao == "Codificar":

        if algoritmo == "Golomb":
            # Retorna os bits e o valor de k usado
            resultado, k = golomb.encoder(mensagem)

            # Guarda no histórico
            historico.append(f"Codificado (Golomb, k={k}): {resultado}")

            # IMPORTANTE:
            # Golomb precisa do k para decodificar depois
            historico.append(f"⚠ Guarde o k={k} para decodificar!")

            # Preenche automaticamente o campo de k na interface
            entrada_k.config(state=tk.NORMAL)
            entrada_k.delete(0, tk.END)
            entrada_k.insert(0, str(k))

        elif algoritmo == "Elias-Gamma":
            resultado = elias_gamma.encoder(mensagem)
            historico.append(f"Codificado (Elias-Gamma): {resultado}")

        elif algoritmo == "Fibonacci":
            resultado = fibonacci.encoder(mensagem)
            historico.append(f"Codificado (Fibonacci): {resultado}")

        elif algoritmo == "Huffman":
            # Retorna os bits e a árvore (raiz)
            resultado, huffman_raiz = huffman.encoder(mensagem)

            # IMPORTANTE:
            # Precisamos guardar a árvore para decodificar depois
            historico.append(f"Codificado (Huffman): {resultado}")

    # ========================
    # DECODIFICAÇÃO
    # ========================
    
    elif acao == "Decodificar":

        # Validação binária (aceita espaços)
        partes = mensagem.split()
        if not all(all(c in "01" for c in parte) for parte in partes):
            messagebox.showerror("Erro", "A entrada deve conter apenas 0s e 1s.")
            return

        if algoritmo == "Golomb":
            # Lê o valor de k digitado pelo usuário
            k_valor = entrada_k.get().strip()

            # Validação: precisa ser número positivo
            if not k_valor.isdigit() or int(k_valor) <= 0:
                messagebox.showerror("Erro", "Informe um k válido (inteiro positivo) para decodificar com Golomb.")
                return

            resultado = golomb.decoder(mensagem, int(k_valor))

        elif algoritmo == "Elias-Gamma":
            resultado = elias_gamma.decoder(mensagem)

        elif algoritmo == "Fibonacci":
            resultado = fibonacci.decoder(mensagem)

        elif algoritmo == "Huffman":
            # Validação importante:
            # Não dá pra decodificar sem a árvore
            if huffman_raiz is None:
                messagebox.showerror("Erro", "Codifique algo com Huffman antes de decodificar!")
                return

            resultado = huffman.decoder(mensagem, huffman_raiz)

        # Adiciona resultado ao histórico
        historico.append(f"Decodificado ({algoritmo}): {resultado}")

    # ========================
    # ATUALIZAÇÃO DA INTERFACE
    # ========================

    # Libera edição temporariamente
    historico_texto.config(state=tk.NORMAL)

    # Limpa o conteúdo atual
    historico_texto.delete(1.0, tk.END)

    # Reescreve todo o histórico
    for linha in historico:
        historico_texto.insert(tk.END, linha + "\n")

    # Bloqueia edição (somente leitura)
    historico_texto.config(state=tk.DISABLED)


# ========================
# CRIAÇÃO DA INTERFACE
# ========================

# Cria a janela principal
janela = tk.Tk()
janela.title("Codificador e Decodificador - TI")

# Campo de entrada da mensagem
tk.Label(janela, text="Digite sua mensagem ou bits:").pack(pady=(10, 0))
entrada_mensagem = tk.Entry(janela, width=50)
entrada_mensagem.pack(pady=(0, 10))

# Campo para o parâmetro k do Golomb
tk.Label(janela, text="Parâmetro k (apenas para decodificação Golomb):").pack()

# Começa desabilitado (só é necessário em um caso específico)
entrada_k = tk.Entry(janela, width=10, state=tk.DISABLED)
entrada_k.pack(pady=(0, 10))


def atualizar_campo_k(*args):
    """
    Controla quando o campo k deve estar ativo.

    Regra:
    - Só é necessário quando:
        algoritmo = Golomb
        ação = Decodificar
    """
    if algoritmo_var.get() == "Golomb" and acao_var.get() == "Decodificar":
        entrada_k.config(state=tk.NORMAL)
    else:
        entrada_k.config(state=tk.DISABLED)


# ========================
# MENUS DE SELEÇÃO
# ========================

# Escolha do algoritmo
algoritmo_var = tk.StringVar(value="Golomb")
algoritmo_var.trace_add("write", atualizar_campo_k)

algoritmo_menu = tk.OptionMenu(
    janela,
    algoritmo_var,
    "Golomb", "Elias-Gamma", "Fibonacci", "Huffman"
)
algoritmo_menu.pack()

# Escolha da ação
acao_var = tk.StringVar(value="Codificar")
acao_var.trace_add("write", atualizar_campo_k)

acao_menu = tk.OptionMenu(
    janela,
    acao_var,
    "Codificar", "Decodificar"
)
acao_menu.pack(pady=(5, 10))


# ========================
# BOTÃO EXECUTAR
# ========================

# Chama a função principal passando as escolhas do usuário
executar_button = tk.Button(
    janela,
    text="Executar",
    command=lambda: executar_opcao(algoritmo_var.get(), acao_var.get())
)
executar_button.pack()


# ========================
# HISTÓRICO
# ========================

tk.Label(janela, text="Histórico:").pack(pady=(10, 0))

# Caixa de texto onde mostramos resultados
historico_texto = tk.Text(
    janela,
    wrap=tk.WORD,
    height=10,
    width=50,
    state=tk.DISABLED
)
historico_texto.pack(pady=(0, 10))

# Lista que guarda o histórico
historico = []


# ========================
# LOOP DA INTERFACE
# ========================

# Mantém a janela rodando
janela.mainloop()