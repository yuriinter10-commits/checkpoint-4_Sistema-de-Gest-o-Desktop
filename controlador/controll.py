from modelo.model import incerir_produto

def processar_cadastro(nome, p_txt, q_txt):
    if nome == "" or p_txt == "":
        return False, "Campos vazios!"
    try:
        preco = float(p_txt)
        qtd = int(q_txt)

    except ValueError:
        return False, "Erro nos números!"

# Tudo correto, manda para o Banco!
    incerir_produto(nome, preco, qtd)
    return True, "Produto cadastrado!"


if __name__ == "__main__":
    processar_cadastro()