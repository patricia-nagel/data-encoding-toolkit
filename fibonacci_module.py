class Fibonacci:
    """
    Implementa a codificação de Fibonacci baseada no Teorema de Zeckendorf.

    IDEIA CENTRAL:
    - Todo número pode ser representado como soma de números de Fibonacci
    - Sem usar números consecutivos da sequência
    - Isso garante uma representação única

    Ex: 10 = 8 + 2 (não usamos 5 + 3 + 2, pois 3 e 2 são consecutivos)
    """

    def gerar_sequencia_fibonacci(self, limite):
        """
        Gera a sequência de Fibonacci até um determinado valor.

        IMPORTANTE:
        - Começamos em [1, 2] (F2, F3)
        - Ignoramos o primeiro '1' da sequência clássica
        - Isso evita ambiguidade na codificação
        """
        sequencia = [1, 2]

        while True:
            proximo = sequencia[-1] + sequencia[-2]

            # Continua enquanto não ultrapassar o valor desejado
            if proximo <= limite:
                sequencia.append(proximo)
            else:
                break

        return sequencia


    def encoder(self, mensagem):
        """
        Codifica a mensagem usando Fibonacci (Zeckendorf).

        PIPELINE:
        texto → ASCII → decomposição em Fibonacci → bits
        """
        resultado_binario = ""

        # Converte cada caractere para valor ASCII
        valores_ascii = [ord(char) for char in mensagem]

        for valor in valores_ascii:

            # ========================
            # PASSO 1 — GERAR SEQUÊNCIA
            # ========================
            
            # Gera Fibonacci até o valor atual
            fib_seq = self.gerar_sequencia_fibonacci(valor)

            # Inicializa todos os bits como 0
            bits = [0] * len(fib_seq)
            
            # ========================
            # PASSO 2 — DECOMPOSIÇÃO (GREEDY)
            # ========================
            
            # Estratégia gulosa:
            # sempre pega o maior Fibonacci possível
            resto = valor

            for i in range(len(fib_seq) - 1, -1, -1):
                if fib_seq[i] <= resto:
                    bits[i] = 1
                    resto -= fib_seq[i]

            # ========================
            # PASSO 3 — GERAR CODEWORD
            # ========================
            
            # Transforma lista de bits em string
            # Ex: [1,0,1] → "101"
            codeword = "".join(map(str, bits))

            # Adiciona o STOP BIT "1"
            # Isso cria o padrão "11" no final
            codeword += "1"

            resultado_binario += codeword

        return resultado_binario


    def decoder(self, bits_codificados):
        """
        Decodifica a sequência de bits.

        PIPELINE:
        bits → detectar '11' → reconstruir número → ASCII → texto
        """
        mensagem_decodificada = ""

        # Sequência grande o suficiente para cobrir ASCII
        fib_seq = self.gerar_sequencia_fibonacci(255)
        
        buffer_bits = ""
        i = 0

        while i < len(bits_codificados):
            # ========================
            # PASSO 1 — ACUMULAR BITS
            # ========================
            
            buffer_bits += bits_codificados[i]
            
            # ========================
            # PASSO 2 — DETECTAR FIM DO SÍMBOLO
            # ========================
            
            # "11" indica fim de um número
            if buffer_bits.endswith("11"):

                # Remove o último '1' (stop bit)
                bits_uteis = buffer_bits[:-1]
                
                soma_ascii = 0

                # ========================
                # PASSO 3 — RECONSTRUIR VALOR
                # ========================
                
                # Soma os Fibonacci correspondentes aos bits '1'
                for j in range(len(bits_uteis)):
                    if bits_uteis[j] == "1":
                        soma_ascii += fib_seq[j]
                
                # Converte para caractere
                mensagem_decodificada += chr(soma_ascii)

                # Limpa buffer para próximo símbolo
                buffer_bits = ""

            i += 1
            
        return mensagem_decodificada