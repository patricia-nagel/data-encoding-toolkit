import tkinter as tk
from tkinter import messagebox

# Importação dos seus módulos (certifique-se que os arquivos tenham esses nomes)
from elias_gamma_module import EliasGamma
from fibonacci_module import Fibonacci
from golomb_module import Golomb
from huffman_module import Huffman

# Instanciando as classes dos algoritmos
golomb = Golomb()
elias = EliasGamma()
huff = Huffman()
fibo = Fibonacci()

# Variáveis globais para "lembrar" dados entre codificação e decodificação
# Isso é essencial para o Huffman e o Golomb funcionarem
golomb_k = None
huffman_raiz = None

def executar_opcao(algoritmo, acao):
    global golomb_k, huffman_raiz

    # Pega o que o usuário digitou e limpa espaços extras
    mensagem = entrada_mensagem.get().strip()

    if not mensagem:
        messagebox.showerror("Erro", "Por favor, digite uma mensagem ou bits.")
        return

    resultado = ""

    # --- LÓGICA DE CODIFICAÇÃO ---
    if acao == "codificar":
        if algoritmo == "Golomb":
            # O encoder de Golomb retorna o binário e o K que ele calculou
            resultado, golomb_k = golomb.encoder(mensagem)
            historico.append(f"Codificado (Golomb, k={golomb_k}): {resultado}")
            
        elif algoritmo == "Elias-Gamma":
            resultado = elias.encoder(mensagem)
            historico.append(f"Codificado (Elias-Gamma): {resultado}")
            
        elif algoritmo == "Fibonacci":
            resultado = fibo.encoder(mensagem)
            historico.append(f"Codificado (Fibonacci): {resultado}")
            
        elif algoritmo == "Huffman":
            # O encoder de Huffman retorna o binário e a Árvore (raiz)
            resultado, huffman_raiz = huff.encoder(mensagem)
            historico.append(f"Codificado (Huffman): {resultado}")

    # --- LÓGICA DE DECODIFICAÇÃO ---
    elif acao == "decodificar":
        # Validação para Huffman: ele precisa da árvore gerada na codificação
        if algoritmo == "Huffman" and huffman_raiz is None:
            messagebox.showerror("Erro", "Codifique algo com Huffman antes de decodificar!")
            return

        if algoritmo == "Golomb":
            # Para Golomb, usamos o K que foi guardado na codificação
            resultado = golomb.decoder(mensagem, golomb_k)
        elif algoritmo == "Elias-Gamma":
            resultado = elias.decoder(mensagem)
        elif algoritmo == "Fibonacci":
            resultado = fibo.decoder(mensagem)
        elif algoritmo == "Huffman":
            resultado = huff.decoder(mensagem, huffman_raiz)

        historico.append(f"Decodificado ({algoritmo}): {resultado}")

    # --- ATUALIZAR A TELA ---
    # Limpa a caixa de histórico e escreve tudo de novo com o novo resultado
    historico_texto.config(state=tk.NORMAL)
    historico_texto.delete(1.0, tk.END)
    for linha in historico:
        historico_texto.insert(tk.END, linha + "\n")
    historico_texto.config(state=tk.DISABLED)

# --- CONFIGURAÇÃO DA INTERFACE (Igual ao seu original) ---
janela = tk.Tk()
janela.title("Codificador e Decodificador - TI")

# Label e campo de entrada
tk.Label(janela, text="Digite sua mensagem ou bits:").pack(pady=(10, 0))
entrada_mensagem = tk.Entry(janela, width=50)
entrada_mensagem.pack(pady=(0, 10))

# Menu de escolha do Algoritmo
algoritmo_var = tk.StringVar(value="Golomb")
algoritmo_menu = tk.OptionMenu(janela, algoritmo_var, "Golomb", "Elias-Gamma", "Fibonacci", "Huffman")
algoritmo_menu.pack()

# Menu de escolha da Ação (Codificar/Decodificar)
acao_var = tk.StringVar(value="codificar")
acao_menu = tk.OptionMenu(janela, acao_var, "codificar", "decodificar")
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