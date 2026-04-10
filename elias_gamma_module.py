import math

class EliasGamma():

    def encoder(self, mensagem):
        mensagem_codificada = ""

        # Converte cada caractere da mensagem para seu valor decimal ASCII
        valores_ascii = [ord(simbolo) for simbolo in mensagem]

        for valor in valores_ascii:

            if valor <= 0:
                continue # Elias-Gamma não define codificação para zero ou negativos

            # n é a potência de 2 mais próxima (abaixo) do valor
            n = int(math.log2(valor))

            prefixo = "0" * n
            stop_bit = "1"

            # O sufixo é o que resta após subtrair 2^n do valor original
            resto = valor - (2**n)

            # Transformamos o resto em binário e garantimos que ele tenha n bits (zfill)
            sufixo = bin(resto)[2:].zfill(n)

            # Montagem do codeword do símbolo atual
            codeword = prefixo + stop_bit + sufixo
            mensagem_codificada += codeword

        return mensagem_codificada
    
    def decoder(self, mensagem_codificada):
        mensagem_decodificada = ""
        ponteiro = 0

        while ponteiro < len(mensagem_codificada):
            # Conta o número de zeros no prefixo para descobrir o valor de 'n'
            n = 0
            while ponteiro < len(mensagem_codificada) and mensagem_codificada[ponteiro] == "0":
                n += 1
                ponteiro += 1
                #simbolo = np.power(2, n)

            # Pula o stop bit ('1')
            ponteiro += 1

            # Lê o sufixo (os próximos n bits)
            sufixo_binario = mensagem_codificada[ponteiro : ponteiro + n]
            ponteiro += n #adianta o i no while para continuar depois do sufixo

            # Reconstrói o valor: 2^n + valor_do_sufixo
            # Caso o sufixo esteja vazio (quando n=0), o valor é 0
            valor_sufixo = int(sufixo_binario, 2) if sufixo_binario else 0 #converte de binário para int
            valor_original = (2**n) + valor_sufixo

            # Converte o valor ASCII de volta para caractere
            mensagem_decodificada += chr(valor_original)

        return mensagem_decodificada
