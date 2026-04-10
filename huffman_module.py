import heapq
from collections import Counter

class NoHuffman:
    """
    Representa um nó da árvore de Huffman.

    Pode ser:
    - Nó folha → contém um símbolo (letra)
    - Nó interno → contém apenas a soma das frequências

    A árvore é construída de baixo para cima.
    """
    def __init__(self, frequencia, simbolo=None, esquerda=None, direita=None):
        # Frequência total daquele nó (quantas vezes aparece na mensagem)
        self.frequencia = frequencia

        # Símbolo (apenas folhas têm)
        self.simbolo = simbolo

        # Filhos da árvore binária
        self.esquerda = esquerda
        self.direita = direita

    # Define como comparar nós dentro da fila de prioridade (heap)
    def __lt__(self, outro):
        # O heap precisa saber qual nó é "menor"
        # Aqui usamos a frequência como critério
        return self.frequencia < outro.frequencia


class Huffman:
    """
    Implementa o algoritmo de Huffman estático.

    IDEIA CENTRAL:
    - Símbolos mais frequentes recebem códigos menores
    - Símbolos menos frequentes recebem códigos maiores

    Isso reduz o tamanho total da mensagem.
    """

    def gerar_tabela_codigos(self, no, codigo_atual, tabela):
        """
        Percorre a árvore para gerar os códigos binários.

        COMO FUNCIONA:
        - Caminhar para esquerda → adiciona '0'
        - Caminhar para direita → adiciona '1'
        - Quando chega em uma folha → encontrou um símbolo
        """
        if no is None:
            return

        # Se chegou numa folha, associa o código ao símbolo
        if no.simbolo is not None:
            tabela[no.simbolo] = codigo_atual
            return

        # Continua descendo na árvore
        self.gerar_tabela_codigos(no.esquerda, codigo_atual + "0", tabela)
        self.gerar_tabela_codigos(no.direita, codigo_atual + "1", tabela)


    def encoder(self, mensagem):
        """
        Codifica uma mensagem usando Huffman.

        PIPELINE:
        texto → frequência → árvore → códigos → bits
        """
        if not mensagem:
            return "", None

        # ========================
        # PASSO 1 — CONTAR FREQUÊNCIA
        # ========================
        
        # Conta quantas vezes cada caractere aparece
        # Ex: "banana" → {'b':1, 'a':3, 'n':2}
        frequencias = Counter(mensagem)
        
        # ========================
        # PASSO 2 — CRIAR FILA DE PRIORIDADE
        # ========================
        
        # Cria um nó para cada símbolo
        fila_prioridade = [NoHuffman(freq, simb) for simb, freq in frequencias.items()]

        # Transforma a lista em um heap (fila de prioridade)
        # Sempre conseguimos pegar os menores rapidamente
        heapq.heapify(fila_prioridade)

        # ========================
        # PASSO 3 — CONSTRUIR ÁRVORE
        # ========================
        
        while len(fila_prioridade) > 1:
            # Remove os dois nós com menor frequência
            esquerda = heapq.heappop(fila_prioridade)
            direita = heapq.heappop(fila_prioridade)

            # Cria um novo nó pai
            # A frequência dele é a soma dos filhos
            novo_no = NoHuffman(
                esquerda.frequencia + direita.frequencia,
                esquerda=esquerda,
                direita=direita
            )

            # Insere o novo nó de volta na fila
            heapq.heappush(fila_prioridade, novo_no)

        # O último nó restante é a raiz da árvore completa
        raiz = fila_prioridade[0]
        
        # ========================
        # PASSO 4 — GERAR CÓDIGOS
        # ========================
        
        tabela_codigos = {}

        # Percorre a árvore para montar os códigos binários
        self.gerar_tabela_codigos(raiz, "", tabela_codigos)

        # ========================
        # PASSO 5 — CODIFICAR MENSAGEM
        # ========================
        
        # Substitui cada caractere pelo seu código binário
        mensagem_bits = "".join(tabela_codigos[char] for char in mensagem)
        
        return mensagem_bits, raiz


    def decoder(self, bits, raiz):
        """
        Decodifica a sequência de bits usando a árvore de Huffman.

        PIPELINE:
        bits → percorrer árvore → texto
        """
        if raiz is None:
            return ""

        mensagem_decodificada = ""

        # Começa sempre da raiz
        no_atual = raiz

        for bit in bits:
            # ========================
            # PASSO 1 — PERCORRER ÁRVORE
            # ========================
            
            if bit == "0":
                no_atual = no_atual.esquerda
            else:
                no_atual = no_atual.direita

            # ========================
            # PASSO 2 — VERIFICAR SE É FOLHA
            # ========================
            
            # Se chegou em uma folha, encontramos um símbolo
            if no_atual.simbolo is not None:
                mensagem_decodificada += no_atual.simbolo

                # Volta para a raiz para começar o próximo símbolo
                no_atual = raiz

        return mensagem_decodificada