from src.encoder import elias_gamma, fibonacci, golomb, huffman

print("Projeto de compressão iniciado 🚀")

def encode(method, value):
    if method == "golomb":
        return golomb(value)
    elif method == "elias":
        return elias_gamma(value)
    elif method == "fibonacci":
        return fibonacci(value)
    elif method == "huffman":
        return huffman(value)