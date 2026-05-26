import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modelo.model import (inserir_produto, buscar_produtos, atualizar_preco,
                           excluir_produto, criar_tabela, registrar_venda,
                           buscar_vendas, buscar_vendas_por_produto)  

def dados_dashboard():
    resultados = buscar_vendas_por_produto()
    return [
        {"nome": row[0], "quantidade": row[1], "faturamento": row[2]}
        for row in resultados
    ]

criar_tabela()


def cadastrar_validar_cadastro(nome, preco, qtd):
    if nome.strip() == "":
        return False, "Erro: Nome está vazio!"
    try:
        preco_convertido = float(preco)
        qtd_convertida = int(qtd)
    except ValueError:
        return False, "ERRO: Digite apenas números para preço e quantidade."

    sucesso = inserir_produto(nome, preco_convertido, qtd_convertida)

    if sucesso:
        return True, f"Produto '{nome}' cadastrado com sucesso!"
    else:
        return False, "Erro ao salvar no banco de dados."


def listar_produto():
    resultados = buscar_produtos()
    return [
        {"id": row[0], "nome": row[1], "preco": row[2], "qtd": row[3]}
        for row in resultados
    ]


def editar_produto(id_produto, novo_preco):
    return atualizar_preco(novo_preco, id_produto)


def excluir_produto_ctrl(id_produto):
    return excluir_produto(id_produto)


# valida e repassa a venda para o model
def realizar_venda(id_produto, quantidade):
    try:
        qtd = int(quantidade)
        if qtd <= 0:
            return False, "A quantidade deve ser maior que zero."
    except ValueError:
        return False, "ERRO: Digite apenas números para quantidade."

    return registrar_venda(id_produto, qtd)


# retorna histórico formatado
def listar_vendas():
    resultados = buscar_vendas()
    return [
        {
            "id": row[0],
            "id_produto": row[1],
            "nome_produto": row[2],
            "quantidade": row[3],
            "valor_total": row[4],
            "data_venda": row[5]
        }
        for row in resultados
    ]