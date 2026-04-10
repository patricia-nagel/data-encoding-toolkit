import heapq
from collections import Counter

class NoHuffman:
    """
    Representa um nó na árvore de Huffman.
    Pode ser uma folha (contém um caractere) ou um nó interno (contém a soma das frequências).
    """
    def __init__(self, frequencia, simbolo=None, esquerda=None, direita=None):
        self.frequencia = frequencia
        self.simbolo = simbolo
        self.esquerda = esquerda
        self.direita = direita

    # Este método permite que o heapq compare os nós pela frequência
    def __lt__(self, outro):
        return self.frequencia < outro.frequencia

class Huffman:
    """
    Implementa a compressão de Huffman usando uma árvore binária e fila de prioridade.
    """

    def gerar_tabela_codigos(self, no, codigo_atual, tabela):
        """
        Função recursiva que percorre a árvore para gerar os códigos binários.
        Esquerda recebe '0', Direita recebe '1'.
        """
        if no is None:
            return

        # Se for um nó folha (tem símbolo), salva o código acumulado
        if no.simbolo is not None:
            tabela[no.simbolo] = codigo_atual
            return

        self.gerar_tabela_codigos(no.esquerda, codigo_atual + "0", tabela)
        self.gerar_tabela_codigos(no.direita, codigo_atual + "1", tabela)

    def encoder(self, mensagem):
        """Cria a árvore de Huffman e codifica a mensagem."""
        if not mensagem:
            return "", None

        # 1. Conta a frequência de cada caractere
        frequencias = Counter(mensagem)
        
        # 2. Cria uma fila de prioridade (heap) com nós para cada caractere
        fila_prioridade = [NoHuffman(freq, simb) for simb, freq in frequencias.items()]
        heapq.heapify(fila_prioridade)

        # 3. Constroi a Árvore de Huffman
        while len(fila_prioridade) > 1:
            # Retira os dois nós com as menores frequências
            esquerda = heapq.heappop(fila_prioridade)
            direita = heapq.heappop(fila_prioridade)

            # Cria um novo nó pai com a soma das frequências
            novo_no = NoHuffman(esquerda.frequencia + direita.frequencia, 
                                esquerda=esquerda, direita=direita)
            heapq.heappush(fila_prioridade, novo_no)

        # O último nó restante é a raiz da árvore
        raiz = fila_prioridade[0]
        
        # 4. Gera o dicionário de códigos (ex: {'A': '10', 'B': '110'})
        tabela_codigos = {}
        self.gerar_tabela_codigos(raiz, "", tabela_codigos)

        # 5. Transforma a mensagem original em bits
        mensagem_bits = "".join(tabela_codigos[char] for char in mensagem)
        
        return mensagem_bits, raiz

    def decoder(self, bits, raiz):
        """Percorre a árvore bit a bit para recuperar o texto original."""
        if raiz is None:
            return ""

        mensagem_decodificada = ""
        no_atual = raiz

        for bit in bits:
            # Se o bit for '0', vai para a esquerda; se '1', para a direita
            if bit == "0":
                no_atual = no_atual.esquerda
            else:
                no_atual = no_atual.direita

            # Se chegamos numa folha, encontramos um caractere
            if no_atual.simbolo is not None:
                mensagem_decodificada += no_atual.simbolo
                no_atual = raiz # Volta para o topo para o próximo caractere

        return mensagem_decodificada
    
'''
Explicação:
    - Primeiro, contamos quantas vezes cada letra aparece. Usamos uma Fila de Prioridade (Heap) para garantir que as letras que
      aparecem menos fiquem sempre 'na mão' para serem processadas primeiro.
    - Retiramos os dois nós de menor frequência da fila e unimos-os num novo nó pai, cuja frequência é a soma dos dois.
      Repetimos isto até sobrar apenas um nó: a Raiz.
    - Com a árvore pronta, percorremos ela do topo até as folhas. Sempre que vamos para a esquerda, atribuimos o bit 0. 
      Para a direita, o bit 1. Isso garante que nenhum código seja prefixo de outro (Propriedade do Prefixo), evitando ambiguidades.
    - Para decodificar, pegamos na sequência de bits e vamos 'andando' pela árvore. Se o bit for 0, descemos para o filho da 
      esquerda; se for 1, para o da direita. Quando chegamos a uma folha, o símbolo é revelado e voltamos para o topo da árvore 
      para processar o resto dos bits.
'''