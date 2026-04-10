class Fibonacci:
    """
    Implementa a codificação de Fibonacci (Teorema de Zeckendorf).
    Cada número é representado como uma soma de números de Fibonacci não consecutivos.
    """

    def gerar_sequencia_fibonacci(self, limite):
        """
        Gera a sequência de Fibonacci (F2, F3, F4...) até atingir o limite.
        Usamos 1, 2, 3, 5, 8, 13... (pulando o primeiro '1' para evitar ambiguidade).
        """
        sequencia = [1, 2]
        while True:
            proximo = sequencia[-1] + sequencia[-2]
            if proximo <= limite:
                sequencia.append(proximo)
            else:
                break
        return sequencia

    def encoder(self, mensagem):
        """Codifica a mensagem usando a representação de Zeckendorf."""
        resultado_binario = ""
        # Converte cada letra para seu valor ASCII decimal
        valores_ascii = [ord(char) for char in mensagem]

        for valor in valores_ascii:
            # Gera a sequência necessária para este valor específico
            fib_seq = self.gerar_sequencia_fibonacci(valor)
            # Lista de bits (começa tudo com zero)
            bits = [0] * len(fib_seq)
            
            # Algoritmo Ganancioso (Greedy): subtrai o maior Fibonacci possível
            resto = valor
            for i in range(len(fib_seq) - 1, -1, -1):
                if fib_seq[i] <= resto:
                    bits[i] = 1
                    resto -= fib_seq[i]
            
            # Transforma a lista [1, 0, 1] na string "101" e adiciona o stop bit "1"
            codeword = "".join(map(str, bits)) + "1"
            resultado_binario += codeword

        return resultado_binario

    def decoder(self, bits_codificados):
        """Decodifica os bits encontrando o padrão '11' que indica o fim de um símbolo."""
        mensagem_decodificada = ""
        # Geramos uma sequência grande o suficiente para cobrir qualquer ASCII (até 255)
        fib_seq = self.gerar_sequencia_fibonacci(255)
        
        buffer_bits = ""
        i = 0
        while i < len(bits_codificados):
            buffer_bits += bits_codificados[i]
            
            # O Teorema de Zeckendorf garante que nunca haverá "11" exceto no fim do símbolo
            if buffer_bits.endswith("11"):
                # Remove o último '1' (que é apenas o stop bit)
                bits_uteis = buffer_bits[:-1]
                
                soma_ascii = 0
                # Para cada bit '1', soma o valor de Fibonacci correspondente à posição
                for j in range(len(bits_uteis)):
                    if bits_uteis[j] == "1":
                        soma_ascii += fib_seq[j]
                
                mensagem_decodificada += chr(soma_ascii)
                buffer_bits = "" # Limpa para o próximo caractere
            
            i += 1
            
        return mensagem_decodificada
    
'''
Explicação: 
    - Utilizamos a sequência de Fibonacci começando em 1 e 2 ($F(2)$ e $F(3)$). Ignoramos o primeiro '1' da sequência matemática 
    para garantir que cada número tenha uma representação única (Teorema de Zeckendorf).
    - Para codificar um valor ASCII, procuramos o maior número de Fibonacci que cabe dentro dele. Subtraimos esse valor, marcamos 
    '1' naquela posição, e repitimos o processo com o que sobrou até chegar a zero.
    - A característica única de Zeckendorf é que nunca existem dois bits '1' seguidos na codificação de um número. 
    Por isso, adicionamos um bit '1' extra no final de cada símbolo. Isso cria o padrão 11, que serve como um 
    separador universal.
    - O decoder lê os bits um por um. Assim que ele encontra o padrão 11, ele sabe que um caractere terminou. 
    Ele então pega os bits anteriores, multiplica cada bit '1' pelo seu peso na sequência de Fibonacci e soma tudo 
    para recuperar o código ASCII original.
    - No encoder, a sequência de Fibonacci é percorrida de trás para frente (reversed), mas os bits são gravados na ordem da sequência.
    Isso é importante para que o bit menos significativo (o menor Fibonacci) fique na esquerda.
'''
