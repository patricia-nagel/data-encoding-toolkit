import math

class Golomb:
    """
    Implementa a codificação de Golomb.
    
    IDEIA CENTRAL:
    - Cada número é dividido por um valor k
    - O quociente vira código unário (prefixo)
    - O resto vira código binário (sufixo)
    
    Isso funciona bem quando os valores têm distribuição previsível.
    """

    def calcular_k_ideal(self, lista_ascii):
        """
        Escolhe o melhor valor de k baseado nos dados.
        
        POR QUE ISSO EXISTE?
        - O desempenho do Golomb depende muito da escolha de k
        - Se k for muito pequeno → quociente fica grande → muitos bits
        - Se k for muito grande → resto fica grande → mais bits
        
        ESTRATÉGIA:
        - Usa a média dos valores ASCII como referência
        - Escolhe a potência de 2 mais próxima
        
        POR QUE potência de 2?
        - Facilita MUITO a codificação
        - O resto sempre terá tamanho fixo (log2(k))
        """
        media = sum(lista_ascii) / len(lista_ascii)
        
        # log2(media) → descobre "em que potência de 2" a média está
        # int(...) → pega a parte inteira
        # 2**(...) → reconstrói a potência de 2
        k = 2 ** int(math.log2(media))
        
        return k


    def encoder(self, mensagem):
        """
        Transforma texto em bits usando Golomb.
        
        PIPELINE:
        texto → ASCII → Golomb → bits
        """
        mensagem_codificada = ""

        # Converte cada caractere para seu valor ASCII
        # Ex: 'a' → 97
        valores_ascii = [ord(caractere) for caractere in mensagem]
        
        # Define o melhor k baseado na mensagem
        k = self.calcular_k_ideal(valores_ascii)

        # Como k é potência de 2:
        # o número de bits do resto é fixo
        # Ex: k=8 → log2(8)=3 bits
        tamanho_sufixo = int(math.log2(k))

        for valor in valores_ascii:
            # Divide o número em duas partes:
            # quociente → parte "grande"
            # resto → parte "pequena"
            quociente = valor // k
            resto = valor % k

            # ========================
            # CODIFICAÇÃO DO QUOCIENTE
            # ========================
            
            # Codificação unária:
            # usamos "0" repetido + "1" como marcador de parada
            
            # Ex: quociente = 3 → "0001"
            
            # IMPORTANTE:
            # Poderia ser "1110" também (outra convenção),
            # mas aqui escolhemos:
            # - 0 = repetição
            # - 1 = fim
            prefixo = ("0" * quociente) + "1"
            
            # ========================
            # CODIFICAÇÃO DO RESTO
            # ========================
            
            # Converte o resto para binário
            # bin(x) → '0b101'
            # [2:] → remove '0b'
            sufixo = bin(resto)[2:]
            
            # Garante tamanho fixo (muito importante!)
            # Ex: se precisa de 3 bits:
            # 2 → '10' → vira '010'
            sufixo = sufixo.zfill(tamanho_sufixo)

            # Junta prefixo + sufixo
            mensagem_codificada += (prefixo + sufixo)

        # Retorna também o k, pois ele é necessário para decodificar
        return mensagem_codificada, k


    def decoder(self, bits, k):
        """
        Reconstrói o texto original a partir dos bits.
        
        PIPELINE:
        bits → Golomb → ASCII → texto
        """
        mensagem_decodificada = ""

        # Precisamos saber quantos bits ler para o resto
        tamanho_sufixo = int(math.log2(k))

        # Ponteiro percorre a string de bits
        ponteiro = 0

        while ponteiro < len(bits):
            
            # ========================
            # DECODIFICAR QUOCIENTE
            # ========================
            
            # Conta quantos '0' aparecem até o primeiro '1'
            # Isso representa o valor do quociente
            quociente = 0
            
            while bits[ponteiro] == "0":
                quociente += 1
                ponteiro += 1
            
            # Pula o '1' (marcador de fim do unário)
            ponteiro += 1

            # ========================
            # DECODIFICAR RESTO
            # ========================
            
            # Lê os próximos N bits (tamanho fixo)
            sufixo_binario = bits[ponteiro : ponteiro + tamanho_sufixo]
            ponteiro += tamanho_sufixo
            
            # Converte de binário para inteiro
            valor_resto = int(sufixo_binario, 2)
            
            # ========================
            # RECONSTRUIR VALOR ORIGINAL
            # ========================
            
            # Fórmula fundamental do Golomb:
            # n = (quociente * k) + resto
            valor_original = (quociente * k) + valor_resto
            
            # Converte de ASCII para caractere
            mensagem_decodificada += chr(valor_original)

        return mensagem_decodificada