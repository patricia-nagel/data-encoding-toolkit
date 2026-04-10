import tkinter as tk
from tkinter import messagebox

from elias_gamma_module import EliasGamma
from fibonacci_module import Fibonacci
from golomb_module import Golomb
from huffman_module import Huffman

# Instanciando as classes dos algoritmos
golomb = Golomb()
elias_gamma = EliasGamma()
huffman = Huffman()
fibonacci = Fibonacci()

# Variável global para a árvore do Huffman (necessária para decodificação)
huffman_raiz = None

def executar_opcao(algoritmo, acao):
    global huffman_raiz

    # Pega o que o usuário digitou e limpa espaços extras
    mensagem = entrada_mensagem.get().strip()

    if not mensagem:
        messagebox.showerror("Erro", "Por favor, digite uma mensagem ou bits.")
        return

    resultado = ""

    # --- LÓGICA DE CODIFICAÇÃO ---
    if acao == "Codificar":
        if algoritmo == "Golomb":
            resultado, k = golomb.encoder(mensagem)
            # Exibe o k no histórico e preenche o campo automaticamente
            historico.append(f"Codificado (Golomb, k={k}): {resultado}")
            historico.append(f"⚠ Guarde o k={k} para decodificar!")
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
            resultado, huffman_raiz = huffman.encoder(mensagem)
            historico.append(f"Codificado (Huffman): {resultado}")

    # --- LÓGICA DE DECODIFICAÇÃO ---
    elif acao == "Decodificar":
        if algoritmo == "Golomb":
            # Lê o k informado pelo usuário no campo específico
            k_valor = entrada_k.get().strip()
            if not k_valor.isdigit() or int(k_valor) <= 0:
                messagebox.showerror("Erro", "Informe um k válido (inteiro positivo) para decodificar com Golomb.")
                return
            resultado = golomb.decoder(mensagem, int(k_valor))

        elif algoritmo == "Elias-Gamma":
            resultado = elias_gamma.decoder(mensagem)

        elif algoritmo == "Fibonacci":
            resultado = fibonacci.decoder(mensagem)

        elif algoritmo == "Huffman":
            if huffman_raiz is None:
                messagebox.showerror("Erro", "Codifique algo com Huffman antes de decodificar!")
                return
            resultado = huffman.decoder(mensagem, huffman_raiz)

        historico.append(f"Decodificado ({algoritmo}): {resultado}")

    # --- ATUALIZAR A TELA ---
    # Limpa a caixa de histórico e escreve tudo de novo com o novo resultado
    historico_texto.config(state=tk.NORMAL)
    historico_texto.delete(1.0, tk.END)
    for linha in historico:
        historico_texto.insert(tk.END, linha + "\n")
    historico_texto.config(state=tk.DISABLED)

# --- CONFIGURAÇÃO DA INTERFACE ---
janela = tk.Tk()
janela.title("Codificador e Decodificador - TI")

# Label e campo de entrada da mensagem
tk.Label(janela, text="Digite sua mensagem ou bits:").pack(pady=(10, 0))
entrada_mensagem = tk.Entry(janela, width=50)
entrada_mensagem.pack(pady=(0, 10))

# Campo para o k do Golomb (começa desabilitado pois a ação padrão é codificar)
tk.Label(janela, text="Parâmetro k (apenas para decodificação Golomb):").pack()
entrada_k = tk.Entry(janela, width=10, state=tk.DISABLED)
entrada_k.pack(pady=(0, 10))

# Função que habilita/desabilita o campo k conforme a seleção
def atualizar_campo_k(*args):
    if algoritmo_var.get() == "Golomb" and acao_var.get() == "Decodificar":
        entrada_k.config(state=tk.NORMAL)
    else:
        entrada_k.config(state=tk.DISABLED)

# Menu de escolha do Algoritmo
algoritmo_var = tk.StringVar(value="Golomb")
algoritmo_var.trace_add("write", atualizar_campo_k)
algoritmo_menu = tk.OptionMenu(janela, algoritmo_var, "Golomb", "Elias-Gamma", "Fibonacci", "Huffman")
algoritmo_menu.pack()

# Menu de escolha da Ação (Codificar/Decodificar)
acao_var = tk.StringVar(value="Codificar")
acao_var.trace_add("write", atualizar_campo_k)
acao_menu = tk.OptionMenu(janela, acao_var, "Codificar", "Decodificar")
acao_menu.pack(pady=(5, 10))

# Botão Executar
executar_button = tk.Button(janela, text="Executar",
                            command=lambda: executar_opcao(algoritmo_var.get(), acao_var.get()))
executar_button.pack()

# Caixa de Histórico
tk.Label(janela, text="Histórico:").pack(pady=(10, 0))
historico_texto = tk.Text(janela, wrap=tk.WORD, height=10, width=50, state=tk.DISABLED)
historico_texto.pack(pady=(0, 10))

# Lista que armazena as frases do histórico
historico = []

janela.mainloop()