import math

class EliasGamma():
    """
    Implementa a codificação de Elias-Gamma.

    IDEIA CENTRAL:
    - Representar números inteiros positivos usando:
        prefixo → quantidade de bits do número
        sufixo → o número sem o bit mais significativo

    Isso funciona bem para números pequenos.
    """

    def encoder(self, mensagem):
        """
        Codifica uma mensagem usando Elias-Gamma.

        PIPELINE:
        texto → ASCII → Elias-Gamma → bits
        """
        mensagem_codificada = ""

        # Converte cada caractere da mensagem para seu valor ASCII
        valores_ascii = [ord(simbolo) for simbolo in mensagem]

        for valor in valores_ascii:

            # Elias-Gamma só funciona para inteiros positivos
            if valor <= 0:
                continue

            # ========================
            # PASSO 1 — CALCULAR n
            # ========================
            
            # n representa o tamanho do número em bits (sem contar o primeiro bit)
            # Ex: valor = 13 (1101) → n = 3
            n = int(math.log2(valor))

            # ========================
            # PASSO 2 — PREFIXO
            # ========================
            
            # O prefixo indica o tamanho do número
            # Regra:
            # - n zeros
            # - seguido de um '1' (stop bit)
            
            # Ex: n = 3 → "0001"
            prefixo = "0" * n
            stop_bit = "1"

            # ========================
            # PASSO 3 — SUFIXO
            # ========================
            
            # Remove o bit mais significativo (2^n)
            resto = valor - (2**n)

            # Converte o resto para binário
            # e garante que tenha exatamente n bits
            sufixo = bin(resto)[2:].zfill(n)

            # ========================
            # PASSO 4 — JUNÇÃO
            # ========================
            
            # Codeword final = prefixo + stop bit + sufixo
            codeword = prefixo + stop_bit + sufixo

            mensagem_codificada += codeword

        return mensagem_codificada
    

    def decoder(self, mensagem_codificada):
        """
        Decodifica uma sequência de bits usando Elias-Gamma.

        PIPELINE:
        bits → Elias-Gamma → ASCII → texto
        """
        mensagem_decodificada = ""
        ponteiro = 0

        while ponteiro < len(mensagem_codificada):

            # ========================
            # PASSO 1 — LER PREFIXO
            # ========================
            
            # Conta quantos zeros aparecem antes do primeiro '1'
            # Isso define o valor de n
            n = 0
            
            while ponteiro < len(mensagem_codificada) and mensagem_codificada[ponteiro] == "0":
                n += 1
                ponteiro += 1

            # ========================
            # PASSO 2 — PULAR STOP BIT
            # ========================
            
            # O '1' marca o fim do prefixo
            ponteiro += 1

            # ========================
            # PASSO 3 — LER SUFIXO
            # ========================
            
            # Lê os próximos n bits
            sufixo_binario = mensagem_codificada[ponteiro : ponteiro + n]

            # Avança o ponteiro
            ponteiro += n

            # ========================
            # PASSO 4 — RECONSTRUIR NÚMERO
            # ========================
            
            # Converte sufixo para inteiro
            valor_sufixo = int(sufixo_binario, 2) if sufixo_binario else 0

            # Fórmula principal:
            # valor = 2^n + sufixo
            valor_original = (2**n) + valor_sufixo

            # ========================
            # PASSO 5 — ASCII → CARACTERE
            # ========================
            
            mensagem_decodificada += chr(valor_original)

        return mensagem_decodificada