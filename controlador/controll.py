from modelo.model import inserir_produto

def cadastrar_validar_cadastro(nome, preco, qtd):
    if nome == "":
        print("Erro: Nome está vazio!")
        return False
    try:
    #fazer converção utilizando o float (0.0), int(preco inteiro 1) no pdf 44 da aula 17 
        preco = float(qtd)
        qtd
    inserir_produto(nome, preco, qtd)
    return True

# Lista global para simular o banco de dados temporário
lista_produto = [
    {"id": 1, "nome": "Ana Silva", "email": "ana@email.com", "telefone": "11999999999"},
    {"id": 2, "nome": "Carlos Souza", "email": "carlos@email.com", "telefone": "11888888888"}
]
proximo_id = 3  # Controla o autoincremento para novos cadastros


def listar():
    #Retorna todos os produto cadastrados. Útil para preencher tabelas ou caixas de texto."""
    if not lista_produto:
        print("Nenhum produto cadastrado.")
        return []
    
    print("\n--- LISTA DE PRODUTO ---")
    for produto in lista_produto:
        print(f"ID: {produto['id']} | Nome: {produto['nome']} | Email: {produto['email']} | Tel: {cliente['telefone']}")
    
    return lista_produto


def buscar(id_produto):
  for produto in lista_produto:
        if produto["id"] == int(id_produto):
            print(f"Produto encontrado: {produto['nome']}")
            return produto
            
        print(f"Produto com ID {id_produto} não foi encontrado.")
        return None
   


def editar(id_produto, novos_dados):
    produto = buscar(id_produto)
    if produto:
        # Atualiza apenas os campos que foram enviados em 'novos_dados'
        for chave, valor in novos_dados.items():
            if chave in produto:
                produto[chave] = valor
        print(f"Produto ID {id_produto} atualizado com sucesso!")
        return True
        
    return False


def excluir(id_produto):
    #Remove o produto da lista com base no ID."""
    produto = buscar(id_produto)
    if produto:
        lista_produto.remove(produto)
        print(f"Produto ID {id_produto} excluído com sucesso!")
        return True
        
    return False