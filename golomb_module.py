import math

class Golomb:
    """
    Implementa a codificação de Golomb, que divide um número por um divisor 'k'.
    O quociente é codificado em unário e o resto em binário.
    """

    def calcular_k_ideal(self, lista_ascii):
        """
        Escolhe o k como a potência de 2 mais próxima da média da mensagem.
        Isso ajuda a otimizar a compressão.
        """
        media = sum(lista_ascii) / len(lista_ascii)
        # Escolhe a potência de 2 (2, 4, 8, 16...) mais próxima da média
        k = 2 ** int(math.log2(media))
        return k


    def encoder(self, mensagem):
        """Codifica a mensagem textual para binário de Golomb."""
        mensagem_codificada = ""
        # Converte o texto para uma lista de números (ASCII)
        valores_ascii = [ord(caractere) for caractere in mensagem]
        
        # Define o divisor K baseado nos dados da mensagem
        k = self.calcular_k_ideal(valores_ascii)
        # Tamanho fixo do sufixo para potências de 2 (ex: se k=8, sufixo tem 3 bits)
        tamanho_sufixo = int(math.log2(k))

        for valor in valores_ascii:
            # Calcula o quociente (quantas vezes o k cabe no valor)
            quociente = valor // k
            # O prefixo é o quociente em unário (zeros seguidos de um '1' de parada)
            prefixo = ("0" * quociente) + "1"
            
            # O resto da divisão vira o sufixo binário
            resto = valor % k
            # Garante que o binário tenha o tamanho fixo (zfill)
            sufixo = bin(resto)[2:].zfill(tamanho_sufixo)

            mensagem_codificada += (prefixo + sufixo)

        return mensagem_codificada, k

    def decoder(self, bits, k):
        """Decodifica os bits para texto usando o divisor k fornecido."""
        mensagem_decodificada = ""
        tamanho_sufixo = int(math.log2(k))
        ponteiro = 0

        while ponteiro < len(bits):
            # Conta quantos zeros existem até encontrar o '1' (Stop Bit do quociente)
            quociente = 0
            while bits[ponteiro] == "0":
                quociente += 1
                ponteiro += 1
            
            # Pula o '1' que serviu de separador
            ponteiro += 1

            # Lê os bits do sufixo baseado no tamanho fixo calculado por log2(k)
            sufixo_binario = bits[ponteiro : ponteiro + tamanho_sufixo]
            ponteiro += tamanho_sufixo
            
            # Reconstrói o número: (Quociente * K) + Resto
            valor_resto = int(sufixo_binario, 2)
            valor_original = (quociente * k) + valor_resto
            
            mensagem_decodificada += chr(valor_original)

        return mensagem_decodificada

'''
Explicação:
    - Primeiro, calculamos a média dos valores ASCII da mensagem. Escolhemos k como a potência de 2 
    mais próxima dessa média para que o sufixo binário tenha sempre o mesmo número de bits, o que facilita a decodificação.
    - Depois, para cada caractere, dividimos o valor dele pelo nosso k. Isso dá um quociente e um resto.
    - O quociente codificamos de forma unária: se o quociente for 3, colocamos três zeros e um '1' no final. 
    Esse '1' avisa o decoder que o quociente acabou.
    - O resto da divisão transformamos em binário puro. Usamos o comando zfill para garantir que ele tenha o
    tamanho correto (ex: 3 bits se k for 8).
    - No decoder, fazemos o caminho inverso: contamos os zeros até o primeiro '1' para descobrir o quociente, 
    lemos os próximos bits fixos para descobrir o resto e aplicamos a fórmula (Quociente * k) + Resto para recuperar o 
    caractere ASCII original.
'''
